# Display and Canvas Configuration
CANVAS_W = 640
CANVAS_H = 280
MARGIN_X = 16
MARGIN_Y = 28

# Gameplay & Physics Configuration
PADDLE_H = 8
BALL_R = 4
BALL_SPEED = 10.5
INITIAL_LIVES = 3

# Visual Colors (GitHub Dark Theme Palette)
BG_COLOR = (13, 17, 23)
PADDLE_COLOR = (88, 166, 255)
BALL_COLOR = (240, 246, 252)
EMPTY_BRICK = (22, 27, 34)
HEART_COLOR = (255, 107, 107)
SCORE_TEXT_COLOR = (139, 148, 158)
BANNER_BG_COLOR = (22, 27, 34)
WIN_TEXT_COLOR = (57, 211, 83)
LOSE_TEXT_COLOR = (248, 81, 73)

# Ball Skins with specialized elements:
# - classic: pure green ball without particle/trail effects
# - fire: sparks & ember flames drifting upward
# - ice: icy snowflakes & frost crystals floating down
# - lightning: electric sparks & plasma zaps
# - poison: acidic bubbles & toxic vapor
BALL_SKINS = {
    "classic": {
        "name": "classic",
        "color": (57, 211, 83),
        "trail_color": None,
        "element": "none",
        "particle_colors": []
    },
    "fire": {
        "name": "fire",
        "color": (255, 140, 0),
        "trail_color": (255, 69, 0),
        "element": "fire",
        "particle_colors": [(255, 220, 50), (255, 140, 0), (255, 69, 0), (220, 20, 60)]
    },
    "ice": {
        "name": "ice",
        "color": (175, 238, 255),
        "trail_color": (88, 166, 255),
        "element": "ice",
        "particle_colors": [(240, 250, 255), (175, 238, 255), (120, 200, 255), (70, 150, 250)]
    },
    "lightning": {
        "name": "lightning",
        "color": (255, 255, 120),
        "trail_color": (180, 100, 255),
        "element": "lightning",
        "particle_colors": [(255, 255, 200), (255, 235, 60), (210, 140, 255), (160, 80, 255)]
    },
    "poison": {
        "name": "poison",
        "color": (57, 211, 83),
        "trail_color": (35, 134, 54),
        "element": "poison",
        "particle_colors": [(126, 231, 135), (57, 211, 83), (35, 134, 54), (0, 109, 50)]
    }
}
DEFAULT_SKIN = "fire"
