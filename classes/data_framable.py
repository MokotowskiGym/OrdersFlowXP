import abc


class iDataFrameable(abc.ABC):
    @abc.abstractmethod
    def to_dataframe(self):
        """zamienia obiekt na dataframe"""