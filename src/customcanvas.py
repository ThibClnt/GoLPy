"""
Copyright © 2021 Erkstone

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from tkinter import Canvas
from vector2 import Vector2
from rect import Rect


class CustomCanvas(Canvas):

    def __init__(self, parent, zoom_magnitude=1.3, **kwargs):
        """
            Tkinter Canvas with zoom and pan supported for simple geometry.
        Does not support zoom for images and texts.

        You can experiments some cut off when moving fast a small item due to tkinter Canvas refresh system.
        You can fix that as described here : https://stackoverflow.com/a/47000930.

        Please don't use tkinter.Canvas' scan_mark(), scan_dragto() and scale() functions
        but CustomCanvas pan_begin(), pan() and zoom().

        :param parent: tkinter parent Widget
        :param zoom_magnitude: zoom factor when zooming in or out
        :param kwargs: tkinter Canvas kwargs
        """
        self.view = Rect(Vector2(0, 0), Vector2(0, 0))
        self.zoom_magnitude = zoom_magnitude
        self.mark = Vector2(0, 0)

        Canvas.__init__(self, parent, **kwargs)

        self.__bind_controls()

    def __bind_controls(self):
        # Bind pans
        self.bind("<ButtonPress-2>", self.pan_begin)
        self.bind("<B2-Motion>", self.pan)

        # Bind zoom for Windows, MacOS and Linux
        self.bind("<MouseWheel>", self.zoom)
        self.bind("<Button-4>", self.zoom)
        self.bind("<Button-5>", self.zoom)
        self.bind("<Configure>", lambda event: self._geometry_update())

    def _geometry_update(self):
        """
        Called when resizing or using tkinter's pack, grid or place methods.
        """
        super().update()
        self.view.scale.x = self.winfo_width()
        self.view.scale.y = self.winfo_height()

    def pan_begin(self, event):
        """
        Mark the beginning point of the drag action
        :param event: tkinter Event
        """
        # Event coordinates in scene coordinates (for a delta, so we don't need to take care of view.position)
        self.mark.x = event.x
        self.mark.y = event.y

    def pan(self, event):
        """
        Follow the drag action and pan the view
        :param event: tkinter Event
        """
        # Compute of the pan vector
        pan_vector = self.mark - Vector2(event.x, event.y)
        self.view.position.x += pan_vector.x * self.view.scale.x / self.winfo_width()
        self.view.position.y += pan_vector.y * self.view.scale.y / self.winfo_height()

        # Move objects on Canvas
        self.move("all", -pan_vector.x, -pan_vector.y)
        self.mark.x = event.x
        self.mark.y = event.y

    def zoom(self, event):
        """
        Allow zooming in the Canvas by rescaling and redrawing all the items.
        :param event: tkinter Event
        """

        # Check if we are zooming in or out
        if event.delta >= 0:
            f = self.zoom_magnitude
        else:
            f = 1 / self.zoom_magnitude

        # Update the view
        x = self.view.position.x + event.x / self.winfo_width() * self.view.scale.x
        y = self.view.position.y + event.y / self.winfo_height() * self.view.scale.y
        dx = (x - self.view.position.x) / f
        dy = (y - self.view.position.y) / f
        self.view.position = Vector2(x - dx, y - dy)
        self.view.scale /= f

        # Rescale the items
        self.scale("all", event.x, event.y, f, f)

    def to_scene(self, p: Vector2) -> Vector2:
        """
        Convert p to scene coordinates
        
        :param p: Canvas coordinates
        :return: p converted to scene coordinates
        """
        x = self.view.position.x + p.x * self.view.scale.x / self.winfo_width()
        y = self.view.position.y + p.y * self.view.scale.y / self.winfo_height()
        to_scene = Vector2(x, y)
        return to_scene

    def to_draw(self, p: Vector2) -> Vector2:
        """
        Convert p to Canvas coordinates for drawing functions

        :param p: Scene coordinates
        :return: p converted to Canvas coordinates
        """
        x = (p.x - self.view.position.x) * self.winfo_width() / self.view.scale.x
        y = (p.y - self.view.position.y) * self.winfo_height() / self.view.scale.y
        to_draw = Vector2(x, y)
        return to_draw
