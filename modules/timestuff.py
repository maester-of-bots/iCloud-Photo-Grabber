
import time
from datetime import datetime, timedelta
import pytz


# Constants for date and time format
UTC = pytz.UTC
DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S %Z%z'


# Function to convert string to datetime
def convert_to_datetime(date_string):
    """
    Convert a date string to a datetime object.

    Parameters:
    date_string (str): The date string to convert.

    Returns:
    datetime: The converted datetime object.
    """
    return datetime.strptime(date_string, DATE_FORMAT)


# Function to check if current time is daylight saving time
def is_daylight_saving():
    """
    Check if the current time is in daylight saving time.

    Returns:
    bool: True if it's daylight saving time, False otherwise.
    """
    return bool(time.localtime().tm_isdst)


# Function to adjust time for 'stupidApple' time discrepancy
def adjust_apple_time(created_time):
    """
    Adjust the time from Apple's format to standard format.

    Parameters:
    created_time (datetime): The original time from Apple.

    Returns:
    datetime: The adjusted time.
    """
    formatted_time = "{}-{}-{}-{}-{}-{}-{}".format(
        created_time.year, created_time.month, created_time.day,
        created_time.hour, created_time.minute,
        created_time.second, created_time.microsecond
    )
    parsed_time = datetime.strptime(formatted_time, '%Y-%m-%d-%H-%M-%S-%f')
    if is_daylight_saving():
        adjusted_time = parsed_time - timedelta(hours=4)
    else:
        adjusted_time = parsed_time - timedelta(hours=5)
    return adjusted_time


