from colour import Color
from shapes import *
class File():
    def __init__(self, path):
        self.path = path
    
    def read(self):
        with open(self.path, 'r') as f:
            content = f.read().strip().strip('\n')
        f.close()
        return content
    
class Interpreter():
    #Private method to check if colours read from file are valid
    def _check_colour(self, _colour):
        try:
            _colour = _colour.replace(" ", "")
            Color(_colour)
        except ValueError:
            raise ValueError("Argument for colour was not valid: {}".format(_colour))


    def parse_commands(self):
        self.commands = []
        lines = self.file.read()
        idx = 0
        state = 0 
        #State machine to parse file. 0 = looking for shape, 1 = looking for modifier start 2 = looking for modifiers 3 = grabbing colours
        
        while True:
            #Exit condition if the index exceeds the file length
            if idx >= len(lines):
                if state == 1: #If the state machine is still in state 1 then the last shape was not added to the list so it must be done here
                    self.commands.append(shape)
                break

            #Searching for shape
            if state == 0:
                shape = []
                fill = False
                if lines[idx].isupper():
                    fill = True
                #check what shape current letter is
                match lines[idx].lower():
                    case 't':
                        shape.append("triangle")
                        state = 1
                    case 's':
                        shape.append("square")
                        state = 1
                    case 'c':
                        shape.append("circle")
                        state = 1
                    case ' ':
                        shape.append("blank")
                        state = 1
                    case '\n':
                        shape.append("newLine")
                        state = 1
                    case _:
                        raise ValueError("Unknown shape type: {}".format(lines[idx]))
                
                if fill:
                    shape.append("fill")
            #Searching for start of modifiers
            elif state == 1:
                if lines[idx] == '[':
                    state = 2
                else:
                    #if modifiers did not start append and go back so machine can check for shape again
                    self.commands.append(shape)
                    state = 0
                    idx -=1
            #Check which modifier has been found (additional modifiers must be added here)
            elif state == 2:
                match lines[idx].lower():
                    case 'd':
                        shape.append("dashed") 
                    case '[':
                        colour = ["colour"]
                        current = ""
                        state = 3
                    case ']':
                        self.commands.append(shape)
                        state = 0
                    case _:
                        raise ValueError("Unkown Modifier: {}".format(lines[idx]))
            #Get colours to add to colour modifier
            elif state == 3:
                match lines[idx]:
                    case ",":
                        colour.append(current)
                        self._check_colour(current)
                        current=""
                    case "]":
                        colour.append(current)
                        shape.append(colour)
                        state = 2
                        if len(colour) > 3:
                            raise TypeError("Expected 2 arguments for colour but {} were given".format(len(colour)-1))
                        self._check_colour(current)
                    case _:
                        current += str(lines[idx])                     
            idx += 1


    def __init__(self, filePath):
        self.file = File(filePath)
        self.parse_commands()

    def __repr__(self):
        return str(self.commands)

"""
if __name__ == "__main__":
    interpreter = Interpreter("test.txt")
    print(interpreter)
    """