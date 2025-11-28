import turtle
from shapes import Shape, Square, Circle, Triangle, Blank

# Factory class to create shapes
# shapeType is a list where the first element is the shape name and all other items are modifiers
class Factory():
    @staticmethod
    def create_shape(shapeType):
        if shapeType[0] == "square":
            return Square(shapeType[1:])
        elif shapeType[0] == "circle":
            return Circle(shapeType[1:])
        elif shapeType[0] == "triangle":
            return Triangle(shapeType[1:])
        elif shapeType[0] == "blank":
            return Blank(shapeType[1:])
        else:
            raise ValueError("Unknown shape type: {}, Ensure factory was fed a list".format(shapeType[0]))

class Renderer():
    t = None
    xLimit = 400
    shapeWidth = 100
    dashLength = 2
    thickness = 2
    def __init__(self):
        self.t = turtle.Turtle()
        self.t.speed(0)
        self.t.penup()
        self.t.goto(self.xLimit *-1, 200)
        self.t.pendown()
        self.t.pensize(self.thickness)
        Shape.shapeWidth = self.shapeWidth
        Shape.dashLength = self.dashLength
    
    def render(self, shapes):
        for shape in shapes:
            # use the turtle instance, not the module-level turtle functions
            if self.t.xcor() + shape.shapeWidth > self.xLimit:
                self.t.penup()
                self.t.goto(self.xLimit * -1, self.t.ycor() - Shape.shapeWidth - (0.1 * Shape.shapeWidth))
                self.t.pendown()
            # call begin on the instance, not the class
            shape.begin(self.t)
            self.t.penup()
            self.t.forward(Shape.shapeWidth + (0.1 * shape.shapeWidth))
            self.t.pendown()
        # don't call done on the Turtle instance; call turtle.done() in main
        


if __name__ == "__main__":
    import random
    shapes = ["circle", "square", "triangle", "blank"]
    modifiers = ["fill", "dashed", "colour"]
    queue = []
    for i in range(10):
        newShape = [random.choice(shapes)]#
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
    turtle.done()
