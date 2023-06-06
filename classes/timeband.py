import zzz_tools as t
from typing import List, Dict

from classes.schedule_break import ScheduleBreak


class Timeband:
    def __init__(self, tbId: str):
        self.tbId = tbId
        self.schedule_breaks: t.Collection = t.Collection()

    def add_schedule_break(self, schedule_break: ScheduleBreak):
        self.schedule_breaks.add(schedule_break, schedule_break.blockId)

    def __str__(self):
        return self.tbId
