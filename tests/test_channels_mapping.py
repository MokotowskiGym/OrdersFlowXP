from unittest import TestCase
import zzz_ordersTools as ot
import pandas as pd


class TestChannelsMapping(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.json_path = "./source/json channels.txt"

    def test_channels_mapping(self):
        df = ot.get_channels_df(self.json_path)
        self.assertIsInstance(df, pd.DataFrame)
        cannon_columns = "supplier channelGroup channel channelPossibleName".split()
        self.assertTrue(all(col in df.columns for col in cannon_columns))
