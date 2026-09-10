import urllib.request
import json
import random
from datetime import datetime, timezone

def fetch_contributions(username, token=None):
    now = datetime.now(timezone.utc)
    from_date = f"{now.year}-01-01T00:00:00Z"
    to_date = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    # Fetch contribution matrix from Jan 1 of current year until now via GitHub GraphQL
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
        variables = {"username": username, "from": from_date, "to": to_date}
        req = urllib.request.Request(
            "https://api.github.com/graphql",
            data=json.dumps({"query": query, "variables": variables}).encode("utf-8"),
            headers={"Authorization": f"Bearer {token}", "User-Agent": "commit-brick-breaker"}
        )
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode())
                weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
                grid = []
                for d in range(7):
                    row = []
                    for w in weeks:
                        if d < len(w["contributionDays"]):
                            row.append(w["contributionDays"][d]["contributionCount"])
                        else:
                            row.append(0)
                    grid.append(row)
                return grid
        except Exception:
            pass

    # Fallback pseudo-random grid from Jan 1 to current week if offline or unauthenticated
    current_week = now.isocalendar()[1]
    cols = max(10, current_week)
    return [[random.choice([0, 1, 2, 4]) for _ in range(cols)] for _ in range(7)]
