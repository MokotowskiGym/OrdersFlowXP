import abc

class iSerializable(abc.ABC):
    @property
    @abc.abstractmethod
    def serialize(self):
        """zamienia obiekt na dict"""
