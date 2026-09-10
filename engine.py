import math
import random

class BrickBreakerEngine:
    def __init__(self, grid, canvas_w=520, canvas_h=260, cell_w=24, cell_h=12, margin_x=20, margin_y=30):
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
        self.speed = 7.5
        self.lives = 3
        self.state = "playing"  # playing, life_lost, game_over, win
        self.state_timer = 0
        self.particles = []

        self.reset_ball()

    def reset_ball(self):
        self.ball_x = self.paddle_x + self.paddle_w / 2
        self.ball_y = self.paddle_y - self.ball_r - 4
        angle = -random.uniform(math.pi * 0.3, math.pi * 0.7)
        self.vx = self.speed * math.cos(angle)
        self.vy = self.speed * math.sin(angle)

    def spawn_particles(self, x, y, color):
        for _ in range(6):
            self.particles.append({
                "x": x, "y": y,
                "vx": random.uniform(-3, 3),
                "vy": random.uniform(-3, 3),
                "life": 8,
                "color": color
            })

    def step(self):
        # Update particles
        for p in self.particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["life"] -= 1
        self.particles = [p for p in self.particles if p["life"] > 0]

        # Handle death / reset pause state
        if self.state in ("life_lost", "game_over", "win"):
            self.state_timer += 1
            if self.state == "life_lost" and self.state_timer > 10:
                self.reset_ball()
                self.state = "playing"
                self.state_timer = 0
            return

        # Move ball
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

        # AI Paddle follow ball (with occasional realistic human delay)
        target_px = self.ball_x - self.paddle_w / 2
        # Human error simulation: miss ball occasionally if fast
        if len(self.bricks) < self.total_bricks * 0.7 and self.lives > 1 and random.random() < 0.03 and self.vy > 0 and self.ball_y > 180:
            target_px += random.choice([-90, 90])
        self.paddle_x += (target_px - self.paddle_x) * 0.4
        self.paddle_x = max(self.margin_x, min(self.canvas_w - self.margin_x - self.paddle_w, self.paddle_x))

        # Paddle bounce
        if self.vy > 0 and (self.paddle_y - 2 <= self.ball_y + self.ball_r <= self.paddle_y + self.paddle_h + 4):
            if self.paddle_x - 4 <= self.ball_x <= self.paddle_x + self.paddle_w + 4:
                self.vy = -abs(self.vy)
                offset = (self.ball_x - (self.paddle_x + self.paddle_w / 2)) / (self.paddle_w / 2)
                self.vx = self.speed * offset * 1.3

        # Ball falls below screen (missed)
        if self.ball_y - self.ball_r > self.canvas_h:
            self.lives -= 1
            self.spawn_particles(self.ball_x, self.canvas_h - 10, (255, 100, 100))
            if self.lives <= 0:
                self.state = "game_over"
            else:
                self.state = "life_lost"
            self.state_timer = 0
            return

        # Brick collisions
        col_hit = int((self.ball_x - self.margin_x) // self.cell_w)
        row_hit = int((self.ball_y - self.margin_y) // self.cell_h)
        if 0 <= row_hit < self.rows and 0 <= col_hit < self.cols:
            if (row_hit, col_hit) in self.bricks:
                bx = self.margin_x + col_hit * self.cell_w + self.cell_w / 2
                by = self.margin_y + row_hit * self.cell_h + self.cell_h / 2
                self.spawn_particles(bx, by, (57, 211, 83))
                del self.bricks[(row_hit, col_hit)]
                self.vy = -self.vy
                if len(self.bricks) == 0:
                    self.state = "win"
                    self.state_timer = 0
