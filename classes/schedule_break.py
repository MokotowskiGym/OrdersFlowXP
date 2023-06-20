class ScheduleBreak:
    def __init__(
        self, blockId, row_index, date_time, ratecard, channel, is_wanted, subcampaign, origin, is_booked, tbId1, tbId2
    ):
        self.blockId = blockId
        self.row_index = row_index
        self.date_time = date_time
        self.ratecard = ratecard
        self.channel = channel
        self.is_wanted = is_wanted
        self.subcampaign = subcampaign
        self.origin = origin
        self.is_booked = is_booked
        self.tbId1 = tbId1
        self.tbId2 = tbId2

    def __str__(self):
        return str(self.blockId)

    def book(self):
        self.is_booked = True