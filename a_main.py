# This is a sample Python script.
import c_matching as matching
import d_process_schedule as ps
import zzz_ordersTools as ot
import zzz_tools as t
from classes.schedule import get_schedule
from zzz_enums import *


def process_booking(supplier:GluSupplier, booking_quality:GluBookingQuality, schedule_type:GluScheduleType)->str:
    # print(calculate_circle_data(5, CircleDataType.PERIMETER))
    json_channels_path = r"C:\Users\macie\PycharmProjects\MnrwOrdersFlow\project\json channels.txt"
    json_copyLengths_path = r"C:\Users\macie\PycharmProjects\MnrwOrdersFlow\project\json copy lengths.txt"



    do_export_debug_files = True

    df_channelsMapping = ot.get_channels_df(json_channels_path)
    df_copyIndexes = ot.get_copy_indexes_df(json_copyLengths_path)

    booking = ot.get_booking(supplier, df_channelsMapping, df_copyIndexes, booking_quality=booking_quality)

    schedule = get_schedule(schedule_type, df_channelsMapping)

    ot.check_time_space_consistency(booking.df, schedule.df)
    matching.match_channel_breaks_step1_id(booking.get_unmatched_channel_breaks(), schedule.schedule_breaks)
    matching.match_channel_breaks_step2_timebands(booking.get_unmatched_channel_breaks(), schedule.get_timebands_dict())
    ps.process_schedule_after_booking(schedule.schedule_breaks, booking.channel_breaks)  # modyfikuje schedule brejki

    result_schedule_path = t.export_df(schedule.to_dataframe(GluExportFormat.ScheduleBreak_minerwa), "schedule - minerwa", file_type=t.GluFileType.CSV)

    if do_export_debug_files:
        t.export_df(booking.to_dataframe(GluExportFormat.ChannelBreak), "channel breaks")
        t.export_df(schedule.to_dataframe(GluExportFormat.ScheduleBreak_rozkminki), "schedule - rozkminki")


        # t.export_df(schedule.df, "1a schedule_processed")
        # t.export_df(booking.df, "1b booking_processed")
        # # t.export_df(df_matching, "2 matching")
        # df_channelBreaks = booking.get_df()
        # t.export_df(df_channelBreaks, "channel breaks")
        # t.export_df(df_channelsMapping, "channels_mapping")
    return result_schedule_path


def main():

    supplier:GluSupplier = GluSupplier.POLSAT
    booking_quality:GluBookingQuality = GluBookingQuality.OK
    schedule_type:GluScheduleType = GluScheduleType.OK_4CHANNELS

    # schedule_path = r"C:\Users\macie\PycharmProjects\MnrwOrdersFlow\project\source\1a schedule 2022-10-06 112529 Schedule czysta - wrong channels.txt"

    process_booking(supplier, booking_quality, schedule_type)
if __name__ == "__main__":
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
