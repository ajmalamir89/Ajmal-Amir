from turtle import Turtle, Screen
import random
import tkinter as tk
from tkinter import messagebox

def confetti():
    confetti_turtle.clear()
    for _ in range(100):
        confetti_turtle.speed("fast")
        x = random.randint(-250, 250)
        y = random.randint(-200, 200)
        confetti_turtle.penup()
        confetti_turtle.color(random.choice(confetti_colors))
        confetti_turtle.goto(x, y)
        confetti_turtle.dot(10)

def display_message(message):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showinfo("Race Result", message)
    root.destroy()  # Destroy the Tkinter main window

# Set up the screen
screen = Screen()
screen.title("Turtle Race Developed by Ajmal Amir")  # Set the title of the turtle graphics window
screen.bgcolor("black")
screen.setup(width=500, height=400)

# Get user bet
user_bet = screen.textinput("Name of Turtle you bet on", "Please enter a color for the turtle you bet on")

# Initialize turtles
colors = ["red", "orange", "yellow", "green", "blue", "purple"]
y_positions = [-70, -40, -10, 20, 50, 80]
all_turtles = []

for turtle_index in range(6):
    tim = Turtle("turtle")
    tim.color(colors[turtle_index])
    tim.penup()
    tim.goto(x=-230, y=y_positions[turtle_index])
    all_turtles.append(tim)

# Initialize confetti turtle
confetti_turtle = Turtle()
confetti_turtle.hideturtle()
confetti_colors = ["yellow", "pink", "green", "orange"]

is_race_on = False

if user_bet:
    is_race_on = True

while is_race_on:
    for turtle in all_turtles:
        if turtle.xcor() > 250:
            is_race_on = False
            winning_color = turtle.pencolor()
            if winning_color == user_bet:
                display_message(f"You've won! The {winning_color} turtle is the winner!")
                confetti()
            else:
                display_message(f"You've lost! The {winning_color} turtle is the winner!")

            screen.bye()  # Close the Tkinter GUI window
            turtle.done()  # Close the turtle graphics window

        rand_distance = random.randint(0, 10)
        turtle.forward(rand_distance)



# def move_Forward():
#     tim.forward(10)
#
# def move_backward():
#     tim.backward(10)
# def move_counter_Clickwise():
#     tim.right(10)
# def move_clockwise():
#     tim.right(-10)
# def clear():
#     tim.home()
#     tim.clear()
#
#
# screen.listen()
# screen.onkey(move_Forward, 'w')
# screen.onkey(move_backward, 's')
# screen.onkey(move_counter_Clickwise, 'a')
# screen.onkey(move_clockwise, 'd')
# screen.onkey(clear, 'c')
screen.exitonclick()