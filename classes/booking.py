from typing import List

import pandas
import pandas as pd
import zzz_tools as t
from classes.channel_break import ChannelBreak, get_channel_break
from classes.data_framable import iDataFrameable
from zzz_enums import GluSupplier, GluMatchLevel


class Booking(iDataFrameable):
    def __init__(self, supplier: GluSupplier, df: pandas.DataFrame, channel_breaks: List[ChannelBreak]):
        self.supplier = supplier
        self.df = df
        self.channel_breaks = channel_breaks


    def to_dataframe(self):
        df = pd.DataFrame(data=[vars(x) for x in self.channel_breaks])
        return df

    def get_unmatched_channel_breaks(self):
        breaks = t.Collection()
        for channel_break in self.channel_breaks:
            if channel_break.match_level == GluMatchLevel.NO_MATCH:
                breaks.add(channel_break, channel_break.blockId)
        return breaks

def get_channel_breaks(df: pd.DataFrame) -> List[ChannelBreak]:
    channel_breaks = []
    for _, row in df.iterrows():
        channel_break = get_channel_break(row)
        channel_breaks.append(channel_break)
    return channel_breaks
