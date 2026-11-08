# Drone Telemetry Anomaly Detection

This is a software-in-the-loop drone simulation in Python. A virtual drone flies a waypoint route while simulated sensors;
 GPS and an IMU (Inertial Measurement Unit which is the accelerometer motion sensor); stream telemetry to log files. I am
going to add later sessions for injecting sensor faults i.e. GPS drift, IMU spikes, battery sag, motor failure etc. and build
a detector that flags them from the logs, graded on precision, recall, F1 score, and detection delay.
I built as a hands-on practice with simulation, sensor data, and telemetry-based debugging; the workflow real flight software 
teams use before anything files on hardware.

## Scope

This is a simulation so no real drone, ROS/ROS2, or real hardware. The sensor behavior is simplified but, I modeled it based
on how real sensors behave.

## How To Run It

I used PyCharm (using virtual environment and python 3.13) and ran main.py.
The output is the flight progress in console and 2 log files:
- 'telemetry_clean.csv' - GPS readings, 1 per second
- 'imu_clean.csv' - IMU reading, 10 per second

## First Session - Simulation + Telemetry Logging: Nov 3, 2026

**What I built**
- A flight model: the drone flies a 50m x 50m square route at 10m altitude, advancing in a fixed 0.1-second timesteps to imitates the check-move-check loop used in a flight software 
- A simulated GPS: it reports the true position and random noise i.e. ±1.5m horizontal, ±0.5m altitude, sampled once per second
- A simulated IMU: to get acceleration computed from velocity changes, sampled 10x per second; the vertical axis includes gravity (9.81), as a real accelerometer
- A full clean flight runs end to end and writes both telemetry logs
- **Results**: Flight time was 42.0 seconds, 5 waypoints reached with 42 GPS readings and 420 IMU readings saved

**What I learnt**

I learnt how to simulate a drone flying along a planed route, calculate its movement. I imitate GPS and IMU sensor readings,
and save the collected data into CSV files. I tried to model a real-world system behaves.

## Second Session - Fault injection + detector: Nov 4, 2026



## Limits

- Simulation only: The sensor noise is uniform random, not physical model
- It is a rule-based detection not a trained machine learning (ML) model
- 