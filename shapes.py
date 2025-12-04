#Shape is an abstract class
class Shape():
    shapeWidth = 50 #Determines length of shape along x axis
    dashLength = 5 #Determines how long the dashes should be in draw_dashed methods (excluding circle class). Shape positions may get offset at higher values.
    modifiers = [] 

    def __init__(self, modifiers = None):
        if modifiers is not None:
            self.modifiers = modifiers

    #draw and draw_dashed must be implemented by the subclass
    def draw(self, t):
        raise NotImplementedError("Subclasses should implement this method")

    def draw_dashed(self, t):
        raise NotImplementedError("Subclasses should implement this method")

# method to handle fill can be overridden if needed
    def _begin_fill(self, t):
        t.begin_fill()
    
    def _end_fill(self, t):
        t.end_fill()
        
    def begin(self, t):
        for i in self.modifiers:
            if type(i) == list and i[0] == "colour":
                t.pencolor(i[1])
                if len(i) > 2:
                    t.fillcolor(i[2])
        #Fill conditions must be the first and last conditions to properly fill the shape
        if "fill" in self.modifiers:
            self._begin_fill(t)

        #different line types can be added to this chain
        if "dashed" in self.modifiers:
            self.draw_dashed(t)
        else:
            self.draw(t)
        
        if "fill" in self.modifiers:
            self._end_fill(t)
        t.pencolor("black") # reset line colour after drawing shape
        t.fillcolor("black") # reset fill colour after drawing shape

    def __eq__(self,other): #Equivalance function
        if type(other) != type(self):
            return False
        if other.modifiers == self.modifiers:
            return True
        else:
            return False

class Square(Shape):
    def draw(self, t):
        for side in range(4):
            t.forward(Shape.shapeWidth)
            t.left(90)
    
    def draw_dashed(self, t):
        done = False
        progress = [0, 0] # [distance covered on current side, sides completed]
        while not done:
            #exit condition
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
    #Turns can be modified and the function should compensate
    turns = 30
    
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
        t.goto(999, t.ycor()) #Shape classes do not directly have access to xLimit so send the turtle to the right to trigger the new line function
        t.pendown()
    
    def draw_dashed(self, t):
        self.draw()