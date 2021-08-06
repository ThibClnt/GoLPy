"""
Copyright © 2021 Erkstone

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from customcanvas import *
from cell_grid import CellGrid


class CentralWidget(CustomCanvas):

    def __init__(self, parent=None, **kwargs):
        """
        Central Widget of a game of life app.
        Inherit from CustomCanvas class to create a tkinter Canvas with zoom and pan.

        :param parent: tkinter parent of the Widget
        :param kwargs:
            -cell_size
            -grid_color
            -maxsize
            -can_move
            -can_zoom
            -max_zoom
            -min_zoom
            -CustomCanvas kwargs
        """
        self.parent = parent
        self.cell_size = kwargs.pop("cell_size", 50)
        self.grid_color = kwargs.pop("grid_color", "black")
        self.maxsize = kwargs.pop("maxsize", None)
        self.can_move = kwargs.pop("can_move", True)
        self.can_zoom = kwargs.pop("can_zoom", True)
        self.max_zoom = kwargs.pop("max_zoom", 10)
        self.min_zoom = kwargs.pop("min_zoom", 0.1)
        self.background = kwargs.pop("background", kwargs.pop("bg", "white"))

        self.cell_grid: CellGrid = CellGrid()
        self.zooming_scale = 1

        CustomCanvas.__init__(self, parent, bg=self.background, **kwargs)

    def draw_grid(self):
        """
        Draw the grid for the game of life
        """
        self.delete("grid")
        # Draw vertical lines
        for x in range(0, self.maxsize.x, self.cell_size):
            self.create_line(x, -self.maxsize.y, x, self.maxsize.y, fill=self.grid_color, width=0, tags="grid")
            self.create_line(-x, -self.maxsize.y, -x, self.maxsize.y, fill=self.grid_color, width=0, tags="grid")

        # Draw horizontal lines
        for y in range(0, self.maxsize.y, self.cell_size):
            self.create_line(-self.maxsize.x, y, self.maxsize.x, y, fill=self.grid_color, width=0, tags="grid")
            self.create_line(-self.maxsize.x, -y, self.maxsize.x, -y, fill=self.grid_color, width=0, tags="grid")

    def pan(self, event):
        """
        Override the Custom Canvas pan to make sure the user does not pan too far

        :param event: tkinter Event
        """

        # Make sure we don't go too far (out maxsize) then pan
        rect = self.view.rect
        dx = self.mark.x - event.x * self.view.scale.x / self.winfo_width()
        dy = self.mark.y - event.y * self.view.scale.y / self.winfo_height()
        if (self.can_move and not (
                rect[0] + dx < -self.maxsize.x or
                rect[1] + dy < -self.maxsize.y or
                rect[2] + dx > self.maxsize.x or
                rect[3] + dy > self.maxsize.y
        )):
            super(CentralWidget, self).pan(event)
        self.mark = Vector2(event.x, event.y)

    def zoom(self, event):
        """
        Override the Custom Canvas zoom to make sure the user does not zoom out too far

        :param event: tkinter Event
        """
        # Check if we are zooming in or out
        if event.delta >= 0:
            f = self.zoom_magnitude
        else:
            f = 1 / self.zoom_magnitude

        # Forecast the potential future view rectangle
        x = self.view.position.x + event.x / self.winfo_width() * self.view.scale.x
        y = self.view.position.y + event.y / self.winfo_height() * self.view.scale.y
        dx = (x - self.view.position.x) / f
        dy = (y - self.view.position.y) / f

        rect = Rect(
            Vector2(x - dx, y - dy),
            self.view.scale / f
        ).rect

        # Don't zoom if we are zooming out too far
        if (self.can_zoom and not (
                rect[0] < -self.maxsize.x or
                rect[1] < -self.maxsize.y or
                rect[2] > self.maxsize.x or
                rect[3] > self.maxsize.y or
                self.zooming_scale * f > self.max_zoom or
                self.zooming_scale * f < self.min_zoom
        )):
            super(CentralWidget, self).zoom(event)
            if f < 1 and self.zooming_scale > 0.2 and self.zooming_scale * f < 0.2:
                self.itemconfigure("grid", state="hidden")

            if f > 1 and self.zooming_scale < 0.2 and self.zooming_scale * f > 0.2:
                self.itemconfigure("grid", state="normal")

            self.zooming_scale *= f

    def _geometry_update(self):
        """
        Update the geometry (size informations) and redraw the grid when configuring the canvas by resizing the window
        or calling the tkinter pack, grid or place method.
        """
        super(CentralWidget, self)._geometry_update()
        if self.maxsize is None:
            self.maxsize = Vector2(self.winfo_width(), self.winfo_height())
        self.draw_grid()

    def set_cell_grid(self, cell_grid: CellGrid):
        """
        :param cell_grid: handle the simulation and grid state storage
        """
        if self.cell_grid.exists:
            return
        else:
            self.cell_grid = cell_grid

    def change_state(self, event):
        """
        Snap event to grid then call the cell_grid.change_state function
        :param event: tkinter Event
        """
        # Convert the event into scene coordinates with a Vector2
        e = self.to_scene(Vector2(event.x, event.y))

        # Snap event to grid
        pos = Vector2(
            (e.x - e.x % self.cell_size) // self.cell_size,
            (e.y - e.y % self.cell_size) // self.cell_size
        )
        self.cell_grid.change_state(pos)
