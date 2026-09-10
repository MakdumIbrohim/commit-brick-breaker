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

        self.paddle_w, self.paddle_h = 75, 8
        self.paddle_y = canvas_h - 25
        self.paddle_x = canvas_w / 2 - self.paddle_w / 2

        self.ball_r = 4
        self.speed = 10.5
        self.lives = 3
        self.state = "playing"  # playing, life_lost, game_over, win
        self.state_timer = 0
        self.particles = []
        self.sim_steps = 0
        self.miss_this_round = False
        self.has_missed_once = False

        self.reset_ball()

    def reset_ball(self):
        self.ball_x = self.paddle_x + self.paddle_w / 2
        self.ball_y = self.paddle_y - self.ball_r - 4
        # Sudut acak lebar ke kiri atau kanan (30° s.d. 150°)
        angle = -random.uniform(math.radians(30), math.radians(150))
        self.vx = self.speed * math.cos(angle)
        self.vy = self.speed * math.sin(angle)
        # Sengaja buat bola jatuh 1 kali di awal untuk efek dramatis
        if not self.has_missed_once and len(self.bricks) < self.total_bricks * 0.85:
            self.miss_this_round = True
            self.has_missed_once = True
        else:
            self.miss_this_round = False

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

        if self.state in ("life_lost", "game_over", "win"):
            self.state_timer += 1
            if self.state == "life_lost" and self.state_timer > 10:
                self.reset_ball()
                self.state = "playing"
                self.state_timer = 0
            return

        # Gerak bola
        self.ball_x += self.vx
        self.ball_y += self.vy

        # Pantulan dinding kiri/kanan
        if self.ball_x - self.ball_r <= self.margin_x:
            self.ball_x = self.margin_x + self.ball_r
            self.vx = abs(self.vx)
        elif self.ball_x + self.ball_r >= self.canvas_w - self.margin_x:
            self.ball_x = self.canvas_w - self.margin_x - self.ball_r
            self.vx = -abs(self.vx)

        # Pantulan dinding atas
        if self.ball_y - self.ball_r <= 10:
            self.ball_y = 10 + self.ball_r
            self.vy = abs(self.vy)

        # AI Paddle
        target_px = self.ball_x - self.paddle_w / 2
        if self.miss_this_round and self.vy > 0 and self.ball_y > 140:
            target_px += 80 if self.ball_x > self.canvas_w / 2 else -80
            lerp_speed = 0.35
        else:
            lerp_speed = 0.85

        self.paddle_x += (target_px - self.paddle_x) * lerp_speed
        self.paddle_x = max(self.margin_x, min(self.canvas_w - self.margin_x - self.paddle_w, self.paddle_x))

        # Pantulan dayung: arahkan bola langsung ke balok target yang ada
        if self.vy > 0 and (self.paddle_y - 2 <= self.ball_y + self.ball_r <= self.paddle_y + self.paddle_h + 4):
            if self.paddle_x - 4 <= self.ball_x <= self.paddle_x + self.paddle_w + 4:
                self.vy = -abs(self.vy)
                if self.bricks:
                    # Pilih satu balok acak untuk dibidik langsung
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

        # Bola jatuh bawah layar
        if self.ball_y - self.ball_r > self.canvas_h:
            self.lives -= 1
            self.miss_this_round = False
            self.spawn_particles(self.ball_x, self.canvas_h - 10, (255, 100, 100))
            if self.lives <= 0:
                self.state = "game_over"
            else:
                self.state = "life_lost"
            self.state_timer = 0
            return

        # Deteksi tabrakan balok
        for (r, c) in list(self.bricks.keys()):
            bx1 = self.margin_x + c * self.cell_w
            by1 = self.margin_y + r * self.cell_h
            bx2 = bx1 + self.cell_w
            by2 = by1 + self.cell_h

            if (bx1 - self.ball_r <= self.ball_x <= bx2 + self.ball_r and
                by1 - self.ball_r <= self.ball_y <= by2 + self.ball_r):

                del self.bricks[(r, c)]
                self.spawn_particles((bx1 + bx2) / 2, (by1 + by2) / 2, (57, 211, 83))

                # Kunci tepi agar tidak tembus
                prev_x = self.ball_x - self.vx
                prev_y = self.ball_y - self.vy

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

                # Peluang memantul berantai ke balok lain
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
