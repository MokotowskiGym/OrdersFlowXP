from classes import schedule_break
from classes.channel_break import ChannelBreak
from classes.schedule_break import ScheduleBreak


def process_schedule_after_booking(schedule_breaks, channel_breaks)->None:
    for channel_break in channel_breaks:
        if channel_break.schedule_break is None:
            raise Exception("todo: implement")
        else:
            channel_break: ChannelBreak = channel_break
            schdule_break: ScheduleBreak = channel_break.schedule_break