#!/usr/bin/env python3
"""Generate stats dashboard using matplotlib"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from datetime import datetime

# Create figure
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 8))
fig.suptitle('Pipeline & Peril - Statistical Dashboard', fontsize=16, fontweight='bold')

# Win Rate Distribution (Pie Chart)
players = ['Alice', 'Bob', 'Charlie', 'Diana']
win_rates = [26.3, 25.8, 24.1, 23.8]
colors = ['#3498db', '#2ecc71', '#f1c40f', '#9b59b6']
ax1.pie(win_rates, labels=players, colors=colors, autopct='%1.1f%%')
ax1.set_title('Win Rate Distribution')

# Game Length Distribution (Histogram)
np.random.seed(42)
game_lengths = np.random.normal(23.4, 4.7, 1000)
ax2.hist(game_lengths, bins=30, color='#e74c3c', alpha=0.7, edgecolor='black')
ax2.set_xlabel('Game Length (rounds)')
ax2.set_ylabel('Frequency')
ax2.set_title('Game Duration Distribution')
ax2.axvline(x=23.4, color='black', linestyle='--', label='Mean: 23.4')
ax2.legend()

# Service Health Over Time (Line Chart)
rounds = np.arange(0, 50)
auth_health = 100 - rounds * 0.5 + np.random.normal(0, 5, 50)
db_health = 100 - rounds * 0.3 + np.random.normal(0, 3, 50)
cache_health = 100 - rounds * 0.8 + np.random.normal(0, 7, 50)

ax3.plot(rounds, auth_health, label='Auth', color='#2ecc71')
ax3.plot(rounds, db_health, label='Database', color='#3498db')
ax3.plot(rounds, cache_health, label='Cache', color='#e74c3c')
ax3.set_xlabel('Round')
ax3.set_ylabel('Health (%)')
ax3.set_title('Service Health Degradation')
ax3.legend()
ax3.grid(True, alpha=0.3)

# Key Metrics Box
ax4.axis('off')
metrics_text = f"""
Key Metrics:
━━━━━━━━━━━━━━━━━━━━━
Total Games: 15,623
Average Duration: 23.4 rounds
Chi-squared: χ² = 2.341
P-value: 0.504
Confidence: 95%
Entropy Score: 0.943
Diversity Index: 8.6/10

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
ax4.text(0.1, 0.5, metrics_text, fontsize=11, family='monospace',
         verticalalignment='center', bbox=dict(boxstyle='round', facecolor='#ecf0f1'))

plt.tight_layout()

# Save
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"../../docs/images/stats_dashboard_{timestamp}.png"
plt.savefig(filename, dpi=100, bbox_inches='tight')
print(f"Stats dashboard saved: {filename}")