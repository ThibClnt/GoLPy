"""
Copyright © 2021 Erkstone

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from math import sqrt, cos, sin, atan2


class Vector2:

    def __init__(self, x, y):
        """ Basic 2D Vector"""
        self.x = x
        self.y = y

    def clone(self):
        """Returns a vector with the same coordinates"""
        return Vector2(self.x, self.y)

    def magnitude(self):
        """ Returns the magnitude ( = 'length') of the vector """
        return sqrt(self.x * self.x + self.y * self.y)

    def squared_magnitude(self):
        """ Same as Vector2.magnitude() ** 2, but can save the sqrt if needed """
        return self.x * self.x + self.y * self.y

    def normalize(self):
        """ The vector has the same orientation, but set the magnitude to 1 """
        magnitude = self.magnitude()
        self.x = self.x / magnitude
        self.y = self.y / magnitude
        return Vector2(self.x, self.y)

    def translate(self, dx, dy):
        """ Simple translation """
        self.x += dx
        self.y += dy
        return Vector2(self.x, self.y)

    def rotate(self, angle, point=(0, 0), clockwise=False):
        """ Rotates the vector around the given point, by the specified angle in radians"""
        angle *= -1 if clockwise else 1
        x, y = self.x, self.y
        dx, dy = point[0], point[1]
        sn, cs = sin(angle), cos(angle)
        self.x = (x - dx) * cs - (y - dy) * sn + dx
        self.y = (x - dx) * sn + (y - dy) * cs + dy
        return Vector2(self.x, self.y)

    def angle(self, vector):
        """ Returns the angle with the vector (vector O if non specified) """
        return atan2(vector.y - self.y, vector.x - self.x)

    def tuple(self):
        return self.x, self.y

    def __add__(self, vector):
        """ When adding a vector - translation by a vector """
        return Vector2(self.x + vector.x, self.y + vector.y)

    def __iadd__(self, vector):
        return Vector2(self.x + vector.x, self.y + vector.y)

    def __sub__(self, vector):
        """ When subtracting a vector - translation by a the opposite vector """
        return Vector2(self.x - vector.x, self.y - vector.y)

    def __mul__(self, scalar):
        """ Multiply by a scalar """
        return Vector2(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):
        """ Multiply by a scalar by the right """
        return Vector2(self.x * scalar, self.y * scalar)

    def __imul__(self, other):
        return Vector2(self.x * other, self.y * other)

    def __truediv__(self, scalar):
        """ divide by a scalar """
        return Vector2(self.x / scalar, self.y / scalar)

    def __itruediv__(self, other):
        return Vector2(self.x / other, self.y / other)

    def __repr__(self):
        """ Very quick description of the object """
        return str(self)

    def __str__(self):
        """ When converting to a string object"""
        return f"{self.x : <6_.0f}{self.y : <6_.0f}"

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return hash(self) == hash(other)

    @staticmethod
    def cross_product(vector_a, vector_b):
        """ Returns the "cross product" of two vectors. This is actually the determinant of them """
        return vector_a.x * vector_b.y - vector_a.y * vector_b.x

    @staticmethod
    def dot(*args):
        """ Returns the dot product of two (or more) vectors """
        x_product, y_product = 1, 1
        for vector in args:
            x_product *= vector.x
            y_product *= vector.y
        return x_product + y_product
