# Power System Simulator for Autonomous Robotics

This project simulates power consumption, battery drain, and safety conditions for an autonomous robotic system with multiple onboard loads (e.g., compute, sensors, and thrusters). It is designed to model realistic mission phases and provide telemetry and diagnostics useful for system integration and safety analysis.

## What This Simulator Does (v0.4)
- Models a battery with voltage and capacity (Ah)
- Models multiple electrical loads (Jetson, sensors, thrusters)
- Simulates mission phases with different current profiles (idle, transit, maneuver)
- Logs telemetry at 1 Hz to CSV
- Tracks remaining battery capacity over time
- Implements safety checks:
    - **Overcurrent detection**
    - **Low battery capacity detection**
- Generates plots for post-run analysis:
    - Total current vs time (with safety trigger markers)
    - Remaining battery capacity vs time

## Example Output

**Total Current vs Time with Safety Trigger**
The dashed red line indicates the first detected overcurrent event during a high-load maneuver phase, demonstrating how safety thresholds can be monitored during autonomous operation.

![Current vs Time](reports/examples/current_vs_time_overcurrent.png)

## Project Structure
src/ - Contains the simulator source code, organized by version as functionality evolved from basic battery modeling to safety-aware telemetry logging.

tools/ - Contains analysis and visualization scripts (e.g., plotting telemetry and marking safety events).

logs/ - Generated CSV telemetry logs from simulation runs (git-ignored).

reports/ - Generated plots and reports.

    reports/examples/ - contains curated example outputs tracked in git.

## How to run
```bash
python3 src/power_sim_v0.py

python3 tools/plot_run.py
```

## Motivation
This simulator was built as a foundation for understanding and validating power system behavior in autonomous robots. Really, I wanted to upgrade my previous understanding of managing battery levels and usage by considering indivudual embdedded components as opposed to a computer system as a whole.
