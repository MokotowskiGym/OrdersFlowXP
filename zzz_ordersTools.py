import json
import os
import re
from datetime import datetime
from typing import List

import pandas as pd

import zzz_constants as CONST_
import zzz_strings as STR_
import zzz_tools as t
from classes.booking import Booking, get_channel_breaks
from classes.break_info import BreakInfo
from classes.dfProcessor import get_df_processor
from classes.exceptions import MyProgramException
from classes.merger import get_merger
from classes.schedule_break import ScheduleBreak
from classes.status_info import StatusInfo
from classes.timeband import Timeband
from classes.tv.channel import Channel
from classes.tv.channel_group import ChannelGroup
from classes.tv.supplier import Supplier
from zzz_enums import *
from zzz_projectTools import GluCannonColumnsSet


def get_date_time_tvp(xDate: str, xHour: str, xMinute: str) -> datetime:
    if re.match("\d{4}-\d{2}-\d{2}$", xDate):
        date_safe = xDate
    elif re.match("\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}$", xDate):
        date_safe = xDate.split(" ")[0]
    else:
        raise ValueError(f"Wrong date format: {xDate}")

    date_string = f"{date_safe} {xHour.zfill(2)}:{xMinute.zfill(2)}:00"
    dt = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")

    if not isinstance(dt, datetime):
        raise ValueError(f"Wrong date format: {xDate} {xHour} {xMinute}")
    return dt


def get_date_time_tvn(xDate: str, xTime: str) -> datetime:
    if re.match(r"^\d{4}-\d{2}-\d{2}$", xDate):
        date = datetime.strptime(xDate, "%Y-%m-%d")
    else:
        raise ValueError(f"Wrong date format: {xDate}")

    if re.match(r"^\d{2}:\d{2}:\d{2}$", xTime):
        time = datetime.strptime(xTime, "%H:%M").time()
    else:
        raise ValueError(f"Wrong time format: {xTime}")

    dt = datetime.combine(date.date(), time)

    if not isinstance(dt, datetime):
        raise ValueError(f"Wrong date format: {xDate} {xTime}")
    return dt


def get_date_time_polsat(xDate, xTime) -> datetime:
    dt = datetime.combine(xDate, xTime)

    if not isinstance(dt, datetime):
        raise ValueError(f"Wrong date format: {xDate} {xTime}")
    return dt


def get_booking(
    supplier: GluSupplier,
    df_channelsMapping: pd.DataFrame,
    booking_quality: GluBookingQuality,
) -> Booking:
    path = get_booking_path(supplier, booking_quality)

    if supplier == GluSupplier.TVP:
        print(0 / 0)  # wywalić wczytywanie jako string
        df_booking = pd.read_excel(path, dtype=str)

    elif supplier == GluSupplier.TVN:
        df_booking = pd.read_csv(path, sep=";", encoding="utf-8")
    #     dateTime = get_date_time_tvn(row["DATA"], row["PLANOWANA GODZ."])
    #     channel = row["KANAŁ"]
    #     ratecard = t.get_float(row["WARTOŚĆ SPOTU"])

    elif supplier == GluSupplier.POLSAT:
        df_booking = get_df_processor(GluDfProcessorType.SCHEDULE_POLSAT, path).get_df

    else:
        raise MyProgramException(f"Wrong supplier: {supplier}")

    t.check_cannon_columns(df_booking, GluCannonColumnsSet.BookingOrg, drop_excess_columns=True)
    df_booking = get_merger(
        "Merge channels",
        df_booking,
        df_channelsMapping,
        "channelOrg",
        right_on="channelPossibleName",
        exception_type_unjoined=GluExceptionType.MERGER_ILLEGAL_CHANNELS_IN_BOOKING,
    ).return_merged_df()

    df_booking["tbId"] = df_booking.apply(
        lambda row: t.getTimebandId(row["channel"], row["dateTime"], 30, 15, 30), axis=1
    )

    t.check_cannon_columns(df_booking, GluCannonColumnsSet.BookingProcessed, drop_excess_columns=True)
    channel_breaks = get_channel_breaks(df_booking)
    # t.msgBox("templarriuuuusz", f"channel_breaks: {len(channel_breaks)}")

    booking = Booking(supplier, df_booking, channel_breaks)
    return booking


def get_suppliers(json_path: str) -> List[Supplier]:
    with open(json_path, "r") as f:
        data = json.load(f)

    suppliers = []

    for supplier_data in data["suppliers"]:
        channel_groups = []
        for group_data in supplier_data["channelGroups"]:
            channels = []
            for channel_data in group_data["channels"]:
                channel = Channel(channel_data["name"], channel_data["possibleNames"])
                channels.append(channel)
            group = ChannelGroup(group_data["name"], channels)
            channel_groups.append(group)
        supplier = Supplier(supplier_data["name"], channel_groups)
        suppliers.append(supplier)
    return suppliers


def get_channels_df(json_path: str) -> pd.DataFrame:
    with open(json_path, "r") as file:
        json_channels = json.load(file)

    suppliers = []
    channel_groups = []
    channels = []
    possible_names = []

    for supplier in json_channels["supplier"]:
        for channel_group in supplier["channelGroup"]:
            for channel in channel_group["channel"]:
                for name in channel["channelPossibleName"]:
                    suppliers.append(supplier["name"])
                    channel_groups.append(channel_group["name"])
                    channels.append(channel["name"])
                    possible_names.append(name)

    # Create a DataFrame
    df = pd.DataFrame(
        {
            "supplier": suppliers,
            "channelGroup": channel_groups,
            "channel": channels,
            "channelPossibleName": possible_names,
        }
    )
    return df


def get_copy_indexes_df() -> pd.DataFrame:
    json_copyLengths_path = CONST_.JSON_COPY_INDEXES

    with open(json_copyLengths_path, "r") as f:
        data = json.load(f)

    # Create a DataFrame from the JSON data
    df = pd.DataFrame(data["CopyLengths"])
    return df


def get_booking_path(supplier: GluSupplier, booking_quality: GluBookingQuality) -> str:
    folder = r"C:\Users\macie\PycharmProjects\MnrwOrdersFlow\project\source"
    case = supplier.value + booking_quality.value
    if case == GluSupplier.POLSAT.value + GluBookingQuality.OK.value:
        file = "2 booking polsat no pato2023-04-22 1052.xlsx"
    elif case == GluSupplier.POLSAT.value + GluBookingQuality.ABSENT_CHANNELS.value:
        file = "2 booking polsat no pato2023-04-22 1052 -brakujące stacje.xlsx"
    elif case == GluSupplier.POLSAT.value + GluBookingQuality.ILLEGAL_CHANNELS.value:
        file = "2 booking polsat no pato2023-04-22 1052 -zjebane stacje.xlsx"
    elif case == GluSupplier.POLSAT.value + GluBookingQuality.FUCKED_UP_DATES.value:
        file = "2 booking polsat no pato2023-04-22 1052 - zjebane daty.xlsx"
    else:
        raise MyProgramException(f"Wrong supplier: {supplier} / booking_quality: {booking_quality}")
    # elif supplier == GluSupplier.TVN:
    #     file = "2 booking 2022-10-06 114034 TVN no pato.txt"
    # elif Supplier == GluSupplier.TVP:
    #     file = "2 booking 2022-10-06 113747 TVP 1z2.xls"
    return os.path.join(folder, file)


def get_schedule_path(schedule_type: GluScheduleType) -> str:
    path: str
    if schedule_type == GluScheduleType.OK_4CHANNELS_CLEAR:
        path = r"C:\Users\macie\PycharmProjects\MnrwOrdersFlow\project\source\1 schedule 2022-10-06 112529 Schedule czysta.txt"
    elif schedule_type == GluScheduleType.ILLEGAL_CHANNELS:
        path = r"C:\Users\macie\PycharmProjects\MnrwOrdersFlow\project\source\1a schedule 2022-10-06 112529 Schedule czysta - wrong channels.txt"
    elif schedule_type == GluScheduleType.OK_4CHANNELS_1WANTED:
        path = r"C:\Users\macie\PycharmProjects\MnrwOrdersFlow\project\source\1b schedule 2022-10-06 112529 Schedule wanted.txt"

    else:
        raise ValueError("Wrong schedule type")

    return path


def check_time_space_consistency(df_booking: pd.DataFrame, df_schedule: pd.DataFrame):
    get_merger(
        "check_time_space_consistency",
        df_booking,
        df_schedule,
        "channel",
        "channel",
        exception_type_unjoined=GluExceptionType.MERGER_ABSENT_CHANNELS,
    ).return_merged_df()

    min_date_booking = df_booking["dateTime"].min()
    max_date_booking = df_booking["dateTime"].max()
    min_date_schedule = df_schedule["dateTime"].min()
    max_date_schedule = df_schedule["dateTime"].max()

    dates_ok: bool = False
    if max_date_booking <= max_date_schedule:
        if min_date_booking >= min_date_schedule:
            dates_ok = True

    if not dates_ok:
        raise MyProgramException(
            f"Dates are not consistent:\n "
            f"Booking: {min_date_booking} to  {max_date_booking} \n "
            f"Schedule: {min_date_schedule} to {max_date_schedule}"
        )


def get_empty_timeband() -> Timeband:
    timeband = Timeband(STR_.IRELEVANT)
    return timeband


def get_empty_break_info() -> BreakInfo:
    break_info = BreakInfo(0, CONST_.FAKE_DATE, CONST_.FAKE_INT, STR_.IRELEVANT)
    return break_info


def get_empty_schedule_break(break_info: BreakInfo) -> ScheduleBreak:
    schedule_break = ScheduleBreak(
        break_info,
        get_empty_status_info(),
        STR_.IRELEVANT,
        STR_.IRELEVANT,
        STR_.IRELEVANT,
        STR_.IRELEVANT,
        STR_.IRELEVANT,
        999,
        STR_.IRELEVANT,
        0,
        0,
        0,
        0,
        0,
        50,
    )
    return schedule_break


def get_empty_status_info() -> StatusInfo:
    status_info: StatusInfo = StatusInfo(subcampaign=-1, origin=GluOrigin.NotWanted, is_booked=False)
    return status_info


def get_schedule_break_from_channel_break(break_info: BreakInfo) -> ScheduleBreak:
    schedule_break = ScheduleBreak(
        break_info,
        get_empty_status_info(),
        STR_.IRELEVANT,
        STR_.IRELEVANT,
        STR_.ADDED_BY_STATION,
        STR_.UNKNOWN,
        STR_.UNKNOWN,
        999,
        STR_.BOOKEDNESS_NOT_BOOKED,
        0,
        0,
        0,
        0,
        0,
        50,
    )
    return schedule_break
