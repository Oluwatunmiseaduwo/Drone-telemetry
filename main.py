import math
import random
import csv

# The flight path: (x, y, altitude) meters.
# This route is a square, 50m per side, and 10m up.

Waypoints = [(0, 0, 10), (50, 0, 10), (50, 50, 10), (0, 50, 10), (0, 0, 10)]

dt = 0.1 # timestep: the simulation advances 0.1 seconds at a time
speed = 5.0 # drone speed, meter per second (m/s)

def fly():
    x, y, a = 0.0, 0.0, 0.0 # the drone starts on the ground
    t = 0.0 # elapsed time in seconds
    rows = [] # save each GPS reading
    steps = 0 # counts the 0.1s so we know when a full second passed
    imu_rows = [] # each IMU reading are saved here
    prev_vx, prev_vy, prev_va = 0.0, 0.0, 0.0 # for previous velocity at each step

    for (wx,wy,wa) in Waypoints: # To keep moving towards the waypoint until we arrive

        while True:
            dx, dy, da = wx - x, wy - y, wa - a
            dist = math.sqrt(dx * dx + dy * dy + da * da)
            if dist < speed * dt:  # when it is close enough; snap to the waypoint
                x, y, a = wx, wy, wa
                break
            step = (speed * dt) / dist # remaining distance
            old_x, old_y, old_a = x, y, a
            x += dx * step
            y += dy * step
            a += da * step
            t += dt
            vx = (x - old_x) / dt # to find velocity, divide the distance by time
            vy = (y - old_y) / dt
            va = (a - old_a) / dt
            ax = (vx - prev_vx) / dt + random.uniform(-0.2, 0.2) # acceleration + noise
            ay = (vy - prev_vy) / dt + random.uniform(-0.2, 0.2)
            aa = (va - prev_va) / dt + random.uniform(-0.2, 0.2) # acceleration + noise + gravity
            imu_rows.append([round(t, 1), round(ax, 2), round(ay, 2), round(aa, 2)])
            prev_vx, prev_vy, prev_va = vx, vy, va

            steps += 1
            if steps % 10 == 0: # 10 steps * 0.1s = 1 second so it is time for a GPS reading
                gx = x + random.uniform(-1.5, 1.5) # GPS x = true x + noise
                gy = y + random.uniform(-1.5, 1.5) # GPS y = true y + noise
                ga = a + random.uniform(-0.5, 0.5) # GPS altitude + smaller noise
                rows.append([round(t, 1), round(x, 1), round(y, 1), round(a, 1), round(gx, 1), round(gy, 1), round(ga, 1)])
        print(f"t={t:5.1f}s reached ({wx}, {wy}, {wa}) pos=({x:.1f}, {y:.1f}, {a:.1f})")

    print("Flight complete.")

    with open("telemetry_clean.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["time", "true_x", "true_y", "true_a", "gps_x", "gps_y", "gps_a"])
        writer.writerows(rows)
    print(f"Saved {len(rows)} GPS readings to telemetry_clean.csv")

    with open("imu_clean.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["time", "accel_x", "accel_y", "accel_a"])
        writer.writerows(imu_rows)
    print(f"Saved {len(imu_rows)} IMU readings to imu_clean.csv")

if __name__ == "__main__":
    fly()