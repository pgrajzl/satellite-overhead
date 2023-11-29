from datetime import datetime
from sopp.custom_dataclasses.frequency_range.frequency_range import FrequencyRange
from sopp.custom_dataclasses.satellite.satellite import Satellite
from sopp.custom_dataclasses.reservation import Reservation
from sopp.custom_dataclasses.facility import Facility, Coordinates
from sopp.custom_dataclasses.time_window import TimeWindow
from sopp.frequency_filter.frequency_filter import FrequencyFilter


class TestFrequencyFilter:

    def test_single_sat_no_bandwidth(self):
        frequency_filtered_sats = FrequencyFilter(satellites=[self._arbitrary_satellite_in_band], observation_frequency=self._arbitrary_reservation_with_nonzero_timewindow.frequency).filter_frequencies()
        assert frequency_filtered_sats == [
            Satellite(
                name='name',
                frequency=[FrequencyRange(
                    frequency=136,
                    bandwidth=None
                )]
            )
        ]

    def test_two_sats_no_bandwidth(self):
        frequency_filtered_sats = FrequencyFilter(satellites=[self._arbitrary_satellite_in_band, self._arbitrary_satellite_out_of_band()], observation_frequency=self._arbitrary_reservation_with_nonzero_timewindow.frequency).filter_frequencies()
        assert frequency_filtered_sats == [
            Satellite(
                name='name',
                frequency=[FrequencyRange(
                    frequency=136,
                    bandwidth=None
                )]
            )
        ]

    def test_single_sat_with_bandwidth(self):
        frequency_filtered_sats = FrequencyFilter(satellites=[self._arbitrary_satellite_with_bandwidth], observation_frequency=self._arbitrary_reservation_with_nonzero_timewindow.frequency).filter_frequencies()
        assert frequency_filtered_sats == [
            Satellite(
                name='name',
                frequency=[FrequencyRange(
                    frequency=128,
                    bandwidth=10
                )]
            )
        ]

    def test_inactive_sat(self):
        frequency_filtered_sats = FrequencyFilter(satellites=[self._arbitrary_inactive_satellite()], observation_frequency=self._arbitrary_reservation_with_nonzero_timewindow.frequency).filter_frequencies()
        assert frequency_filtered_sats == []

    def test_active_and_inactive_sat(self):
        frequency_filtered_sats = FrequencyFilter(satellites=[self._arbitrary_satellite_with_bandwidth, self._arbitrary_inactive_satellite()], observation_frequency=self._arbitrary_reservation_with_nonzero_timewindow.frequency).filter_frequencies()
        assert frequency_filtered_sats == [
            Satellite(
                name='name',
                frequency=[FrequencyRange(
                    frequency=128,
                    bandwidth=10
                )]
            )
        ]

    def test_no_frequency_data_sat(self):
        no_freq_data_sat = self._arbitrary_satellite_in_band
        no_freq_data_sat.frequency = []

        sats = FrequencyFilter(
            satellites=[no_freq_data_sat],
            observation_frequency=self._arbitrary_reservation_with_nonzero_timewindow.frequency
        ).filter_frequencies()

        assert sats == [
            Satellite(
                name='name',
                frequency=[]
            )
        ]

    def test_frequency_data_none(self):
        frequency_filtered_sats = FrequencyFilter(
            satellites=[self._arbitrary_satellite_freq_is_none],
            observation_frequency=self._arbitrary_reservation_with_nonzero_timewindow.frequency
        ).filter_frequencies()

        assert frequency_filtered_sats == [
            Satellite(
                name='name',
                frequency=[FrequencyRange(
                    frequency=None,
                    bandwidth=None
                )]
            )
        ]
            
    @property
    def _arbitrary_satellite_in_band(self) -> Satellite:
        return Satellite(
            name='name',
            frequency=[FrequencyRange(
                frequency=136,
                bandwidth=None
            )]
        )

    def _arbitrary_satellite_out_of_band(self) -> Satellite:
        return Satellite(
            name='name',
            frequency=[FrequencyRange(
                frequency=200,
                bandwidth=None
            )]
        )

    @property
    def _arbitrary_satellite_with_bandwidth(self) -> Satellite:
        return Satellite(
            name='name',
            frequency=[FrequencyRange(
                frequency=128,
                bandwidth=10
            )]
        )

    def _arbitrary_inactive_satellite(self) -> Satellite:
        return Satellite(
            name='name',
            frequency=[FrequencyRange(
                frequency=130,
                bandwidth=10,
                status='inactive'
            )]
        )

    @property
    def _arbitrary_satellite_freq_is_none(self) -> Satellite:
        return Satellite(
            name='name',
            frequency=[FrequencyRange(
                frequency=None,
                bandwidth=None
            )]
        )

    @property
    def _arbitrary_reservation_with_nonzero_timewindow(self) -> Reservation:
        return Reservation(facility=Facility(elevation=0,
                                             coordinates=Coordinates(latitude=0, longitude=0),
                                             name='name'),
                           time=TimeWindow(begin=datetime(year=2001, month=2, day=1, hour=1),
                                           end=datetime(year=2001, month=2, day=1, hour=6)),
                           frequency=FrequencyRange(
                                           frequency=135.5,
                                           bandwidth=10
                           )
                           )
