import turtle
from shapes import Shape, Square, Circle, Triangle, Blank, NewLine

#
class Renderer():
    t = None
    xLimit = 400
    thickness = 4 

    def __init__(self):
        #initialise turtle and set it to start position
        self.t = turtle.Turtle()
        self.t.speed(0)
        self.t.penup()
        self.t.goto(self.xLimit *-1, 200)
        self.t.pendown()
        self.t.pensize(self.thickness)
    def render(self, shapes):
        for shape in shapes:
            #If turtle is too far right send it to the start of a new line
            if self.t.xcor() + shape.shapeWidth > self.xLimit:
                self.t.penup()
                self.t.goto(self.xLimit * -1, self.t.ycor() - Shape.shapeWidth - (0.1 * Shape.shapeWidth))
                self.t.pendown()
            #draw next shape then add a gap between shapes
            shape.begin(self.t)
            self.t.penup()
            self.t.forward(Shape.shapeWidth + (0.1 * shape.shapeWidth))
            self.t.pendown()
        turtle.done()        


"""if __name__ == "__main__":
    #code will randomly generate multiple shapes selected from the list
    import random
    shapes = ["circle", "square", "triangle", "blank"]
    modifiers = ["fill", "dashed", "colour"]
    queue = []
    for i in range(10):
        newShape = [random.choice(shapes)]
        modCount = random.randint(0, 3)
        for j in range(modCount):
            mod = random.choice(modifiers)
            if mod == "colour":
                colour = random.choice(["red", "blue", "green", "yellow", "purple"])
                fillColour = random.choice(["red", "blue", "green", "yellow", "purple"])
                newShape.append([mod, colour, fillColour])
            else:
                if mod not in newShape:
                    newShape.append(mod)#
        queue.append(newShape)
    
    
    request = [Factory.create_shape(s) for s in queue]

    renderer = Renderer()
    renderer.render(request)
    turtle.done()"""
