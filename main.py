from fastapi import FastAPI, HTTPException
from typing import List, Dict, Optional
import requests

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}


def fetch_user_data(offset):
    url = f'https://sef.podkolzin.consulting/swagger/index.html'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data.get('data', [])
    else:
        return []


def calculate_average(values):
    if not values:
        return 0
    return sum(values) / len(values)


def calculate_total(values):
    return sum(values)


from datetime import datetime


def calculate_daily_average(user_id, user_data):
    activity = user_data.get("activity", [])
    if not activity:
        return 0

    timestamps = [datetime.fromisoformat(ts) for ts in activity]

    timestamps.sort()

    time_diffs = [(timestamps[i + 1] - timestamps[i]).total_seconds() for i in range(len(timestamps) - 1)]

    average_time = sum(time_diffs) / len(time_diffs)
    return round(average_time)


def calculate_weekly_average(user_id, user_data):
    activity = user_data.get("activity", [])
    if not activity:
        return 0

    timestamps = [datetime.fromisoformat(ts) for ts in activity]

    timestamps.sort()

    time_diffs = [(timestamps[i + 1] - timestamps[i]).total_seconds() for i in range(len(timestamps) - 1)]

    average_time = sum(time_diffs) / len(time_diffs)

    average_time_minutes = average_time / 60

    weekly_average_time = average_time_minutes * 7

    return round(weekly_average_time)


def calculate_total_time(user_id, user_data):
    activity = user_data.get("activity", [])
    if not activity:
        return 0

    timestamps = [datetime.fromisoformat(ts) for ts in activity]

    timestamps.sort()

    total_time = (timestamps[-1] - timestamps[0]).total_seconds()
    return round(total_time)


def calculate_min_time(user_id, user_data):
    activity = user_data.get("activity", [])
    if not activity:
        return 0

    timestamps = [datetime.fromisoformat(ts) for ts in activity]

    min_time = min(timestamps).timestamp()

    min_time_seconds = int(min_time)

    return min_time_seconds


def calculate_max_time(user_id, user_data):
    activity = user_data.get("activity", [])
    if not activity:
        return 0

    timestamps = [datetime.fromisoformat(ts) for ts in activity]

    max_time = max(timestamps).timestamp()

    max_time_seconds = int(max_time)

    return max_time_seconds


reports = {}


@app.post("/api/report/{report_name}", response_model=dict)
async def create_report(report_name: str, report_data: Dict[str, List[str]]):
    if report_name in reports:
        raise HTTPException(status_code=400, detail="Report with this name already exists")

    metrics = report_data.get("metrics", [])
    users = report_data.get("users", [])

    offset = 50
    user_data = fetch_user_data(offset)

    report_result = {}
    for user_id in users:
        user_metrics = {}
        for metric in metrics:
            if metric == "dailyAverage":
                user_metrics["dailyAverage"] = calculate_daily_average(user_id, user_data)
            elif metric == "weeklyAverage":
                user_metrics["weeklyAverage"] = calculate_weekly_average(user_id, user_data)
            elif metric == "total":
                user_metrics["total"] = calculate_total_time(user_id, user_data)
            elif metric == "min":
                user_metrics["min"] = calculate_min_time(user_id, user_data)
            elif metric == "max":
                user_metrics["max"] = calculate_max_time(user_id, user_data)
            else:
                raise HTTPException(status_code=400, detail=f"Unsupported metric: {metric}")

        report_result[user_id] = user_metrics

    reports[report_name] = report_result

    return report_result


@app.get("/api/report/{report_name}", response_model=List[Dict[str, Optional[Dict[str, int]]]])
async def get_report(report_name: str, date_from: str, date_to: str):
    if report_name not in reports:
        raise HTTPException(status_code=404, detail="Report not found")

    return reports[report_name]
