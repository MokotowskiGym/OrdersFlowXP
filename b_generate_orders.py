
import zzz_ordersTools as ot

from classes.schedule import get_schedule

from zzz_enums import *


def main():
    supplier: Supplier = Supplier.POLSAT
    booking_quality: BookingQuality = BookingQuality.FUCKED_UP_DATES
    schedule_type: ScheduleType = ScheduleType.OK_4CHANNELS_1WANTED
    df_channelsMapping = ot.get_channels_df()

    schedule = get_schedule(schedule_type, df_channelsMapping)


if __name__ == "__main__":
    main()