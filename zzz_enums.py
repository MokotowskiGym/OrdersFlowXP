from enum import Enum


class GluSupplier(Enum):
    TVP = "TVP"
    TVN = "TVN"
    POLSAT = "Polsat"


class GluMatchLevel(Enum):
    NO_MATCH = "No match"
    TIME = "Time"
    RATECARD = "Ratecard"
    ID = "ID"
