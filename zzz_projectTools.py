from enum import Enum


class GluCannonColumnsList(Enum):
    DoNotCheck = "DoNotCheck"
    BookingOrg = "BookingOrg"
    BookingProcessed = "BookingProcessed"
    Matching = "Matching"
    ScheduleProcessedFull = "ScheduleProcessedFull"
    ScheduleMatching = "ScheduleMatching"