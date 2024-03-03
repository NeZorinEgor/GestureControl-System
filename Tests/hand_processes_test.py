import pytest
from Cv.Hand.Recognized import get_coordinate, calculate_distance_between_finger, calculate_hand_distance


def test_zero_width_hand():
    hand_landmark = [[0, 0], [0, 0]]
    focal_length = 1000
    with pytest.raises(ZeroDivisionError):
        calculate_hand_distance(hand_landmark, focal_length)


def test_distance_positive_values():
    assert calculate_distance_between_finger(0, 0, 3, 4) == 5.0


def test_distance_negative_values():
    assert calculate_distance_between_finger(-1, -1, -4, -5) == 5.0


def test_distance_fractional_values():
    assert calculate_distance_between_finger(1.5, 2.5, 4.5, 6.5) == 5.0
