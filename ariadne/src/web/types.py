import datetime

from ariadne import ScalarType


datetime_scalar = ScalarType("Datetime")


@datetime_scalar.serializer
def serialize_datetime_scalar(date) -> str:
    return date.isoformat()


@datetime_scalar.value_parser
def parse_datetime_scalar(date):
    return datetime.datetime.fromisoformat(date)
