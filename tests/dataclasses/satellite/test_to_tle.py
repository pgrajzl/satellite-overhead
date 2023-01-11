from datetime import datetime

from satellite_determination.dataclasses.satellite import EPOCH_START_YEAR, InternationalDesignator, Satellite


class TestToTle:
    def test_name_takes_24_characters(self):
        tle_data = Satellite(name='name').to_tle()
        assert tle_data[0] == 'name                    '

    def test_line_number_exists(self):
        tle_data = Satellite().to_tle()
        assert all(line[0:1] == f'{i + 1}' for i, line in enumerate(tle_data[1:]))

    def test_catalog_number_is_padded_with_zeros(self):
        arbitrary_number_less_than_five_digits = 22
        tle_data = Satellite(catalog_number=arbitrary_number_less_than_five_digits).to_tle()
        assert all(line[2:7] == f'00022' for i, line in enumerate(tle_data[1:]))

    def test_classification_is_in_position_8(self):
        classification = 'C'
        tle_data = Satellite(classification=classification).to_tle()
        assert tle_data[1][7:8] == f'{classification}'

    def test_international_designator_year_is_padded(self):
        arbitrary_single_digit_year = 2
        tle_data = Satellite(international_designator=InternationalDesignator(year=arbitrary_single_digit_year, launch_number=0, launch_piece='')).to_tle()
        assert tle_data[1][9:11] == '02'

    def test_international_designator_launch_number_is_padded(self):
        arbitrary_launch_number_less_than_three_digits = 2
        tle_data = Satellite(international_designator=InternationalDesignator(year=0,
                                                                              launch_number=arbitrary_launch_number_less_than_three_digits,
                                                                              launch_piece='')
                             ).to_tle()
        assert tle_data[1][11:14] == '002'

    def test_international_designator_piece_is_padded(self):
        arbitrary_piece_less_than_three_characters = 'B'
        tle_data = Satellite(international_designator=InternationalDesignator(year=0,
                                                                              launch_number=0,
                                                                              launch_piece=arbitrary_piece_less_than_three_characters)
                             ).to_tle()
        assert tle_data[1][14:17] == 'B  '

    def test_epoch_year_is_padded(self):
        arbitrary_single_digit_year = 2
        arbitrary_datetime_with_single_digit_year = datetime(year=EPOCH_START_YEAR + arbitrary_single_digit_year, month=1, day=1)
        tle_data = Satellite(timestamp=arbitrary_datetime_with_single_digit_year).to_tle()
        assert tle_data[1][18:20] == '02'

    def test_epoch_day_is_padded(self):
        arbitrary_datetime_with_fractional_day = datetime(year=2000, month=2, day=1, hour=6)
        tle_data = Satellite(timestamp=arbitrary_datetime_with_fractional_day).to_tle()
        assert tle_data[1][20:32] == '32.250000000'

    def test_spaces_exist_in_correct_positions(self):
        expected_space_positions = [1, 8, 17, 32]
        tle_data = Satellite().to_tle()
        assert all(character == ' ' for character in (tle_data[1][position] for position in expected_space_positions))

