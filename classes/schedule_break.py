from classes.break_info import BreakInfo
from classes.iSerializable import iSerializable
from classes.status_info import StatusInfo
from zzz_enums import GluOrigin


class ScheduleBreak(iSerializable):
    def __init__(
        self, break_info:BreakInfo, status_info:StatusInfo  ,tbId1:str, tbId2:str
    ):
        self.break_info = break_info
        self.status_info = status_info
        self.tbId1 = tbId1
        self.tbId2 = tbId2

    def __str__(self):
        return str(self.break_info.blockId)

    def book(self, subcampaign:int):

        if self.status_info.get_is_wanted:
            origin= self.status_info.origin
        else:
            origin = GluOrigin.Channel

        self.status_info = StatusInfo(subcampaign=subcampaign, origin=origin, is_booked=True)
    @property
    def serialize(self):
        my_dict = self.break_info.serialize | self.status_info.serialize
        return my_dict