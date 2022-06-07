# construct a triangle using random angles and lengths
import random
import turtle
import math


# solve for missing angles and sides of triangles
def finder(angles, lengths):
    # print known angles for testing purposes
    print(angles[1], angles[0], lengths[0])

    # first find missing angle
    c = 180 - sum(angles)
    angles.append(c)

    # sort angles in ascending order
    angles.sort()

    # assume known side is smallest side
    B = (lengths[0] * math.sin(math.radians(angles[1]))) / math.sin(math.radians(angles[0]))
    C = (lengths[0] * math.sin(math.radians(angles[2]))) / math.sin(math.radians(angles[0]))
    print(round(B, 2), round(C, 2))
    lengths.append(round(B, 2))
    lengths.append(round(C, 2))
    perimeter = sum(lengths)
    print(lengths, perimeter)

    # sort out lengths to match respective angles
    lengths[0] = lengths[1]
    lengths[1] = lengths[2]
    lengths[2] = perimeter - (lengths[0] + lengths[1])
    print(lengths)
    triangle(lengths, angles)

# draws a triangle using given parameters
def triangle(displacement, angle):
    # initialise turtles
    wn = turtle.Screen()  # Set up the window and its attributes

    # This just makes the screen full screen without the user having to touch the maximize button repeatedly
    wn.setup(width=0.5, height=0.5, startx=None, starty=None)
    wn.bgcolor("lightgreen")
    wn.title("Triangle")

    to_draw = turtle.Turtle()  # Create to_draw and set some attributes
    place_text = turtle.Turtle()
    to_draw.hideturtle()
    place_text.hideturtle()
    place_text.penup()

    to_draw.color("black")
    to_draw.pensize(5)
    place_text.write('A', font = 'style', move = True, align = 'right')
    to_draw.forward(displacement[0] * 10)  # Make to_draw draw a triangle
    to_draw.left(180 - angle[0])

    place_text.forward(displacement[0] * 10)  # move text
    place_text.write('B', font = 'style', align = 'left', move=True)	
    place_text.left(180 - angle[0])
    

   	
    to_draw.forward(displacement[1] * 10)	
    to_draw.left(180 - angle[1])	
    
    place_text.forward(displacement[1] * 10)  # move text
    place_text.write('C', move = True, font = 'style', align = 'center')	
    to_draw.forward(displacement[2] * 10)
    # Complete the triangle

    # show triangle for a few seconds then continue program
    wn.mainloop()


# lists for angles and sides
some_angles = []
some_sides = []

# generate angles and append to list
a = random.randint(30, 90)
b = random.randint(30, 89)
some_angles.append(a)
some_angles.append(b)

# generate sides and append to list
A = random.randint(5, 15)
some_sides.append(A)

finder(some_angles, some_sides)
