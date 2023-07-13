from typing import List, Set

import pandas
import pandas as pd

import zzz_tools as t
from classes.channel_break import ChannelBreak, get_channel_break
from classes.dfProcessor import get_df_processor
from classes.exceptions import MyProgramException
from classes.iData_framable import iDataFrameable
from classes.merger import get_merger
from zzz_enums import *
from zzz_projectTools import GluCannonColumnsSet


class Booking(iDataFrameable):
    def __init__(self, supplier: GluSupplier, df: pandas.DataFrame, channel_breaks: List[ChannelBreak]):
        self.supplier = supplier
        self.df = df
        self.channel_breaks = channel_breaks

    def to_dataframe(self, export_format: GluExportFormat) -> pd.DataFrame:
        df = pd.DataFrame(data=[x.serialize(export_format) for x in self.channel_breaks])

        return df

    def get_unmatched_channel_breaks(self):
        breaks = t.Collection()
        for channel_break in self.channel_breaks:
            if channel_break.match_level == GluMatchLevel.NO_MATCH:
                breaks.add(channel_break, channel_break.break_info.blockId)
        return breaks

    def get_subcampaings_orgs_set(self) -> Set[str]:
        subcampaigns_orgs = []
        for channel_break in self.channel_breaks:
            subcampaigns_org = channel_break.subcampaing_org
            subcampaigns_orgs.append(subcampaigns_org)
        return set(subcampaigns_orgs)

def get_booking(
    supplier: GluSupplier,
    df_channelsMapping: pd.DataFrame,
    booking_quality: GluBookingQuality,
) -> Booking:
    from zzz_ordersTools import get_booking_path

    path = get_booking_path(supplier, booking_quality)

    if supplier == GluSupplier.TVP:
        print(0 / 0)  # wywalić wczytywanie jako string
        df_booking_org = pd.read_excel(path, dtype=str)

    elif supplier == GluSupplier.TVN:
        df_booking_org = pd.read_csv(path, sep=";", encoding="utf-8")
    #     dateTime = get_date_time_tvn(row["DATA"], row["PLANOWANA GODZ."])
    #     channel = row["KANAŁ"]
    #     ratecard = t.get_float(row["WARTOŚĆ SPOTU"])

    elif supplier == GluSupplier.POLSAT:
        df_booking_org = get_df_processor(GluDfProcessorType.BOOKING_POLSAT, path).get_df
    else:
        raise MyProgramException(f"Wrong supplier: {supplier}")

    df_booking = get_merger(
        "Merge channels",
        df_booking_org,
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


def get_channel_breaks(df: pd.DataFrame) -> List[ChannelBreak]:
    channel_breaks = []
    for _, row in df.iterrows():
        channel_break = get_channel_break(row)
        channel_breaks.append(channel_break)
    return channel_breaks
