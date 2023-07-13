from typing import Dict

from classes.channel_break import ChannelBreak
from classes.subcampaign import Subcampaign
from zzz_ordersTools import get_empty_schedule_break


def process_schedule_after_matching(schedule_breaks, channel_breaks, subcampaigns_dict:Dict[Subcampaign, str]) -> None:
    channel_break: ChannelBreak
    for channel_break in channel_breaks:
        if (
            channel_break.schedule_break is None
        ):  # jeżeli w schedulebrejkach nie ma brejka który mugby się zmaczować to musimy dodać do schedula schedulebrejka wytworzonego na podstaiwe channelbrejka
            channel_break.schedule_break = get_empty_schedule_break(channel_break.break_info)
            schedule_breaks.add(channel_break.schedule_break, channel_break.schedule_break.break_info.blockId)
        # po tym ifie każdy channel break ma schedule breaka
        subcampaign = subcampaigns_dict[channel_break.subcampaing_org]
        channel_break.schedule_break.book(subcampaign_id = subcampaign.id)

