import json
import logging
import os
import urllib
from models.TPI import TPI

class TPIManager:
    def __init__(self):
        self.model = TPI()

    def setEvent(self, event):
        self.event = event
        return self

    def setContext(self, context):
        self.context = context
        return self

    def list(self):
        pageDefault = 0
        pageSizeDefault = 0
        searchDefault = ''

        status = 200
        try:
            page = int(self.event['queryStringParameters']['page'])
        except:
            page = pageDefault

        try:
            pageSize = int(self.event['queryStringParameters']['pageSize'])
        except:
            pageSize = pageSizeDefault

        try:
            search = self.event['queryStringParameters']['search']
        except:
            search = searchDefault

        if search == '':
            query = self.model.selectQuery()
        else:
            query = self.model.searchQuery(search)
        if (pageSize > 0):
            offset = page * pageSize
            query += " LIMIT {0} OFFSET {1}".format(pageSize, offset)
        response = self.model.executeStatment(query)
        result = self.model.formatResponse(response)

        query = self.model.countQuery()
        response = self.model.executeStatment(query)
        countResult = self.model.formatResponse(response)

        body = {}
        body['result'] = result
        body['total'] = countResult[0]['cnt']

        response = {
            "statusCode": status,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True
            },
            "body": json.dumps(body),
            "isBase64Encoded": False
        }
        return response

    def create(self):
        status = 200

        data = dict(urllib.parse.parse_qsl(self.event['body']))
        # todo: validation
        query = self.model.insertQuery(data)
        response = self.model.executeStatment(query)
        result = self.model.formatResponse(response)

        tpiId = result[0]['tpiId']

        query = self.model.selectQuery(tpiId)
        response = self.model.executeStatment(query)
        result = self.model.formatResponse(response)

        body = {}
        count = len(result)
        if (count == 1):
            body['result'] = result[0]
        else:
            body['result'] = result
        body['total'] = count

        response = {
            "statusCode": status,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True
            },
            "body": json.dumps(body),
            "isBase64Encoded": False
        }
        return response

    def read(self):
        try:
            id = int(self.event['path']['id'])
        except:
            raise Exception('invalid argument')

        query = self.model.selectQuery(id)
        response = self.model.executeStatment(query)
        result = self.model.formatResponse(response)

        body = {}
        count = len(result)
        if (count == 1):
            body['result'] = result[0]
        else:
            body['result'] = result
        body['total'] = count
        return body

    def update(self):
        try:
            id = int(self.event['path']['id'])
        except:
            raise Exception('invalid argument')

        data = self.event['body']
        # todo: validation
        query = self.model.updateQuery(id, data)
        result = self.model.executeStatment(query)

        query = self.model.selectQuery(id)
        response = self.model.executeStatment(query)
        result = self.model.formatResponse(response)

        body = {}
        count = len(result)
        if (count == 1):
            body['result'] = result[0]
        else:
            body['result'] = result
        body['total'] = count
        return body 

    def delete(self):
        try:
            id = int(self.event['path']['id'])
        except:
            raise Exception('invalid argument')

        query = self.model.deleteQuery(id)
        response = self.model.executeStatment(query)

        body = {
            "result": {}
        }
        return body
