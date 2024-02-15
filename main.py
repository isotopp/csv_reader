#! /usr/bin/env python
#
# Python 3.11 used
#

import csv
import re
from dataclasses import make_dataclass
from typing import List, Union, Type, Any


def sanitize_field_name(field_name: str) -> str:
    """
    Sanitize a CSV header field name to ensure it's a valid Python identifier.

    This includes prepending 'f_' if the name starts with a digit, transliterating German umlauts,
    replacing invalid characters with '_', and collapsing consecutive underscores.

    :param field_name: The original field name from the CSV header.
    :return: A sanitized version of the field name suitable for use as a Python identifier.
    """
    if field_name[0].isdigit():
        field_name = 'F' + field_name

    transliterations = {
        'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss',
        'Ä': 'Ae', 'Ö': 'Oe', 'Ü': 'Ue',
    }
    for umlaut, transliteration in transliterations.items():
        field_name = field_name.replace(umlaut, transliteration)

    field_name = re.sub(r'[^a-zA-Z0-9_]', '_', field_name)
    field_name = re.sub(r'__+', '_', field_name)

    return field_name


def maybe_float(value: str) -> Union[str, float]:
    """
    Attempt to convert a string to a float, returning the string itself if conversion fails.

    :param value: The string value to attempt to convert.
    :return: The converted float value, or the original string if conversion is not possible.
    """
    try:
        return float(value)
    except ValueError:
        return value


def create_dataclass_from_csv(csv_filepath: str) -> List[Any]:
    """
    Dynamically create instances of a dataclass named DynamicDataClass based on CSV data.

    The dataclass fields are determined by the CSV headers, with values converted to float where possible.

    :param csv_filepath: Path to the CSV file.
    :return: A list of dataclass instances with CSV data.
    """
    with open(csv_filepath, newline='') as csvfile:
        reader = csv.reader(csvfile)
        _ = next(reader)  # skip sep=,
        original_field_names = next(reader)
        field_names = [(sanitize_field_name(name), Union[str, float]) for name in original_field_names]

    # Create the dataclass dynamically, specifying fields as Union[str, float]
    DynamicDataClass: Type[Any] = make_dataclass(
        'DynamicDataClass',
        field_names,
        frozen=True,
        slots=True
    )

    result = []
    with open(csv_filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=[name for name, _ in field_names])
        _ = next(reader)  # skip sep=,
        next(reader)  # Skip the header row as we already processed it
        for row in reader:
            row = {key: maybe_float(value) for key, value in row.items()}
            data_instance = DynamicDataClass(**row)
            result.append(data_instance)

    return result


# Example usage
csv_filepath = 'testdata.csv'
data_instances = create_dataclass_from_csv(csv_filepath)
for instance in data_instances:
    print(instance)
    print(f"{instance.Waermepumpe=}")

things = sorted(dir(data_instances[0]))
print(things)