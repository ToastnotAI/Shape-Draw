from colour import Color
class File():
    def __init__(self, path):
        self.path = path
    
    def read(self):
        with open(self.path, 'r') as f:
            content = f.read().strip().replace('\n','')
        f.close()
        return content
    
class Interpreter():
    commands = []

    def _check_colour(self, _colour):
        try:
            _colour = _colour.replace(" ", "")
            Color(_colour)
        except ValueError:
            raise ValueError("Argument for colour was not valid: {}".format(_colour))


    def parse_commands(self):
        lines = self.file.read()
        idx = 0
        state = 0 # 0 = looking for shape, 1 = looking for modifier start 2 = looking for modifiern 3 = grabbing colour
        
        while True:
            if idx > len(lines)-1:
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
                    
                    case _:
                        raise ValueError("Unknown shape type: {}".format(lines[idx]))

                
                if fill:
                    shape.append("fill")

            elif state == 1:
                if lines[idx] == '[':
                    state = 2
                else:
                    self.commands.append(shape)
                    state = 0
                    idx -=1
                
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


    def get_commands(self):
        return commands


    def __init__(self, filePath):
        self.file = File(filePath)
        self.parse_commands()

    def __repr__(self):
        return commands




if __name__ == "__main__":
    interpreter = Interpreter("test.txt")
    print(interpreter.commands)