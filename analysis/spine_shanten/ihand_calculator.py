from abc import ABC, abstractmethod

class IHandCalculator(ABC):
    @abstractmethod
    def Shanten(self):
        pass

    @abstractmethod
    def Ankan(self, tileType):
        pass

    @abstractmethod
    def Chii(self, lowestTileType, calledTileType):
        pass

    @abstractmethod
    def Daiminkan(self, tileType):
        pass

    @abstractmethod
    def Discard(self, tileType):
        pass

    @abstractmethod
    def Draw(self, tileType):
        pass

    @abstractmethod
    def Pon(self, tileType):
        pass

    @abstractmethod
    def Shouminkan(self, tileType):
        pass

    @abstractmethod
    def ShantenAfterDiscard(self, tileType):
        pass

    @abstractmethod
    def ShantenWithTile(self, tileType):
        pass

    @abstractmethod
    def Clone(self):
        pass

    @abstractmethod
    def GetUkeIreFor13(self):
        pass
    
    @abstractmethod
    def Init(self, tiles):
        pass
  