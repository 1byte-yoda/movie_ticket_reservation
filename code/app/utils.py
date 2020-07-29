from datetime import datetime


def deserialize_datetime(datetime_obj):
    """Deserialize a datetime object to string to be fed in JSON data."""
    if isinstance(datetime_obj, datetime):
        datetime_obj = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
    return datetime_obj
