from tkinter import *
import random

GAME_WIDTH = 600
GAME_HEIGHT = 540
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOUR = "#00FF00"
FOOD_COLOUR = "#FF0000"
BACKGROUND_COLOUR = "#000000"
OBSTACLE_COLOUR = "#0000FF"  # Blue color for obstacles
DEFAULT_SPEED = 300

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for _ in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOUR, tag="snake")
            self.squares.append(square)


class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOUR, tag="food")


class Obstacle:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=OBSTACLE_COLOUR, tag="obstacle")


def next_turn(snake, food, obstacles):
    global SPEED

    x, y = snake.coordinates[0]

    if direction == 'up':
        y -= SPACE_SIZE
    elif direction == 'down':
        y += SPACE_SIZE
    elif direction == 'left':
        x -= SPACE_SIZE
    elif direction == 'right':
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOUR)

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score, SPEED
        score += 1
        SPEED -= 5  # Increase speed
        label.config(text="Score: {}".format(score))
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake, obstacles):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food, obstacles)


def change_direction(new_direction):
    global direction
    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction


def check_collisions(snake, obstacles):
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    for obstacle in obstacles:
        if x == obstacle.coordinates[0] and y == obstacle.coordinates[1]:
            return True
    return False


def game_over():
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, font=('consolas', 70), text="GAME OVER",
                       fill="red", tag="gameover")
    global high_score
    if score > high_score:
        high_score = score
        high_score_label.config(text="High Score: {}".format(high_score))

    reset_button = Button(text="Restart", font=('consolas', 20), command=reset)
    canvas.create_window(300, 400, window=reset_button)


def reset():
    global score, direction, SPEED
    score = 0
    direction = 'down'
    SPEED = DEFAULT_SPEED  # Reset speed
    label.config(text="Score:{}".format(score))
    canvas.delete(ALL)
    snake = Snake()
    food = Food()
    obstacles = [Obstacle() for _ in range(5)]  # Generate 5 obstacles
    next_turn(snake, food, obstacles)


window = Tk()
window.title("Snake Game")
window.resizable(True, True)

score = 0
direction = 'down'
SPEED = DEFAULT_SPEED
high_score = 0

label = Label(window, text="Score:{}".format(score), font=('consolas', 20))
label.pack()

high_score_label = Label(window, text="High Score:{}".format(high_score), font=('consolas', 20))
high_score_label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOUR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
food = Food()
obstacles = [Obstacle() for _ in range(5)]  # Generate 5 obstacles

next_turn(snake, food, obstacles)

window.mainloop()