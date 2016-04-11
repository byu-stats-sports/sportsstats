#!/usr/bin/env python

"""Utilities used in sportsstats
"""

import json


def write_file(path, content):
    with open(path, 'w') as f:
        f.write(content)


def beautify_json(content):
    """Parse JSON string and make it more human readable
    """
    json_data = json.loads(content)
    return json.dumps(json_data, sort_keys=True, indent=4)


def split_date(date):
    count = date.count('-')
    if count == 1:
        split = date.split('-')
        start = split[0]
        end = split[1]
    elif count == 0:
        start = end = date
    else:
        raise ValueError("Incorrect date format.")
    return (start, end)


def add_years(dt, years):
    try:
        dt = dt.replace(year=dt.year+years)
    except ValueError:
        # handle leap years
        dt = dt.replace(year=dt.year+years, day=dt.day-1)
    return dt
