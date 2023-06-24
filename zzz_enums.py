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
    FUCKED_UP_DATES = "Fucked up dates"

class GluScheduleType(Enum):
    OK_4CHANNELS_CLEAR = "OK_4channels"
    ILLEGAL_CHANNELS = "Illegal channels"
    OK_4CHANNELS_1WANTED = "OK_4channels_1wanted"

class GluExceptionType(Enum):
    MERGER_GENERIC = "There are unjoined values \n _UnjoinedValues_ \n in merge operation \n _Caption_  \n that are absent in schedule:"
    MERGER_ILLEGAL_CHANNELS_IN_BOOKING = "Unknown channels \n _UnjoinedValues_ \n in imported booking'"
    MERGER_ILLEGAL_CHANNELS_IN_SCHEDULE = "Unknown channels \n _UnjoinedValues_ \n in imported schedule'"
    MERGER_ABSENT_CHANNELS = "There are channels in booking that are absent in schedule\n _UnjoinedValues_:"
