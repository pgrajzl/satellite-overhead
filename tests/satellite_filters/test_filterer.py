from sopp.satellite_filters.filterer import Filterer


class TestFilterer:
    def test_add_filter(self):
        filterer = (
            Filterer()
            .add_filter(lambda x: x % 2)
        )

        assert len(filterer._filters) == 1

    def test_apply_filter(self):
        values = [1, 12, 16, 40, 42, 43, 44, 45, 47, 48, 50]
        actual = (
            Filterer()
            .add_filter(lambda x: x % 2 == 0)
            .add_filter(lambda x: x > 40)
            .add_filter(lambda x: x < 47)
            .apply_filters(values)
        )

        assert actual == [ 42, 44 ]
