from enum import Enum


class GluSupplier(Enum):
    TVP = "TVP"
    TVN = "TVN"
    POLSAT = "Polsat"


class GluMatchLevel(Enum):
    NO_TIMEBAND = "No timeband"
    NO_MATCH = "No match"
    TIME = "Time"
    RATECARD = "Ratecard"
    ID = "ID"

class GluOrigin(Enum):
    NotWanted = "NotWanted"
    Optimizer = "Optimizer"
    Manual = "Manual"
    Station = "Station"


    @classmethod
    def get_from_str(cls, my_str):
        for origin in cls:
            if origin.value == my_str:
                return origin
        raise ValueError("No such origin: " + my_str)

class GluExportFormat(Enum):
    ChannelBreak = "ChannelBreak"
    ScheduleBreak_minerwa = "ScheduleBreak_minerwa"
    ScheduleBreak_rozkminki = "ScheduleBreak_rozkminki"
    Irrelevant = "Irrelevant"

class GluBookingQuality(Enum):
    OK = "OK"
    ABSENT_CHANNELS = "Absent channels"
    ILLEGAL_CHANNELS = "Illegal channels"

class GluScheduleType(Enum):
    OK_4CHANNELS = "OK_4channels"
    ILLEGAL_CHANNELS = "Illegal channels"