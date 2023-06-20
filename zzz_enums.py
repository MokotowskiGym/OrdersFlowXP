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

class GLuOrigin(Enum):
    Optimizer = "Optimizer"
    Manual = "Manual"
    Channel = "Channel"
