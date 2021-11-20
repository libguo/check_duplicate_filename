#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import unittest
import json

from log_check import LogAnalyzer


test_log_path = "tests/logs"


class TestCheckUniqueFileName(unittest.TestCase):

    def setUp(self) -> None:
        self.analyzer = LogAnalyzer(enable_debug=False)

    def tearDown(self) -> None:
        self.analyzer.output_result()

    def test_analyse_log_with_default_log(self):
        # Default json file, include
        # - normal line with valid json data
        #    - same file name with same file extension
        #    - same file name with different file extension
        #    - different file name with same file extension
        # - invalid line with bad json data
        # - invalid line with missing 'nm' field
        result = self.analyzer.analyse_log(os.path.join(test_log_path, "default_log.json"))

        self.assertEqual(len(result), 44)
        self.assertEqual(len(result['exe']), 173)
        self.assertEqual(len(result['xls']), 155)
        self.assertEqual(self.analyzer.total_lines, 10001)
        self.assertEqual(self.analyzer.invalid_lines, 3)

    def test_analyse_log_with_invalid_file(self):
        result = self.analyzer.analyse_log(os.path.join(test_log_path, "not_exist.json"))
        self.assertEqual(len(result), 0)

    def test_parse_line(self):
        miss_quote_str = """{"si":8214ebed-a31b-477f-ac5d-cd35fb04b810", "nm":"ywcgdssxa.qxd", }"""
        json_data = self.analyzer.parse_line(miss_quote_str, 0)
        self.assertFalse(json_data)

        incomplete_str = """{"si":8214ebed-a31b-477f-ac5d-cd35fb04b810", """
        json_data = self.analyzer.parse_line(incomplete_str, 0)
        self.assertFalse(json_data)

    def test_parse_filename_miss_field_nm(self):
        json_data = json.loads("""{ "nm1" : "ddf"}""")
        name, extension = self.analyzer.parse_filename(json_data, 0)
        self.assertTrue(name is None)
        self.assertTrue(extension is None)

    def test_parse_filename_with_dot(self):
        json_data = json.loads("""{ "nm" : "ddf.abc.bdc"}""")
        name, extension = self.analyzer.parse_filename(json_data, 0)
        self.assertEqual(name, "ddf.abc")
        self.assertEqual(extension, "bdc")

    def test_parse_filename_special_char_in_nm(self):
        nm_name = "啊dd*7e323e2)*&^6~~  "
        json_data = json.loads('{ "nm": "' + nm_name + '.vnb"}')
        name, extension = self.analyzer.parse_filename(json_data, 0)
        self.assertEqual(name, nm_name)
        self.assertEqual(extension, "vnb")

        json_data = json.loads('{ "nm": "vnb.' + nm_name + '"}')
        name, extension = self.analyzer.parse_filename(json_data, 0)
        self.assertEqual(name, "vnb")
        self.assertEqual(extension, nm_name)

        json_data = json.loads('{ "nm": "' + nm_name + '"}')
        name, extension = self.analyzer.parse_filename(json_data, 0)
        self.assertEqual(name, nm_name)
        self.assertEqual(extension, "")

    def test_long_filename(self):
        nm_name = ""
        for _ in range(10000):
            nm_name += "a"
        json_data = json.loads('{ "nm": "' + nm_name + '.vnb"}')
        name, extension = self.analyzer.parse_filename(json_data, 0)
        self.assertEqual(name, nm_name)
        self.assertEqual(extension, "vnb")


if __name__ == "__main__":
    unittest.main()
