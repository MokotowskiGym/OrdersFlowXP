from classes.channel_break import ChannelBreak


def process_schedule_after_booking(schedule_breaks, channel_breaks)->None:
    channel_break: ChannelBreak
    for channel_break in channel_breaks:
        if channel_break.schedule_break is None:
            # TODO: Implement the logic for processing the user input
            raise Exception("todo: implement")
        else:
            channel_break.schedule_break.book(subcampaign=channel_break.subcampaign)