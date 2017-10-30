import abc


class ChatClient:
    @abc.abstractmethod
    def textMessage(self, text):
        pass

    @abc.abstractmethod
    def imageMessage(self, imageFile):
        pass

    @abc.abstractmethod
    def stickerMessage(self, stickerId):
        pass
