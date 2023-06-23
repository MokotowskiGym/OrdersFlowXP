import os
from unittest import TestCase

from a_main import process_booking
from classes.exceptions import *
from zzz_enums import *


class TestProcessBooking(TestCase):

    def test_valid(self):
        result_schedule_path = process_booking(GluSupplier.POLSAT, GluBookingQuality.OK, GluScheduleType.OK_4CHANNELS)
        self.assertTrue(os.path.exists(result_schedule_path))


    def test_absent_channels_in_schedule(self):

        try:
            process_booking(GluSupplier.POLSAT, GluBookingQuality.ABSENT_CHANNELS, GluScheduleType.OK_4CHANNELS)
        except MergerException as e:
            self.assertEqual(GluExceptionType.MERGER_ABSENT_CHANNELS,e.exception_type )

    def test_illegal_channels_in_booking(self):

        try:
            process_booking(GluSupplier.POLSAT, GluBookingQuality.ILLEGAL_CHANNELS, GluScheduleType.OK_4CHANNELS)
        except MergerException as e:
            self.assertEqual(GluExceptionType.MERGER_ILLEGAL_CHANNELS_IN_BOOKING, e.exception_type)

    def test_illegal_channels_in_schedule(self):

        try:
            process_booking(GluSupplier.POLSAT, GluBookingQuality.OK, GluScheduleType.ILLEGAL_CHANNELS)
        except MergerException as e:
            self.assertEqual(GluExceptionType.MERGER_ILLEGAL_CHANNELS_IN_SCHEDULE,e.exception_type )


    def test_illegal(self):
        pass