#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json


class LogAnalyzer:

    def __init__(self, enable_debug=False):
        self.debug = enable_debug
        self.total_lines = 0
        self.invalid_lines = 0
        self.file_extensions = {}

    def analyse_log(self, log_file):
        if not os.path.exists(log_file):
            print(f"Log file {log_file} does not exist")
            return self.file_extensions

        with open(log_file, "r") as _log_file:

            for index, line in enumerate(_log_file):
                self.total_lines += 1

                log_data = self.parse_line(line, index)
                if not log_data:
                    continue

                name, extension = self.parse_filename(log_data, index)
                if name is not None and extension is not None:
                    name_set = self.file_extensions.setdefault(extension, set())
                    name_set.add(name)

        self.output_result()
        return self.file_extensions

    def parse_line(self, line, index):
        try:
            return json.loads(line)
        except:
            # Get bad data
            self.invalid_lines += 1
            if self.debug:
                print(f"line {index} - invalid json: {line}")
            return None

    def parse_filename(self, log_data, index):
        """
         Read each line from log file. Skip invalid line (invalid json, missing key field).
         Analysis file name and save it to a directory (file_extensions) per extension.
         Each extension saves a set of file names with this extension.
          :param log_data:
          :param index:
          :return:
        """
        if "nm" not in log_data:
            self.invalid_lines += 1
            if self.debug:
                print(f"line {index} - miss field 'nm' (file name): {log_data}")
            return None, None

        nm_list = log_data['nm'].split('.')
        if len(nm_list) == 1:
            # no extension
            extension = ""
            name = nm_list[0]
        else:
            extension = nm_list[-1]
            name = '.'.join(nm_list[:-1])

        return name, extension

    def output_result(self):
        for rtn_extension, rtn_name_set in self.file_extensions.items():
            print(f"{rtn_extension}: {len(rtn_name_set)}")

        if self.debug:
            self.debug_info()

    def debug_info(self):
        print(f"Get total lines {self.total_lines}; "
              f"invalid lines = {self.invalid_lines}; "
              f"Unique extensions = {len(self.file_extensions)}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Please provide log file ")
        sys.exit()

    user_log_file = sys.argv[1]

    analyzer = LogAnalyzer(enable_debug=True)
    analyzer.analyse_log(user_log_file)
