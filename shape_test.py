import unittest
from unittest.mock import MagicMock, patch, mock_open
import unittest.mock
from interpreter import *
from shapes import *
from shape_renderer import *



class TestInterpreterFileFunctions(unittest.TestCase):
    def test_file_read(self):
        with patch('builtins.open', unittest.mock.mock_open(read_data="test data")) as mock_file:
            file = File("dummy_path")
            data = file.read()
            mock_file.assert_called_once_with("dummy_path", 'r')
            self.assertEqual(data, "test data")
    
    def test_file_read_wrong_path(self):
        with patch('builtins.open', side_effect=FileNotFoundError) as mock_file:
            file = File("wrong_path")
            self.assertRaises(FileNotFoundError, file.read)
            mock_file.assert_called_once_with("wrong_path", 'r')


class TestInterpreterCommands(unittest.TestCase):
    def setUp(self):
        mock_open = unittest.mock.mock_open(read_data="")
        self.patcher = patch('builtins.open', mock_open)
        self.mock_file = self.patcher.start()

    def test_check_colour_valid(self):
        interpreter = Interpreter("dummy_path")
        try:
            interpreter._check_colour("red")
            interpreter._check_colour("#FF0000")
        except ValueError:
            self.fail("_check_colour raised ValueError unexpectedly!")

    def test_check_colour_invalid(self):
        interpreter = Interpreter("dummy_path")
        with self.assertRaises(ValueError):
            interpreter._check_colour("notacolour")

    def test_initializes_with_none_path_when_file_not_found(self):
        self.tearDown()
        interpreter = Interpreter("non_existent_file")
        self.assertEqual(interpreter.commands, [])
        self.assertIsNone(interpreter.file)

    def test_repr_empty(self):
        interpreter = Interpreter(None)
        self.assertEqual(repr(interpreter), "Interpreter with file: None and commands: []")
    
    def test_repr_with_file_and_commands(self):
        interpreter = Interpreter("dummy_path")
        interpreter.commands = [["square"], ["circle", "fill"]]
        self.assertEqual(repr(interpreter), "Interpreter with file: dummy_path and commands: [['square'], ['circle', 'fill']]")

    def tearDown(self):
        self.patcher.stop()

class TestInterpreterBaseCases(unittest.TestCase):

    def test_base_square(self):
        with unittest.mock.patch('interpreter.File.read', return_value="s"):
            self.testInterpret = Interpreter(None)
            self.assertEqual(self.testInterpret.commands, [["square"]])

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

    def test_base_newline(self):
        with unittest.mock.patch('interpreter.File.read', return_value = '\n'):
            self.testInterpret = Interpreter(None)
            self.assertEqual(self.testInterpret.commands, [["newLine"]])

    def test_base_all(self):
        with unittest.mock.patch('interpreter.File.read', return_value = "sct "):
            self.testInterpret = Interpreter(None)
            self.assertEqual(self.testInterpret.commands, [["square"],["circle"],["triangle"],["blank"]])
    
    def test_unkown_character_error(self):
        with unittest.mock.patch('interpreter.File.read', return_value = "sx"):
            self.assertRaises(ValueError, Interpreter, None)

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

    def test_unknown_modifier_error(self):
        with unittest.mock.patch('interpreter.File.read', return_value = "s[x]"):
            self.assertRaises(ValueError, Interpreter, None)
    
    def test_unknown_colour_error(self):
        with unittest.mock.patch('interpreter.File.read', return_value = "s[[unknowncolor]]"):
            self.assertRaises(ValueError, Interpreter, None)

    def test_too_many_colour_arguments_error(self):
        with unittest.mock.patch('interpreter.File.read', return_value = "s[[red,green,blue]]"):
            self.assertRaises(TypeError, Interpreter, None)


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

    def test_create_blank(self):
        blank = ["blank"]
        validBlank = Blank()
        x = self.factory.create_shape(blank)
        self.assertEqual(x, validBlank)

    def test_create_dashed_blank(self):
        blank = ["blank", "dashed"]
        validBlank = Blank(["dashed"])
        x = self.factory.create_shape(blank)
        self.assertEqual(x, validBlank)
    
    def test_create_new_line(self):
        newline = ["newLine"]
        validNewLine = NewLine()
        x = self.factory.create_shape(newline)
        self.assertEqual(x, validNewLine)

    def test_create_new_line_dashed(self):
        newline = ["newLine", "dashed"]
        validNewLine = NewLine(["dashed"])
        x = self.factory.create_shape(newline)
        self.assertEqual(x, validNewLine)

    
    def test_create_triangle_all_modifiers(self):
        triangle = ["triangle", "fill", "dashed", ["colour", "red","#FFFFFF"]]
        validTriangle = Triangle(["fill","dashed",["colour","red","#FFFFFF"]])
        x = self.factory.create_shape(triangle)
        self.assertEqual(x, validTriangle)

    def test_unknown_shape_error(self):
        unknownShape = ["pentagon"]
        self.assertRaises(ValueError, self.factory.create_shape, unknownShape)
    
    def test_wrong_command_format_error(self):
        notAList = "square"
        self.assertRaises(ValueError, self.factory.create_shape, notAList)

    def tearDown(self):
        del(self.factory)


class TestShapeBaseFunctions(unittest.TestCase):
    def test_shape_equality(self):
        shape1 = Shape()
        shape2 = Shape()
        self.assertEqual(shape1, shape2)

    def test_shape_equality_different_types(self):
        shape1 = Shape()
        shape2 = Square()
        self.assertNotEqual(shape1, shape2)

    def test_shape_equality_different_modifiers(self):
        shape1 = Square(["fill"])
        shape2 = Square(["dashed"])
        self.assertNotEqual(shape1, shape2)

    def test_shape_equality_same_modifiers_different_order(self):
        shape1 = Square(["fill", "dashed"])
        shape2 = Square(["dashed", "fill"])
        self.assertEqual(shape1, shape2)

    def test_shape_equality_same_modifiers_same_order(self):
        shape1 = Square(["fill", "dashed"])
        shape2 = Square(["fill", "dashed"])
        self.assertEqual(shape1, shape2)
    
    def test_shape_equality_same_modifiers_different_colour_arguments(self):
        shape1 = Square([["colour", "red"]])
        shape2 = Square([["colour", "blue"]])
        self.assertNotEqual(shape1, shape2)

class TestTurtleDrawsShapes(unittest.TestCase):
    def setUp(self):
        self.t = MagicMock()
        Shape.shapeWidth = 50
    
    def test_draw_not_implemented_error(self):
        shape = Shape()
        self.assertRaises(NotImplementedError, shape.draw, self.t)
        self.assertRaises(NotImplementedError, shape.draw_dashed, self.t)

    def test_draws_basic_square(self):
        sq = Square()
        sq.begin(self.t)
        forward_total = 0
        left_total = 0
        for name, arguments, _ in self.t.mock_calls:
            if name == 'forward':
                forward_total += arguments[0]
            elif name == 'left':
                left_total += arguments[0]
        
        self.assertEqual(forward_total, (Shape.shapeWidth * 4))
        self.assertEqual(left_total, 360)
            
    def test_draws_basic_circle(self):
        circle = Circle()
        circle.begin(self.t)
        forward_total = 0
        left_total = 0
        for name, arguments, _ in self.t.mock_calls:
            if name == 'forward':
                forward_total += arguments[0]
            if name == 'left':
                left_total += arguments[0]
        self.assertEqual(left_total, 360)#
        #If width is correct, circumference should be pi * width
        self.assertAlmostEqual(forward_total, Shape.shapeWidth * 3.14) #due to rounding, the number will not be exact
        
        

    def test_draws_basic_triangle(self):
        triangle = Triangle()
        triangle.begin(self.t)
        forward_total = 0
        left_total = 0
        for name, arguments, _ in self.t.mock_calls:
            if name == 'forward':
                forward_total += arguments[0]
            elif name == 'left':
                left_total += arguments[0]
        self.assertEqual(forward_total, (Shape.shapeWidth * 3))
        self.assertEqual(left_total, 360)

    def test_draws_filled_square(self):
        sq = Square(["fill"])
        sq.begin(self.t)
        begin_fill_called = any(name == 'begin_fill' for name, _, _ in self.t.mock_calls)
        end_fill_called = any(name == 'end_fill' for name, _, _ in self.t.mock_calls)
        self.assertTrue(begin_fill_called)
        self.assertTrue(end_fill_called)

    def test_draws_coloured_triangle(self):
        triangle = Triangle([["colour", "red","green"]])
        triangle.begin(self.t)
        pencolor_called = any(name == 'pencolor' for name, _, _ in self.t.mock_calls)
        fillcolor_called = any(name == 'fillcolor' for name, _, _ in self.t.mock_calls)
        self.assertTrue(pencolor_called)
        self.assertTrue(fillcolor_called)

    def mock_isdown(self):

        if self.pen_state:
            self.pen_state = False
        else: 
            self.pen_state = True
        return self.pen_state

    def test_draws_dashed_square(self):
        sq = Square(["dashed"])
        self.pen_state = True
        self.t.isdown.side_effect = self.mock_isdown   # Simulate pen up and down
        sq.begin(self.t)
        penup_called = any(name == 'penup' for name, _, _ in self.t.mock_calls)
        pendown_called = any(name == 'pendown' for name, _, _ in self.t.mock_calls)
        self.assertTrue(penup_called)
        self.assertTrue(pendown_called)
        del(self.pen_state)

    def test_draws_dashed_circle(self):
        circle = Circle(["dashed"])
        self.pen_state = True
        self.t.isdown.side_effect = self.mock_isdown   # Simulate pen up and down
        circle.begin(self.t)
        penup_called = any(name == 'penup' for name, _, _ in self.t.mock_calls)
        pendown_called = any(name == 'pendown' for name, _, _ in self.t.mock_calls)
        print(self.t.mock_calls)
        self.assertTrue(penup_called)
        self.assertTrue(pendown_called)
        del(self.pen_state)

    def test_draws_dashed_triangle(self):
        triangle = Triangle(["dashed"])
        self.pen_state = True
        self.t.isdown.side_effect = self.mock_isdown   # Simulate pen up and down
        triangle.begin(self.t)
        penup_called = any(name == 'penup' for name, _, _ in self.t.mock_calls)
        pendown_called = any(name == 'pendown' for name, _, _ in self.t.mock_calls)
        self.assertTrue(penup_called)
        self.assertTrue(pendown_called)
        del(self.pen_state)

    def test_draws_blank_shape(self):
        blank = Blank()
        blank.begin(self.t)
        # Blank shape should not call forward or left
        forward_called = any(name == 'forward' for name, _, _ in self.t.mock_calls)
        left_called = any(name == 'left' for name, _, _ in self.t.mock_calls)
        self.assertFalse(forward_called)
        self.assertFalse(left_called)

    def test_draws_dashed_blank_shape(self):
        blank = Blank(["dashed"])
        blank.begin(self.t)
        # Dashed Blank shape should not call forward or left
        forward_called = any(name == 'forward' for name, _, _ in self.t.mock_calls)
        left_called = any(name == 'left' for name, _, _ in self.t.mock_calls)
        self.assertFalse(forward_called)
        self.assertFalse(left_called)

    def test_draws_newline_shape(self):
        newline = NewLine()
        newline.begin(self.t)
        goto_called = any(name == 'goto' for name, _, _ in self.t.mock_calls)
        penup_called = any(name == 'penup' for name, _, _ in self.t.mock_calls)
        pendown_called = any(name == 'pendown' for name, _, _ in self.t.mock_calls)
        self.assertTrue(goto_called)
        self.assertTrue(penup_called)
        self.assertTrue(pendown_called)

    def test_draws_newline_dashed_shape(self):
        newline = NewLine(["dashed"])
        newline.begin(self.t)
        goto_called = any(name == 'goto' for name, _, _ in self.t.mock_calls)
        penup_called = any(name == 'penup' for name, _, _ in self.t.mock_calls)
        pendown_called = any(name == 'pendown' for name, _, _ in self.t.mock_calls)
        self.assertTrue(goto_called)
        self.assertTrue(penup_called)
        self.assertTrue(pendown_called)

    def tearDown(self):
        del(self.t)



class TestShapeRenderer(unittest.TestCase):
    def setUp(self):
        self.testShape = MagicMock()
        self.turtle = MagicMock()

    # Patch the Turtle class in shape_renderer to mock turtle graphics for testing Renderer initialization.
    @patch('shape_renderer.turtle.Turtle')
    def test_initializes_offcenter(self, mock_turtle):
        mock_turtle.return_value = self.turtle
        testRenderer = Renderer()
        mock_turtle.assert_called_once()
        self.turtle.goto.assert_called()
        self.turtle.pendown.assert_called_once()
        self.turtle.penup.assert_called_once()
        self.turtle.pensize.assert_called_once_with(testRenderer.thickness)
    
    @patch('shape_renderer.turtle.Turtle')
    def test_renders_shapes(self, mock_turtle):
        mock_turtle.return_value = self.turtle
        self.testShape.shapeWidth = 50
        self.turtle.xcor.return_value = 0
        testRenderer = Renderer()
        shapes = [self.testShape for _ in range(5)]
        testRenderer.render(shapes)
        self.assertEqual(self.testShape.begin.call_count, 5)
        self.turtle.forward.assert_called()
        
    @patch('shape_renderer.turtle.Turtle')    
    def test_goes_to_new_line_when_exceeding_limit(self, mock_turtle):
        mock_turtle.return_value = self.turtle
        self.testShape.shapeWidth = 300
        self.turtle.xcor.return_value = 200
        testRenderer = Renderer()
        testRenderer.xLimit = 400
        shapes = [self.testShape]
        testRenderer.render(shapes)
        self.turtle.goto.assert_called()
        args, _ = self.turtle.goto.call_args
        self.assertEqual(args[0], testRenderer.xLimit * -1)