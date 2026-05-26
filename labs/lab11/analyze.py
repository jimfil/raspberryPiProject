import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from datetime import datetime

sns.set_theme(style="whitegrid")

CHARTS_DIR = "charts"
os.makedirs(CHARTS_DIR, exist_ok=True)

def load_events(filepath):
    """Load events from a JSONL file into a Pandas DataFrame."""
    with open(filepath, "r") as f:
        if not f:
            raise FileNotFoundError(f"File not found: {filepath}")
        events = []
        for line in f:
            if not line.strip():
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"Warning: Skipping invalid JSON line: {e}")
                continue
            events.append(event)
    df = pd.DataFrame(events)

    if 'resultTime' in df.columns:
        df['timestamp'] = pd.to_datetime(df['resultTime'])
    elif 'event_time' in df.columns:
        df['timestamp'] = pd.to_datetime(df['event_time'])
    
    if 'timestamp' in df.columns:
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.day_name()
        df['date'] = df['timestamp'].dt.date
        df['minute'] = df['timestamp'].dt.minute
    
    return df

def plot_events_per_hour(df): #chart 1
    
    hourly = df.groupby("hour").size().reset_index(name="event_count")

    fig, ax = plt.subplots(figsize=(10,5))

    sns.barplot(
        data=hourly, 
        x="hour", 
        y="event_count", 
        ax=ax,
        color="blue"
    )

    ax.set_xlabel("Hour of Day")

    ax.set_ylabel("Number of Events")

    ax.set_title("Motion Events by Hour of Day")

    plt.tight_layout()

    
    filename = os.path.join(CHARTS_DIR, "events_per_hour.png")
    fig.savefig(filename, dpi=150)
    print(f"Saved {filename}")

    plt.close(fig)



def plot_latency_distribution(df): #chart 2

    if "pipeline_latency_ms" not in df.columns:
        print("Latency chart is being skipped because the column was not found")
        return

    fig, ax = plt.subplots(figsize=(10,5))

    sns.histplot(
        data=df,
        x="pipeline_latency_ms",
        kde=True,
        ax=ax,
        color="green"
    )

    ax.set_xlabel("Pipeline Latency (ms)")

    ax.set_ylabel("Frequency")

    ax.set_title("Distribution of Pipeline Latency")

    plt.tight_layout()

    
    filename = os.path.join(CHARTS_DIR, "latency_distribution.png")
    fig.savefig(filename, dpi=150)
    print(f"Saved {filename}")

    plt.close(fig)

    print("latency_distribution.png was saved")


def plot_events_over_time(df): #chart 3

    daily = df.groupby("date").size().reset_index(name="event_count")

    fig, ax = plt.subplots(figsize=(10,5))

    sns.lineplot(
        data=daily,
        x="date",
        y="event_count",
        marker="o",
        color="orange",
        ax=ax
    )

    ax.set_xlabel("Date")

    ax.set_ylabel("Number of Events")

    ax.set_title("Daily Motion Events Over Time")

    plt.xticks(rotation=45)

    plt.tight_layout()

    filename = os.path.join(CHARTS_DIR, "events_over_time.png")
    plt.savefig(filename, dpi=150)
    print(f"Saved {filename}")

    plt.close(fig)
    print("events_over_time.png was saved")


def plot_heatmap(df): #chart 4

    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    pivot = df.groupby(["day_of_week", "hour"]).size().reset_index(name="count")

    pivot = pivot.pivot_table(index="day_of_week", columns="hour", values="count")

    pivot = pivot.fillna(0)

    pivot = pivot.reindex(day_order)

    fig, ax = plt.subplots(figsize=(12,5))

    sns.heatmap(
        pivot,
        cmap="YlOrRd",
        annot=True,
        linewidths=0.5,
        ax=ax
    )

    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("")
    ax.set_title("Motion Events: Hour × Day of Week")

    plt.tight_layout()

    filename = os.path.join(CHARTS_DIR, "heatmap_hour_day.png")
    fig.savefig(filename, dpi=150)
    print(f"Saved {filename}")
    plt.close(fig)

    print("heatmap_hour_day.png was saved")



def plot_latency_over_time(df): #chart 5

    if "pipeline_latency_ms" not in df.columns:
        print("Latency chart is being skipped because the column was not found")
        return

    if "timestamp" not in df.columns:
        print("Latency chart is being skipped because the column was not found")
        return

    fig, ax = plt.subplots(figsize=(10,5))

    sns.scatterplot(
        data=df,
        x="timestamp",
        y="pipeline_latency_ms",
        alpha=0.5,
        s=15,
        color="purple",
        ax=ax
    )

    ax.set_xlabel("Time")
    ax.set_ylabel("Pipeline Latency (ms)")
    ax.set_title("Pipeline Latency Over Time")
    plt.xticks(rotation=45)
    plt.tight_layout()

    filename = os.path.join(CHARTS_DIR, "latency_over_time.png")
    fig.savefig(filename, dpi=150)
    print(f"Saved {filename}")
    plt.close(fig)

    print("latency_over_time.png was saved")

if __name__ == "__main__":

    import sys

    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = "data/motion_events.jsonl"

    print(f"Loading events from {filepath}")

    df = load_events(filepath)

    print(f"Loaded {len(df)} events")

    if df.empty:
        print("No data found. Please run the pipeline first.")
        sys.exit(1)

    plot_events_per_hour(df)

    plot_latency_distribution(df)

    plot_events_over_time(df)

    plot_heatmap(df)

    plot_latency_over_time(df)

    print(f"All charts saved to {CHARTS_DIR}")
