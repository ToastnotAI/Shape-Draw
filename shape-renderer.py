import turtle
t = turtle.Turtle()


#Shape is an abstract class
class Shape():
    shapeWidth = 50
    dashLength = 5
    modifiers = []

    def __init__(self, modifiers = None):
        if modifiers is not None:
            self.modifiers = modifiers

    def draw(self, t):
        raise NotImplementedError("Subclasses should implement this method")

    def draw_dashed(self, t):
        raise NotImplementedError("Subclasses should implement this method")

# method to handle fill can be overridden if needed
    def begin_fill(self, t):
        t.begin_fill()
    
    def end_fill(self, t):
        t.end_fill()
        
    def begin(self, t):
        if "fill" in self.modifiers:
            self.begin_fill(t)

        if "dashed" in self.modifiers:
            self.draw_dashed(t)

        if "dashed" not in self.modifiers:
            self.draw(t)
        
        if "fill" in self.modifiers:
            t.end_fill()



class Square(Shape):

    def draw(self, t):
        for side in range(4):
            t.forward(shape.shapeWidth)
            t.right(90)
    
    def draw_dashed(self, t):
        done = False
        progress = [0, 0] # [distance covered on current side, sides completed]
        penDown = True
        while not done:
            if progress[1] == 3 and progress[0] >= shape.shapeWidth:
                done = True
            elif progress[0] >= shape.shapeWidth:
                t.right(90)
                progress[0] = 0
                progress[1] += 1
            elif penDown:
                t.forward(shape.dashLength)
                progress[0] += shape.dashLength
                penDown = False
                t.penup()
            else:
                t.forward(shape.dashLength)
                progress[0] += shape.dashLength
                penDown = True
                t.pendown()
        t.right(90)
        t.penup()


class Circle(Shape):
    turns = 72
    
    def draw(self, t, dashed = False):
        pen = t.isdown()
        t.penup()
        t.forward(Shape.shapeWidth / 2)
        if pen:
            t.pendown()
        for turn in range(self.turns):
            t.right(360 / self.turns)
            t.forward((3.14 * Shape.shapeWidth) / self.turns) # use shapeWidth as diameter to find circumference
            if dashed: # dashLength is not compatible with circles so it is handled differently
                if t.isdown():
                    t.penup()
                else:
                    t.pendown()

        t.penup()
        t.backward(Shape.shapeWidth / 2)
        if pen:
            t.pendown()
    

    def draw_dashed(self, t):
        self.draw(t, dashed = True)





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
