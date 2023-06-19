# This is a sample Python script.
import zzz_ordersTools as ot
import zzz_tools as t
import c_matching as matching
from classes.merger import get_merger
from classes.schedule import get_schedule
from zzz_enums import *
from zzz_projectTools import GluCannonColumnsList


def main():
    # print(calculate_circle_data(5, CircleDataType.PERIMETER))
    json_channels_path = r"C:\Users\macie\PycharmProjects\MnrwOrdersFlow\project\json channels.txt"
    json_copyLengths_path = r"C:\Users\macie\PycharmProjects\MnrwOrdersFlow\project\json copy lengths.txt"
    do_export = True

    df_channelsMapping = ot.get_channels_df(json_channels_path)
    df_copyIndexes = ot.get_copy_indexes_df(json_copyLengths_path)

    booking = ot.get_booking(GluSupplier.POLSAT, df_channelsMapping, df_copyIndexes)
    schedule = get_schedule(
        r"C:\Users\macie\PycharmProjects\MnrwOrdersFlow\project\source\1 schedule 2022-10-06 112529 Schedule czysta.txt",
        df_channelsMapping,
    )

    matching.match_channel_breaks_step1_id(booking.get_unmatched_channel_breaks(), schedule.schedule_breaks)
    matching.match_channel_breaks_step2_timebands(booking.get_unmatched_channel_breaks(), schedule.get_timebands_dict())
    if do_export:
        t.export_df(booking.to_dataframe(), "channel breaks")
        t.export_df(schedule.to_dataframe(), "schedule")
        # t.export_df(schedule.df, "1a schedule_processed")
        # t.export_df(booking.df, "1b booking_processed")
        # # t.export_df(df_matching, "2 matching")
        # df_channelBreaks = booking.get_df()
        # t.export_df(df_channelBreaks, "channel breaks")
        # t.export_df(df_channelsMapping, "channels_mapping")


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
