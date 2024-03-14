import json
import zlib
from uuid import uuid4
from datetime import datetime, timezone
from typing import Optional

from sopp.custom_dataclasses.reservation import Reservation


class Tardys4Generator:
    """
    A class that generates a spectrum reservation for the TARDYs4 specification.

    Parameters:
    - reservation: The Reservation object used during satellite interference
      detection.
    - begin: The elected begin time for the actual observation.
    - end: The elected end time for the actual observation.
    - location_radius: The protection radius in km. Defaults to 1.
    """

    def __init__(
        self,
        reservation: Reservation,
        begin: datetime,
        end: datetime,
        dpa_id: Optional[str] = None,
        location_radius: float = 1
    ):
        self._reservation = reservation
        self._begin = begin.astimezone(timezone.utc).isoformat()
        self._end = end.astimezone(timezone.utc).isoformat()
        self._loc_radius = location_radius
        self._loc_lat = reservation.facility.coordinates.latitude
        self._loc_long = reservation.facility.coordinates.longitude
        self._elevation = reservation.facility.elevation
        self._freq_start_hz = int(reservation.frequency.low_mhz * 10**6)
        self._freq_end_hz = int(reservation.frequency.high_mhz * 10**6)
        self._region_size = reservation.facility.beamwidth
        self._transaction_id = str(uuid4())
        self._dpa_id = dpa_id
        self._time = datetime.now(timezone.utc).isoformat()
        self._event_id = str(uuid4())

    def generate(self):
        tardys4 = {
            "transactionId": self._transaction_id,
            "dateTimePublished": self._time,
            "dateTimeCreated": self._time,
            "checksum": self._checksum,
            "scheduledEvents": self._scheduled_events,
        }

        self._tardys4 = tardys4

        return self._tardys4

    @property
    def _scheduled_events(self):
        return [
            {
                "eventId": self._event_id,
                "dpaId": self._dpa_id,
                "locLat": self._loc_lat,
                "locLong": self._loc_long,
                "locRadius": self._loc_radius,
                "locElevation": self._elevation,
                "coordType": "azel",
                "eventStatus": "actual",
                "dateTimeStart": self._begin,
                "dateTimeEnd": self._end,
                "freqStart": self._freq_start_hz,
                "freqStop": self._freq_end_hz,
                "regionSize": self._region_size,
                "regionX": 90,
                "regionY": 45,
            },
        ]

    @property
    def _checksum(self) -> str:
        return format(zlib.crc32(json.dumps(self._scheduled_events).encode()), "x")

    def write_to_file(self, filename: str = "tardys4_reservation.json"):
        if self._tardys4 is None:
            self.generate()
        with open(filename, "w") as f:
            json.dump(self._tardys4, f)
