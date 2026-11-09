from detector import expected_position, grade

# Making unit test using the planned-route math, checked on its own

def test_origin_route(): # During the 2-second climb, x and y have not moved yet
    assert expected_position(0.0) == (0.0, 0.0)
    assert expected_position(2.0) == (0.0, 0.0)

def test_mid_first_route(): # t=7 is halfway through the first side
    assert expected_position(7.0) == (25.0, 0.0)

def test_mid_second_route(): # t=7 is halfway through the second side
    assert expected_position(17.0) == (50.0, 25.0)
    assert expected_position(42.0) == (0.0, 0.0) # The route ends back where it started

# Making Integration test for the real log files in the full pipelines

def test_clean_no_false_alarms():
    tp, fp, fn, tn, delay = grade("telemetry_clean.csv")
    assert tp == 0
    assert fp == 0
    assert tn == 42

def test_detector_for_the_drift():
    tp, fp, fn, tn, delay = grade("telemetry_faulty.csv")
    assert fp == 0 # still no false alarms even on the faulty log
    assert tp >= 5 # it catches most of the fault readings
    assert delay is not None and delay <= 5.0 # and it catches them quickly
