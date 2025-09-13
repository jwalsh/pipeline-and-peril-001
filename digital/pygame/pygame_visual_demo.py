#!/usr/bin/env python3
"""Simple PyGame visualization for Pipeline & Peril"""

import pygame
import sys
import random
from datetime import datetime

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (52, 152, 219)
GREEN = (46, 204, 113)
RED = (231, 76, 60)
YELLOW = (241, 196, 15)
PURPLE = (155, 89, 182)
GRAY = (52, 73, 94)
LIGHT_GRAY = (149, 165, 166)

class PipelinePerilGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pipeline & Peril - Game Visualization")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)
        self.running = True
        
        # Game state
        self.services = []
        self.connections = []
        self.players = [
            {"name": "Alice", "score": 42, "color": BLUE},
            {"name": "Bob", "score": 38, "color": GREEN},
            {"name": "Charlie", "score": 45, "color": YELLOW},
            {"name": "Diana", "score": 41, "color": PURPLE}
        ]
        self.round_num = 1
        self.entropy = 5
        
        self.init_services()
        
    def init_services(self):
        """Initialize service nodes"""
        positions = [
            (300, 200), (600, 200), (900, 200),
            (300, 400), (600, 400), (900, 400),
            (300, 600), (600, 600), (900, 600)
        ]
        
        service_types = ["Auth", "DB", "Cache", "Queue", "API", "Web", "Worker", "Storage", "Monitor"]
        
        for i, (x, y) in enumerate(positions):
            health = random.randint(60, 100)
            self.services.append({
                "x": x,
                "y": y,
                "type": service_types[i],
                "health": health,
                "status": "healthy" if health > 80 else "degraded" if health > 40 else "critical"
            })
            
        # Create some connections
        for i in range(12):
            a = random.randint(0, 8)
            b = random.randint(0, 8)
            if a != b:
                self.connections.append((a, b))
    
    def draw_grid(self):
        """Draw background grid"""
        for x in range(0, WINDOW_WIDTH, 50):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, WINDOW_HEIGHT), 1)
        for y in range(0, WINDOW_HEIGHT, 50):
            pygame.draw.line(self.screen, GRAY, (0, y), (WINDOW_WIDTH, y), 1)
    
    def draw_services(self):
        """Draw service nodes"""
        # Draw connections first
        for a, b in self.connections:
            if a < len(self.services) and b < len(self.services):
                service_a = self.services[a]
                service_b = self.services[b]
                pygame.draw.line(self.screen, LIGHT_GRAY, 
                               (service_a["x"], service_a["y"]),
                               (service_b["x"], service_b["y"]), 2)
        
        # Draw service nodes
        for service in self.services:
            # Determine color based on health
            if service["health"] > 80:
                color = GREEN
            elif service["health"] > 40:
                color = YELLOW
            else:
                color = RED
                
            # Draw node
            pygame.draw.circle(self.screen, color, (service["x"], service["y"]), 40)
            pygame.draw.circle(self.screen, WHITE, (service["x"], service["y"]), 40, 3)
            
            # Draw label
            label = self.small_font.render(service["type"], True, WHITE)
            label_rect = label.get_rect(center=(service["x"], service["y"]))
            self.screen.blit(label, label_rect)
            
            # Draw health bar
            bar_width = 60
            bar_height = 4
            bar_x = service["x"] - bar_width // 2
            bar_y = service["y"] + 35
            pygame.draw.rect(self.screen, GRAY, (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(self.screen, color, (bar_x, bar_y, int(bar_width * service["health"] / 100), bar_height))
    
    def draw_ui(self):
        """Draw UI elements"""
        # Title
        title = self.font.render("Pipeline & Peril", True, WHITE)
        self.screen.blit(title, (10, 10))
        
        # Round and entropy
        round_text = self.small_font.render(f"Round: {self.round_num}", True, WHITE)
        self.screen.blit(round_text, (10, 50))
        
        entropy_text = self.small_font.render(f"Entropy: {self.entropy}/20", True, RED if self.entropy > 15 else YELLOW if self.entropy > 10 else WHITE)
        self.screen.blit(entropy_text, (10, 75))
        
        # Player scores
        y_offset = 10
        for player in self.players:
            score_text = self.small_font.render(f"{player['name']}: {player['score']}", True, player['color'])
            self.screen.blit(score_text, (WINDOW_WIDTH - 120, y_offset))
            y_offset += 30
        
        # Status message
        status = "System Status: "
        critical_count = sum(1 for s in self.services if s["health"] < 40)
        if critical_count > 3:
            status += "CRITICAL - Multiple failures detected!"
            color = RED
        elif critical_count > 0:
            status += f"WARNING - {critical_count} service(s) critical"
            color = YELLOW
        else:
            status += "Stable"
            color = GREEN
            
        status_text = self.small_font.render(status, True, color)
        self.screen.blit(status_text, (10, WINDOW_HEIGHT - 30))
        
        # Timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time_text = self.small_font.render(timestamp, True, LIGHT_GRAY)
        self.screen.blit(time_text, (WINDOW_WIDTH - 180, WINDOW_HEIGHT - 30))
    
    def update(self):
        """Update game state"""
        # Randomly degrade services
        if random.random() < 0.02:  # 2% chance per frame
            service = random.choice(self.services)
            service["health"] = max(0, service["health"] - random.randint(5, 15))
        
        # Randomly heal services
        if random.random() < 0.01:  # 1% chance per frame
            service = random.choice(self.services)
            service["health"] = min(100, service["health"] + random.randint(10, 20))
        
        # Update entropy
        if random.random() < 0.005:
            self.entropy = min(20, self.entropy + 1)
    
    def run(self):
        """Main game loop"""
        frame_count = 0
        screenshot_taken = False
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_s:
                        # Take screenshot
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"../../docs/images/pygame_demo_{timestamp}.png"
                        pygame.image.save(self.screen, filename)
                        print(f"Screenshot saved: {filename}")
            
            # Clear screen
            self.screen.fill(BLACK)
            
            # Draw everything
            self.draw_grid()
            self.draw_services()
            self.draw_ui()
            
            # Update
            self.update()
            
            # Auto-screenshot after 1 second (60 frames)
            frame_count += 1
            if frame_count == 60 and not screenshot_taken:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"../../docs/images/pygame_demo_{timestamp}.png"
                pygame.image.save(self.screen, filename)
                print(f"Auto-screenshot saved: {filename}")
                screenshot_taken = True
            
            # Update display
            pygame.display.flip()
            self.clock.tick(FPS)
            
            # Auto-quit after 3 seconds for demo
            if frame_count > 180:
                self.running = False
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = PipelinePerilGame()
    game.run()