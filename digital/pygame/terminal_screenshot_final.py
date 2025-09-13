#!/usr/bin/env python3
"""Generate final terminal screenshot incorporating UX feedback"""

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

# Create larger image with better resolution
width = 1400
height = 900
# Use lighter background for better contrast
img = Image.new('RGB', (width, height), color='#2d3748')
draw = ImageDraw.Draw(img)

# Try to use a monospace font with better size
try:
    font = ImageFont.truetype("/System/Library/Fonts/Monaco.dfont", 18)
    title_font = ImageFont.truetype("/System/Library/Fonts/Monaco.dfont", 32)
    header_font = ImageFont.truetype("/System/Library/Fonts/Monaco.dfont", 22)
    small_font = ImageFont.truetype("/System/Library/Fonts/Monaco.dfont", 16)
except:
    font = ImageFont.load_default()
    title_font = font
    header_font = font
    small_font = font

y = 40
x_margin = 50

# Main Title with value proposition
draw.text((x_margin, y), "Pipeline & Peril", fill="#63b3ed", font=title_font)
draw.text((x_margin + 350, y + 5), "Learn Distributed Systems Through Play", fill="#a0aec0", font=header_font)
y += 60

# Tutorial hint for new users
draw.rectangle([(x_margin - 5, y), (width - x_margin + 5, y + 35)], fill='#374151')
draw.text((x_margin, y + 8), "💡 Tutorial Mode Active: Press H for help • Tab to switch views • Space to pause", 
          fill="#fbbf24", font=small_font)
y += 50

# PLAYER STATUS - Better visual hierarchy
draw.text((x_margin, y), "▶ PLAYER STATUS", fill="#ffffff", font=header_font)
y += 35

# Headers with better spacing
headers = ["Player", "Score", "Resources", "Services", "Status", "Trend"]
x_positions = [x_margin, 200, 320, 480, 650, 800]
for i, header in enumerate(headers):
    draw.text((x_positions[i], y), header, fill="#cbd5e0", font=font)
y += 30

# Horizontal line for separation
draw.line([(x_margin, y), (850, y)], fill="#4a5568", width=1)
y += 10

# Player data with consistent color scheme
players = [
    ("Charlie", "45", "7", "4 running", "Leader 👑", "↑ +3", "#10b981"),  # Green for leader
    ("Alice", "42", "8", "3 running", "Active", "↑ +1", "#3b82f6"),     # Blue
    ("Diana", "41", "9", "3 running", "Active", "→ 0", "#8b5cf6"),      # Purple
    ("Bob", "38", "6", "2 running", "At Risk", "↓ -2", "#ef4444"),      # Red for at risk
]

for player_data in players:
    color = player_data[6]
    # Add status indicator
    if "Leader" in player_data[4]:
        draw.rectangle([(x_margin - 10, y - 2), (x_margin - 5, y + 18)], fill=color)
    
    for i in range(6):
        text_color = color if i == 0 else "#ffffff" if i < 4 else color if i == 5 else "#a0aec0"
        draw.text((x_positions[i], y), player_data[i], fill=text_color, font=font)
    y += 28

y += 30

# SERVICE HEALTH - Improved with criticality indicators
draw.text((x_margin, y), "▶ SERVICE HEALTH", fill="#ffffff", font=header_font)
draw.text((x_margin + 250, y + 2), "(Critical Path Services ⚠)", fill="#fbbf24", font=small_font)
y += 35

# Service categories for better organization
service_categories = [
    ("Core Infrastructure", [
        ("✓", "Auth Service", "Operational", "99.9% uptime", "#10b981", False),
        ("✓", "Database (Primary)", "Operational", "42ms latency", "#10b981", True),
        ("✓", "API Gateway", "Operational", "1.2k req/s", "#10b981", True),
    ]),
    ("Supporting Services", [
        ("⚠", "Cache Layer", "Degraded", "78% capacity", "#f59e0b", False),
        ("⚠", "Message Queue", "High Latency", "1.2s avg", "#f59e0b", True),
        ("✓", "Storage Service", "Operational", "82% used", "#10b981", False),
    ]),
    ("Monitoring & Recovery", [
        ("✗", "Search Service", "Failed", "Circuit Open", "#ef4444", False),
        ("✓", "Health Monitor", "Operational", "All checks passing", "#10b981", False),
    ])
]

for category_name, services in service_categories:
    draw.text((x_margin + 20, y), category_name, fill="#9ca3af", font=small_font)
    y += 25
    
    for icon, name, status, metric, color, is_critical in services:
        # Critical path indicator
        if is_critical:
            draw.text((x_margin, y), "→", fill="#fbbf24", font=font)
        
        draw.text((x_margin + 30, y), icon, fill=color, font=font)
        draw.text((x_margin + 70, y), f"{name:20}", fill="#ffffff", font=font)
        draw.text((x_margin + 350, y), status, fill=color, font=font)
        draw.text((x_margin + 550, y), metric, fill="#9ca3af", font=small_font)
        y += 25
    y += 10

y += 20

# LEARNING PROGRESS - New section based on product feedback
draw.text((x_margin, y), "▶ LEARNING PROGRESS", fill="#ffffff", font=header_font)
y += 35

# Progress metrics
learning_metrics = [
    ("Concepts Mastered:", "12 / 15", 0.80, "#10b981"),
    ("Scenarios Completed:", "8 / 10", 0.80, "#3b82f6"),
    ("Achievement Points:", "420 / 500", 0.84, "#8b5cf6"),
]

bar_width = 400
bar_height = 22

for metric_name, metric_value, progress, color in learning_metrics:
    draw.text((x_margin, y), metric_name, fill="#ffffff", font=font)
    draw.text((x_margin + 250, y), metric_value, fill=color, font=font)
    
    # Progress bar
    bar_y = y
    draw.rectangle([(x_margin + 400, bar_y), (x_margin + 400 + bar_width, bar_y + bar_height)], 
                   outline="#4a5568", width=2)
    draw.rectangle([(x_margin + 400, bar_y), (x_margin + 400 + int(bar_width * progress), bar_y + bar_height)], 
                   fill=color)
    draw.text((x_margin + 400 + bar_width + 15, y), f"{int(progress*100)}%", fill=color, font=font)
    y += 35

# Business metrics section
y += 20
draw.text((x_margin, y), "▶ SESSION METRICS", fill="#ffffff", font=header_font)
y += 35

metrics_data = [
    ("Session Duration:", "24:31", "#10b981"),
    ("Actions Per Minute:", "3.2", "#3b82f6"),
    ("Error Recovery Rate:", "87%", "#10b981"),
    ("Learning Velocity:", "+15%", "#fbbf24"),
]

for i, (metric, value, color) in enumerate(metrics_data):
    x_offset = (i % 2) * 350
    y_offset = (i // 2) * 30
    draw.text((x_margin + x_offset, y + y_offset), metric, fill="#cbd5e0", font=font)
    draw.text((x_margin + x_offset + 200, y + y_offset), value, fill=color, font=font)

# Footer with better information
y = height - 80
draw.line([(x_margin, y), (width - x_margin, y)], fill="#4a5568", width=2)
y += 15

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
draw.text((x_margin, y), f"Session: {timestamp}", fill="#9ca3af", font=small_font)
draw.text((x_margin + 400, y), "15,623 games analyzed", fill="#9ca3af", font=small_font)
draw.text((width - 350, y), "Pipeline & Peril v2.0", fill="#9ca3af", font=small_font)

y += 25
draw.text((x_margin, y), "Next: Complete 'Cascading Failure Recovery' scenario to unlock advanced monitoring", 
          fill="#10b981", font=small_font)

# Save
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"../../docs/images/terminal_demo_final_{timestamp}.png"
img.save(filename, quality=95)
print(f"Final terminal screenshot saved: {filename}")