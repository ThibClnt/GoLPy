"""
Copyright © 2021 Erkstone

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from tkinter import Tk, Button, Frame, LabelFrame
from settings import *
from centralwidget import *
from PIL import ImageTk, Image


class Window(Tk):

    def __init__(self):
        """
        Main Window of the app, with only a constructor
        """
        Tk.__init__(self)
        self.title("Golpy")
        self.geometry(f"{WIDTH}x{HEIGHT}+{WINDOW_X}+{WINDOW_Y}")

        # Create the central widget and make it expand
        self.central = CentralWidget(self,
                                     bg=BACKGROUND_COLOR,
                                     highlightthickness=0,
                                     grid_color=GRID_COLOR,
                                     cell_size=CELL_SIZE,
                                     maxsize=Vector2(MAX_X, MAX_Y),
                                     min_zoom=ZOOM_MIN,
                                     max_zoom=ZOOM_MAX,
                                     zoom_magnitude=WHEEL_FACTOR)
        self.cell_grid = CellGrid(self.central, CELL_SIZE, ACTIVE_CELL_COLOR)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(2, weight=1)
        self.central.grid(row=2, column=2, sticky='nsew')

        # Create the buttons
        button_frame = Frame(self, padx=5, pady=5)
        button_frame.columnconfigure(0, weight=1)

        # Load the start/stop image
        load_play_image = Image.open("images/play.png").resize((32, 32))
        render_play_image = ImageTk.PhotoImage(load_play_image)
        play_button = Button(button_frame,
                             image=render_play_image,
                             text="Play/Stop",
                             compound="left",
                             command=self.cell_grid.start_stop)
        play_button.image = render_play_image
        play_button.grid(row=0, column=0, sticky="nsew", padx=5)

        # Buttons for speed control in its own Frame
        speed_frame = LabelFrame(button_frame, text="Speed control")
        speed_frame.columnconfigure(0, weight=1)
        speed_frame.columnconfigure(1, weight=1)

        Button(speed_frame, text="  +  ", command=self.cell_grid.speed_up).grid(row=0, column=0, sticky="nsew", padx=2)
        Button(speed_frame, text="  -  ", command=self.cell_grid.speed_down).grid(row=0, column=1, sticky="nsew", padx=2)
        speed_frame.grid(row=0, column=1, padx=5, sticky="ns")

        button_frame.grid(row=1, column=2, sticky='nsew')

        # Bind to mouse left click on the central widget to add or remove living cells
        self.central.bind("<Button-1>", self.central.change_state)
