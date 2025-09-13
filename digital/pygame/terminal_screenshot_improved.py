#!/usr/bin/env python3
"""Generate improved terminal screenshot as image using PIL"""

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

# Create larger image with better resolution
width = 1200
height = 800
img = Image.new('RGB', (width, height), color='#1a1a2e')
draw = ImageDraw.Draw(img)

# Try to use a monospace font with better size
try:
    font = ImageFont.truetype("/System/Library/Fonts/Monaco.dfont", 20)
    title_font = ImageFont.truetype("/System/Library/Fonts/Monaco.dfont", 28)
    header_font = ImageFont.truetype("/System/Library/Fonts/Monaco.dfont", 24)
except:
    font = ImageFont.load_default()
    title_font = font
    header_font = font

# Terminal content with better formatting
y = 40
x_margin = 40

# Title
draw.text((x_margin, y), "Pipeline & Peril", fill="#00ff9f", font=title_font)
draw.text((x_margin + 300, y), "Rich Terminal Interface", fill="#888888", font=header_font)
y += 50

# Separator line
draw.line([(x_margin, y), (width - x_margin, y)], fill="#444444", width=2)
y += 30

# Player Status Table
draw.text((x_margin, y), "━━━ PLAYER STATUS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", fill="#00ff9f", font=header_font)
y += 40

# Table header
headers = ["Player", "Score", "Resources", "Services", "Status"]
x_positions = [x_margin, 200, 350, 520, 750]
for i, header in enumerate(headers):
    draw.text((x_positions[i], y), header, fill="#ffffff", font=font)
y += 35

# Table data
players = [
    ("Alice", "42", "8", "3 running", "Active", "#3498db"),
    ("Bob", "38", "6", "2 running", "Active", "#2ecc71"),
    ("Charlie", "45", "7", "4 running", "Leader", "#f1c40f"),
    ("Diana", "41", "9", "3 running", "Active", "#9b59b6")
]

for player_data in players:
    for i in range(5):
        color = player_data[5] if i == 0 else "#ffffff"
        draw.text((x_positions[i], y), player_data[i], fill=color, font=font)
    y += 30

y += 20

# Service Health Status
draw.text((x_margin, y), "━━━ SERVICE HEALTH ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", fill="#00ff9f", font=header_font)
y += 40

services = [
    ("✓", "Auth Service", "Operational", "#2ecc71"),
    ("✓", "Database", "Operational", "#2ecc71"),
    ("✓", "API Gateway", "Operational", "#2ecc71"),
    ("⚠", "Cache Layer", "Degraded (78% capacity)", "#f39c12"),
    ("⚠", "Message Queue", "High Latency (1.2s avg)", "#f39c12"),
    ("✗", "Search Service", "Failed - Circuit Breaker Open", "#e74c3c")
]

for icon, name, status, color in services:
    draw.text((x_margin, y), f"  {icon}", fill=color, font=font)
    draw.text((x_margin + 60, y), f"{name:20}", fill="#ffffff", font=font)
    draw.text((x_margin + 300, y), status, fill=color, font=font)
    y += 30

y += 20

# Simulation Metrics
draw.text((x_margin, y), "━━━ SIMULATION METRICS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", fill="#00ff9f", font=header_font)
y += 40

# Progress bars with better visualization
draw.text((x_margin, y), "Games Completed:", fill="#ffffff", font=font)
draw.text((x_margin + 250, y), "15,623 / 20,000", fill="#2ecc71", font=font)
y += 30

# Progress bar 1
bar_width = 500
bar_height = 20
progress = 0.78
draw.rectangle([(x_margin, y), (x_margin + bar_width, y + bar_height)], outline="#444444", width=2)
draw.rectangle([(x_margin, y), (x_margin + int(bar_width * progress), y + bar_height)], fill="#3498db")
draw.text((x_margin + bar_width + 20, y), "78%", fill="#3498db", font=font)
y += 35

draw.text((x_margin, y), "Analysis Progress:", fill="#ffffff", font=font)
y += 30

# Progress bar 2
progress = 0.92
draw.rectangle([(x_margin, y), (x_margin + bar_width, y + bar_height)], outline="#444444", width=2)
draw.rectangle([(x_margin, y), (x_margin + int(bar_width * progress), y + bar_height)], fill="#2ecc71")
draw.text((x_margin + bar_width + 20, y), "92%", fill="#2ecc71", font=font)
y += 35

draw.text((x_margin, y), "Report Generation:", fill="#ffffff", font=font)
y += 30

# Progress bar 3
progress = 0.42
draw.rectangle([(x_margin, y), (x_margin + bar_width, y + bar_height)], outline="#444444", width=2)
draw.rectangle([(x_margin, y), (x_margin + int(bar_width * progress), y + bar_height)], fill="#f39c12")
draw.text((x_margin + bar_width + 20, y), "42%", fill="#f39c12", font=font)

# Footer
y = height - 60
draw.line([(x_margin, y), (width - x_margin, y)], fill="#444444", width=2)
y += 20
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
draw.text((x_margin, y), f"Generated: {timestamp}", fill="#888888", font=font)
draw.text((width - 300, y), "Pipeline & Peril v1.0", fill="#888888", font=font)

# Save
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"../../docs/images/terminal_demo_{timestamp}.png"
img.save(filename, quality=95)
print(f"Improved terminal screenshot saved: {filename}")