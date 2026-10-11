import turtle
from koblitz import *
# initializing the turtle settings

# ob = turtle.Turtle()
# ob.speed(10000)
# ob.hideturtle()
# wn = turtle.Screen()
# wn.bgcolor("black")
# ob.pencolor("teal")


def turn_sequence_generator(private_key):
    iterations = private_key[1]
    old = ['f', 'l']
    new = ['f', 'l']
    steps = []
    k = 0
    while(k < iterations):
        for i in range(0, len(old)-1):
            if old[i] == 'r':
                old[i] = 'l'
            elif old[i] == 'l':
                old[i] = 'r'
        for i in range(0, len(old)//2):
            t = old[i]
            old[i] = old[len(old)-i-2]
            old[len(old)-i-2] = t
        for i in old:
            new.append(i)
        for i in old[:]:
            old.remove(i)
        for i in new:
            old.append(i)
        for i in steps[:]:
            steps.remove(i)
        for i in range(0, len(new)):
            steps.append(new[i])
        k += 1
    return steps


def dragon_render(starting_point, private_key):
    size = private_key[0]

    x_start = starting_point[0]
    y_start = starting_point[1]
    angle = private_key[2]

    #print('Starting Point : (' + str(x_start) + ', ' + str(y_start) + ')')

    ob.penup()
    ob.goto(x_start, y_start)
    ob.pendown()

    ob.left(angle)

    steps = turn_sequence_generator(private_key)
    steps = steps[:-1]
    ob.pencolor('green')
    for i in steps:
        if i == 'f':
            ob.forward(size)
        elif i == 'r':
            ob.right(90)
        elif i == 'l':
            ob.left(90)

    x_end = round(ob.xcor())
    y_end = round(ob.ycor())

    #print('Ending Point : (' + str(x_end) + ', ' + str(y_end) + ')')
    return (x_end,y_end)


def reverse_dragon_render(starting_point, private_key):
    size = private_key[0]

    x_start = starting_point[0]
    y_start = starting_point[1]

    angle = private_key[2]

    #print('Reverse Starting Point : (' + str(x_start) + ', ' + str(y_start) + ')')

    ob.penup()
    ob.goto(x_start, y_start)
    ob.pendown()

    steps = turn_sequence_generator(private_key)
    steps = steps[:-1]
    ob.left(180+angle)
    ob.pencolor('red')
    for i in steps:
        if i == 'f':
            ob.forward(size)
        elif i == 'r':
            ob.right(90)
        elif i == 'l':
            ob.left(90)

    x_end = round(ob.xcor())
    y_end = round(ob.ycor())

    #print('Reverse Ending Point : (' + str(x_end) + ', ' + str(y_end) + ')')
    return (x_end,y_end)

def point_to_character(points):
    output_x = 'X'
    output_y = 'Y'
    for x,y in points:
        output_x += str(x) + 'X'
        output_y += str(y) + 'Y'

    return output_x+output_y

def character_to_point(output):
    output_x,output_y = output.split('XY')
    x_end = output_x.split('X')
    x_end = x_end[1:]
    x_end = [int(x) for x in x_end]
    y_end = output_y.split('Y')
    y_end = y_end[:-1]
    y_end = [int(y) for y in y_end]
    points = []
    for i in range(len(x_end)):
        points.append((x_end[i],y_end[i]))  
    return points


# private_key = (10, 5, 30)

# dragon_render((2082, 66), private_key)

# #reverse_dragon_render((1856, 292), private_key)

# turtle.done()
