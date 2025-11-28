from shape_renderer import Renderer, Factory
from interpreter import File, Interpreter

file1 = Interpreter("test.txt")
request = [Factory.create_shape(s) for s in file1.commands]
canvas = Renderer()
canvas.render(request)