from datetime import datetime

from zzz_enums import *

FAKE_DATE = datetime(2005, 4, 2, 21, 37, 0)
FAKE_INT = 666
PATH_JSON_COPY_INDEXES = r"C:\Users\macie\PycharmProjects\MnrwOrdersFlow\project\json copy lengths.txt"
PATH_JSON_CHANNELS = r"C:\Users\macie\PycharmProjects\MnrwOrdersFlow\project\json channels.txt"
PATH_JSON_COPYLENGTHS = r"C:\Users\macie\PycharmProjects\MnrwOrdersFlow\project\json copy lengths.txt"
PATH_DICT_SUBCAMPAIGNS = r"C:\Users\macie\PycharmProjects\MnrwOrdersFlow\project\dict subcampaignss.txt"


def get_path_schedule(schedule_type: GluScheduleType) -> str:
    path: str
    if schedule_type == GluScheduleType.OK_4CHANNELS_CLEAR:
        path = r"C:\Users\macie\PycharmProjects\MnrwOrdersFlow\project\source\1 schedule 2022-10-06 112529 Schedule czysta.txt"
    elif schedule_type == GluScheduleType.ILLEGAL_CHANNELS:
        path = r"C:\Users\macie\PycharmProjects\MnrwOrdersFlow\project\source\1a schedule 2022-10-06 112529 Schedule czysta - wrong channels.txt"
    elif schedule_type == GluScheduleType.OK_4CHANNELS_1WANTED:
        path = r"C:\Users\macie\PycharmProjects\MnrwOrdersFlow\project\source\1b schedule 2022-10-06 112529 Schedule wanted.txt"

    else:
        raise ValueError("Wrong schedule type")

    return path
