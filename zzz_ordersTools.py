import json
import os
import re
from datetime import datetime
from typing import List

import pandas as pd
import zzz_tools as t
from classes.booking import Booking, get_channel_breaks
from classes.exceptions import MyProgramException
from classes.merger import get_merger
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


def get_booking(supplier: GluSupplier, df_channelsMapping: pd.DataFrame, df_copyIndexes:pd.DataFrame) -> Booking:
    path = get_booking_path(supplier)

    if supplier == GluSupplier.TVP:
        print(0 / 0)  # wywalić wczytywanie jako string
        df_booking = pd.read_excel(path, dtype=str)

        #     dateTime = get_date_time_tvp(row["data_emisji"], row["godzina_emisji"], row["minuta_emisji"])
        #     channel = row["kanal_telewizyjny"]
        #     ratecard = 0 / 0

    elif supplier == GluSupplier.TVN:
        df_booking = pd.read_csv(path, sep=";", encoding="utf-8")
    #     dateTime = get_date_time_tvn(row["DATA"], row["PLANOWANA GODZ."])
    #     channel = row["KANAŁ"]
    #     ratecard = t.get_float(row["WARTOŚĆ SPOTU"])

    elif supplier == GluSupplier.POLSAT:
        df_booking = pd.read_excel(path)
        df_booking['CopyLength'] = df_booking['Długość'].str.replace('"', '').astype(int)
        df_booking = get_merger("copy indexes", df_booking, df_copyIndexes, "CopyLength",  case_sensitive=True).return_merged_df()
        df_booking["dateTime"] = df_booking.apply(lambda x: get_date_time_polsat(x["Data"], x["Godzina"]), axis=1)
        df_booking["channelOrg"] = df_booking["Stacja"]
        df_booking["ratecard_indexed"] = df_booking.apply(lambda x: t.get_float(x["Base price"]), axis=1)
        df_booking["ratecard"] = df_booking["ratecard_indexed"] / df_booking["CopyIndex"]
        df_booking["blockId"] = df_booking["ID Bloku"]
    else:
        raise MyProgramException(f"Wrong supplier: {supplier}")

    t.check_cannon_columns(df_booking, GluCannonColumnsSet.BookingOrg, drop_excess_columns=True)
    df_booking = get_merger(
        "Merge channels", df_booking, df_channelsMapping, "channelOrg", right_on="channelPossibleName"
    ).return_merged_df()

    df_booking["tbId"] = df_booking.apply(
        lambda row: t.getTimebandId(row["channel"],  row["dateTime"], 30, 15, 30), axis=1
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


def get_copy_indexes_df(path: str) -> pd.DataFrame:
    with open(path, "r") as f:
        data = json.load(f)

    # Create a DataFrame from the JSON data
    df = pd.DataFrame(data["CopyLengths"])
    return df


def get_booking_path(supplier: GluSupplier) -> str:
    folder = r"C:\Users\macie\PycharmProjects\MnrwOrdersFlow\project\source"
    if supplier == GluSupplier.POLSAT:
        file = "2 booking polsat no pato2023-04-22 1052.xlsx"
        # file = "2 booking polsat no pato2023-04-22 1052 - zjebane stacje.xlsx"
    elif supplier == GluSupplier.TVN:
        file = "2 booking 2022-10-06 114034 TVN no pato.txt"
    elif Supplier == GluSupplier.TVP:
        file = "2 booking 2022-10-06 113747 TVP 1z2.xls"
    return os.path.join(folder, file)
