from zzz_enums import *


class StatusInfo:
    def __init__(
            self,
            subcampaign: int,
            origin: GluOrigin,
            is_booked: bool
    ):
        self.subcampaign = subcampaign
        self.origin = origin
        self.is_booked = is_booked