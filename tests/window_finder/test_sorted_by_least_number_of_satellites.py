from datetime import datetime, timedelta
from typing import List

from satellite_determination.dataclasses.frequency_range import FrequencyRange
from satellite_determination.dataclasses.overhead_window import OverheadWindow
from satellite_determination.dataclasses.reservation import Reservation
from satellite_determination.dataclasses.satellite import Satellite
from satellite_determination.dataclasses.time_window import TimeWindow
from satellite_determination.window_finder import WindowFinder
from tests.window_finder.definitions import ARBITRARY_FACILITY
from tests.window_finder.support.validator_satellites_are_overhead_at_specific_times import \
    ValidatorSatellitesAreOverheadAtSpecificTimes


class TestSortedByLeastNumberOfSatellites:
    def test(self):
        suggestions = WindowFinder(
            ideal_reservation=self._reservation,
            satellites=[window.satellite for window in self._overhead_windows],
            validator=ValidatorSatellitesAreOverheadAtSpecificTimes(
                overhead_times=[window.overhead_time for window in self._overhead_windows]),
            start_time_increments=timedelta(days=1),
            search_window=timedelta(weeks=1)
        ).find()
        assert suggestions == self._expected_suggestions

    @property
    def _overhead_windows(self) -> List[OverheadWindow]:
        arbitrary_frequency_range = FrequencyRange(high_in_megahertz=2., low_in_megahertz=1.)
        arbitrary_satellite_number = 'satellite_number'
        return [
            OverheadWindow(satellite=Satellite(frequency=arbitrary_frequency_range,
                                               satellite_number=arbitrary_satellite_number,
                                               name='name1'),
                           overhead_time=TimeWindow(begin=datetime(year=2022, month=11, day=20),
                                                    end=datetime(year=2022, month=11, day=20, hour=1))),
            OverheadWindow(satellite=Satellite(frequency=arbitrary_frequency_range,
                                               satellite_number=arbitrary_satellite_number,
                                               name='name2'),
                           overhead_time=TimeWindow(begin=datetime(year=2022, month=11, day=20),
                                                    end=datetime(year=2022, month=11, day=20, hour=1))),
            OverheadWindow(satellite=Satellite(frequency=arbitrary_frequency_range,
                                               satellite_number=arbitrary_satellite_number,
                                               name='name3'),
                           overhead_time=TimeWindow(begin=datetime(year=2022, month=11, day=21),
                                                    end=datetime(year=2022, month=11, day=21, hour=1))),
        ]

    @property
    def _reservation(self) -> Reservation:
        return Reservation(
            facility=ARBITRARY_FACILITY,
            time=TimeWindow(begin=datetime(year=2022, month=11, day=20), end=datetime(year=2022, month=11, day=21)))

    @property
    def _expected_suggestions(self) -> List[datetime]:
        return [
            datetime(year=2022, month=11, day=19),
            datetime(year=2022, month=11, day=22),
            datetime(year=2022, month=11, day=18),
            datetime(year=2022, month=11, day=23),
            datetime(year=2022, month=11, day=17),
            datetime(year=2022, month=11, day=21),
            datetime(year=2022, month=11, day=20)
        ]
