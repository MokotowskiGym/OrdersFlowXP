from typing import Dict

import zzz_ordersTools as ot
import zzz_tools as t
from classes.channel_break import ChannelBreak
from classes.timeband import Timeband
from zzz_enums import GluMatchLevel


def match_channel_breaks_step1_id(channel_breaks, schedule_breaks: t.Collection):
    channel_break: ChannelBreak
    for channel_break in channel_breaks:
        if channel_break.blockId in schedule_breaks.keys():
            channel_break.schedule_break = schedule_breaks[channel_break.blockId]
            channel_break.match_level = GluMatchLevel.ID


def match_channel_breaks_step2_timebands(channel_breaks: t.Collection, timebands_dict: Dict[str, Timeband]) -> None:
    channel_break: ChannelBreak
    for channel_break in channel_breaks.values():
        try:
            channel_break.schedule_timeband = timebands_dict[channel_break.tbId]
        except KeyError:
            channel_break.match_level  = GluMatchLevel.NO_TIMEBAND

        if channel_break.blockId == 15107428494:
            pass
        if channel_break.schedule_timeband is not None:
            potential_matches_ratecard = channel_break.get_potential_matches_ratecard()
            if len(potential_matches_ratecard) > 0:
                channel_break.schedule_break = channel_break.get_closest_break(potential_matches_ratecard)
                channel_break.match_level = GluMatchLevel.RATECARD
            else:
                potential_matches_time = channel_break.schedule_timeband.schedule_breaks
                if len(potential_matches_time) > 0:
                    channel_break.schedule_break = channel_break.get_closest_break(potential_matches_time)
                    channel_break.match_level = GluMatchLevel.TIME
                else:
                    channel_break.match_level = GluMatchLevel.NO_MATCH


def modify_schedule(schedule_breaks: t.Collection, channel_breaks: t.Collection):
    for channel_break in channel_breaks.values():
        if channel_break.schedule_break is not None:
            schedule_break: ot.ScheduleBreak = channel_break.schedule_break
