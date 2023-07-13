from enum import Enum


class GluCannonColumnsSet(Enum):
    DoNotCheck = "DoNotCheck"
    BookingProcessed = "BookingProcessed"
    Matching = "Matching"
    ScheduleProcessedFull = "ScheduleProcessedFull"
    ScheduleMatching = "ScheduleMatching"
    ScheduleOrg = "ScheduleOrg"
