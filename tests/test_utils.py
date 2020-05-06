import pytest

from pdepy.utils import validate_method


class TestValidateMethod:
    @pytest.fixture
    def dummy_func(self):
        @validate_method(valid_methods=["m1"])
        def dummy(*, method):
            pass

        return dummy

    def test_valid(self, dummy_func):
        assert dummy_func(method="m1") is None

    def test_invalid(self, dummy_func):
        with pytest.raises(Exception):
            dummy_func(method="m2")
