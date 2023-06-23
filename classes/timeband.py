import zzz_tools as t
from classes.iEmptyable import iEmptyable

from classes.schedule_break import ScheduleBreak


class Timeband(iEmptyable):
    def __init__(self, tbId: str, is_empty: bool = False):
        self.tbId = tbId
        self.schedule_breaks: t.Collection = t.Collection()
        self._is_empty:bool = is_empty

    def add_schedule_break(self, schedule_break: ScheduleBreak):
        self.schedule_breaks.add(schedule_break, schedule_break.break_info.blockId)

    def __str__(self):
        return self.tbId

    def is_empty(self):
        return self._is_empty