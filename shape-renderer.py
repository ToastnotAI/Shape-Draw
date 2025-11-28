import turtle
from shapes import Shape, Square, Circle, Triangle

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
        else:
            raise ValueError("Unknown shape type: {}, Ensure factory was fed a list".format(shapeType[0]))

class Renderer():
    t = None
    xLimit = 350
    shapeWidth = 100
    dashLength = 10
    def __init__(self):
        self.t = turtle.Turtle()
        self.t.speed(0)
        self.t.penup()
        self.t.goto(self.xLimit *-1, 200)
        self.t.pendown()
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

    shapes = []
    shapes.append(Factory.create_shape(["square", "fill"]))
    shapes.append(Factory.create_shape(["triangle"]))
    shapes.append(Factory.create_shape(["square", "dashed"]))
    shapes.append(Factory.create_shape(["triangle", "fill", "dashed", ["colour", "red", "yellow"]]))
    shapes.append(Factory.create_shape(["circle", "dashed"]))
    shapes.append(Factory.create_shape(["circle", "fill"]))
    shapes.append(Factory.create_shape(["square", "fill"]))
    shapes.append(Factory.create_shape(["triangle"]))
    shapes.append(Factory.create_shape(["square", "dashed"]))
    shapes.append(Factory.create_shape(["triangle", "fill", "dashed", ["colour", "blue", "#00F034"]]))
    shapes.append(Factory.create_shape(["circle", "dashed"]))
    shapes.append(Factory.create_shape(["circle", "fill"]))
    renderer = Renderer()
    renderer.render(shapes)
    turtle.done()
