import csv
import math

# The planned route is (time, x, y) which is where the drone is supposed to be
# It climbs for the first 2 seconds then flies the square at 5 m/s, so each 50m side takes 10 seconds.
plan = [(2.0, 0.0, 0.0), (12.0, 50.0, 0.0), (22.0, 50.0, 50.0), (32.0, 0.0, 50.0), (42.0, 0.0, 0.0)]
threshold = 4.0 # for the meters off the planned route before we call it a fault.
fault_start = 20.0 # the second the injected fault begins from main.py.

def expected_position(t):
    """Where the plan says the drone should be at time t."""
    if t <= plan[0][0]:
        return plan[0][1], plan[0][2]
    for i in range(len(plan) - 1):
        t1, x1, y1 = plan[i]
        t2, x2, y2 = plan[i + 1]
        if t1 <= t <= t2:
            frac = (t - t1) / (t2 - t1) # how far along this side are we?
            return x1 + frac * (x2 - x1), y1 + frac * (y2 - y1)
    return plan[-1][1], plan[-1][2]

def grade(filename):
    tp = fp = fn = tn = 0 # true/false positives, false negatives, true negatives
    first_flag_time = None
    with open(filename) as f:
        for row in csv.DictReader(f):
            t = float(row["time"])
            ex, ey = expected_position(t)
            err = math.sqrt((float(row["gps_x"]) - ex) ** 2 + (float(row["gps_y"]) - ey) ** 2)
            flagged = err > threshold
            actual = int(row["is_fault"]) == 1
            if flagged and actual:
                tp += 1
                if first_flag_time is None:
                    first_flag_time = t
            elif flagged:
                fp += 1
            elif actual:
                fn += 1
            else:
                tn += 1

    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    delay = first_flag_time - fault_start if first_flag_time is not None else None

    print(f"File: {filename}")
    print(f"Caught (TP): {tp}  False alarms (FP): {fp}  Missed (FN): {fn}  Correctly quiet (TN): {tn}")
    print(f"Precision: {precision:.2f}  Recall: {recall:.2f}  F1: {f1:2f}")
    print(f"Detection delay: {delay} seconds after the fault started")

if __name__ == "__main__":
    grade("telemetry_clean.csv")
    grade("telemetry_faulty.csv")
