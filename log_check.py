#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json


def check_unique_filename(log_file):
    """
    Read each line from log file. Skip invalid line (invalid json, missing key field).
    Analysis file name and save it to a directory (file_extensions) per extension.
    Each extension saves a set of file names with this extension.
    :param log_file:
    :return:
    """
    if not os.path.exists(log_file):
        print(f"Log file {log_file} does not exist")
        return {}

    file_extensions = {}

    with open(log_file, "r") as _log_file:
        for index, line in enumerate(_log_file):
            try:
                log_data = json.loads(line)
            except:
                # Get bad data
                #print(f"line {index} - invalid json: {line}")
                continue

            if "nm" not in log_data:
                #print(f"line {index} - miss field 'nm' (file name): {line}")
                continue

            nm_list = log_data['nm'].split('.')
            if len(nm_list) == 1:
                # no extension
                extension = ""
                name = nm_list[0]
            else:
                extension = nm_list[-1]
                name = '.'.join(nm_list[:-1])

            name_set = file_extensions.setdefault(extension, set())

            name_set.add(name)

    #print(f"total lines = {total_lines}; invalid lines = {invalid_lines}; total unque = {total_unique_file_name}")
    return file_extensions


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Please provide log file ")
        sys.exit()

    log_file = sys.argv[1]

    rtn_file_extensions = check_unique_filename(log_file)
    for rtn_extension, rtn_name_set in rtn_file_extensions.items():
        print(f"{rtn_extension}: {len(rtn_name_set)}")
