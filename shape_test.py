import unittest
from unittest.mock import MagicMock, patch
import unittest.mock
from interpreter import *
from shapes import *



class TestInterpreterBaseCases(unittest.TestCase):

    def test_base_square(self):
        with unittest.mock.patch('interpreter.File.read', return_value="s"):
            self.testInterpret = Interpreter(None)
            self.assertEqual(self.testInterpret.commands, [["square"]])
            print(File.read())

    def test_base_circle(self):
        with unittest.mock.patch('interpreter.File.read', return_value="c"):
            self.testInterpret = Interpreter(None)
            self.assertEqual(self.testInterpret.commands, [["circle"]])
    
    def test_base_triangle(self):
        with unittest.mock.patch('interpreter.File.read', return_value = "t"):
            self.testInterpret = Interpreter(None)
            self.assertEqual(self.testInterpret.commands, [["triangle"]])
    
    def test_base_blank(self):
        with unittest.mock.patch('interpreter.File.read', return_value = ' '):
            self.testInterpret = Interpreter(None)
            self.assertEqual(self.testInterpret.commands, [["blank"]])

    def test_base_all(self):
        with unittest.mock.patch('interpreter.File.read', return_value = "sct "):
            self.testInterpret = Interpreter(None)
            self.assertEqual(self.testInterpret.commands, [["square"],["circle"],["triangle"],["blank"]])

class TestInterpreterModCases(unittest.TestCase):
    def test_fill(self):
        with unittest.mock.patch('interpreter.File.read', return_value = "S"):
            self.testInterpret = Interpreter(None)
            self.assertEqual(self.testInterpret.commands, [["square","fill"]])
        
        with unittest.mock.patch('interpreter.File.read', return_value = "C"):
            self.testInterpret = Interpreter(None)
            self.assertEqual(self.testInterpret.commands, [["circle","fill"]])
        
        with unittest.mock.patch('interpreter.File.read', return_value = "T"):
            self.testInterpret = Interpreter(None)
            self.assertEqual(self.testInterpret.commands, [["triangle","fill"]])

        with unittest.mock.patch('interpreter.File.read', return_value = "SCT"):
            self.testInterpret = Interpreter(None)
            self.assertEqual(self.testInterpret.commands, [["square","fill"],["circle","fill"],["triangle","fill"]])
    
    def test_dashed(self):
        with unittest.mock.patch('interpreter.File.read', return_value = "s[d]"):
            self.testInterpret = Interpreter(None)
            self.assertEqual(self.testInterpret.commands, [["square","dashed"]])
        with unittest.mock.patch('interpreter.File.read', return_value = "c[d]"):
            self.testInterpret = Interpreter(None)
            self.assertEqual(self.testInterpret.commands, [["circle","dashed"]])
        
        with unittest.mock.patch('interpreter.File.read', return_value = "t[d]"):
            self.testInterpret = Interpreter(None)
            self.assertEqual(self.testInterpret.commands, [["triangle","dashed"]])
        
        with unittest.mock.patch('interpreter.File.read', return_value = "s[d]c[d]t[d]"):
            self.testInterpret = Interpreter(None)
            self.assertEqual(self.testInterpret.commands, [["square","dashed"],["circle","dashed"],["triangle","dashed"]])
        
    def test_colours(self):
        with unittest.mock.patch('interpreter.File.read', return_value = 's[[red]]'):
            self.testInterpret = Interpreter(None)
            self.assertEqual(self.testInterpret.commands, [["square",["colour","red"]]])

        with unittest.mock.patch('interpreter.File.read', return_value = "s[[#FFFFFF,#345678]]"):
            self.testInterpret = Interpreter(None)
            self.assertEqual(self.testInterpret.commands, [["square",["colour","#FFFFFF","#345678"]]])

    def test_colours_multiple_shapes(self):
        with unittest.mock.patch('interpreter.File.read', return_value = "s[[red]]c[[blue]]"):
            self.testInterpret = Interpreter(None)
            self.assertEqual(self.testInterpret.commands, [["square",["colour","red"]],["circle",["colour","blue"]]])
    
    def test_combined_modifiers(self):
        with unittest.mock.patch('interpreter.File.read', return_value = "S[d]"):
            self.testInterpret = Interpreter(None)
            self.assertEqual(self.testInterpret.commands, [["square","fill","dashed"]])
    
    def test_fill_and_colour(self):
        with unittest.mock.patch('interpreter.File.read', return_value = "S[[green]]"):
            self.testInterpret = Interpreter(None)
            self.assertEqual(self.testInterpret.commands, [["square","fill",["colour","green"]]])
    
    def test_dashed_and_colour(self):
        with unittest.mock.patch('interpreter.File.read', return_value = "s[d[#FF0000]]"):
            self.testInterpret = Interpreter(None)
            self.assertEqual(self.testInterpret.commands, [["square","dashed",["colour","#FF0000"]]])
    
    def test_all_modifiers(self):
        with unittest.mock.patch('interpreter.File.read', return_value = "S[d[yellow]]"):
            self.testInterpret = Interpreter(None)
            self.assertEqual(self.testInterpret.commands, [["square","fill","dashed",["colour","yellow"]]])

def test_all_modifiers_multiple_shapes(self):
    with unittest.mock.patch('interpreter.File.read', return_value = "S[d[yellow]]C[d[blue]]T[d[red]]"):
        self.testInterpret = Interpreter(None)
        self.assertEqual(self.testInterpret.commands, [["square","fill","dashed",["colour","yellow"]],["circle","fill","dashed",["colour","blue"]],["triangle","fill","dashed",["colour","red"]]])


class TestFactory(unittest.TestCase):
    def setUp(self):
        self.factory = Factory()
    
    def test_create_base_circle(self):
        circle = ["circle"]
        validCircle = Circle()
        x = self.factory.create_shape(circle)
        self.assertEqual(x, validCircle)
    
    def test_create_base_triangle(self):
        triangle = ["triangle"]
        validTriangle = Triangle()
        x = self.factory.create_shape(triangle)
        self.assertEqual(x, validTriangle)
    
    def test_create_square_filled(self):
        square = ["square", "fill"]
        validSquare = Square(["fill"])
        x = self.factory.create_shape(square)
        self.assertEqual(x, validSquare)
    
    def test_create_circle_dashed(self):
        circle = ["circle", "dashed"]
        validCircle = Circle(["dashed"])
        x = self.factory.create_shape(circle)
        self.assertEqual(x, validCircle)
    
    def test_create_square_with_colour(self):
        square = ["square", ["colour", "red"]]
        validSquare = Square([["colour","red"]])
        x = self.factory.create_shape(square)
        self.assertEqual(x, validSquare)
    
    def test_create_triangle_all_modifiers(self):
        triangle = ["triangle", "fill", "dashed", ["colour", "red","#FFFFFF"]]
        validTriangle = Triangle(["fill","dashed",["colour","red","#FFFFFF"]])
        x = self.factory.create_shape(triangle)
        self.assertEqual(x, validTriangle)
    