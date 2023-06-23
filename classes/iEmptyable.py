import abc


class iEmptyable(abc.ABC):

    @abc.abstractmethod
    def is_empty(self)->bool:
        """zamienia obiekt na dict"""
