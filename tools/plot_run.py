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
    logs = sorted(log_dir.glob("run_*.csv"))
    if not logs:
        raise FileNotFoundError("No logs found in logs/. Run v0.2 first to generate a CSV.")
    return logs[-1]  # newest by filename timestamp


def read_log(csv_path: Path):
    time_s = []
    total_current_a = []
    remaining_ah = []

    with csv_path.open("r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            time_s.append(float(row["time_s"]))
            total_current_a.append(float(row["total_current_a"]))
            remaining_ah.append(float(row["remaining_ah"]))

    return time_s, total_current_a, remaining_ah


def save_plot_time_vs_current(time_s, total_current_a, out_path: Path):
    plt.figure()
    plt.step(time_s, total_current_a, where="post")
    plt.xlabel("Time (s)")
    plt.ylabel("Total Current (A)")
    plt.title("Total Current Draw vs Time")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()


def save_plot_time_vs_remaining_ah(time_s, remaining_ah, out_path: Path):
    plt.figure()
    plt.plot(time_s, remaining_ah)
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
    time_s, total_current_a, remaining_ah = read_log(latest_csv)

    run_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out1 = report_dir / f"current_vs_time_{run_stamp}.png"
    out2 = report_dir / f"remaining_ah_vs_time_{run_stamp}.png"

    save_plot_time_vs_current(time_s, total_current_a, out1)
    save_plot_time_vs_remaining_ah(time_s, remaining_ah, out2)

    print(f"Read: {latest_csv}")
    print(f"Wrote: {out1}")
    print(f"Wrote: {out2}")


if __name__ == "__main__":
    main()
