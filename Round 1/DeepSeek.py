import tkinter as tk
import random

# Constants
WIDTH = 800
HEIGHT = 600
BASKET_WIDTH = 100
BASKET_HEIGHT = 20
OBJECT_SIZE = 40
FALL_SPEED = 5
OBJECT_TYPES = ["🍎", "🍌", "🍇", "🍒", "🍓"]  # Emoji fruits

# Initialize the game window
root = tk.Tk()
root.title("Catch the Falling Objects")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="lightblue")
canvas.pack()

# Variables
score = 0
fall_speed = FALL_SPEED
objects = []

# Score display
score_label = tk.Label(root, text=f"Score: {score}", font=("Arial", 24))
score_label.pack()

# Basket
basket = canvas.create_rectangle(
    WIDTH // 2 - BASKET_WIDTH // 2,
    HEIGHT - BASKET_HEIGHT,
    WIDTH // 2 + BASKET_WIDTH // 2,
    HEIGHT,
    fill="brown",
)

# Function to move the basket
def move_basket(event):
    key = event.keysym
    x1, y1, x2, y2 = canvas.coords(basket)
    if key == "Left" and x1 > 0:
        canvas.move(basket, -20, 0)
    elif key == "Right" and x2 < WIDTH:
        canvas.move(basket, 20, 0)


# Function to create falling objects
def create_object():
    x = random.randint(0, WIDTH - OBJECT_SIZE)
    y = 0
    obj_type = random.choice(OBJECT_TYPES)
    obj = canvas.create_text(x, y, text=obj_type, font=("Arial", OBJECT_SIZE), fill="black")
    objects.append(obj)
    root.after(1000, create_object)  # Create a new object every second


# Function to update falling objects
def update_objects():
    global score, fall_speed
    for obj in objects:
        canvas.move(obj, 0, fall_speed)
        x, y = canvas.coords(obj)
        if y > HEIGHT:  # Object missed
            canvas.delete(obj)
            objects.remove(obj)
        elif check_collision(obj):  # Object caught
            canvas.delete(obj)
            objects.remove(obj)
            score += 1
            score_label.config(text=f"Score: {score}")
            if score % 5 == 0:  # Increase speed every 5 points
                fall_speed += 1
    root.after(50, update_objects)


# Function to check collision between basket and object
def check_collision(obj):
    x1, y1 = canvas.coords(obj)
    x2, y2 = x1 + OBJECT_SIZE, y1 + OBJECT_SIZE
    basket_coords = canvas.coords(basket)
    return (
        basket_coords[0] < x1 < basket_coords[2]
        and basket_coords[1] < y1 < basket_coords[3]
    )


# Bind keyboard events
root.bind("<Left>", move_basket)
root.bind("<Right>", move_basket)

# Start the game
create_object()
update_objects()

# Run the game
root.mainloop()