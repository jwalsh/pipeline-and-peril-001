#!/usr/bin/env python3
"""Generate terminal screenshot as image using PIL"""

import io
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

# Create image
width = 800
height = 600
img = Image.new('RGB', (width, height), color='#0c0c0c')
draw = ImageDraw.Draw(img)

# Try to use a monospace font
try:
    font = ImageFont.truetype("/System/Library/Fonts/Monaco.dfont", 14)
    title_font = ImageFont.truetype("/System/Library/Fonts/Monaco.dfont", 18)
except:
    font = ImageFont.load_default()
    title_font = font

# Terminal content
y = 20
lines = [
    ("Pipeline & Peril - Rich Terminal Output", "#ff00ff"),
    ("", None),
    ("┌─────────────── Player Status ────────────────┐", "#888888"),
    ("│ Player  │ Score │ Resources │ Services      │", "#888888"),
    ("├─────────┼───────┼───────────┼───────────────┤", "#888888"),
    ("│ Alice   │  42   │     8     │ 3 running     │", "#00ff00"),
    ("│ Bob     │  38   │     6     │ 2 running     │", "#00ff00"),
    ("│ Charlie │  45   │     7     │ 4 running     │", "#ffff00"),
    ("│ Diana   │  41   │     9     │ 3 running     │", "#00ff00"),
    ("└─────────┴───────┴───────────┴───────────────┘", "#888888"),
    ("", None),
    ("Service Status:", "#ffffff"),
    ("  ✓ Auth Service: Running", "#00ff00"),
    ("  ✓ Database: Running", "#00ff00"),
    ("  ⚠ Cache: Degraded", "#ffff00"),
    ("  ✗ Queue: Failed", "#ff0000"),
    ("", None),
    ("Simulation Progress:", "#ffffff"),
    ("  Games completed: 15,623 / 20,000", "#00ff00"),
    ("  Analysis: ████████████████░░░░ 78%", "#0088ff"),
    ("  Report: ██████████░░░░░░░░░░ 42%", "#ffff00"),
    ("", None),
    (f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "#888888"),
]

for line, color in lines:
    if line:
        draw.text((20, y), line, fill=color or "#ffffff", font=font)
    y += 20

# Save
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"../../docs/images/terminal_demo_{timestamp}.png"
img.save(filename)
print(f"Terminal screenshot saved: {filename}")