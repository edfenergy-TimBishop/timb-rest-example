from managers.ContactManager import ContactManager

manager = ContactManager()

def list(event, context):
    manager.setEvent(event)
    return manager.list()

def create(event, context):
    manager.setEvent(event)
    return manager.create()

def read(event, context):
    manager.setEvent(event)
    return manager.read()

def update(event, context):
    manager.setEvent(event)
    return manager.update()

def delete(event, context):
    manager.setEvent(event)
    return manager.delete()
