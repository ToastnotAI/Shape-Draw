Expected format for files:

    shape[modifiers[colours]]

Colours have to be in double brackets even with no other modifiers (shape[[colours]])
If square brackets are omitted just the outline will be drawn.


Accepted values for shape are:
s - Square
t - Triangle
c- Circle
' ' - Empty space 
'\n' - New line
Capitilization will fill the shape in

modifiers can be:
d - dashed

colours are expected in the format:
[[border colour, fill colour]]
And accepts any colours turtle accepts

Example usage:
sS[d]c[d[black,green]]T[#FF0000,red]

