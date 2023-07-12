from dataclasses import dataclass
from typing import List, Any, Optional

import pandas as pd

from classes.column_def import columnDef
from classes.merger import get_merger
from zzz_enums import *
from zzz_tools import Collection
from zzz_tools import GluFileType, get_float


@dataclass
class DfProcessorConfig:
    df_processor_type: GluDfProcessorType
    sheet_name: Any
    file_type: GluFileType
    date_format: str = "%Y-%m-%d"  # Specify the date format if needed
    column_separator: str = ";"  # Specify the column separator
    decimal_separator: str = ","  # Specify the decimal separator
    date_columns_to_parse: Optional[List[str]] = None  # Specify the date columns to parse
    import_only_defined_columns: bool = True  # Specify if only defined columns should be imported

    def add_column(self, name_org: str, name_mod: str, data_type: Optional[str] = None) -> None:
        column_def = columnDef(name_org, name_mod, data_type)
        self.column_defs.add(column_def, name_mod)

    def define_columns(self) -> None:
        self.column_defs: Collection = Collection()

        match self.df_processor_type:
            case GluDfProcessorType.HISTORY_ORG:
                self.add_column("Channel", "channelOrg")
                self.add_column("Date", "xDate")  # "Datetime64[ns]")
                self.add_column("Time", "xTime")  # , "Datetime64[ns]")
                self.add_column("Prog Campaign", "programme")
                self.add_column("Cost", "ratecard")
            case GluDfProcessorType.SCHEDULE_POLSAT:
                self.add_column("", "CopyLength")  # "Datetime64[ns]")
                self.add_column("", "dateTime")
                self.add_column("", "channelOrg")
                self.add_column("", "ratecard")
                self.add_column("", "blockId")
            case _:
                raise ValueError(f"Wrong df_processor_type: {self.df_processor_type}")


def get_df_processor_config(df_processor_type: GluDfProcessorType):
    match df_processor_type:
        case GluDfProcessorType.HISTORY_ORG:
            config = DfProcessorConfig(df_processor_type, 0, GluFileType.XLSX)
        case GluDfProcessorType.SCHEDULE_POLSAT:
            config = DfProcessorConfig(df_processor_type, 0, GluFileType.XLSX, import_only_defined_columns=False)
        case _:
            raise ValueError(f"Wrong df_processor_type: {df_processor_type}")
    config.define_columns()
    return config


class DfProcessor:
    def __init__(self, cfg: DfProcessorConfig, file_path: str):
        self.file_path = file_path
        self.cfg = cfg

    @property
    def _get_column_orgs(self) -> List[str]:
        list = [column_def.column_org for column_def in self.cfg.column_defs]
        return list

    @property
    def _get_column_mods(self) -> List[str]:
        list = [column_def.column_mod for column_def in self.cfg.column_defs]
        return list

    @property
    def _get_dtype(self) -> dict:
        dtype = {}
        for column_def in self.cfg.column_defs:
            if column_def.data_type is not None:
                dtype[column_def.column_org] = column_def.data_type
        return dtype

    def _get_df_org_xlsx(self) -> pd.DataFrame:
        header_rows = range(0, 11)
        df_test = None
        if self.cfg.import_only_defined_columns:
            column_orgs = self._get_column_orgs
        else:
            column_orgs = None
        dtype = self._get_dtype

        for row in header_rows:
            try:
                df_test = pd.read_excel(
                    self.file_path, sheet_name=self.cfg.sheet_name, usecols=column_orgs, header=row, nrows=1
                )
                break
            except:
                continue
        if df_test is None:
            raise ValueError(f"Error opening dataframe from: {self.file_path}")
        else:
            df = pd.read_excel(
                self.file_path, sheet_name=self.cfg.sheet_name, usecols=column_orgs, header=row, dtype=dtype
            )
        return df

    def _get_df_org_csv(self) -> pd.DataFrame:
        parse_dates: List[str]
        if self.cfg.date_columns_to_parse is None:
            parse_dates = []
        else:
            if isinstance(self.cfg.date_columns_to_parse, str):
                parse_dates = [self.cfg.date_columns_to_parse]

        df = pd.read_csv(
            self.file_path,
            parse_dates=parse_dates,
            date_format=self.cfg.date_format,
            sep=self.cfg.column_separator,
            decimal=self.cfg.decimal_separator,
            usecols=self._get_column_orgs,
        )
        return df

    def _get_df_org(self) -> pd.DataFrame:
        match self.cfg.file_type:
            case GluFileType.XLSX:
                df = self._get_df_org_xlsx()
            case GluFileType.CSV:
                df = self._get_df_org_csv()

            case _:
                raise ValueError(f"Wrong df_processor_type: {self.cfg.df_processor_type}")

        return df

    def _rename_columns(self, df: pd.DataFrame):
        for old_name, new_name in zip(self._get_column_orgs, self._get_column_mods):
            if old_name != "":
                assert old_name in df.columns, f"Column '{old_name}' does not exist in the DataFrame."
                df.rename(columns={old_name: new_name}, inplace=True)

    def _transform_before_check_header(self, df: pd.DataFrame) -> pd.DataFrame:

        match self.cfg.df_processor_type:
            case GluDfProcessorType.SCHEDULE_POLSAT:
                from zzz_ordersTools import get_date_time_polsat,get_copy_indexes_df

                df_copyIndexes = get_copy_indexes_df()
                df["CopyLength"] = df["Długość"].str.replace('"', "").astype(int)
                df = get_merger(
                    "copy indexes", df, df_copyIndexes, "CopyLength", case_sensitive=True
                ).return_merged_df()
                df["dateTime"] = df.apply(lambda x: get_date_time_polsat(x["Data"], x["Godzina"]), axis=1)
                df["channelOrg"] = df["Stacja"]
                df["ratecard_indexed"] = df.apply(lambda x: get_float(x["Base price"]), axis=1)
                df["ratecard"] = df["ratecard_indexed"] / df["CopyIndex"]
                df.rename(columns={"ID Bloku": "blockId"}, inplace=True)

            case _:
                raise NotImplementedError
        return df

    @property
    def get_df(self) -> pd.DataFrame:
        df: pd.DataFrame = self._get_df_org()
        df =  self._transform_before_check_header(df)
        self._rename_columns(df)
        self._mod_columns(df)
        return df

    def _mod_columns(self, df):
        for new_name in self._get_column_mods:
            assert new_name in df.columns, f"Column '{new_name}' does not exist in the DataFrame."


def get_df_processor(df_processor_type: GluDfProcessorType, file_path: str) -> DfProcessor:
    cfg = get_df_processor_config(df_processor_type)
    df_processor = DfProcessor(cfg, file_path)
    return df_processor
