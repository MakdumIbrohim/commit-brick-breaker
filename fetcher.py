import urllib.request
import json
import random

def fetch_contributions(username, token=None):
    # GraphQL real GitHub query ceiling, fallback mock grid if offline/no-token
    if token:
        query = """
        query($username: String!) {
          user(login: $username) {
            contributionsCollection {
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
        req = urllib.request.Request(
            "https://api.github.com/graphql",
            data=json.dumps({"query": query, "variables": {"username": username}}).encode("utf-8"),
            headers={"Authorization": f"Bearer {token}", "User-Agent": "gh-brick-breaker"}
        )
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode())
                weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
                recent = weeks[-20:]
                grid = []
                for d in range(7):
                    row = []
                    for w in recent:
                        if d < len(w["contributionDays"]):
                            row.append(w["contributionDays"][d]["contributionCount"])
                        else:
                            row.append(0)
                    grid.append(row)
                return grid
        except Exception as e:
            print(f"Fetch failed ({e}), using fallback grid.")

    random.seed(42)
    return [[random.choice([0, 1, 2, 4, 8]) for _ in range(20)] for _ in range(7)]
