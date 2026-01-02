"""
v0.1: Multi-load power simulation with mission phases.

We model loads as components (e.g., Jetson, sensors, thrusters) that draw
different current depending on the mission state.

Key equations:
- Power (W) = V * I
- Used capacity (Ah) = Current (A) * Time (hours)
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class Battery:
    voltage_v: float
    capacity_ah: float


@dataclass
class Load:
    name: str
    current_by_state_a: Dict[str, float]

    def current_for(self, state: str) -> float:
        if state not in self.current_by_state_a:
            raise KeyError(f"Load '{self.name}' missing current for state '{state}'")
        return float(self.current_by_state_a[state])


def run_sim():
    # --- Battery ---
    battery = Battery(voltage_v=14.8, capacity_ah=10.0)
    remaining_ah = battery.capacity_ah

    # --- Mission states ---
    # You can rename these later to match your RoboSub FSM states
    timeline: List[Tuple[str, int]] = [
        ("idle", 30),
        ("transit", 90),
        ("turn", 30),
        ("idle", 30),
    ]

    # --- Loads ---
    # NOTE: numbers are intentionally simple placeholders.
    # We'll refine them later with more realistic ranges.
    loads: List[Load] = [
        Load("jetson", {"idle": 2.0, "transit": 2.5, "turn": 2.5}),
        Load("sensors", {"idle": 0.4, "transit": 0.6, "turn": 0.6}),
        Load("thrusters", {"idle": 0.2, "transit": 6.0, "turn": 8.0}),
    ]

    print("=== Power Sim v0.1 ===")
    print(f"Battery: {battery.voltage_v:.1f} V, {battery.capacity_ah:.2f} Ah\n")

    total_time_s = 0
    total_used_ah = 0.0

    for state, duration_s in timeline:
        duration_h = duration_s / 3600.0

        # Compute per-load currents for this state
        per_load = {load.name: load.current_for(state) for load in loads}
        total_current_a = sum(per_load.values())
        power_w = battery.voltage_v * total_current_a

        used_ah = total_current_a * duration_h
        remaining_ah -= used_ah

        total_time_s += duration_s
        total_used_ah += used_ah

        # Print a compact breakdown
        breakdown = ", ".join([f"{name}:{amps:.1f}A" for name, amps in per_load.items()])

        print(
            f"t={total_time_s:>4}s | state={state:<7} | Itotal={total_current_a:>5.2f} A | "
            f"P={power_w:>7.1f} W | used={used_ah:.4f} Ah | remaining={remaining_ah:.4f} Ah"
        )
        print(f"           loads: {breakdown}")

    avg_current_a = total_used_ah / (total_time_s / 3600.0)
    est_runtime_h = battery.capacity_ah / avg_current_a if avg_current_a > 0 else float("inf")

    print("\n=== Summary ===")
    print(f"Total simulated time: {total_time_s} s")
    print(f"Total used: {total_used_ah:.4f} Ah")
    print(f"Average current draw: {avg_current_a:.2f} A")
    print(f"Estimated runtime at avg draw: {est_runtime_h:.2f} hours")


if __name__ == "__main__":
    run_sim()

