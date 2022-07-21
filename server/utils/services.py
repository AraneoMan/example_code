import traceback
from logging import Handler, LogRecord

from utils.constants import NONE_LOG_EVENT_TYPE


class DatabaseLogHandler(Handler):
    def emit(self, record: LogRecord):
        if record.levelname not in ('INFO', 'WARNING', 'ERROR'):
            return

        user = getattr(record, 'user', None)
        event_type = getattr(record, 'event_type', NONE_LOG_EVENT_TYPE)
        message = record.msg
        extra = getattr(record, 'extra', {})
        if not isinstance(extra, dict):
            extra = {'extra': extra}

        traceback_string = None
        if exception := getattr(record, 'exception', None):
            traceback_string = ''.join(traceback.format_exception(exception))
        elif exc_info := getattr(record, 'exc_info', None):
            traceback_string = ''.join(traceback.format_exception(exc_info))

        from utils.models import Log
        Log.objects.create(
            user=user,
            level=record.levelname,
            event_type=event_type,
            message=message,
            traceback=traceback_string,
            extra=extra,
        )
