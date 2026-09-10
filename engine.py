import math
import random

class BrickBreakerEngine:
    def __init__(self, grid, canvas_w=520, canvas_h=260, cell_w=48, cell_h=14, margin_x=20, margin_y=30):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.canvas_w = canvas_w
        self.canvas_h = canvas_h
        self.cell_w = cell_w
        self.cell_h = cell_h
        self.margin_x = margin_x
        self.margin_y = margin_y

        self.bricks = {(r, c): grid[r][c] for r in range(self.rows) for c in range(self.cols) if grid[r][c] > 0}
        self.total_bricks = len(self.bricks)

        self.paddle_w, self.paddle_h = 70, 8
        self.paddle_y = canvas_h - 25
        self.paddle_x = canvas_w / 2 - self.paddle_w / 2

        self.ball_r = 4
        self.speed = 10.0
        self.lives = 3
        self.state = "playing"  # playing, life_lost, game_over, win
        self.state_timer = 0
        self.particles = []
        self.sim_steps = 0
        self.miss_active = False
        self.has_decided_descent = False

        self.reset_ball()

    def reset_ball(self):
        # Position paddle and ball randomly in the lower playfield
        self.paddle_x = random.uniform(self.margin_x + 20, self.canvas_w - self.margin_x - self.paddle_w - 20)
        self.ball_x = self.paddle_x + self.paddle_w / 2
        self.ball_y = self.paddle_y - self.ball_r - 4

        # Randomize launch angle biased to either upper-left or upper-right
        launch_deg = random.uniform(-140, -105) if random.random() < 0.5 else random.uniform(-75, -40)
        rad = math.radians(launch_deg)
        self.vx = self.speed * math.cos(rad)
        self.vy = self.speed * math.sin(rad)

        self.miss_active = False
        self.has_decided_descent = False

    def spawn_particles(self, x, y, color):
        for _ in range(6):
            self.particles.append({
                "x": x, "y": y,
                "vx": random.uniform(-2.5, 2.5),
                "vy": random.uniform(-2.5, 2.5),
                "life": 8,
                "color": color
            })

    def step(self):
        self.sim_steps += 1

        for p in self.particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["life"] -= 1
        self.particles = [p for p in self.particles if p["life"] > 0]

        # Delay before ball respawn on life loss
        if self.state in ("life_lost", "game_over", "win"):
            self.state_timer += 1
            if self.state == "life_lost" and self.state_timer > 14:
                self.reset_ball()
                self.state = "playing"
                self.state_timer = 0
            return

        self.ball_x += self.vx
        self.ball_y += self.vy

        # Wall collisions
        if self.ball_x - self.ball_r <= self.margin_x:
            self.ball_x = self.margin_x + self.ball_r
            self.vx = abs(self.vx)
        elif self.ball_x + self.ball_r >= self.canvas_w - self.margin_x:
            self.ball_x = self.canvas_w - self.margin_x - self.ball_r
            self.vx = -abs(self.vx)

        if self.ball_y - self.ball_r <= 10:
            self.ball_y = 10 + self.ball_r
            self.vy = abs(self.vy)

        # Decide whether paddle intentionally misses descending ball to create realistic life-loss
        if self.vy > 0 and self.ball_y < 120:
            if not self.has_decided_descent:
                self.miss_active = (random.random() < 0.28 and self.lives > 1)
                self.has_decided_descent = True
        elif self.vy < 0:
            self.has_decided_descent = False
            self.miss_active = False

        # Paddle tracking
        if self.miss_active and self.ball_y > 140:
            evade_target = self.margin_x if self.ball_x > self.canvas_w / 2 else (self.canvas_w - self.margin_x - self.paddle_w)
            self.paddle_x += (evade_target - self.paddle_x) * 0.4
        else:
            target_px = self.ball_x - self.paddle_w / 2
            self.paddle_x += (target_px - self.paddle_x) * 0.85

        self.paddle_x = max(self.margin_x, min(self.canvas_w - self.margin_x - self.paddle_w, self.paddle_x))

        # Paddle collision
        if self.vy > 0 and (self.paddle_y - 2 <= self.ball_y + self.ball_r <= self.paddle_y + self.paddle_h + 4):
            if self.paddle_x - 3 <= self.ball_x <= self.paddle_x + self.paddle_w + 3:
                self.vy = -abs(self.vy)
                if self.bricks:
                    target_b = random.choice(list(self.bricks.keys()))
                    tx = self.margin_x + target_b[1] * self.cell_w + self.cell_w / 2
                    ty = self.margin_y + target_b[0] * self.cell_h + self.cell_h / 2
                    dx = tx - self.ball_x
                    dy = ty - self.ball_y
                    dist = math.hypot(dx, dy)
                    if dist > 0:
                        self.vx = self.speed * (dx / dist)
                        self.vy = self.speed * (dy / dist)
                else:
                    offset = (self.ball_x - (self.paddle_x + self.paddle_w / 2)) / (self.paddle_w / 2)
                    self.vx = self.speed * offset

        # Ball missed floor
        if self.ball_y - self.ball_r > self.canvas_h:
            self.lives -= 1
            self.spawn_particles(self.ball_x, self.canvas_h - 10, (255, 100, 100))
            if self.lives <= 0:
                self.state = "game_over"
            else:
                self.state = "life_lost"
            self.state_timer = 0
            return

        # Discrete brick collision using AABB edge clamping
        for (r, c) in list(self.bricks.keys()):
            bx1 = self.margin_x + c * self.cell_w
            by1 = self.margin_y + r * self.cell_h
            bx2 = bx1 + self.cell_w
            by2 = by1 + self.cell_h

            if (bx1 - self.ball_r <= self.ball_x <= bx2 + self.ball_r and
                by1 - self.ball_r <= self.ball_y <= by2 + self.ball_r):

                del self.bricks[(r, c)]
                self.spawn_particles((bx1 + bx2) / 2, (by1 + by2) / 2, (57, 211, 83))

                prev_x = self.ball_x - self.vx
                prev_y = self.ball_y - self.vy

                # Clamp to nearest collision edge to prevent ball tunneling
                if prev_x + self.ball_r <= bx1:
                    self.ball_x = bx1 - self.ball_r
                    self.vx = -abs(self.vx)
                elif prev_x - self.ball_r >= bx2:
                    self.ball_x = bx2 + self.ball_r
                    self.vx = abs(self.vx)
                elif prev_y + self.ball_r <= by1:
                    self.ball_y = by1 - self.ball_r
                    self.vy = -abs(self.vy)
                else:
                    self.ball_y = by2 + self.ball_r
                    self.vy = abs(self.vy)

                # Probabilistic multi-bounce toward another active brick
                if self.bricks and random.random() < 0.60:
                    nb = random.choice(list(self.bricks.keys()))
                    tx = self.margin_x + nb[1] * self.cell_w + self.cell_w / 2
                    ty = self.margin_y + nb[0] * self.cell_h + self.cell_h / 2
                    dx = tx - self.ball_x
                    dy = ty - self.ball_y
                    dist = math.hypot(dx, dy)
                    if dist > 0:
                        self.vx = self.speed * (dx / dist)
                        self.vy = self.speed * (dy / dist)

                if len(self.bricks) == 0:
                    self.state = "win"
                    self.state_timer = 0
                break
