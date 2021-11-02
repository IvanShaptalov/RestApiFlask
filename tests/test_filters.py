import pytest
from app.filters import filter


@pytest.mark.filtering
def test_digit_filter_invalid_args(number_list_invalid):
    for num in number_list_invalid:
        assert filter.check_is_digit(num) is False, f"filter think that {num} is number"


@pytest.mark.filtering
def test_digit_filter_valid_args(number_list_valid):
    for num in number_list_valid:
        assert filter.check_is_digit(num) is True, f"filter think that {num} is not number"


def test_digit_filter_below_zero(number_list_below_zero):
    for num in number_list_below_zero:
        assert filter.check_is_digit(num, below_zero=True) is True, f"expected True"

    for num in number_list_below_zero:
        assert filter.check_is_digit(num, above_zero=True) is False, f"expected False"


def test_digit_filter_above_zero(number_list_above_zero):
    for num in number_list_above_zero:
        assert filter.check_is_digit(num, above_zero=True) is True, f"expected True"

    for num in number_list_above_zero:
        assert filter.check_is_digit(num, below_zero=True) is False, f"expected False"
