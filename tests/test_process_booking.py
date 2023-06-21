import os
from unittest import TestCase

from a_main import process_booking
from classes.exceptions import MyProgramException
from zzz_enums import *


class TestProcessBooking(TestCase):

    def test_valid(self):
        result_schedule_path = process_booking(GluSupplier.POLSAT, GluBookingQuality.OK, GluScheduleType.OK_4CHANNELS)
        self.assertTrue(os.path.exists(result_schedule_path))


    def test_absent(self):
        # self.assertRaises(MyProgramException, process_booking , GluSupplier.POLSAT, GluBookingQuality.ABSENT_CHANNELS, GluScheduleType.OK_4CHANNELS)
        try:
            process_booking(GluSupplier.POLSAT, GluBookingQuality.ABSENT_CHANNELS, GluScheduleType.OK_4CHANNELS)
        except MyProgramException as e:
            error_ok = 'There are channels in booking that are absent in schedule' in str(e)

            self.assertTrue(error_ok)

    def test_illegal(self):
        pass