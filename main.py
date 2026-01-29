# Simplified version of the Wartorned Spourt Project
import random
import math
import os

min_percent = 65.0
max_percent = 100.0
screen_offset = 40

class Stem:
    def __init__(self,prev=None):
        self.position = 0 # might change
        self.total_height = 0 # for updating when theres complete connection
        self.base_width = 0
        self.width = 0 # for update when theres complete connection
        self.prev = prev # core attribute to be updated
        self.next = None # core attribute to be updated
        self.is_top = False
        self.is_ready = False

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
        percent = min_percent + (max_percent - min_percent) * (1 - float(self.position) / self.total_height)
        stem_width = int(percent / 100 * self.base_width)
        return stem_width
    
    def get_top(self):
        # Render fluffy cloud top with random shape variation on both sides
                max_top_width = self.base_width + self.base_width * 4
                layers = max(math.log2(self.total_height), self.total_height // 2)
                
                for layer in range(layers):
                    # Create fluffier cloud with smoother expansion curve + randomness
                    progress = layer / layers
                    base_expansion = int((max_top_width - self.base_width) * (1 - (progress - 0.5) ** 2 * 4))
                    # Add random variation to make cloud more organic
                    random_variation = random.randint(-self.base_width // 3, self.base_width // 3)
                    expansion = base_expansion + random_variation
                    size = self.base_width + expansion
                    
                    # Add random offset to left side as well
                    left_offset = random.randint(-2, 2)
                    offset = screen_offset + (self.base_width - size) // 2 + left_offset
                    return offset, size

    def render(self):
        if self.is_ready:
            # Render tree top if this is the topmost stem
            if self.is_top:
    
                    offset, size = self.get_top()
                    print(" " * offset + "#" * size)
            
            prev = self.prev if self.prev else self
            offset = screen_offset + (prev.base_width - self.width) // 2
            print(" " * offset + "*" * self.width)

        else:
            print("The tree isn't initialized yet.")

class Root(Stem): # for the lowest stem. the role is to initiate the core values and link that to the linked stems
    def __init__(self, prev=None, total_height=10, base_width=5, position=0):
        super().__init__(prev)
        self.total_height = total_height
        self.base_width = base_width
        self.position = position
        self.width = self.get_stem()
        self.is_ready = True

# functions to manage tree growth
def add_stem(prev_stem):
    new_stem = Stem(prev=prev_stem)
    prev_stem.next = new_stem
    new_stem.update_state()
    return new_stem

def increment_tree_height(root_stem):
    """Increment total_height for the entire tree and recalculate all stems"""
    root_stem.total_height += 1
    root_stem.base_width += 1  # Optionally adjust base width if desired
    current_stem = root_stem
    while current_stem:
        current_stem.update_state()
        current_stem = current_stem.next

def remove_stem(stem):
    if stem.prev:
        stem.prev.next = None
    stem.prev = None
    return stem

def prepare_tree(root_stem):
    current_stem = root_stem
    while current_stem:
        current_stem.update_state()
        current_stem = current_stem.next

if __name__ == "__main__":
    # Base tree parameters
    total_height = 20
    base_width = 5
    root = Root(position=0, total_height=total_height, base_width=base_width)
    current_stem = root

    for pos in range(1, total_height + 1):
        new_stem = Stem(prev=current_stem)
        current_stem.next = new_stem
        current_stem = new_stem # Done base construction of the tree

    # Render the tree from last to first
    current_stem = current_stem  # This is now the last stem
    while current_stem:
        current_stem.render()
        current_stem = current_stem.prev  # Move to the previous stem

    # Try to reuse the objects to make the tree actually grow
    for growth in range(20):
        os.system('cls' if os.name == 'nt' else 'clear')
        # Find the last stem
        last_stem = root
        while last_stem and last_stem.next:
            last_stem = last_stem.next
        
        # Add a new stem and increment the tree height
        new_stem = add_stem(last_stem)
        increment_tree_height(root)

        # Render the tree again
        current_stem = new_stem
        while current_stem:
            current_stem.render()
            current_stem = current_stem.prev

        input("Press Enter to grow the tree further...")
