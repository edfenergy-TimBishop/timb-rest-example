import boto3
from datetime import datetime

class Model:
    def __init__(self):
        self.table = ''
        self.primaryKey = 'id'
        self.fillable = {}
        self.translate = {}
        self.userId = 'admin'
        self.where = ''

        self.ssmClient = boto3.client('ssm')
        self.dbName = self._ssmGetParameter('/smec-example/smec-postgres-db-1/dbName')
        self.dbArn = self._ssmGetParameter('/smec-example/smec-postgres-db-1/dbArn')
        self.dbSecretArn= self._ssmGetParameter('/smec-example/smec-postgres-db-1/dbSecretArn', True)
        self.rdsClient = boto3.client('rds-data')

    def getUserId(self):
        return self.userId

    def setUserId(self, userId):
        self.userId = userId
        return self

    def _ssmGetParameter(self, name, withDecryption = False):
        parameter = self.ssmClient.get_parameter(Name = name, WithDecryption = withDecryption)
        return parameter['Parameter']['Value']

    # Formatting query returned Field
    def _formatField(self, field):
        return list(field.values())[0]

    # Formatting query returned Record
    def _formatRecord(self, record, columnMetadata):
        result = {}
        for index, field in enumerate(record):
            name = columnMetadata[index]['name']
            field = self._formatField(field)
            if name in self.translate:
                result[self.translate[name]] = field
            else:
                result[name] = field
        return result

    # Formatting query returned Field
    def formatResponse(self, response):
        return [self._formatRecord(record, response['columnMetadata']) for record in response['records']]

    def _dictIntersectKeys(self, dict1, *dicts):
        keys = dict1.keys()
        for dict in dicts:
            keys &= dict.keys()
        return {k: dict1[k] for k in keys}

    def _dictFlip(self, dict1):
        return dict((v, k) for k, v in dict1.items())    

    # execute sql query
    def executeStatment(self, query, parameters = []):
        return self.rdsClient.execute_statement(
            resourceArn = self.dbArn,
            secretArn = self.dbSecretArn,
            database = self.dbName,
            sql = query,
            parameters = parameters,
            includeResultMetadata = True
        )

    # build select query
    def selectQuery(self, id = None):
        result = "SELECT * FROM {0}".format(self.table)
        if id != None:
            self.where = "{0}={1}".format(self.primaryKey, id)
            result += " WHERE {0}".format(self.where)
        result += " ORDER BY {0}".format(self.primaryKey)
        return result

    # build search query
    def searchQuery(self, search = ''):
        result = "SELECT * FROM {0}".format(self.table)
        if search != '':
            self.where = "LOWER({0}) LIKE LOWER('{1}')".format('description', '%' + search + '%')
            result += " WHERE {0}".format(self.where)
        result += " ORDER BY {0}".format(self.primaryKey)
        return result

    # build count query
    def countQuery(self):
        result = "SELECT COUNT(*) cnt FROM {0}".format(self.table)
        if self.where != '':
            result += " WHERE {0}".format(self.where)
        return result

    # build insert query
    def insertQuery(self, data):
        now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        data = self._dictIntersectKeys(data, self.fillable)
        data['createdTs'] = now
        data['createdId'] =  self.userId
        data['lastUpdatedTs'] = now
        data['lastUpdatedId'] = self.userId

        keys = ''
        values = ''
        for k, type in self.fillable.items():
            if (keys != ''):
                keys += ", " 
                values += ", "
            keys += k
            if k in data:
                if (type == 'long'):
                    values += '{0}'.format(data[k])
                else:
                    values += "'{0}'".format(data[k])
            else:
                if (type == 'long'):
                    values += '0'
                else:
                    values += "''"
        return "INSERT INTO {0} ({1}) VALUES ({2}) RETURNING {3}".format(self.table, keys, values, self.primaryKey)

    # build update query
    def updateQuery(self, id, data):
        now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        data = self._dictIntersectKeys(data, self.fillable)
        data['lastUpdatedTs'] = now
        data['lastUpdatedId']  = self.userId 

        values = ''
        for k, v in data.items():
            if (values != ''):
                values += ", " 
            values += "{0}='{1}'".format(k, v)
        return "UPDATE {0} SET {1} WHERE {2}={3}".format(self.table, values, self.primaryKey, id)

    # build delete query
    def deleteQuery(self, id):
        return "DELETE FROM {0} WHERE {1}={2}".format(self.table, self.primaryKey, id)
