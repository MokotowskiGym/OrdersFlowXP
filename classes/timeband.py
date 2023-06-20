import zzz_tools as t

from classes.schedule_break import ScheduleBreak


class Timeband:
    def __init__(self, tbId: str):
        self.tbId = tbId
        self.schedule_breaks: t.Collection = t.Collection()

    def add_schedule_break(self, schedule_break: ScheduleBreak):
        self.schedule_breaks.add(schedule_break, schedule_break.break_info.blockId)

    def __str__(self):
        return self.tbId
