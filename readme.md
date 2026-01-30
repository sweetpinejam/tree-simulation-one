# Wartorned Spourt Project (Simplified)

A procedural ASCII tree growth experiment written in Python and rendered directly in the terminal.

This project focuses on **organic growth**, **state propagation**, and **structural architecture**, while deliberately accepting the limitations of terminal-based rendering.

---

## Overview

The tree is built from vertically linked `Stem` objects that form a single trunk.  
Each stem calculates its width based on the total height of the tree, creating a natural tapering effect as the tree grows taller.

The project is intentionally minimal and exploratory, prioritizing clarity and architectural thinking over visual precision. The tree animates in real-time, growing one segment at a time with user interaction.

---

## Design Philosophy

- **Organic over perfect**  
  Irregularities and randomness are part of the design.

- **Terminal as a constraint**  
  The shell is treated as a limited medium, not something to fight against.

- **Architecture-first**  
  The internal model is designed to be reusable with richer renderers later.

- **Minimal abstractions**  
  No external libraries, frameworks, or rendering engines.

---

## Core Components

### Stem

Represents one vertical segment of the tree.

Responsibilities:
- Tracks its position in the tree hierarchy
- Computes its width based on total tree height (tapering effect)
- Knows whether it is the topmost segment
- Renders itself using ASCII characters (`*` for stem, `#` for fluffy top)

Stems are connected using a doubly-linked structure: `prev` (parent) and `next` (child).

**Attributes:**
- `position`: Vertical position in tree (0 = root, increases upward)
- `total_height`: Total height of the entire tree
- `base_width`: Width of the root stem
- `width`: Computed width for this stem based on position
- `prev`: Reference to parent stem (or None if root)
- `next`: Reference to child stem (or None if topmost)
- `is_top`: Boolean flag indicating if this is the topmost stem
- `is_ready`: Boolean flag indicating if the stem has been initialized

### Root

A specialized `Stem` subclass that initializes the tree with base parameters.

- Sets `total_height`, `base_width`, and `position`
- Forms the foundation from which all other stems grow
- Starts in a ready state

### Growth Mechanics

The tree grows by:
1. Adding a new `Stem` to the topmost segment
2. Incrementing the tree's `total_height`
3. Recalculating all stems' widths (they narrow as total height increases)
4. Re-rendering the entire tree from top to bottom

This creates an animation where the tree gets taller while existing segments become thinner.

---

## Usage

Run the program:
```bash
python main.py
```

The tree will:
1. Initialize with a 20-segment trunk
2. Display the initial tree with a fluffy cloud top
3. Wait for user input before each growth cycle
4. Add a new segment and redraw (repeats 5 times)

Press **Enter** to grow the tree at each prompt.

---

## Technical Details

### Width Calculation

Width tapers from 100% at the root to 65% at the top:
```
percent = 65 + (100 - 65) * (1 - position / total_height)
width = percent / 100 * base_width
```

### Rendering

- **Root to current stem**: `*` characters
- **Topmost segment**: Fluffy `#` cloud with random variation
- **Centering**: ASCII art is centered on screen using `screen_offset`

### State Propagation

The `update_state()` method propagates tree metadata down the chain:
- Each stem copies `total_height` and `base_width` from its parent
- Position increments by 1 at each level
- The `is_top` flag is recalculated when tree height changes

---

## File Structure

```
tree-simulation-one/
├── main.py           # Main program with Stem, Root, and growth logic
├── readme.md         # This file
├── requirements.txt  # Python dependencies
└── .python-version   # Python version specification
```

---

## Dependencies

None! The project uses only Python standard library:
- `random` - For organic shape variations
- `math` - For logarithmic layer calculations
- `os` - For screen clearing between frames

---

## Limitations & Future Ideas

**Current Limitations:**
- Single vertical trunk (no branching)
- ASCII-only rendering
- Limited animation speed (terminal refresh rate)

**Possible Extensions:**
- Branching logic to create multiple stems per node
- 2D coordinate system for more complex shapes
- File export to SVG or other formats
- Interactive resizing or parameter tuning
- Color support via ANSI codes

---

## License

Experimental/educational project. Free to use and modify.

