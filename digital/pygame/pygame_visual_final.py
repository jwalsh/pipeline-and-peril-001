#!/usr/bin/env python3
"""Enhanced PyGame visualization with L7 architecture patterns"""

import pygame
import sys
import random
import math
from datetime import datetime

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
FPS = 60

# Enhanced color scheme
BLACK = (20, 24, 35)
WHITE = (255, 255, 255)
BLUE = (59, 130, 246)
GREEN = (16, 185, 129)
RED = (239, 68, 68)
YELLOW = (245, 158, 11)
PURPLE = (139, 92, 246)
GRAY = (75, 85, 99)
LIGHT_GRAY = (156, 163, 175)
DARK_BLUE = (30, 58, 138)
ORANGE = (251, 146, 60)

class EnhancedPipelinePerilGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pipeline & Peril - Distributed Systems Learning Platform")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 42)
        self.medium_font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 24)
        self.tiny_font = pygame.font.Font(None, 20)
        self.running = True
        
        # Game state with L7 architecture patterns
        self.services = []
        self.connections = []
        self.circuit_breakers = {}
        self.traffic_flow = []
        self.players = [
            {"name": "Charlie", "score": 45, "color": YELLOW, "rank": 1},
            {"name": "Alice", "score": 42, "color": BLUE, "rank": 2},
            {"name": "Diana", "score": 41, "color": PURPLE, "rank": 3},
            {"name": "Bob", "score": 38, "color": GREEN, "rank": 4}
        ]
        self.round_num = 1
        self.entropy = 5
        self.slo_violations = 0
        self.error_budget = 100
        
        self.init_services()
        self.init_learning_metrics()
        
    def init_learning_metrics(self):
        """Initialize learning and business metrics"""
        self.learning_metrics = {
            "concepts_mastered": 12,
            "total_concepts": 15,
            "scenarios_completed": 8,
            "total_scenarios": 10,
            "session_time": 1471,  # seconds
            "actions_count": 78,
        }
        
    def init_services(self):
        """Initialize service nodes with architecture patterns"""
        # Service definitions with criticality and dependencies
        service_configs = [
            # Critical path services (Tier 1)
            {"name": "Auth", "x": 250, "y": 200, "tier": 1, "color": YELLOW, "critical": True},
            {"name": "API", "x": 600, "y": 200, "tier": 1, "color": BLUE, "critical": True},
            {"name": "DB", "x": 950, "y": 200, "tier": 1, "color": DARK_BLUE, "critical": True},
            
            # Supporting services (Tier 2)
            {"name": "Cache", "x": 250, "y": 400, "tier": 2, "color": ORANGE, "critical": False},
            {"name": "Queue", "x": 600, "y": 400, "tier": 2, "color": PURPLE, "critical": False},
            {"name": "Storage", "x": 950, "y": 400, "tier": 2, "color": GREEN, "critical": False},
            
            # Monitoring and resilience (Tier 3)
            {"name": "Monitor", "x": 250, "y": 600, "tier": 3, "color": GRAY, "critical": False},
            {"name": "Circuit\nBreaker", "x": 600, "y": 600, "tier": 3, "color": RED, "critical": False},
            {"name": "Load\nBalancer", "x": 950, "y": 600, "tier": 3, "color": BLUE, "critical": False},
        ]
        
        for config in service_configs:
            health = 100 if config["critical"] else random.randint(70, 100)
            self.services.append({
                "name": config["name"],
                "x": config["x"],
                "y": config["y"],
                "tier": config["tier"],
                "color": config["color"],
                "health": health,
                "critical": config["critical"],
                "requests_per_sec": random.randint(100, 1000),
                "latency_ms": random.randint(10, 100),
                "error_rate": random.uniform(0, 0.05),
                "circuit_state": "closed"
            })
            
        # Create connections with flow direction
        self.connections = [
            # Critical path
            (0, 1, "critical", "→"),  # Auth → API
            (1, 2, "critical", "→"),  # API → DB
            (1, 4, "normal", "↓"),    # API → Queue
            (1, 3, "normal", "↓"),    # API → Cache
            
            # Cache patterns
            (3, 2, "cache", "→"),     # Cache → DB
            
            # Async processing
            (4, 5, "async", "→"),     # Queue → Storage
            
            # Monitoring
            (6, 0, "monitor", "↑"),   # Monitor → Auth
            (6, 1, "monitor", "↑"),   # Monitor → API
            (6, 2, "monitor", "↑"),   # Monitor → DB
            
            # Circuit breaker patterns
            (7, 1, "resilience", "↑"), # Circuit Breaker → API
            (7, 4, "resilience", "→"), # Circuit Breaker → Queue
            
            # Load balancing
            (8, 1, "balance", "↑"),   # Load Balancer → API
        ]
    
    def draw_background(self):
        """Draw enhanced background with grid"""
        self.screen.fill(BLACK)
        
        # Draw subtle grid
        for x in range(0, WINDOW_WIDTH, 50):
            pygame.draw.line(self.screen, (30, 35, 45), (x, 0), (x, WINDOW_HEIGHT), 1)
        for y in range(0, WINDOW_HEIGHT, 50):
            pygame.draw.line(self.screen, (30, 35, 45), (0, y), (WINDOW_WIDTH, y), 1)
            
        # Draw tier backgrounds
        tier_colors = [(25, 30, 40), (20, 25, 35), (15, 20, 30)]
        tier_heights = [280, 280, 280]
        y_offset = 100
        
        for i, (color, height) in enumerate(zip(tier_colors, tier_heights)):
            rect = pygame.Rect(50, y_offset + i * 200, WINDOW_WIDTH - 100, 180)
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, GRAY, rect, 2)
            
            # Tier labels
            tier_text = f"Tier {i+1}: {'Critical Path' if i == 0 else 'Supporting Services' if i == 1 else 'Resilience Layer'}"
            text = self.tiny_font.render(tier_text, True, LIGHT_GRAY)
            self.screen.blit(text, (70, y_offset + i * 200 + 10))
    
    def draw_services(self):
        """Draw service nodes with enhanced visualization"""
        # Draw connections first with flow indicators
        for conn in self.connections:
            if conn[0] < len(self.services) and conn[1] < len(self.services):
                service_a = self.services[conn[0]]
                service_b = self.services[conn[1]]
                conn_type = conn[2]
                flow_dir = conn[3]
                
                # Connection color based on type
                conn_colors = {
                    "critical": RED,
                    "normal": GREEN,
                    "cache": YELLOW,
                    "async": PURPLE,
                    "monitor": LIGHT_GRAY,
                    "resilience": ORANGE,
                    "balance": BLUE
                }
                color = conn_colors.get(conn_type, LIGHT_GRAY)
                
                # Draw connection line
                pygame.draw.line(self.screen, color, 
                               (service_a["x"], service_a["y"]),
                               (service_b["x"], service_b["y"]), 
                               3 if conn_type == "critical" else 2)
                
                # Draw flow direction indicator
                mid_x = (service_a["x"] + service_b["x"]) // 2
                mid_y = (service_a["y"] + service_b["y"]) // 2
                flow_text = self.tiny_font.render(flow_dir, True, color)
                self.screen.blit(flow_text, (mid_x - 5, mid_y - 10))
        
        # Draw service nodes
        for i, service in enumerate(self.services):
            # Determine node color based on health
            if service["health"] > 80:
                health_color = GREEN
            elif service["health"] > 50:
                health_color = YELLOW
            else:
                health_color = RED
                
            # Draw outer ring for critical services
            if service["critical"]:
                pygame.draw.circle(self.screen, WHITE, (service["x"], service["y"]), 55, 3)
                
            # Draw node with gradient effect
            pygame.draw.circle(self.screen, service["color"], (service["x"], service["y"]), 45)
            pygame.draw.circle(self.screen, health_color, (service["x"], service["y"]), 45, 4)
            
            # Draw service name
            lines = service["name"].split('\n')
            y_offset = -10 * len(lines)
            for line in lines:
                label = self.small_font.render(line, True, WHITE)
                label_rect = label.get_rect(center=(service["x"], service["y"] + y_offset))
                self.screen.blit(label, label_rect)
                y_offset += 20
            
            # Draw health bar
            bar_width = 70
            bar_height = 6
            bar_x = service["x"] - bar_width // 2
            bar_y = service["y"] + 55
            pygame.draw.rect(self.screen, GRAY, (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(self.screen, health_color, 
                           (bar_x, bar_y, int(bar_width * service["health"] / 100), bar_height))
            
            # Draw metrics
            if service["critical"]:
                metrics_text = f"{service['requests_per_sec']} req/s | {service['latency_ms']}ms"
                text = self.tiny_font.render(metrics_text, True, LIGHT_GRAY)
                text_rect = text.get_rect(center=(service["x"], service["y"] + 70))
                self.screen.blit(text, text_rect)
                
            # Circuit breaker indicator
            if service.get("circuit_state") == "open":
                pygame.draw.circle(self.screen, RED, (service["x"] + 40, service["y"] - 40), 8)
                cb_text = self.tiny_font.render("CB", True, WHITE)
                self.screen.blit(cb_text, (service["x"] + 33, service["y"] - 47))
    
    def draw_ui(self):
        """Draw enhanced UI elements"""
        # Title and value proposition
        title = self.font.render("Pipeline & Peril", True, WHITE)
        self.screen.blit(title, (20, 15))
        
        subtitle = self.medium_font.render("Learn Distributed Systems Through Interactive Gameplay", True, LIGHT_GRAY)
        self.screen.blit(subtitle, (20, 55))
        
        # Learning progress indicator
        progress_text = f"Learning Progress: {self.learning_metrics['concepts_mastered']}/{self.learning_metrics['total_concepts']} concepts"
        progress = self.small_font.render(progress_text, True, GREEN)
        self.screen.blit(progress, (500, 20))
        
        # SLO and Error Budget
        slo_text = f"Error Budget: {self.error_budget}%"
        color = GREEN if self.error_budget > 50 else YELLOW if self.error_budget > 20 else RED
        slo = self.small_font.render(slo_text, True, color)
        self.screen.blit(slo, (750, 20))
        
        # Round and entropy with visual indicators
        round_text = self.medium_font.render(f"Round: {self.round_num}", True, WHITE)
        self.screen.blit(round_text, (20, 90))
        
        entropy_color = RED if self.entropy > 15 else YELLOW if self.entropy > 10 else GREEN
        entropy_text = self.medium_font.render(f"System Entropy: {self.entropy}/20", True, entropy_color)
        self.screen.blit(entropy_text, (180, 90))
        
        # Player scores with ranking
        y_offset = 20
        self.screen.blit(self.medium_font.render("Leaderboard", True, WHITE), (WINDOW_WIDTH - 200, y_offset))
        y_offset += 35
        
        for player in sorted(self.players, key=lambda p: p["score"], reverse=True):
            # Rank indicator
            if player["rank"] == 1:
                rank_text = "👑"
            else:
                rank_text = f"#{player['rank']}"
            
            rank_surface = self.small_font.render(rank_text, True, player['color'])
            self.screen.blit(rank_surface, (WINDOW_WIDTH - 200, y_offset))
            
            score_text = f"{player['name']}: {player['score']}"
            text_surface = self.small_font.render(score_text, True, player['color'])
            self.screen.blit(text_surface, (WINDOW_WIDTH - 160, y_offset))
            y_offset += 30
        
        # Business metrics panel
        metrics_y = WINDOW_HEIGHT - 120
        pygame.draw.rect(self.screen, (30, 35, 45), (20, metrics_y, 400, 100))
        pygame.draw.rect(self.screen, GRAY, (20, metrics_y, 400, 100), 2)
        
        metrics_title = self.small_font.render("Session Metrics", True, WHITE)
        self.screen.blit(metrics_title, (30, metrics_y + 10))
        
        session_time = f"Duration: {self.learning_metrics['session_time'] // 60}:{self.learning_metrics['session_time'] % 60:02d}"
        actions_min = f"APM: {self.learning_metrics['actions_count'] / (self.learning_metrics['session_time'] / 60):.1f}"
        scenarios = f"Scenarios: {self.learning_metrics['scenarios_completed']}/{self.learning_metrics['total_scenarios']}"
        
        self.screen.blit(self.tiny_font.render(session_time, True, LIGHT_GRAY), (30, metrics_y + 35))
        self.screen.blit(self.tiny_font.render(actions_min, True, LIGHT_GRAY), (30, metrics_y + 55))
        self.screen.blit(self.tiny_font.render(scenarios, True, LIGHT_GRAY), (30, metrics_y + 75))
        
        # Help prompt
        help_text = "Press H for tutorial • Tab for analytics • Space to pause"
        help_surface = self.tiny_font.render(help_text, True, YELLOW)
        self.screen.blit(help_surface, (WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT - 30))
        
        # Timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time_text = self.tiny_font.render(timestamp, True, LIGHT_GRAY)
        self.screen.blit(time_text, (WINDOW_WIDTH - 180, WINDOW_HEIGHT - 30))
    
    def update(self):
        """Update game state with realistic patterns"""
        # Simulate service degradation
        if random.random() < 0.02:
            service = random.choice(self.services)
            if not service["critical"]:  # Don't degrade critical services as much
                service["health"] = max(0, service["health"] - random.randint(5, 15))
                if service["health"] < 30:
                    service["circuit_state"] = "open"
        
        # Simulate service recovery
        if random.random() < 0.03:
            service = random.choice(self.services)
            service["health"] = min(100, service["health"] + random.randint(10, 20))
            if service["health"] > 50:
                service["circuit_state"] = "closed"
        
        # Update metrics
        self.learning_metrics["session_time"] += 1
        if random.random() < 0.05:
            self.learning_metrics["actions_count"] += 1
        
        # Update error budget based on service health
        unhealthy_services = sum(1 for s in self.services if s["health"] < 50)
        if unhealthy_services > 0:
            self.error_budget = max(0, self.error_budget - 0.1)
        else:
            self.error_budget = min(100, self.error_budget + 0.05)
        
        # Update entropy
        if random.random() < 0.01:
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
                        filename = f"../../docs/images/pygame_demo_final_{timestamp}.png"
                        pygame.image.save(self.screen, filename)
                        print(f"Screenshot saved: {filename}")
            
            # Draw everything
            self.draw_background()
            self.draw_services()
            self.draw_ui()
            
            # Update
            self.update()
            
            # Auto-screenshot after 1 second
            frame_count += 1
            if frame_count == 60 and not screenshot_taken:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"../../docs/images/pygame_demo_final_{timestamp}.png"
                pygame.image.save(self.screen, filename)
                print(f"Final PyGame screenshot saved: {filename}")
                screenshot_taken = True
            
            # Update display
            pygame.display.flip()
            self.clock.tick(FPS)
            
            # Auto-quit after 3 seconds
            if frame_count > 180:
                self.running = False
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = EnhancedPipelinePerilGame()
    game.run()