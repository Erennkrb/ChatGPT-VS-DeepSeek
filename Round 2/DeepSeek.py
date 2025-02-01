import tkinter as tk
import random

# Constants
WIDTH = 800
HEIGHT = 600
PLAYER_SIZE = 50
ASTEROID_SIZE = 40
BULLET_SIZE = 10
PLAYER_SPEED = 20
BULLET_SPEED = 15
ASTEROID_SPEED = 5
LIVES = 3

# Initialize the game window
root = tk.Tk()
root.title("Galactic Defender")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

# Variables
score = 0
lives = LIVES
asteroids = []  # Stores asteroid canvas IDs
bullets = []    # Stores bullet canvas IDs
game_over = False

# Load sounds (optional)
try:
    import winsound
except ImportError:
    winsound = None

def play_sound(sound):
    if winsound:
        winsound.PlaySound(sound, winsound.SND_ASYNC)

# Main Menu
def show_menu():
    canvas.delete("all")
    canvas.create_text(WIDTH//2, HEIGHT//4, text="Galactic Defender", font=("Arial", 48), fill="white")
    canvas.create_text(WIDTH//2, HEIGHT//2, text="Press [S] to Start", font=("Arial", 24), fill="white")
    canvas.create_text(WIDTH//2, HEIGHT//2 + 50, text="Press [Q] to Quit", font=("Arial", 24), fill="white")
    canvas.create_text(WIDTH//2, HEIGHT//2 + 100, text="Press [H] for Help", font=("Arial", 24), fill="white")

# Help Screen
def show_help():
    canvas.delete("all")
    canvas.create_text(WIDTH//2, HEIGHT//4, text="How to Play", font=("Arial", 36), fill="white")
    canvas.create_text(WIDTH//2, HEIGHT//2, text="Use [Left] and [Right] to move.\nPress [Space] to shoot.\nDestroy asteroids to score points.\nAvoid getting hit!", font=("Arial", 18), fill="white", justify="center")
    canvas.create_text(WIDTH//2, HEIGHT-50, text="Press [M] to return to Menu", font=("Arial", 18), fill="white")

# Game Over Screen
def show_game_over():
    global game_over
    game_over = True
    canvas.delete("all")
    canvas.create_text(WIDTH//2, HEIGHT//3, text="GAME OVER", font=("Arial", 48), fill="red")
    canvas.create_text(WIDTH//2, HEIGHT//2, text=f"Final Score: {score}", font=("Arial", 36), fill="white")
    canvas.create_text(WIDTH//2, HEIGHT-100, text="Press [R] to Restart", font=("Arial", 24), fill="white")
    canvas.create_text(WIDTH//2, HEIGHT-50, text="Press [Q] to Quit", font=("Arial", 24), fill="white")

# Initialize Game
def start_game():
    global score, lives, game_over
    score = 0
    lives = LIVES
    game_over = False
    canvas.delete("all")
    for bullet in bullets:
        canvas.delete(bullet)
    for asteroid in asteroids:
        canvas.delete(asteroid)
    bullets.clear()
    asteroids.clear()
    draw_player()
    update_score()
    update_lives()
    spawn_asteroids()
    root.after(50, game_loop)

# Draw Player
def draw_player():
    x = WIDTH // 2
    y = HEIGHT - 100
    canvas.create_text(x, y, text="🚀", font=("Arial", PLAYER_SIZE), tags="player")

# Draw Bullet (returns bullet ID)
def draw_bullet(x, y):
    bullet = canvas.create_rectangle(x, y, x+BULLET_SIZE, y+BULLET_SIZE, fill="yellow")
    return bullet

# Draw Asteroid (returns asteroid ID)
def draw_asteroid(x, y):
    asteroid = canvas.create_text(x, y, text="🪨", font=("Arial", ASTEROID_SIZE))
    return asteroid

# Update Score
def update_score():
    canvas.delete("score")
    canvas.create_text(100, 30, text=f"Score: {score}", font=("Arial", 24), fill="white", tags="score")

# Update Lives
def update_lives():
    canvas.delete("lives")
    canvas.create_text(WIDTH-100, 30, text=f"Lives: {lives}", font=("Arial", 24), fill="white", tags="lives")

# Spawn Asteroids
def spawn_asteroids():
    if not game_over:
        x = random.randint(0, WIDTH - ASTEROID_SIZE)
        y = 0
        asteroid = draw_asteroid(x, y)
        asteroids.append(asteroid)
        root.after(random.randint(500, 2000), spawn_asteroids)

# Game Loop
def game_loop():
    global lives, score, game_over
    if game_over:
        return

    # Move bullets
    for bullet in bullets[:]:
        coords = canvas.coords(bullet)
        if not coords:
            bullets.remove(bullet)
            continue
        x, y = coords
        if y < 0:
            canvas.delete(bullet)
            bullets.remove(bullet)
        else:
            canvas.move(bullet, 0, -BULLET_SPEED)

    # Move asteroids
    for asteroid in asteroids[:]:
        coords = canvas.coords(asteroid)
        if not coords:
            asteroids.remove(asteroid)
            continue
        x, y = coords
        if y > HEIGHT:
            canvas.delete(asteroid)
            asteroids.remove(asteroid)
            lives -= 1
            update_lives()
            if lives <= 0:
                show_game_over()
                return
        else:
            canvas.move(asteroid, 0, ASTEROID_SPEED)

    # Check collisions
    for bullet in bullets[:]:
        bullet_coords = canvas.coords(bullet)
        if not bullet_coords:
            continue
        for asteroid in asteroids[:]:
            asteroid_coords = canvas.coords(asteroid)
            if not asteroid_coords:
                continue
            # Collision detection
            if (abs(bullet_coords[0] - asteroid_coords[0]) < ASTEROID_SIZE and
                abs(bullet_coords[1] - asteroid_coords[1]) < ASTEROID_SIZE):
                canvas.delete(bullet)
                canvas.delete(asteroid)
                bullets.remove(bullet)
                asteroids.remove(asteroid)
                play_sound("SystemAsterisk")
                score += 10
                update_score()

    root.after(50, game_loop)

# Keyboard Controls
def handle_key(event):
    key = event.keysym
    if key == "s":
        start_game()
    elif key == "q":
        root.quit()
    elif key == "h":
        show_help()
    elif key == "m":
        show_menu()
    elif key == "r" and game_over:
        start_game()
    elif key == "Left":
        x, y = canvas.coords("player")
        if x > PLAYER_SIZE:
            canvas.move("player", -PLAYER_SPEED, 0)
    elif key == "Right":
        x, y = canvas.coords("player")
        if x < WIDTH - PLAYER_SIZE:
            canvas.move("player", PLAYER_SPEED, 0)
    elif key == "space":
        x, y = canvas.coords("player")
        bullet = draw_bullet(x, y - PLAYER_SIZE)
        bullets.append(bullet)
        play_sound("SystemExclamation")

# Bind keys
root.bind("<Key>", handle_key)

# Start with the menu
show_menu()

# Run the game
root.mainloop()