import datetime as dt

from classes.iSerializable import iSerializable


class BreakInfo(iSerializable):
    def __init__(
        self, blockId: int, date_time: dt.datetime, ratecard: int, channel: str
    ):
        self.blockId = blockId
        self.date_time = date_time
        self.ratecard = ratecard
        self.channel = channel

    @property
    def serialize(self):
        return {
            "blockId": self.blockId,
            "date_time": self.date_time,
            "ratecard": self.ratecard,
            "channel": self.channel,
        }