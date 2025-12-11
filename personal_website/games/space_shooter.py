import tkinter as tk
import random
from PIL import Image, ImageTk

# -----------------------------
# Window Setup
# -----------------------------
root = tk.Tk()
root.title("Space Shooter - Improved Graphics")
root.resizable(False, False)

WIDTH = 600
HEIGHT = 700

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack()

# -----------------------------
# Load Images
# -----------------------------
def load_img(path, size=None):
    img = Image.open(path)
    if size:
        img = img.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)

bg_img = load_img("bg.png", (WIDTH, HEIGHT))
player_img = load_img("player.png", (70, 70))
enemy_img = load_img("enemy.png", (60, 60))
bullet_img = load_img("bullet.png", (20, 40))

explosion_frames = [
    load_img("explosion1.png", (60, 60)),
    load_img("explosion2.png", (60, 60)),
    load_img("explosion3.png", (60, 60))
]

# -----------------------------
# Drawing Background
# -----------------------------
bg1 = canvas.create_image(0, 0, image=bg_img, anchor="nw")
bg2 = canvas.create_image(0, -HEIGHT, image=bg_img, anchor="nw")

def scroll_bg():
    canvas.move(bg1, 0, 2)
    canvas.move(bg2, 0, 2)

    if canvas.coords(bg1)[1] >= HEIGHT:
        canvas.coords(bg1, 0, -HEIGHT)
    if canvas.coords(bg2)[1] >= HEIGHT:
        canvas.coords(bg2, 0, -HEIGHT)

    root.after(20, scroll_bg)

scroll_bg()

# -----------------------------
# Player Setup
# -----------------------------
player = canvas.create_image(WIDTH // 2, HEIGHT - 100, image=spaceship.png)
player_speed = 10

keys_pressed = {"left": False, "right": False, "up": False, "down": False}

def move_player():
    x, y = canvas.coords(player)

    if keys_pressed["left"] and x > 40:
        canvas.move(player, -player_speed, 0)
    if keys_pressed["right"] and x < WIDTH - 40:
        canvas.move(player, player_speed, 0)
    if keys_pressed["up"] and y > 40:
        canvas.move(player, 0, -player_speed)
    if keys_pressed["down"] and y < HEIGHT - 40:
        canvas.move(player, 0, player_speed)

    root.after(20, move_player)

move_player()

def key_press(event):
    if event.keysym == "Left": keys_pressed["left"] = True
    if event.keysym == "Right": keys_pressed["right"] = True
    if event.keysym == "Up": keys_pressed["up"] = True
    if event.keysym == "Down": keys_pressed["down"] = True

def key_release(event):
    if event.keysym == "Left": keys_pressed["left"] = False
    if event.keysym == "Right": keys_pressed["right"] = False
    if event.keysym == "Up": keys_pressed["up"] = False
    if event.keysym == "Down": keys_pressed["down"] = False

root.bind("<KeyPress>", key_press)
root.bind("<KeyRelease>", key_release)

# -----------------------------
# Bullets
# -----------------------------
bullets = []

def shoot(event=None):
    px, py = canvas.coords(player)
    bullet = canvas.create_image(px, py - 40, image=bullet_img)
    bullets.append(bullet)

root.bind("<space>", shoot)

def move_bullets():
    for bullet in bullets[:]:
        canvas.move(bullet, 0, -15)
        if canvas.coords(bullet)[1] < 0:
            canvas.delete(bullet)
            bullets.remove(bullet)
    root.after(30, move_bullets)

move_bullets()

# -----------------------------
# Enemies
# -----------------------------
enemies = []

def spawn_enemy():
    x = random.randint(50, WIDTH - 50)
    enemy = canvas.create_image(x, 0, image=enemy_img)
    enemies.append(enemy)
    root.after(random.randint(800, 1400), spawn_enemy)

spawn_enemy()

def move_enemies():
    for enemy in enemies[:]:
        canvas.move(enemy, 0, 4)

        if canvas.coords(enemy)[1] > HEIGHT:
            canvas.delete(enemy)
            enemies.remove(enemy)

    root.after(30, move_enemies)

move_enemies()

# -----------------------------
# Explosion Animation
# -----------------------------
def explode(x, y):
    exp = canvas.create_image(x, y, image=explosion_frames[0])

    def animate(frame=0):
        if frame < len(explosion_frames):
            canvas.itemconfig(exp, image=explosion_frames[frame])
            root.after(80, animate, frame + 1)
        else:
            canvas.delete(exp)

    animate()

# -----------------------------
# Collision Detection
# -----------------------------
score = 0
score_text = canvas.create_text(60, 30, text="Score: 0", fill="white", font=("Arial", 20, "bold"))

def check_collisions():
    global score
    for bullet in bullets[:]:
        bx, by = canvas.coords(bullet)
        for enemy in enemies[:]:
            ex, ey = canvas.coords(enemy)

            # Collision
            if abs(bx - ex) < 30 and abs(by - ey) < 30:
                explode(ex, ey)
                canvas.delete(bullet)
                canvas.delete(enemy)
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 10
                canvas.itemconfig(score_text, text=f"Score: {score}")

    root.after(30, check_collisions)

check_collisions()

# -----------------------------
# Start Game
# -----------------------------
root.mainloop()
