import random
import math
import os
import time

# ======================
# Global config
# ======================
min_percent = 65.0
max_percent = 100.0
screen_offset = 40


# ======================
# Shoot system
# ======================
class Shoot:
    """
    A shoot grows in layers.
    Each layer can grow outward or upward.
    Same shoot_id = same branch identity.
    """
    def __init__(self, shoot_id, side):
        self.id = shoot_id
        self.side = side  # "left" or "right"
        self.layers = []  # list of {"out": int, "up": int}

    def grow(self):
        if not self.layers:
            self.layers.append({"out": 0, "up": 0})

        grow_outward = random.random() < 0.6
        if grow_outward:
            self.layers[-1]["out"] += 1
        else:
            self.layers.append({"out": 0, "up": 1})


# ======================
# Stem system
# ======================
class Stem:
    def __init__(self, prev=None):
        self.position = 0
        self.total_height = 0
        self.base_width = 0
        self.width = 0

        self.prev = prev
        self.next = None

        self.is_top = False
        self.is_ready = False

        self.shoots = {}  # shoot_id -> Shoot

    def add_shoot(self, shoot_id=None):
        if shoot_id is None:
            shoot_id = random.randint(1000, 9999)
        side = random.choice(["left", "right"])
        self.shoots[shoot_id] = Shoot(shoot_id, side)

    def update_state(self):
        if self.prev:
            self.total_height = self.prev.total_height
            self.position = self.prev.position + 1
            self.base_width = self.prev.base_width
            self.width = self.get_stem()
            self.is_top = self.position == self.total_height
            self.is_ready = True

    def get_stem(self):
        if self.total_height == 0:
            return self.base_width
        percent = min_percent + (max_percent - min_percent) * (
            1 - self.position / self.total_height
        )
        return max(1, int(percent / 100 * self.base_width))

    def render(self):
        if not self.is_ready:
            return

        prev = self.prev if self.prev else self
        offset = screen_offset + (prev.base_width - self.width) // 2
        print(" " * offset + "*" * self.width)

        # Render shoots attached to this stem
        for shoot in self.shoots.values():
            direction = -1 if shoot.side == "left" else 1
            for layer in shoot.layers:
                shoot_offset = offset + direction * layer["out"]
                print(" " * shoot_offset + "-")


# ======================
# Root
# ======================
class Root(Stem):
    def __init__(self, total_height=10, base_width=5):
        super().__init__(None)
        self.total_height = total_height
        self.base_width = base_width
        self.position = 0
        self.width = self.get_stem()
        self.is_ready = True


# ======================
# Tree Top
# ======================
class TreeTop:
    def __init__(self, base_width, total_height):
        self.base_width = base_width
        self.total_height = total_height

    def render(self):
        max_top_width = self.base_width * 5
        layers = max(2, int(math.log2(self.total_height + 1)))

        for layer in range(layers):
            progress = layer / layers
            expansion = int((max_top_width - self.base_width) *
                            (1 - (progress - 0.5) ** 2 * 4))
            size = max(self.base_width, self.base_width + expansion)
            offset = screen_offset + (self.base_width - size) // 2
            print(" " * offset + "#" * size)


# ======================
# Tree utilities
# ======================
def add_stem(prev_stem):
    new_stem = Stem(prev=prev_stem)
    prev_stem.next = new_stem
    new_stem.update_state()
    return new_stem


def increment_tree_height(root):
    root.total_height += 1
    root.base_width += 1

    current = root
    while current:
        current.update_state()
        current = current.next


def render_tree(root):
    # find top
    current = root
    while current.next:
        current = current.next

    os.system('cls' if os.name == 'nt' else 'clear')

    TreeTop(root.base_width, root.total_height).render()

    while current:
        current.render()
        current = current.prev


# ======================
# MAIN
# ======================
if __name__ == "__main__":
    random.seed()

    root = Root(total_height=10, base_width=5)
    current = root

    # initial vertical construction
    for _ in range(root.total_height):
        current = add_stem(current)

    # growth loop
    for step in range(12):
        # grow vertical
        last = root
        while last.next:
            last = last.next
        add_stem(last)
        increment_tree_height(root)

        # random shoot growth
        walker = root
        while walker:
            if random.random() < 0.3:
                if not walker.shoots:
                    walker.add_shoot()
                random.choice(list(walker.shoots.values())).grow()
            walker = walker.next

        render_tree(root)
        time.sleep(0.8)
