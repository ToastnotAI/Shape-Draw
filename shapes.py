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
        for i in self.modifiers:
            if type(i) == list and i[0] == "colour":
                t.pencolor(i[1])
                if len(i) > 2:
                    t.fillcolor(i[2])

        if "fill" in self.modifiers:
            self.begin_fill(t)

        if "dashed" in self.modifiers:
            self.draw_dashed(t)

        if "dashed" not in self.modifiers:
            self.draw(t)
        
        if "fill" in self.modifiers:
            t.end_fill()
        t.pencolor("black") # reset line colour after drawing shape
        t.fillcolor("black") # reset fill colour after drawing shape



class Square(Shape):

    def draw(self, t):
        for side in range(4):
            t.forward(Shape.shapeWidth)
            t.left(90)
    
    def draw_dashed(self, t):
        done = False
        progress = [0, 0] # [distance covered on current side, sides completed]
        while not done:
            if progress[1] == 3 and progress[0] >= Shape.shapeWidth:
                done = True
            elif progress[0] >= Shape.shapeWidth:
                t.left(90)
                progress[0] = 0
                progress[1] += 1
            else:
                t.forward(Shape.dashLength)
                progress[0] += Shape.dashLength
                if t.isdown():
                    t.penup()
                else:
                    t.pendown()
        t.left(90)
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
            t.left(360 / self.turns)
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
    

class Triangle(Shape):
    def draw(self, t):
        for side in range(3):
            t.forward(Shape.shapeWidth)
            t.left(120)
    
    def draw_dashed(self, t):
        done = False
        progress = [0, 0] # [distance covered on current side, sides completed]
        while not done:
            if progress[1] == 2 and progress[0] >= Shape.shapeWidth:
                done = True
            elif progress[0] >= Shape.shapeWidth:
                t.left(120)
                progress[0] = 0
                progress[1] += 1
            else:
                t.forward(Shape.dashLength)
                progress[0] += Shape.dashLength
                if t.isdown():
                    t.penup()
                else:
                    t.pendown()
        t.left(120)
        t.penup()

class Blank(Shape):
    def draw(self, t):
        pass
    
    def draw_dashed(self, t):
        pass

class NewLine(Shape):
    def draw(self, t):
        t.penup()
        t.goto(999, t.ycor())
        t.pendown()
    
    def draw_dashed(self, t):
        self.draw()