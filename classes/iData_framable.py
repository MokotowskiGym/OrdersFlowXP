import abc

import pandas as pd
from zzz_enums import GluExportFormat


class iDataFrameable(abc.ABC):
    @abc.abstractmethod
    def to_dataframe(self, export_format: GluExportFormat) -> pd.DataFrame:
        """zamienia obiekt na dataframe"""