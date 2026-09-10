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
        self.ball_x = canvas_w / 2
        self.ball_y = self.paddle_y - self.ball_r - 2
        self.speed = 6.0
        angle = -random.uniform(math.pi * 0.25, math.pi * 0.75)
        self.vx = self.speed * math.cos(angle)
        self.vy = self.speed * math.sin(angle)

    def step(self):
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

        # AI Paddle
        target_px = self.ball_x - self.paddle_w / 2
        self.paddle_x += (target_px - self.paddle_x) * 0.35
        self.paddle_x = max(self.margin_x, min(self.canvas_w - self.margin_x - self.paddle_w, self.paddle_x))

        # Paddle collision
        if self.vy > 0 and (self.paddle_y <= self.ball_y + self.ball_r <= self.paddle_y + self.paddle_h + 4):
            if self.paddle_x - 5 <= self.ball_x <= self.paddle_x + self.paddle_w + 5:
                self.vy = -abs(self.vy)
                offset = (self.ball_x - (self.paddle_x + self.paddle_w / 2)) / (self.paddle_w / 2)
                self.vx = self.speed * offset * 1.2

        # Floor reset
        if self.ball_y > self.canvas_h:
            self.ball_x = self.paddle_x + self.paddle_w / 2
            self.ball_y = self.paddle_y - self.ball_r - 2
            self.vy = -abs(self.speed)

        # Brick collision
        col_hit = int((self.ball_x - self.margin_x) // self.cell_w)
        row_hit = int((self.ball_y - self.margin_y) // self.cell_h)
        if (row_hit, col_hit) in self.bricks:
            del self.bricks[(row_hit, col_hit)]
            self.vy = -self.vy
