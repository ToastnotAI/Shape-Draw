import turtle
from shapes import Shape, Square, Circle
t = turtle.Turtle()

# Factory class to create shapes
# shapeType is a list where the first element is the shape name and all other items are modifiers
class Factory():
    @staticmethod
    def create_shape(shapeType):
        if shapeType[0] == "square":
            return Square(shapeType[1:])
        elif shapeType[0] == "circle":
            return Circle(shapeType[1:])
        else:
            raise ValueError("Unknown shape type: {}, Ensure factory was fed a list".format(shapeType[0]))

if __name__ == "__main__":
    shapes = []
    shapes.append(Factory.create_shape(["square", "fill"]))
    shapes.append(Factory.create_shape(["square"]))
    shapes.append(Factory.create_shape(["square", "dashed"]))
    shapes.append(Factory.create_shape(["square", "fill", "dashed"]))
    shapes.append(Factory.create_shape(["circle", "dashed"]))
    shapes.append(Factory.create_shape(["circle", "fill"]))
    t.penup()
    t.goto(-200, 200)
    t.pendown()
    for shape in shapes:
        shape.begin(t)
        t.penup()
        t.forward(shape.shapeWidth + (0.1 * shape.shapeWidth))
        t.pendown()
    turtle.done()
