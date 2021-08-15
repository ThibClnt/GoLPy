from vector2 import Vector2
import time


class Mask:

    def __init__(self):
        self.mask = dict()

    def add(self, key):
        if key in self.mask.keys():
            self.mask[key] += 1
        else:
            self.mask[key] = 1

    def remove(self, key):
        self.mask[key] -= 1
        if self.mask[key] == 0:
            del self.mask[key]

    def copy(self):
        mask = Mask()
        mask.mask = self.mask.copy()
        return mask

    def __setitem__(self, key, value):
        self.mask[key] = value

    def __getitem__(self, item):
        return self.mask[item]

    def __str__(self):
        return str(self.mask)

    def __contains__(self, item):
        return item in self.mask.keys()

    def __iter__(self):
        return iter(self.mask)

    def __next__(self):
        return next(self.mask)


class CellGrid:

    def __init__(self, canvas=None, cell_size=None, color=None, **kwargs):
        if canvas is None or cell_size is None or color is None:
            self.exists = False
            return

        self.exists = True
        self.active_cells = {}
        self.mask = set()
        self.mask_count = Mask()
        self.simulating = False
        # Speed in Hz
        self.speed = 10
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
                self.mask_count.add(around)

        if pos in self.mask:
            self.mask.remove(pos)
            self.mask_count.remove(pos)

    def __remove(self, pos: Vector2):
        cell = self.active_cells.pop(pos)
        self.canvas.delete(cell)

        for vec in self.__around():
            around = pos + vec
            if around in self.mask:
                if self.mask_count[around] == 1:
                    self.mask.remove(around)
                self.mask_count.remove(around)

            if self.is_alive(around):
                self.mask.add(pos)
                self.mask_count.add(pos)

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
        if self.speed / self.acceleration_factor < 60:
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
