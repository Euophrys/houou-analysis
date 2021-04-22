from abc import ABC, abstractmethod

class LogAnalyzer(ABC):
    @abstractmethod
    def ParseLog(self, log, log_id):
        pass
    
    @abstractmethod
    def PrintResults(self):
        pass