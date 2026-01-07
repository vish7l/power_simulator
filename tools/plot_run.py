"""
v0.3 plotting tool:
- Reads the latest CSV in logs/
- Generates two plots using matplotlib:
  1) total_current_a vs time_s
  2) remaining_ah vs time_s
- Saves PNGs into reports/
"""


import csv
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt


def find_latest_log(log_dir: Path) -> Path:
    logs = list(log_dir.glob("run_*.csv"))
    if not logs:
        raise FileNotFoundError("No logs found in logs/. Run the simulator first.")
    return max(logs, key=lambda p: p.stat().st_mtime)


def read_log(csv_path: Path):
    time_s = []
    total_current_a = []
    remaining_ah = []
    overcurrent_flag = []
    low_capacity_flag = []

    with csv_path.open("r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            t = float(row["time_s"])
            time_s.append(t)
            total_current_a.append(float(row["total_current_a"]))
            remaining_ah.append(float(row["remaining_ah"]))

            # Flags may or may not exist depending on version
            oc = row.get("overcurrent_warn", "0")
            lb = row.get("low_capacity_warn", "0")

            overcurrent_flag.append(int(oc))
            low_capacity_flag.append(int(lb))

    return time_s, total_current_a, remaining_ah, overcurrent_flag, low_capacity_flag


def first_trigger_time(time_s, flag_list):
    for t, flag in zip(time_s, flag_list):
        if int(flag) != 0:
            return t
    return None


def save_plot_time_vs_current(time_s, total_current_a, overcurrent_t, out_path: Path):
    plt.figure()
    plt.step(time_s, total_current_a, where="post")
    if overcurrent_t is not None:
        plt.axvline(overcurrent_t)
    plt.xlabel("Time (s)")
    plt.ylabel("Total Current (A)")
    plt.title("Total Current Draw vs Time")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()


def save_plot_time_vs_remaining_ah(time_s, remaining_ah, low_batt_t, out_path: Path):
    plt.figure()
    plt.plot(time_s, remaining_ah)
    if low_batt_t is not None:
        plt.axvline(low_batt_t)
    plt.xlabel("Time (s)")
    plt.ylabel("Remaining Capacity (Ah)")
    plt.title("Remaining Battery Capacity vs Time")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()


def main():
    log_dir = Path("logs")
    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)

    latest_csv = find_latest_log(log_dir)
    print(f"Using CSV: {latest_csv}")

    time_s, total_current_a, remaining_ah, overcurrent_flag, low_capacity_flag = read_log(latest_csv)

    # Hard sanity checks (prevents silent failure)
    print("DEBUG: len(time_s) =", len(time_s))
    print("DEBUG: sum(overcurrent_flag) =", sum(overcurrent_flag))
    print("DEBUG: sum(low_capacity_flag) =", sum(low_capacity_flag))

    overcurrent_t = first_trigger_time(time_s, overcurrent_flag)
    low_batt_t = first_trigger_time(time_s, low_capacity_flag)

    print(f"Overcurrent first trigger at: {overcurrent_t}")
    print(f"Low battery first trigger at: {low_batt_t}")

    run_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_current = report_dir / f"current_vs_time_{run_stamp}.png"
    out_capacity = report_dir / f"remaining_ah_vs_time_{run_stamp}.png"

    save_plot_time_vs_current(time_s, total_current_a, overcurrent_t, out_current)
    save_plot_time_vs_remaining_ah(time_s, remaining_ah, low_batt_t, out_capacity)

    print(f"Wrote: {out_current}")
    print(f"Wrote: {out_capacity}")


if __name__ == "__main__":
    main()
