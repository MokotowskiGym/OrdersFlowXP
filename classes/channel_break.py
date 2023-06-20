import datetime as dt

import zzz_tools as t
from classes.iSerializable import iSerializable
from classes.schedule_break import ScheduleBreak
from classes.timeband import Timeband
from zzz_enums import GluMatchLevel


class ChannelBreak(iSerializable):
    def __init__(self, blockId: int, channel: str, date_time: dt.datetime, tbId: str, ratecard: float):
        self.blockId = blockId
        self.channel = channel
        self.date_time = date_time
        self.tbId = tbId
        self.ratecard = ratecard
        self.match_level: GluMatchLevel = GluMatchLevel.NO_MATCH
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
        smallest_diff = abs(self.date_time - closest_break.date_time)

        for schedule_break in schedule_breaks:
            time_diff = abs(schedule_break.date_time - self.date_time)
            if time_diff < smallest_diff:
                smallest_diff = time_diff
                closest_break = schedule_break

        return closest_break

    def serialize(self) -> dict:
        return {"ratecard": self.ratecard, "dateTime": self.date_time}

    def get_potential_matches_ratecard(self) -> t.Collection:
        potential_matches = t.Collection()
        for schedule_break in self.schedule_timeband.schedule_breaks:
            if schedule_break.ratecard == self.ratecard:
                potential_matches.add(schedule_break, schedule_break.blockId)
        return potential_matches


def get_channel_break(row) -> ChannelBreak:
    channel_break = ChannelBreak(
        blockId=row["blockId"],
        channel=row["channel"],
        date_time=row["dateTime"],
        tbId=row["tbId"],
        ratecard=row["ratecard"],
    )
    return channel_break
