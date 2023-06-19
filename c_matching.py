from typing import List, Dict

import pandas as pd
import zzz_tools as t
import zzz_ordersTools as ot
from classes.channel_break import ChannelBreak
from classes.schedule import get_schedule_breaks
from classes.timeband import Timeband
from zzz_enums import GluMatchLevel


def match_channel_breaks_old(channelBreaks: List[ChannelBreak], matchingDf: pd.DataFrame) -> None:
    for channelBreak in channelBreaks:
        matched_rows_df = matchingDf[matchingDf["tbId"] == channelBreak.tbId]

        # potentialMatches_time = get_schedule_breaks(matched_rows_df)
        # potentialMatches_id = [sb for sb in potentialMatches_time if sb.blockId == channelBreak.blockId]
        # potentialMatches_ratecard = [sb for sb in potentialMatches_time if sb.ratecard == channelBreak.ratecard]
        #
        # print(f" blockId{len(potentialMatches_id)}")
        # print(f" ratecard{len(potentialMatches_ratecard)}")
        # print(f" time{len(potentialMatches_time)}")


def match_channel_breaks_step2_timebands(
    channel_breaks: t.Collection, timebands_dict: Dict[str, Timeband]
) -> None:

    for channel_break in channel_breaks.values():
        channel_break: ChannelBreak = channel_break
        try:
            channel_break.schedule_timeband = timebands_dict[channel_break.tbId]
        except KeyError:
            channel_break.match_info = "No timeband"

        if channel_break.blockId == 15107428494:
            pass
        if channel_break.schedule_timeband is not None:
            potential_matches_ratecard = channel_break.get_potential_matches_ratecard()
            if len(potential_matches_ratecard) >0:
                channel_break.schedule_break = channel_break.get_closest_break(potential_matches_ratecard)
                channel_break.match_level = GluMatchLevel.RATECARD
            else:
                potential_matches_time = channel_break.schedule_timeband.schedule_breaks
                if len(potential_matches_time) >0:
                    channel_break.schedule_break = channel_break.get_closest_break(potential_matches_time)
                    channel_break.match_level = GluMatchLevel.TIME
                else:
                    channel_break.match_level = GluMatchLevel.NO_MATCH


def match_channel_breaks_step1_id(channel_breaks, schedule_breaks: t.Collection):
    for channel_break in channel_breaks:
        if channel_break.blockId in schedule_breaks.keys():
            channel_break.schedule_break = schedule_breaks[channel_break.blockId]
            channel_break.match_level = GluMatchLevel.ID
            channel_break.match_info = "Matched by blockId"
