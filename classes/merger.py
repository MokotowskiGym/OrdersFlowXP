import pandas as pd

from classes.exceptions import MyProgramException
from classes.result_folder import ResultFolder
from zzz_projectTools import GluCannonColumnsList
from zzz_tools import export_df, GluFileType, check_cannon_columns


def get_merger(
    caption: str,
    df1: pd.DataFrame,
    df2: pd.DataFrame,
    left_on: str,
    right_on: str = "",
    case_sensitive: bool = False,
    cannon_columns_list: GluCannonColumnsList = GluCannonColumnsList.DoNotCheck,
    right_prefix:str=""
):

    if right_prefix == "":
        df2_safe = df2
    else:
        df2_safe = df2.add_prefix(right_prefix)
    if caption == 'copy indexes':
        pass
    if right_on =="":
        right_safe = left_on
    else:
        right_safe = right_on

    if case_sensitive:
        right_key = right_safe
        left_key = left_on
        delete_temp = False
    else:
        right_key = "temp_right"
        left_key = "temp_left"

        df1[left_key] = df1[left_on].str.lower()
        df2_safe[right_key] = df2_safe[right_safe].str.lower()

        delete_temp = True

    return Merger(
        caption, df1, df2_safe, left_key, right_key, caption, case_sensitive,  delete_temp, cannon_columns_list
    )


class Merger:
    def __init__(
        self,
        caption: str,
        df1: pd.DataFrame,
        df2: pd.DataFrame,
        left_key: str,
        right_key: str,
        base_err_msg: str,
        case_sensitive: bool,

        delete_temp: bool,
        cannon_columns_list: GluCannonColumnsList = GluCannonColumnsList.DoNotCheck
    ):
        self.caption = caption
        self.df1 = df1
        self.df2 = df2
        self.left_key = left_key
        self.right_key = right_key
        self.base_err_msg = base_err_msg
        self.case_sensitive = case_sensitive
        self.delete_temp = delete_temp
        self.cannon_columns_list = cannon_columns_list

    def _clear(self, merged_df) -> None:
        if self.delete_temp:
            merged_df.drop(["temp_right", "temp_left"], axis=1, inplace=True)

    def _process_unjoined(self, merged_df: pd.DataFrame) -> None:
        unjoined_values = merged_df.loc[merged_df[self.right_key].isnull(), self.left_key].unique()
        if len(unjoined_values) > 0:
            raise MyProgramException(f"Unjoined value in {self.caption}")

    def export_merge_info(self, merged_df: pd.DataFrame, error_caption: str) -> None:

        export_dir = self.get_export_dir()
        export_df(self.df1, "df1", GluFileType.XLSX, export_dir=export_dir)
        export_df(self.df2, "df2", GluFileType.XLSX, export_dir=export_dir)
        if not merged_df is None:
            export_df(merged_df,"merged_df", GluFileType.XLSX, export_dir=export_dir )

    def get_export_dir(self)->str:
        dir =  ResultFolder().get_result_sub_dir(sub_folder_name=self.caption)
        return dir
    def return_merged_df(self) -> pd.DataFrame:
        try:

            merged_df:pd.DataFrame = pd.merge(
                self.df1,
                self.df2,
                left_on=self.left_key,
                right_on=self.right_key,
                how="left",
                suffixes=("", "_y"),
            )

            self._process_unjoined(merged_df)
            self._clear(merged_df)
            check_cannon_columns(merged_df, self.cannon_columns_list, True )
        except Exception as e:
            self.export_merge_info(merged_df, str(e))
            # print (f"Error in merge operation '{self.caption}\nFiles saved at:\n{self.get_export_dir()}")
            raise Exception (f"Error in merge operation '{self.caption}\nFiles saved at:\n{self.get_export_dir()}")
        return merged_df
