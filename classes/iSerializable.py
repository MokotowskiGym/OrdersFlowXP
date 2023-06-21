import abc

from zzz_enums import GluExportFormat


class iSerializable(abc.ABC):

    @abc.abstractmethod
    def serialize(self, export_format:GluExportFormat):
        """zamienia obiekt na dict"""
