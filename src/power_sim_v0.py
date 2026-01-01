# src/power_sim_v0.py
"""
v0: Battery drain simulation with a simple mission timeline.

Concepts:
- Power (W) = V * I
- Battery capacity is in amp-hours (Ah)
- Used capacity (Ah) = Current (A) * Time (hours)
"""

from dataclasses import dataclass

@dataclass
class Battery:
    voltage_v: float
    capacity_ah: float

def run_sim():
    # Battery model
    battery = Battery(voltage_v=14.8, capacity_ah=10.0)
    remaining_ah = battery.capacity_ah

    # Load model (one motor)
    motor_current_idle_a = 1.0
    motor_current_active_a = 5.0

    # Mission timeline: (state, duration_seconds)
    timeline = [
        ("idle", 30),
        ("active", 60),
        ("idle", 30),
    ]

    print("=== Power Sim v0 ===")
    print(f"Battery: {battery.voltage_v:.1f} V, {battery.capacity_ah:.2f} Ah\n")

    t_s = 0
    for state, duration_s in timeline:
        duration_h = duration_s / 3600.0

        if state == "idle":
            current_a = motor_current_idle_a
        elif state == "active":
            current_a = motor_current_active_a
        else:
            raise ValueError(f"Unknown state: {state}")

        used_ah = current_a * duration_h
        remaining_ah -= used_ah

        power_w = battery.voltage_v * current_a

        t_s += duration_s
        print(
            f"t={t_s:>4}s | state={state:<6} | I={current_a:>4.1f} A | "
            f"P={power_w:>6.1f} W | used={used_ah:.4f} Ah | remaining={remaining_ah:.4f} Ah"
        )

    avg_current_a = (battery.capacity_ah - remaining_ah) / (t_s / 3600.0)
    est_runtime_h = battery.capacity_ah / avg_current_a if avg_current_a > 0 else float("inf")

    print("\n=== Summary ===")
    print(f"Total simulated time: {t_s} s")
    print(f"Average current draw: {avg_current_a:.2f} A")
    print(f"Estimated runtime at avg draw: {est_runtime_h:.2f} hours")

if __name__ == "__main__":
    run_sim()

