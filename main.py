import os
import turtle
from turtle import *
from math import sqrt, pow
import platform

if platform.system() == "Windows":

    try:
        import winsound
    except:
        print("Winsound module not available")

# Set up the screen
screen = Screen()
screen.setup(width=700, height=700)
screen.bgcolor("black")
screen.title("Space Invaders")
screen.bgpic("space_invaders_background.gif")
screen.tracer(0)

# Register Shapes
register_shape("invader.gif")
register_shape("player.gif")

# Draw border
border_pen = Turtle()
border_pen.color("white")
border_pen.speed(0)
border_pen.pensize(3)
border_pen.penup()
border_pen.goto(-300, -300)
border_pen.pendown()
for _ in range(4):
    border_pen.forward(600)
    border_pen.left(90)
border_pen.hideturtle()

score = 0

score_pen = Turtle()
score_pen.hideturtle()
score_pen.color("white")
score_pen.penup()
score_pen.goto(-290, 275)
score_pen.pendown()
score_string = f"Score: {score}"
score_pen.write(score_string, False, align="Left", font=("Arial", 14, "normal"))

# Create the player turtle
player = Turtle()
player.speed(0)
player.penup()
player.shape("player.gif")
player.color("blue")
player.goto(0, -250)
player.left(90)
player.speed = 0

enemy_count = 30
enemy_list = []


# Add enemies to the list
for i in range(enemy_count):
    # Create the enemy
    enemy_list.append(Turtle())

enemy_start_x = -225
enemy_start_y = 250
enemy_number = 0

# Customize enemies
for enemy in enemy_list:
    enemy.shape("invader.gif")
    enemy.color("red")
    enemy.speed(0)
    enemy.penup()
    x = enemy_start_x + (50 * enemy_number)
    y = enemy_start_y
    enemy.goto(x, y)
    # Update the enemy number
    enemy_number += 1
    if enemy_number == 10:
        enemy_start_y -= 50
        enemy_number = 0

enemy_speed = 0.2

# Create the player's bullet
bullet = Turtle()
bullet.speed(0)
bullet.shape("triangle")
bullet.color("yellow")
bullet.penup()
bullet.shapesize(0.5, 0.5)
bullet.setheading(90)
bullet.hideturtle()

bullet_speed = 7

# Define bullet state
# ready - ready to fire
# fire - bullet is firing
bullet_state = "ready"


# Move player left and right
def move_left():
    player.speed = -3


def move_right():
    player.speed = 3


def move_player():
    x = player.xcor()
    x += player.speed
    if x < -280:
        x = -280
    if x > 280:
        x = 280
    player.setx(x)


def fire_bullet():
    # Declare bulletstate as global if it needs changed
    global bullet_state
    if bullet_state == "ready":
        play_sound("laser.wav")
        bullet_state = "fire"
        # Move the bullet just above the player
        x = player.xcor()
        y = player.ycor() + 10
        bullet.goto(x, y)
        bullet.showturtle()


def is_collision(t1, t2):
    distance = sqrt(pow(t1.xcor() - t2.xcor(), 2) + pow(t1.ycor() - t2.ycor(), 2))
    if distance < 15:
        return True
    else:
        return False


def play_sound(sound_file, time=0):
    # Windows
    if platform.system() == "Windows":
        winsound.PlaySound(sound_file, winsound.SND_ASYNC)
    # Linux
    elif platform.system() == "Linux":
        os.system("aplay -q {}&".format(sound_file))
    else:
        os.system("afplay {}&".format(sound_file))

    # Repeat sound
    if time > 0:
        turtle.ontimer(lambda: play_sound(sound_file, time), t=int(time * 1000))


# Create keyboard binding
screen.listen()
screen.onkeypress(move_left, "Left")
screen.onkeypress(move_right, "Right")
screen.onkeypress(fire_bullet, "space")

# Play background music
play_sound("bgm.wav", 119)

# Main Game Loop
while True:
    screen.update()
    move_player()

    for enemy in enemy_list:
        # Move the enemy
        x = enemy.xcor()
        x += enemy_speed
        enemy.setx(x)

        # Move the enemy back and down
        if enemy.xcor() > 280:
            # Move all enemies down
            for e in enemy_list:
                y = e.ycor()
                y -= 40
                e.sety(y)
            # Change enemy direction
            enemy_speed *= -1

        if enemy.xcor() < -280:
            # Move all enemies down
            for e in enemy_list:
                y = e.ycor()
                y -= 40
                e.sety(y)
            # Change enemy direction
            enemy_speed *= -1

        # Check for a collision between the bullet and the enemy
        if is_collision(bullet, enemy):
            play_sound("explosion.wav")
            # Reset the bullet
            bullet.hideturtle()
            bullet_state = "ready"
            bullet.setposition(0, -400)
            # Reset the enemy
            enemy.goto(0, 10000)
            score += 10
            score_string = f"Score: {score}"
            score_pen.clear()
            score_pen.write(score_string, False, align="Left", font=("Arial", 14, "normal"))

        if is_collision(player, enemy):
            play_sound("explosion.wav")
            player.hideturtle()
            enemy.hideturtle()
            print("Game Over")
            break

    # Move the bullet
    if bullet_state == "fire":
        y = bullet.ycor()
        y += bullet_speed
        bullet.sety(y)

    # Check if bullet has reached top
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bullet_state = "ready"
