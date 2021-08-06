from vector2 import Vector2
import time


class CellGrid:

    def __init__(self, canvas=None, cell_size=None, color=None, **kwargs):
        if canvas is None or cell_size is None or color is None:
            self.exists = False
            return

        self.exists = True
        self.active_cells = {}
        self.mask = set()
        self.simulating = False
        # Speed in Hz
        self.speed = 2
        self.acceleration_factor = kwargs.pop("acceleration_factor", 1.3)

        self.canvas = canvas
        self.canvas.set_cell_grid(self)
        self.cell_size = cell_size
        self.color = color

    def is_alive(self, pos: Vector2):
        return pos in self.active_cells.keys()

    def change_state(self, pos: Vector2):
        if self.simulating:
            return

        if not(self.is_alive(pos)):
            self.__add(pos)
        else:
            self.__remove(pos)

    def __add(self, pos: Vector2):
        top_left = self.canvas.to_draw(Vector2(
            pos.x * self.cell_size,
            pos.y * self.cell_size
        )).tuple()
        bottom_right = self.canvas.to_draw(Vector2(
            (pos.x + 1) * self.cell_size,
            (pos.y + 1) * self.cell_size
        )).tuple()

        self.active_cells[pos] = self.canvas.create_rectangle(
            *top_left, *bottom_right,
            fill=self.color, width=0
        )

        self.canvas.tag_raise("grid")

        for vec in self.__around():
            around = pos + vec
            if not self.is_alive(around):
                self.mask.add(around)

        if pos in self.mask:
            self.mask.remove(pos)

    def __remove(self, pos: Vector2):
        cell = self.active_cells.pop(pos)

        # Remove neighbours from mask
        for vec in self.__around():
            around = pos + vec
            if around in self.mask:
                self.mask.remove(around)

        # Regenerate the mask
        for vec in self.__around():
            around = pos + vec
            if self.is_alive(around):
                for vec2 in self.__around():
                    around2 = vec2 + around
                    if not self.is_alive(around2):
                        self.mask.add(around2)
            around = pos + vec * 2
            if self.is_alive(around):
                for vec2 in self.__around():
                    around2 = vec2 + around
                    if not self.is_alive(around2):
                        self.mask.add(around2)

        self.canvas.delete(cell)

    def start_stop(self):
        self.simulating = not self.simulating
        if self.simulating:
            self.loop()

    def loop(self):
        refresh = 1000 / self.speed

        if self.simulating:
            top = time.time_ns() // 1000000
            self.__update()
            self.canvas.after(int(refresh - time.time_ns() // 1000000 + top), self.loop)

    def __update(self):
        tmp_active, tmp_mask = self.active_cells.copy(), self.mask.copy()

        for dead_cell in tmp_mask:
            if self.count_around(dead_cell, tmp_active) == 3:
                self.__add(dead_cell)

        for active_cell in tmp_active.keys():
            count = self.count_around(active_cell, tmp_active)
            if count < 2 or count > 3:
                self.__remove(active_cell)

    def speed_up(self):
        if self.speed / self.acceleration_factor < 8:
            self.speed *= self.acceleration_factor

    def speed_down(self):
        self.speed /= self.acceleration_factor

    @staticmethod
    def __around():
        return (
            Vector2(-1, -1),
            Vector2(0, -1),
            Vector2(1, -1),
            Vector2(-1, 0),
            Vector2(1, 0),
            Vector2(-1, 1),
            Vector2(0, 1),
            Vector2(1, 1)
        )

    def count_around(self, pos: Vector2, active_list):
        around = self.__around()
        count = 0
        for vec in around:
            vec2 = pos + vec
            if vec2 in active_list.keys():
                count += 1

        return count
