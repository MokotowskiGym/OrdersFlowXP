from classes.channel_break import ChannelBreak
from zzz_ordersTools import get_empty_schedule_break


def process_schedule_after_booking(schedule_breaks, channel_breaks)->None:
    channel_break: ChannelBreak
    for channel_break in channel_breaks:
        if channel_break.schedule_break is None:
            channel_break.schedule_break = get_empty_schedule_break(channel_break.break_info)
            schedule_breaks.add(channel_break.schedule_break, channel_break.schedule_break.break_info.blockId)
        channel_break.schedule_break.book(subcampaign=channel_break.subcampaign)