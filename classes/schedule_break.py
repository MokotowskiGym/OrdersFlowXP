from classes.break_info import BreakInfo
from classes.iEmptyable import iEmptyable
from classes.iSerializable import iSerializable
from classes.status_info import StatusInfo
from zzz_enums import GluOrigin, GluExportFormat


class ScheduleBreak(iSerializable, iEmptyable):
    def __init__(
        self,
        break_info:BreakInfo,
        status_info:StatusInfo  ,
        tbId1:str,
        tbId2:str,
        programme: str,
        blockType_org: str ,
        blockType_mod: str,
        freeTime: int,
        bookedness: str,
        grpTg_01: float,
        grpTg_02: float,
        grpTg_50: float,
        grpTg_98: float,
        grpTg_99: float,
        positionCode: int,

    ):
        self.break_info = break_info
        self.status_info = status_info
        self.tbId1 = tbId1
        self.tbId2 = tbId2
        self.programme = programme
        self.blockType_org = blockType_org
        self.blockType_mod = blockType_mod
        self.freeTime = freeTime
        self.bookedness = bookedness
        self.grpTg_01 = grpTg_01
        self.grpTg_02 = grpTg_02
        self.grpTg_50 = grpTg_50
        self.grpTg_98 = grpTg_98
        self.grpTg_99 = grpTg_99
        self.positionCode = positionCode

    def __str__(self):
        return str(self.break_info.blockId)

    def book(self, subcampaign:int):

        if self.status_info.get_is_wanted:
            origin= self.status_info.origin
        else:
            origin = GluOrigin.Station

        self.status_info = StatusInfo(subcampaign=subcampaign, origin=origin, is_booked=True)

    def serialize(self, export_format:GluExportFormat):
        if export_format == GluExportFormat.ScheduleBreak_rozkminki:
            my_dict = self.break_info.serialize(GluExportFormat.Irrelevant) | self.status_info.serialize(GluExportFormat.Irrelevant)
        elif export_format == GluExportFormat.ScheduleBreak_minerwa:
            my_dict = self.get_export_row_minerwa()
        else:
            raise ValueError("Wrong export format")
        return my_dict

    def get_export_row_minerwa(self)->dict:
        my_dict:dict = {}
        my_dict["blockId"] = self.break_info.blockId
        my_dict["channel"] = self.break_info.channel
        my_dict["programme"] = self.programme
        my_dict["blockType_org"] = self.blockType_org
        my_dict["blockType_mod"] = self.blockType_mod
        my_dict["xDate"] = self.break_info.date_time.date()
        my_dict["xTime"] = self.break_info.date_time.time()
        my_dict["ratecard"] = self.break_info.ratecard
        my_dict["freeTime"] = self.freeTime
        my_dict["week"] = "irrelevant"
        my_dict["timeband"] = "irrelevant"
        my_dict["wantedness"] = self.status_info.get_wantedness
        my_dict["bookedness"] = self.bookedness
        my_dict["eqPriceNet"] = 2137
        # print (type(self.grpTg_01))
        my_dict["grpTg_01"] = self.grpTg_01
        my_dict["grpTg_02"] = self.grpTg_02
        my_dict["grpTg_50"] = self.grpTg_50
        my_dict["grpTg_98"] = self.grpTg_98
        my_dict["grpTg_99"] = self.grpTg_99
        my_dict["positionCode"] = self.positionCode
        # my_dict["scheduleInfo"] = self.scheduleInfo


        return  my_dict