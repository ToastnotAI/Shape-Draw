from shape_renderer import Renderer
from interpreter import File, Interpreter
from shapes import *

target = input("Name of file to be interpreted: ")
file1 = Interpreter(target)
request = [Factory.create_shape(s) for s in file1.commands]
canvas = Renderer()
canvas.render(request)
