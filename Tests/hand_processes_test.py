import pytest
from Cv.Hand.Recognized import get_coordinate, calculate_distance_between_finger, calculate_hand_distance


def test_distance_calculation():
    hand_landmark = [[0, 0], [10, 0]]  # Assuming hand width of 10 pixels
    focal_length = 1000  # Assuming focal length of 1000
    expected_distance = (0.05 * focal_length) / 10  # Expected distance calculation
    assert calculate_hand_distance(hand_landmark, focal_length) == pytest.approx(expected_distance, abs=0.001)


def test_zero_width_hand():
    hand_landmark = [[0, 0], [0, 0]]  git
    focal_length = 1000  # Assuming focal length of 1000
    with pytest.raises(ZeroDivisionError):
        calculate_hand_distance(hand_landmark, focal_length)


def test_negative_focal_length():
    hand_landmark = [[0, 0], [10, 0]]  # Assuming hand width of 10 pixels
    focal_length = -1000  # Negative focal length
    with pytest.raises(ValueError):
        calculate_hand_distance(hand_landmark, focal_length)


def test_large_focal_length():
    hand_landmark = [[0, 0], [10, 0]]  # Assuming hand width of 10 pixels
    focal_length = 1000000  # Very large focal length
    # The hand should appear very close to the camera, so distance should be small
    assert calculate_hand_distance(hand_landmark, focal_length) < 0.1


def test_invalid_input():
    hand_landmark = [[0, 0], [10, 0], [20, 0]]  # Invalid input with more than 2 landmarks
    focal_length = 1000  # Assuming focal length of 1000
    with pytest.raises(ValueError):
        calculate_hand_distance(hand_landmark, focal_length)
