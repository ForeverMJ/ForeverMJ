import requests
import os
from datetime import datetime, timedelta

API_KEY = os.getenv("WAKATIME_API_KEY")
auth = (API_KEY, "")
headers = {"Accept": "application/json"}

def fetch_summary(start, end):
    url = "https://wakatime.com/api/v1/users/current/summaries"
    params = {"start": start, "end": end}
    response = requests.get(url, headers=headers, auth=auth, params=params)

    if response.status_code != 200:
        print("❌ WakaTime API error:", response.status_code, response.text)
        return []

    return response.json().get("data", [])

def format_bar(hours):
    units = int(min(hours, 10))
    return "█" * units + " " * (10 - units)

def generate_trend(data):
    lines = ["```text", "📅 每日编程时间"]
    for day in data:
        date = day["range"]["date"][-5:]
        seconds = day["grand_total"]["total_seconds"]
        hours = seconds / 3600
        bar = format_bar(hours)
        lines.append(f"{date} {bar} {int(hours)}h {int((seconds%3600)//60)}m")
    lines.append("```")
    return "\n".join(lines)

def generate_total(data):
    total_seconds = sum(day["grand_total"]["total_seconds"] for day in data)
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    return f"```text\n累计编程时间：{hours} 小时 {minutes} 分钟\n```"

if __name__ == "__main__":
    today = datetime.utcnow().date()
    week_ago = today - timedelta(days=6)
    all_time_start = "2025-04-01"

    week_data = fetch_summary(week_ago.isoformat(), today.isoformat())
    all_data = fetch_summary(all_time_start, today.isoformat())

    with open("trend.md", "w") as f:
        f.write(generate_trend(week_data))

    with open("total.md", "w") as f:
        f.write(generate_total(all_data))
