from classes.break_info import BreakInfo
from classes.status_info import StatusInfo


class ScheduleBreak:
    def __init__(
        self, break_info:BreakInfo, status_info:StatusInfo  ,tbId1:str, tbId2:str
    ):
        self.break_info = break_info
        self.status_info = status_info
        self.tbId1 = tbId1
        self.tbId2 = tbId2

    def __str__(self):
        return str(self.break_info.blockId)

    def book(self):
        self.is_booked = True