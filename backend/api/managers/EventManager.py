from .GenericInfoManager import GenericInfoManager

class EventManager(GenericInfoManager):
    def searchEvent(self,name):
        event = self.filter(eventName__contains=name)
        return event