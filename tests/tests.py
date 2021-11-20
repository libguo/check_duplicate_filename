#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import unittest
import datetime

from log_check import check_unique_filename


test_log_path = "tests/logs"


class TestCheckUniqueFileName(unittest.TestCase):

    def test_performance_default_log(self):
        # like to do performance test, but 10,000 lines are not big. just show intention.
        # in fact, the solution doesn't support performance/load very well.
        before = datetime.datetime.now()

        result = check_unique_filename(os.path.join(test_log_path, "default_log.json"))

        after = datetime.datetime.now()

        self.assertTrue((after - before).total_seconds() < 1)

        self.assertEqual(len(result), 44)
        self.assertEqual(len(result['exe']), 173)
        self.assertEqual(len(result['xls']), 155)

    def test_invalid_file(self):
        result = check_unique_filename(os.path.join(test_log_path, "not_exist.json"))
        self.assertEqual(len(result), 0)

    def test_invalid_json(self):
        result = check_unique_filename(os.path.join(test_log_path, "invalid_json.json"))
        self.assertEqual(len(result), 1)
        self.assertEqual(len(result['ext']), 1)

    def test_special_char_filename(self):
        result = check_unique_filename(os.path.join(test_log_path, "special_char_filename.json"))
        self.assertEqual(len(result), 1)
        self.assertEqual(len(result['txt']), 1)

    def test_long_filename(self):
        result = check_unique_filename(os.path.join(test_log_path, "long_filename.json"))
        self.assertEqual(len(result), 1)
        self.assertEqual(len(result['txt']), 4)

    def test_dup_extension(self):
        """
        this include
        1. same file name with different file extension.
        2. same file name with same file extension.
        3. no file extension.
        :return:
        """
        result = check_unique_filename(os.path.join(test_log_path, "dup_extension.json"))
        self.assertEqual(len(result['txt']), 1)
        self.assertEqual(len(result['qxd']), 1)
        self.assertEqual(len(result['ext']), 1)
        self.assertEqual(len(result['']), 2)
        self.assertEqual(len(result['psp']), 2)


if __name__ == "__main__":
    unittest.main()
