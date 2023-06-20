from classes.break_info import BreakInfo
from zzz_enums import *



class ScheduleBreak:
    def __init__(
        self, break_info:BreakInfo , is_wanted:bool, subcampaign:int, origin:GLuOrigin, is_booked:bool, tbId1:str, tbId2:str
    ):
        self.break_info = break_info
        self.is_wanted = is_wanted
        self.subcampaign = subcampaign
        self.origin = origin
        self.is_booked = is_booked
        self.tbId1 = tbId1
        self.tbId2 = tbId2

    def __str__(self):
        return str(self.break_info.blockId)

    def book(self):
        self.is_booked = True