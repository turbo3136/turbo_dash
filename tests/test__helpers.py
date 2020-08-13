import pytest
from turbo_dash._helpers import *


class TestHelpers:
    _list_of_0_to_31 = list(range(32))

    @pytest.mark.parametrize('length', _list_of_0_to_31)
    def test_length(self, length):
        test_string = generate_random_string(length=length)
        assert length == len(test_string)

    @pytest.mark.parametrize('length', _list_of_0_to_31)
    def test_lowercase_or_digit(self, length):
        test_string = generate_random_string(length=length)
        assert all(character.isdigit() or character.islower() for character in test_string)
