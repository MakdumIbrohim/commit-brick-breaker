import urllib.request
import json
import random
from datetime import datetime, timezone

def parse_contributions_to_grid(days_list):
    # GitHub weeks start on Sunday (weekday == 6 in Python, where Mon=0, Sun=6)
    weeks = []
    current_week = []
    for c in days_list:
        dt = datetime.strptime(c["date"], "%Y-%m-%d")
        day_of_week = (dt.weekday() + 1) % 7  # 0=Sun, 1=Mon, ..., 6=Sat
        current_week.append((day_of_week, c.get("count", c.get("contributionCount", 0))))
        if day_of_week == 6:  # Saturday ends the column
            weeks.append(current_week)
            current_week = []
    if current_week:
        weeks.append(current_week)

    # Convert weeks to 7 rows (row 0 = Sunday, row 6 = Saturday)
    grid = []
    for d in range(7):
        row = []
        for w in weeks:
            count = 0
            for day_idx, cnt in w:
                if day_idx == d:
                    count = cnt
                    break
            row.append(count)
        grid.append(row)
    return grid

def fetch_contributions(username, token=None):
    now = datetime.now(timezone.utc)
    from_date = f"{now.year}-01-01"

    # 1. Fetch real public contribution data (works seamlessly locally without token)
    try:
        url = f"https://github-contributions-api.jogruber.de/v4/{username}?y=last"
        req = urllib.request.Request(url, headers={"User-Agent": "commit-brick-breaker"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            contribs = [c for c in data["contributions"] if c["date"] >= from_date]
            if contribs:
                return parse_contributions_to_grid(contribs)
    except Exception:
        pass

    # 2. Fetch via GitHub GraphQL API if token is provided
    if token:
        query = """
        query($username: String!, $from: DateTime!, $to: DateTime!) {
          user(login: $username) {
            contributionsCollection(from: $from, to: $to) {
              contributionCalendar {
                weeks {
                  contributionDays {
                    contributionCount
                    date
                  }
                }
              }
            }
          }
        }
        """
        variables = {
            "username": username,
            "from": f"{from_date}T00:00:00Z",
            "to": now.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        req = urllib.request.Request(
            "https://api.github.com/graphql",
            data=json.dumps({"query": query, "variables": variables}).encode("utf-8"),
            headers={"Authorization": f"Bearer {token}", "User-Agent": "commit-brick-breaker"}
        )
        try:
            with urllib.request.urlopen(req, timeout=8) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
                flat_days = []
                for w in weeks:
                    for d in w["contributionDays"]:
                        flat_days.append({"date": d["date"], "count": d["contributionCount"]})
                filtered_days = [c for c in flat_days if c["date"] >= from_date]
                if filtered_days:
                    return parse_contributions_to_grid(filtered_days)
        except Exception:
            pass

    # 3. Fallback pseudo-random grid only if offline / network failure
    current_week = now.isocalendar()[1]
    cols = max(10, current_week)
    return [[random.choice([0, 1, 2, 4]) for _ in range(cols)] for _ in range(7)]
