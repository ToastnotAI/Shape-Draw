import turtle
t = turtle.Turtle()

#Shape is an abstract class
class Shape():
    # scale will change size of all shapes
    scale = 1
    modifiers = []
    def draw(self, t):
        raise NotImplementedError("Subclasses should implement this method")

    def fill(self, t):
        t.begin_fill()
        self.draw(t)
        t.end_fill()
    
    def begin(self, t):
        if "fill" in self.modifiers:
            self.fill(t)
        if self.modifiers == []:
            self.draw(t)



class Square(Shape):
    def __init__(self, modifiers = None):
        if modifiers is not None:
            self.modifiers = modifiers

    def draw(self, t):
        for side in range(4):
            t.forward(100 * Shape.scale)
            t.right(90)



# Factory class to create shapes
# shapeType is a list where the first element is the shape name and all other items are modifiers
class Factory():
    @staticmethod
    def create_shape(shapeType):
        if shapeType[0] == "square":
            return Square(shapeType[1:])
        else:
            raise ValueError("Unknown shape type: {}, Ensure factory was fed a list".format(shapeType[0]))

if __name__ == "__main__":
    shapes = []
    shapes.append(Factory.create_shape(["square", "fill"]))
    shapes.append(Factory.create_shape(["square"]))
    t.penup()
    t.goto(-200, 200)
    t.pendown()
    for shape in shapes:
        shape.begin(t)
        t.penup()
        t.forward(150 * Shape.scale)
        t.pendown()
    turtle.done()
