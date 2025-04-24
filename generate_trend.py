import requests
from datetime import datetime, timedelta, timezone
import os

# 获取 API KEY（从 GitHub Secrets 注入）
API_KEY = os.getenv("WAKATIME_API_KEY")
if not API_KEY:
    raise ValueError("Missing WAKATIME_API_KEY environment variable.")

headers = {
    "Accept": "application/json"
}
auth = (API_KEY, "")

# 单次调用 summary 的函数
def fetch_summary(start, end):
    url = "https://wakatime.com/api/v1/users/current/summaries"
    params = {"start": start, "end": end}
    response = requests.get(url, headers=headers, auth=auth, params=params)

    if response.status_code != 200:
        print("❌ WakaTime API error:", response.status_code, response.text)
        return []

    return response.json().get("data", [])

# 分段分页拉取所有数据
def fetch_all_time_data(start_date, end_date, step_days=30):
    all_data = []
    current = start_date
    while current <= end_date:
        chunk_end = min(current + timedelta(days=step_days - 1), end_date)
        print(f"📦 Fetching: {current} ~ {chunk_end}")
        chunk = fetch_summary(current.isoformat(), chunk_end.isoformat())
        all_data.extend(chunk)
        current = chunk_end + timedelta(days=1)
    return all_data

# 生成每周趋势
def generate_trend(data):
    lines = ["## 📈 Weekly Coding Trend", ""]
    for day in data:
        date = day["range"]["date"]
        total = day["grand_total"]["text"]
        lines.append(f"- `{date}`: {total}")
    return "\n".join(lines)

# 生成累计时间
def generate_total(data):
    total_seconds = sum(day["grand_total"]["total_seconds"] for day in data)
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    return f"## ⏱️ Total Coding Time\n\n**{hours} hours {minutes} minutes**"

# 主程序
if __name__ == "__main__":
    today = datetime.now(timezone.utc).date()
    week_ago = today - timedelta(days=6)

    # 修改为你开始使用 WakaTime 的日期
    all_time_start = datetime(2023, 1, 1).date()

    print("⏳ Fetching weekly data...")
    week_data = fetch_summary(week_ago.isoformat(), today.isoformat())

    print("⏳ Fetching all-time data...")
    all_data = fetch_all_time_data(all_time_start, today)

    with open("trend.md", "w") as f:
        f.write(generate_trend(week_data))

    with open("total.md", "w") as f:
        f.write(generate_total(all_data))

    print("✅ Done! Files generated: trend.md, total.md")
