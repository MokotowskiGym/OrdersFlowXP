from datetime import datetime


@property
def STR_IRELEVANT():
    return "irrelevant"
@property
def STR_UNKNOWN():
    return "unknown"
@property
def STR_ADDED_BY_STATION():
    return "added by station"


@property
def STR_BOOKEDNESS_BOOKED()->str:
    return "Booked"

@property
def STR_BOOKEDNESS_NOT_BOOKED()->str    :
    return "NotBooked"

def CONST_FAKE_DATE()->datetime:
    return datetime(2005, 4, 2, 21, 37, 0)

def CONST_FAKE_INT()->int:
    return 666
