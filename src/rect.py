"""
Copyright © 2021 Erkstone

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from vector2 import Vector2


class Rect:

    def __init__(self, position: Vector2, scale: Vector2):
        """
        Abstract a rectangle with its top left corner's position and its size

        :param position: Vector2 for top left corner's position
        :param scale: Vector2 for size
        """
        self.position = position
        self.scale = scale

    @property
    def rect(self):
        """
        :return: A tuple with the coordinates of the four corners of the object
        """
        return (
            self.position.x,
            self.position.y,
            self.position.x + self.scale.x,
            self.position.y + self.scale.y
        )
