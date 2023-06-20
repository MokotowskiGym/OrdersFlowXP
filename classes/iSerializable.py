import abc


class iSerializable(abc.ABC):
    @abc.abstractmethod
    def serialize(self):
        """zamienia obiekt na dict"""
