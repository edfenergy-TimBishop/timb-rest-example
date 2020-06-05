from models.Model import Model

class Contact(Model):
    def __init__(self):
        super(Contact, self).__init__()
        self.table = 'Contacts'
        self.primaryKey = 'contactId'
        self.fillable = {
            'contactType': 'string',
            'description': 'string',
            'tpiId': 'long',
            'createdTs': 'string',
            'createdId': 'string',
            'lastUpdatedTs': 'string',
            'lastUpdatedId': 'string'
        }
        self.translate = {
            'contacttype': 'contactType',
            'description': 'description',
            'tpiid': 'tpiId',
            'createdts': 'createdTs',
            'createdid': 'createdId',
            'lastupdatedts': 'lastUpdatedTs',
            'lastupdatedid': 'lastUpdatedId'
        }

    # table joins
    def tpis(self):
        # fromColumn, toTable, toColumn
        return 'tpiId', 'TPIs', 'tpiId' 
