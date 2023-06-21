from typing import Dict

import pandas as pd
import zzz_tools as t
from classes.break_info import BreakInfo
from classes.exceptions import MyProgramException
from classes.iData_framable import iDataFrameable
from classes.merger import get_merger
from classes.schedule_break import ScheduleBreak
from classes.status_info import StatusInfo
from classes.timeband import Timeband
from classes.wantedness_info import WantednessInfo
from zzz_enums import *
from zzz_projectTools import GluCannonColumnsList


def getProcessedScheduleDf(df_scheduleOrg: pd.DataFrame, df_channelsMapping: pd.DataFrame) -> pd.DataFrame:
    df_scheduleOrg.rename(columns={"channel": "channel_org"}, inplace=True)
    df_scheduleProcessed = get_merger(
        "Processed schedule", df_scheduleOrg, df_channelsMapping, "channel_org", right_on="channelPossibleName"
    ).return_merged_df()
    df_scheduleProcessed["dateTime"] = pd.to_datetime(
        df_scheduleProcessed["xDate"] + " " + df_scheduleProcessed["xTime"]
    )

    df_scheduleProcessed["tbId1"] = df_scheduleProcessed.apply(
        lambda row: t.getTimebandId(row["channel"], row["dateTime"], 30, 0, 30), axis=1
    )
    df_scheduleProcessed["tbId2"] = df_scheduleProcessed.apply(
        lambda row: t.getTimebandId(row["channel"], row["dateTime"], 30, 0, 0), axis=1
    )
    # t.msgBox("Templariusz", f'{len(df)}')

    # value_vars = "tb1 tb2".split()
    # id_vars = df_scheduleProcessed.columns.difference(value_vars).tolist()
    # df2 = pd.melt(df_scheduleProcessed, id_vars=id_vars, value_vars=value_vars, var_name="tbType", value_name="tb")
    # df2["tbId"] = df2["tb"].dt.strftime("%Y-%m-%d %H%M") + "|" + df2["channel"]
    t.check_cannon_columns(df_scheduleProcessed, GluCannonColumnsList.ScheduleMatching, drop_excess_columns=True)
    return df_scheduleProcessed


class Schedule(iDataFrameable):
    def __init__(self, source_path: str, df: pd.DataFrame, schedule_breaks: t.Collection):
        self.source_path = source_path
        self.df = df
        self.schedule_breaks = schedule_breaks

    def get_timebands_dict(self) -> Dict[str, Timeband]:
        timebands_dict: Dict[str, Timeband] = {}
        for schedule_break in self.schedule_breaks.values():
            if schedule_break.tbId1 in timebands_dict.keys():
                timeband1 = timebands_dict[schedule_break.tbId1]
            else:
                timeband1 = Timeband(schedule_break.tbId1)
                timebands_dict[schedule_break.tbId1] = timeband1

            timeband1.add_schedule_break(schedule_break)

            if schedule_break.tbId2 in timebands_dict.keys():
                timeband2 = timebands_dict[schedule_break.tbId2]
            else:
                timeband2 = Timeband(schedule_break.tbId2)
                timebands_dict[schedule_break.tbId2] = timeband2
            timeband2.add_schedule_break(schedule_break)
        return timebands_dict

    def to_dataframe(self):
        df = pd.DataFrame(data=[x.serialize for x in self.schedule_breaks.values()])
        return df


def get_wantedness_info_from_row(wantedness) -> WantednessInfo:
    if wantedness == "NotWanted":
        is_wanted: bool = False
        subcampaign:int = 0
        origin:GluOrigin = GluOrigin.NotWanted
    elif wantedness.startswith("Wanted"):
        is_wanted: bool  = True
        sub_string = t.get_substring_between_parentheses(wantedness)
        subcampaign: int  = int(sub_string.split(",")[0].strip())
        origin_str = sub_string.split(",")[1].strip()
        origin = GluOrigin.get_from_str(origin_str)
    else:
        raise MyProgramException(f"Wrong wantedness: {wantedness}")

    wantedness_info: WantednessInfo = WantednessInfo(is_wanted=is_wanted, subcampaign=subcampaign, origin=origin)
    return wantedness_info


def get_schedule_breaks(df: pd.DataFrame) -> t.Collection:
    breaks = t.Collection()
    for index, row in df.iterrows():
        wantedness_info = get_wantedness_info_from_row(row["wantedness"])
        block_id = row["blockId"]
        break_info = BreakInfo(
            blockId=block_id,
            date_time=row["dateTime"],
            ratecard=row["ratecard"],
            channel=row["channel"],
        )

        status_info = StatusInfo(
            subcampaign=wantedness_info.subcampaign,
            origin=wantedness_info.origin,
            is_booked=row["bookedness"]
        )

        schedule_break = ScheduleBreak(
            break_info=break_info,
            status_info=status_info,
            tbId1=row["tbId1"],
            tbId2=row["tbId2"],
        )
        breaks.add(schedule_break, block_id)

    return breaks


def get_schedule(path_schedule: str, df_channelsMapping: pd.DataFrame) -> Schedule:
    df_scheduleOrg = pd.read_csv(path_schedule, sep=";", encoding="utf-8")
    df_scheduleProcessed = getProcessedScheduleDf(df_scheduleOrg, df_channelsMapping)

    schedule_breaks = get_schedule_breaks(df_scheduleProcessed)

    schedule = Schedule(path_schedule, df_scheduleProcessed, schedule_breaks)
    return schedule
