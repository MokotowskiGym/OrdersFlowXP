import datetime as dt


class BreakInfo:
    def __init__(
        self, blockId: int, date_time: dt.datetime, ratecard: int, channel: str
    ):
        self.blockId = blockId
        self.date_time = date_time
        self.ratecard = ratecard
        self.channel = channel