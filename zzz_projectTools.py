from enum import Enum


class GluCannonColumnsSet(Enum):
    DoNotCheck = "DoNotCheck"
    BookingOrg = "BookingOrg"
    BookingProcessed = "BookingProcessed"
    Matching = "Matching"
    ScheduleProcessedFull = "ScheduleProcessedFull"
    ScheduleMatching = "ScheduleMatching"
    ScheduleOrg = "ScheduleOrg"
