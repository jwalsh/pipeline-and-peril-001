#!/usr/bin/env python3
"""
Simplified game state for demonstration
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
from enum import Enum
import uuid
import json


class ServiceType(Enum):
    COMPUTE = "compute"
    DATABASE = "database"
    CACHE = "cache"
    QUEUE = "queue"
    LOAD_BALANCER = "load_balancer"
    API_GATEWAY = "api_gateway"


@dataclass
class HexCoordinate:
    row: int
    col: int
    
    def __hash__(self):
        return hash((self.row, self.col))


@dataclass
class Service:
    id: str
    service_type: ServiceType
    location: HexCoordinate
    owner_id: int
    current_capacity: int = 5
    max_capacity: int = 5
    
    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())


@dataclass
class Player:
    id: int
    name: str
    cpu: int = 5
    memory: int = 5
    storage: int = 5
    services: List[str] = field(default_factory=list)
    current_uptime: float = 100.0


@dataclass
class GameState:
    game_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    round: int = 1
    players: List[Player] = field(default_factory=list)
    services: Dict[str, Service] = field(default_factory=dict)
    grid_width: int = 8
    grid_height: int = 6
    
    def add_service(self, service: Service) -> bool:
        """Add service to game"""
        if (0 <= service.location.row < self.grid_height and
            0 <= service.location.col < self.grid_width):
            self.services[service.id] = service
            self.players[service.owner_id].services.append(service.id)
            return True
        return False
    
    def display_status(self):
        """Display game status"""
        print(f"🎮 Pipeline & Peril - Round {self.round}")
        print(f"Game ID: {self.game_id}")
        print(f"Players: {len(self.players)}")
        print(f"Services: {len(self.services)}")
        
        for player in self.players:
            print(f"  {player.name}: {len(player.services)} services, {player.current_uptime:.1f}% uptime")


def create_demo_game() -> GameState:
    """Create a demo game for testing"""
    game = GameState()
    
    # Add players
    game.players = [
        Player(id=0, name="Alice"),
        Player(id=1, name="Bob"),
        Player(id=2, name="Charlie")
    ]
    
    # Add some services
    services = [
        Service("svc1", ServiceType.COMPUTE, HexCoordinate(1, 1), 0),
        Service("svc2", ServiceType.DATABASE, HexCoordinate(1, 2), 0),
        Service("svc3", ServiceType.LOAD_BALANCER, HexCoordinate(2, 1), 1),
        Service("svc4", ServiceType.CACHE, HexCoordinate(3, 3), 2),
    ]
    
    for service in services:
        game.add_service(service)
    
    return game


if __name__ == "__main__":
    print("🧪 Testing simple game state...")
    
    game = create_demo_game()
    game.display_status()
    
    print("\n✅ Simple game state working!")
    print(f"📊 Stats: {len(game.services)} services across {len(game.players)} players")