from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class TimeWindow:
    begin: datetime
    end: datetime

    @property
    def duration(self) -> timedelta:
        return self.end - self.begin

    def overlaps(self, time_window: 'TimeWindow'):
        return self.begin <= time_window.end and self.end >= time_window.begin
