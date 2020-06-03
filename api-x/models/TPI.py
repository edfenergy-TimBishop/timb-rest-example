from models.Model import Model

class TPI(Model):
    def __init__(self):
        super(TPI, self).__init__()
        self.table = 'TPIs'
        self.primaryKey = 'tpiId'
        self.fillable = {
            'tpiBusinessKey': 'string',
            'tpiChannel': 'string',
            'description': 'string',
            'status': 'string',
            'relationshipManagerId': 'long',
            'statusRepFreq': 'string',
            'statementRepFreq': 'string',
            'contractVersionId': 'long',
            'notes': 'string',
            'dataSource': 'string',
            'poReference': 'string',
            'createdTs': 'string',
            'createdId': 'string',
            'lastUpdatedTs': 'string',
            'lastUpdatedId': 'string'
        }
        self.translate = {
            'tpiid': 'tpiId',
            'tpibusinesskey': 'tpiBusinessKey',
            'tpichannel': 'tpiChannel',
            'description': 'description',
            'status': 'status',
            'relationshipmanagerid': 'relationshipManagerId',
            'statusrepfreq': 'statusRepFreq',
            'statementrepfreq': 'statementRepFreq',
            'contractversionid': 'contractVersionId',
            'notes': 'notes',
            'datasource': 'dataSource',
            'poreference': 'poReference',
            'createdts': 'createdTs',
            'createdid': 'createdId',
            'lastupdatedts': 'lastUpdatedTs',
            'lastupdatedid': 'lastUpdatedId'
        }
