from typing import List
from unittest import TestCase
from unittest.mock import patch, MagicMock

from coalesce import main
import config
from models import MemberRecord

TEST_RECORD_SET_A = [MemberRecord(1000, 10000, 5000),
                     MemberRecord(1200, 13000, 6000),
                     MemberRecord(1000, 10000, 6000)]
TEST_RECORD_SET_B = [MemberRecord(1000, 10000, 5000),
                     MemberRecord(2000, 13000, 7000),
                     None]


class CoalesceTest(TestCase):

    def test_coalesce_member_data(self):
        main._invoke_api = MagicMock(side_effect=TEST_RECORD_SET_A)
        response = main.coalesce_member_data(1, coalesce_function_name="mean")
        self.assertEqual(response["failed_sources"], 0)
        self.assertEqual(response["member_data"], MemberRecord(1066, 11000, 5666))

    def test_coalesce_member_data_returns_fail_count(self):
        main._invoke_api = MagicMock(side_effect=TEST_RECORD_SET_B)
        response = main.coalesce_member_data(1, coalesce_function_name="mean")
        self.assertEqual(response["failed_sources"], 1)
        self.assertEqual(response["member_data"], MemberRecord(1500, 11500, 6000))

    def test_builtin_agg_functions(self):
        max_record = main._apply_agg_function(TEST_RECORD_SET_A, config.FUNCTIONS["max"])
        self.assertEqual(MemberRecord(1200, 13000, 6000), max_record)
        min_record = (main._apply_agg_function(TEST_RECORD_SET_A, config.FUNCTIONS["min"]))
        self.assertEqual(MemberRecord(1000, 10000, 5000), min_record)
        mean_record = (main._apply_agg_function(TEST_RECORD_SET_A, config.FUNCTIONS["mean"]))
        self.assertEqual(MemberRecord(1066, 11000, 5666), mean_record)

    def test_can_use_custom_function(self):
        double_max = main._apply_agg_function(TEST_RECORD_SET_A, lambda x: max(x)*2)
        self.assertEqual(MemberRecord(2400, 26000, 12000), double_max)


