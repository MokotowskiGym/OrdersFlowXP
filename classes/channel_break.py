import zzz_tools as t
from classes.break_info import BreakInfo
from classes.iSerializable import iSerializable
from classes.schedule_break import ScheduleBreak
from classes.timeband import Timeband
from zzz_enums import GluMatchLevel


class ChannelBreak(iSerializable):
    def __init__(self, break_info:BreakInfo, subcampaign:int, tbId: str):
        self.break_info = break_info
        self.tbId = tbId
        self.subcampaign = subcampaign
        self._match_level = GluMatchLevel.NO_MATCH


    @property
    def match_level(self) -> GluMatchLevel:
        return self._match_level

    @match_level.setter
    def match_level(self, value: GluMatchLevel) -> None:
        self._match_level = value


    @property
    def schedule_timeband(self) -> Timeband:
        return self._schedule_timeband

    @schedule_timeband.setter
    def schedule_timeband(self, value: Timeband) -> None:
        self._schedule_timeband = value

    @property
    def schedule_break(self) -> ScheduleBreak:
        return self._schedule_break

    @schedule_break.setter
    def schedule_break(self, value: ScheduleBreak) -> None:
        self._schedule_break = value

    def get_closest_break(self, schedule_breaks: t.Collection) -> ScheduleBreak:
        schedule_break: ScheduleBreak
        closest_break: ScheduleBreak = schedule_breaks.get_first_value()
        smallest_diff = abs(self.break_info.date_time - closest_break.break_info.date_time)

        for schedule_break in schedule_breaks:
            time_diff = abs(schedule_break.break_info.date_time - self.break_info.date_time)
            if time_diff < smallest_diff:
                smallest_diff = time_diff
                closest_break = schedule_break

        return closest_break

    def serialize(self) -> dict:
        return {"ratecard": self.break_info.ratecard, "dateTime": self.break_info.date_time}

    def get_potential_matches_ratecard(self) -> t.Collection:
        potential_matches = t.Collection()
        schedule_break: ScheduleBreak
        for schedule_break in self.schedule_timeband.schedule_breaks:
            if schedule_break.break_info.ratecard == self.break_info.ratecard:
                potential_matches.add(schedule_break, schedule_break.break_info.blockId)
        return potential_matches


def get_channel_break(row) -> ChannelBreak:

    break_info = BreakInfo(
        blockId=row["blockId"],
        channel=row["channel"],
        date_time=row["dateTime"],
        ratecard=row["ratecard"]
    )

    channel_break = ChannelBreak(
        break_info=break_info,
        subcampaign=1, # TODO: ogarnąć subcampaign
        tbId=row["tbId"],
    )
    return channel_break
