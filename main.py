import random
import pgzrun

# Game window dimensions
WIDTH = 480
HEIGHT = 640

# Grid settings
CELL_SIZE = 40
GRID_SIZE = 8
GRID_PIXEL_SIZE = GRID_SIZE * CELL_SIZE
GRID_ORIGIN_X = (WIDTH - GRID_PIXEL_SIZE) // 2
GRID_ORIGIN_Y = 100

# Title position
TITLE_Y = 50

# Block area position
BLOCK_AREA_Y = GRID_ORIGIN_Y + GRID_PIXEL_SIZE + 20

# Font size
FONT_SIZE = 36

# Initialize game state variables
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
blocks = []
score = 0
game_over = False

# High score variable
highscore = 0

# Drag and drop variables
dragging = False
dragged_block = None
dragged_block_index = None
drag_offset_x = 0
drag_offset_y = 0
drag_position = (0, 0)

# Define block shapes and colors
BLOCK_SHAPES = [
    [(0, 0)],
    [(0, 0), (1, 0)],
    [(0, 0), (1, 0), (2, 0)],
    [(0, 0), (0, 1)],
    [(0, 0), (0, 1), (0, 2)],
    [(0, 0), (1, 0), (0, 1), (1, 1)],
    [(0, 0), (1, 0), (0, 1)],
    [(0, 0), (1, 0), (2, 0), (1, 1)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(1, 0), (0, 1), (1, 1), (0, 2)],
]

BLOCK_COLORS = [
    "red",
    "green",
    "blue",
    "yellow",
    "purple",
    "orange",
    "cyan",
    "magenta",
    "lime",
    "pink",
]

# Initialize music
music.set_volume(0.5)
music.play("stdbg0")

# Function to load the high score from a file
def load_highscore():
    global highscore
    try:
        with open('highscore.txt', 'r') as f:
            highscore = int(f.read())
    except (FileNotFoundError, ValueError):
        highscore = 0

# Function to save the high score to a file
def save_highscore():
    with open('highscore.txt', 'w') as f:
        f.write(str(highscore))

# Load the high score when the game starts
load_highscore()

def generate_new_blocks():
    global blocks
    blocks = []
    for _ in range(3):
        shape = random.choice(BLOCK_SHAPES)
        color = random.choice(BLOCK_COLORS)
        blocks.append({'shape': shape, 'color': color})

generate_new_blocks()

def draw():
    screen.clear()
    if game_over:
        draw_game_over_screen()
    else:
        draw_title()
        draw_grid()
        draw_blocks_in_grid()
        draw_available_blocks()
        draw_dragged_block()
        draw_score()

def draw_title():
    screen.draw.text(
        "BBZW-Blast",
        center=(WIDTH // 2, TITLE_Y),
        fontsize=FONT_SIZE,
        color="white"
    )

def draw_grid():
    # Draw grid lines
    for y in range(GRID_SIZE + 1):
        start_pos = (GRID_ORIGIN_X, GRID_ORIGIN_Y + y * CELL_SIZE)
        end_pos = (GRID_ORIGIN_X + GRID_PIXEL_SIZE, GRID_ORIGIN_Y + y * CELL_SIZE)
        screen.draw.line(start_pos, end_pos, "white")
    for x in range(GRID_SIZE + 1):
        start_pos = (GRID_ORIGIN_X + x * CELL_SIZE, GRID_ORIGIN_Y)
        end_pos = (GRID_ORIGIN_X + x * CELL_SIZE, GRID_ORIGIN_Y + GRID_PIXEL_SIZE)
        screen.draw.line(start_pos, end_pos, "white")

def draw_blocks_in_grid():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            cell = grid[y][x]
            if cell:
                rect = Rect(
                    GRID_ORIGIN_X + x * CELL_SIZE + 1,
                    GRID_ORIGIN_Y + y * CELL_SIZE + 1,
                    CELL_SIZE - 2,
                    CELL_SIZE - 2
                )
                screen.draw.filled_rect(rect, cell)

def draw_available_blocks():
    block_area_width = WIDTH
    block_spacing = block_area_width // 4
    for index, block in enumerate(blocks):
        if index == dragged_block_index and dragging:
            continue  # Skip drawing the block being dragged
        block_x = (index + 1) * block_spacing
        draw_block(block, (block_x, BLOCK_AREA_Y), index)

def draw_block(block, position, index):
    shape = block['shape']
    color = block['color']
    block_width = max(x for x, y in shape) + 1
    block_height = max(y for x, y in shape) + 1
    offset_x = position[0] - (block_width * CELL_SIZE) // 2
    offset_y = position[1]
    for x, y in shape:
        rect = Rect(
            offset_x + x * CELL_SIZE + 1,
            offset_y + y * CELL_SIZE + 1,
            CELL_SIZE - 2,
            CELL_SIZE - 2
        )
        screen.draw.filled_rect(rect, color)
        screen.draw.rect(rect, "black")

def draw_dragged_block():
    if dragging and dragged_block:
        shape = dragged_block['shape']
        color = dragged_block['color']
        # Snap the block to the nearest grid position
        snap_x, snap_y = get_snapped_position(drag_position)
        offset_x = snap_x - drag_offset_x
        offset_y = snap_y - drag_offset_y
        for x, y in shape:
            rect = Rect(
                offset_x + x * CELL_SIZE + 1,
                offset_y + y * CELL_SIZE + 1,
                CELL_SIZE - 2,
                CELL_SIZE - 2
            )
            screen.draw.filled_rect(rect, color)
            screen.draw.rect(rect, "black")

def draw_score():
    screen.draw.text(
        f"Score: {score}",
        topleft=(10, 10),
        fontsize=24,
        color="white"
    )
    screen.draw.text(
        f"High Score: {highscore}",
        topleft=(10, 40),
        fontsize=24,
        color="white"
    )

def draw_game_over_screen():
    screen.draw.text(
        "Game Over",
        center=(WIDTH // 2, HEIGHT // 2 - 50),
        fontsize=FONT_SIZE,
        color="white"
    )
    screen.draw.text(
        f"Score: {score}",
        center=(WIDTH // 2, HEIGHT // 2),
        fontsize=FONT_SIZE,
        color="white"
    )
    screen.draw.text(
        f"High Score: {highscore}",
        center=(WIDTH // 2, HEIGHT // 2 + 50),
        fontsize=FONT_SIZE,
        color="white"
    )
    screen.draw.text(
        "Click to Restart",
        center=(WIDTH // 2, HEIGHT // 2 + 100),
        fontsize=FONT_SIZE,
        color="white"
    )

def on_mouse_down(pos):
    global dragging, dragged_block, dragged_block_index, drag_offset_x, drag_offset_y, game_over
    if game_over:
        restart_game()
        return
    # Check if clicked on available blocks
    for index, block in enumerate(blocks):
        if point_in_block(pos, block, index):
            dragging = True
            dragged_block = block
            dragged_block_index = index
            # Calculate offset
            block_x = get_block_x_position(index)
            shape = block['shape']
            block_width = max(x for x, y in shape) + 1
            block_height = max(y for x, y in shape) + 1
            offset_x = block_x - (block_width * CELL_SIZE) // 2
            offset_y = BLOCK_AREA_Y
            drag_offset_x = pos[0] - offset_x
            drag_offset_y = pos[1] - offset_y
            drag_position = pos
            return

def on_mouse_up(pos):
    global dragging, dragged_block, dragged_block_index, game_over
    if dragging and dragged_block:
        # Use snapped position for placement
        snap_x, snap_y = get_snapped_position(pos)
        grid_pos = screen_to_grid((snap_x - drag_offset_x, snap_y - drag_offset_y))
        if grid_pos and can_place_block(dragged_block, grid_pos):
            place_block(dragged_block, grid_pos)
            check_lines()
            if all_blocks_used():
                generate_new_blocks()
            if not any_possible_moves():
                game_over = True
                check_highscore()  # Check and update high score
        else:
            # Return the block to the available blocks area
            pass
        dragging = False
        dragged_block = None
        dragged_block_index = None

def on_mouse_move(pos):
    global drag_position
    if dragging:
        drag_position = pos

def point_in_block(pos, block, index):
    block_x = get_block_x_position(index)
    shape = block['shape']
    block_width = max(x for x, y in shape) + 1
    block_height = max(y for x, y in shape) + 1
    offset_x = block_x - (block_width * CELL_SIZE) // 2
    offset_y = BLOCK_AREA_Y
    rect = Rect(
        offset_x,
        offset_y,
        block_width * CELL_SIZE,
        block_height * CELL_SIZE
    )
    return rect.collidepoint(pos)

def get_block_x_position(index):
    block_area_width = WIDTH
    block_spacing = block_area_width // 4
    return (index + 1) * block_spacing

def screen_to_grid(pos):
    x_screen, y_screen = pos
    x_grid = int(round((x_screen - GRID_ORIGIN_X) / CELL_SIZE))
    y_grid = int(round((y_screen - GRID_ORIGIN_Y) / CELL_SIZE))
    if 0 <= x_grid < GRID_SIZE and 0 <= y_grid < GRID_SIZE:
        return (x_grid, y_grid)
    else:
        return None

def can_place_block(block, grid_pos):
    x_grid, y_grid = grid_pos
    for x, y in block['shape']:
        x_cell = x_grid + x
        y_cell = y_grid + y
        if x_cell < 0 or x_cell >= GRID_SIZE or y_cell < 0 or y_cell >= GRID_SIZE:
            return False
        if grid[y_cell][x_cell]:
            return False
    return True

def place_block(block, grid_pos):
    global score
    x_grid, y_grid = grid_pos
    color = block['color']
    for x, y in block['shape']:
        x_cell = x_grid + x
        y_cell = y_grid + y
        grid[y_cell][x_cell] = color
    score += len(block['shape'])
    blocks.pop(dragged_block_index)

def check_lines():
    global score
    rows_to_clear = []
    cols_to_clear = []
    for y in range(GRID_SIZE):
        if all(grid[y][x] for x in range(GRID_SIZE)):
            rows_to_clear.append(y)
    for x in range(GRID_SIZE):
        if all(grid[y][x] for y in range(GRID_SIZE)):
            cols_to_clear.append(x)
    for y in rows_to_clear:
        for x in range(GRID_SIZE):
            grid[y][x] = 0
    for x in cols_to_clear:
        for y in range(GRID_SIZE):
            grid[y][x] = 0
    score += (len(rows_to_clear) + len(cols_to_clear)) * GRID_SIZE

def all_blocks_used():
    return len(blocks) == 0

def any_possible_moves():
    for block in blocks:
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if can_place_block(block, (x, y)):
                    return True
    return False

def restart_game():
    global grid, score, game_over, dragging, dragged_block, dragged_block_index
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    score = 0
    game_over = False
    dragging = False
    dragged_block = None
    dragged_block_index = None
    generate_new_blocks()

def get_snapped_position(pos):
    # Adjust the position to snap to the nearest grid cell
    x_screen, y_screen = pos
    x_grid = round((x_screen - GRID_ORIGIN_X - drag_offset_x) / CELL_SIZE)
    y_grid = round((y_screen - GRID_ORIGIN_Y - drag_offset_y) / CELL_SIZE)
    snapped_x = GRID_ORIGIN_X + x_grid * CELL_SIZE + drag_offset_x
    snapped_y = GRID_ORIGIN_Y + y_grid * CELL_SIZE + drag_offset_y
    return snapped_x, snapped_y

# Function to check and update high score
def check_highscore():
    global highscore
    if score > highscore:
        highscore = score
        save_highscore()

pgzrun.go()
