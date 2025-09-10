"""
Core game state management for Pipeline & Peril PyGame implementation.

This module provides the fundamental data structures and state management
for the Pipeline & Peril game, including:
- Game state representation
- Player state tracking  
- Grid management with hexagonal coordinates
- Service placement and connections
- Resource management
- Turn and phase tracking

Based on requirements specification from PYGAME-REQUIREMENTS.md
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Set
from enum import Enum
import uuid
import json
from datetime import datetime


class GamePhase(Enum):
    """Game phases following the turn structure"""
    SETUP = "setup"
    TRAFFIC = "traffic"
    ACTION = "action"
    RESOLUTION = "resolution"
    CHAOS = "chaos"
    END = "end"


class ServiceType(Enum):
    """Service types with their properties"""
    COMPUTE = "compute"
    DATABASE = "database"
    CACHE = "cache"
    QUEUE = "queue"
    LOAD_BALANCER = "load_balancer"
    API_GATEWAY = "api_gateway"


class ResourceType(Enum):
    """Resource types used in the game"""
    CPU = "cpu"
    MEMORY = "memory"
    STORAGE = "storage"


@dataclass
class ServiceCosts:
    """Resource costs for services"""
    cpu: int
    memory: int
    storage: int
    capacity: int
    
    @classmethod
    def get_costs(cls, service_type: ServiceType) -> 'ServiceCosts':
        """Get resource costs for a service type"""
        costs_table = {
            ServiceType.COMPUTE: cls(2, 2, 1, 5),
            ServiceType.DATABASE: cls(1, 2, 3, 3),
            ServiceType.CACHE: cls(1, 3, 1, 8),
            ServiceType.QUEUE: cls(1, 1, 2, 6),
            ServiceType.LOAD_BALANCER: cls(2, 1, 1, 10),
            ServiceType.API_GATEWAY: cls(1, 1, 1, 7),
        }
        return costs_table[service_type]


@dataclass
class HexCoordinate:
    """Hexagonal grid coordinate system"""
    row: int
    col: int
    
    def __hash__(self):
        return hash((self.row, self.col))
    
    def neighbors(self) -> List['HexCoordinate']:
        """Get adjacent hexagonal coordinates"""
        # Hexagonal grid neighbors (offset coordinates)
        if self.row % 2 == 0:  # Even row
            offsets = [(-1, -1), (-1, 0), (0, -1), (0, 1), (1, -1), (1, 0)]
        else:  # Odd row
            offsets = [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, 0), (1, 1)]
        
        return [HexCoordinate(self.row + dr, self.col + dc) for dr, dc in offsets]
    
    def distance(self, other: 'HexCoordinate') -> int:
        """Calculate hexagonal distance to another coordinate"""
        # Convert to cube coordinates for easier distance calculation
        def offset_to_cube(coord):
            x = coord.col - (coord.row - (coord.row & 1)) // 2
            z = coord.row
            y = -x - z
            return (x, y, z)
        
        x1, y1, z1 = offset_to_cube(self)
        x2, y2, z2 = offset_to_cube(other)
        
        return (abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)) // 2


@dataclass
class Service:
    """Individual service instance"""
    id: str
    service_type: ServiceType
    location: HexCoordinate
    owner_id: int
    current_capacity: int
    max_capacity: int
    connections: Set[str] = field(default_factory=set)
    bugs: int = 0
    upgrades: int = 0
    
    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())
    
    def can_handle_load(self, load: int) -> bool:
        """Check if service can handle additional load"""
        return self.current_capacity >= load
    
    def add_load(self, load: int) -> bool:
        """Add load to service, return False if overloaded"""
        if self.can_handle_load(load):
            self.current_capacity -= load
            return True
        return False
    
    def connect_to(self, other_service_id: str):
        """Create connection to another service"""
        self.connections.add(other_service_id)


@dataclass 
class Player:
    """Player state"""
    id: int
    name: str
    resources: Dict[ResourceType, int] = field(default_factory=lambda: {
        ResourceType.CPU: 5,
        ResourceType.MEMORY: 5,
        ResourceType.STORAGE: 5
    })
    actions_remaining: int = 3
    services: List[str] = field(default_factory=list)
    uptime_history: List[float] = field(default_factory=list)
    current_uptime: float = 100.0
    character_ability_used: bool = False
    
    def can_afford(self, costs: ServiceCosts) -> bool:
        """Check if player can afford service costs"""
        return (self.resources[ResourceType.CPU] >= costs.cpu and
                self.resources[ResourceType.MEMORY] >= costs.memory and
                self.resources[ResourceType.STORAGE] >= costs.storage)
    
    def spend_resources(self, costs: ServiceCosts) -> bool:
        """Spend resources if affordable"""
        if self.can_afford(costs):
            self.resources[ResourceType.CPU] -= costs.cpu
            self.resources[ResourceType.MEMORY] -= costs.memory
            self.resources[ResourceType.STORAGE] -= costs.storage
            return True
        return False


@dataclass
class Grid:
    """Hexagonal game grid"""
    width: int = 8
    height: int = 6
    services: Dict[HexCoordinate, str] = field(default_factory=dict)
    
    def is_valid_coordinate(self, coord: HexCoordinate) -> bool:
        """Check if coordinate is within grid bounds"""
        return 0 <= coord.row < self.height and 0 <= coord.col < self.width
    
    def is_empty(self, coord: HexCoordinate) -> bool:
        """Check if grid position is empty"""
        return coord not in self.services
    
    def place_service(self, coord: HexCoordinate, service_id: str) -> bool:
        """Place service at coordinate if valid and empty"""
        if self.is_valid_coordinate(coord) and self.is_empty(coord):
            self.services[coord] = service_id
            return True
        return False
    
    def remove_service(self, coord: HexCoordinate) -> Optional[str]:
        """Remove service from coordinate"""
        return self.services.pop(coord, None)
    
    def get_adjacent_services(self, coord: HexCoordinate) -> List[str]:
        """Get services adjacent to coordinate"""
        adjacent = []
        for neighbor in coord.neighbors():
            if neighbor in self.services:
                adjacent.append(self.services[neighbor])
        return adjacent


@dataclass
class Metrics:
    """Game metrics and statistics"""
    total_requests_handled: int = 0
    cascade_failures: int = 0
    chaos_events_triggered: int = 0
    services_built: int = 0
    connections_created: int = 0
    average_uptime: float = 100.0
    
    def update_average_uptime(self, player_uptimes: List[float]):
        """Update average uptime from all players"""
        if player_uptimes:
            self.average_uptime = sum(player_uptimes) / len(player_uptimes)


@dataclass
class GameState:
    """Complete game state"""
    game_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    round: int = 1
    phase: GamePhase = GamePhase.SETUP
    players: List[Player] = field(default_factory=list)
    grid: Grid = field(default_factory=Grid)
    services: Dict[str, Service] = field(default_factory=dict)
    metrics: Metrics = field(default_factory=Metrics)
    entropy: int = 0
    current_player_index: int = 0
    action_log: List[Dict] = field(default_factory=list)
    
    def get_current_player(self) -> Player:
        """Get the player whose turn it is"""
        return self.players[self.current_player_index]
    
    def next_player(self):
        """Move to next player"""
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
    
    def next_phase(self):
        """Advance to next game phase"""
        phase_order = [GamePhase.TRAFFIC, GamePhase.ACTION, GamePhase.RESOLUTION, GamePhase.CHAOS]
        
        if self.phase == GamePhase.SETUP:
            self.phase = GamePhase.TRAFFIC
        elif self.phase in phase_order:
            current_index = phase_order.index(self.phase)
            if current_index == len(phase_order) - 1:  # End of turn
                self.round += 1
                self.phase = GamePhase.TRAFFIC
                self.current_player_index = 0
                # Reset player actions
                for player in self.players:
                    player.actions_remaining = 3
                    player.character_ability_used = False
            else:
                self.phase = phase_order[current_index + 1]
    
    def add_service(self, service: Service) -> bool:
        """Add service to game state"""
        if self.grid.place_service(service.location, service.id):
            self.services[service.id] = service
            self.players[service.owner_id].services.append(service.id)
            self.metrics.services_built += 1
            return True
        return False
    
    def remove_service(self, service_id: str) -> bool:
        """Remove service from game state"""
        if service_id not in self.services:
            return False
        
        service = self.services[service_id]
        self.grid.remove_service(service.location)
        del self.services[service_id]
        
        # Remove from player's service list
        if service_id in self.players[service.owner_id].services:
            self.players[service.owner_id].services.remove(service_id)
        
        return True
    
    def log_action(self, action_type: str, player_id: int, parameters: Dict, result: Dict = None):
        """Log game action for replay and analysis"""
        action = {
            "timestamp": datetime.now().isoformat(),
            "round": self.round,
            "phase": self.phase.value,
            "action_type": action_type,
            "player_id": player_id,
            "parameters": parameters,
            "result": result or {}
        }
        self.action_log.append(action)
    
    def is_game_over(self) -> bool:
        """Check if game has ended"""
        # Game ends after 20 rounds or if all players have 0 uptime
        return (self.round > 20 or 
                all(player.current_uptime <= 0 for player in self.players))
    
    def get_winner(self) -> Optional[Player]:
        """Determine game winner based on victory conditions"""
        if not self.is_game_over():
            return None
        
        # Cooperative victory: >80% average uptime for 10+ rounds
        if self.round >= 10:
            avg_uptime = sum(p.current_uptime for p in self.players) / len(self.players)
            if avg_uptime > 80:
                return None  # Cooperative victory
        
        # Competitive victory: highest uptime * requests handled
        best_player = None
        best_score = -1
        
        for player in self.players:
            score = player.current_uptime * len(player.services)  # Simplified metric
            if score > best_score:
                best_score = score
                best_player = player
        
        return best_player
    
    def to_dict(self) -> Dict:
        """Convert game state to dictionary for serialization"""
        return {
            "game_id": self.game_id,
            "round": self.round,
            "phase": self.phase.value,
            "players": [
                {
                    "id": p.id,
                    "name": p.name,
                    "resources": {rt.value: amount for rt, amount in p.resources.items()},
                    "actions_remaining": p.actions_remaining,
                    "services": p.services,
                    "current_uptime": p.current_uptime,
                    "uptime_history": p.uptime_history
                }
                for p in self.players
            ],
            "grid": {
                "width": self.grid.width,
                "height": self.grid.height,
                "services": {f"{coord.row},{coord.col}": service_id 
                           for coord, service_id in self.grid.services.items()}
            },
            "services": {
                service_id: {
                    "id": service.id,
                    "type": service.service_type.value,
                    "location": {"row": service.location.row, "col": service.location.col},
                    "owner_id": service.owner_id,
                    "current_capacity": service.current_capacity,
                    "max_capacity": service.max_capacity,
                    "connections": list(service.connections),
                    "bugs": service.bugs,
                    "upgrades": service.upgrades
                }
                for service_id, service in self.services.items()
            },
            "metrics": {
                "total_requests_handled": self.metrics.total_requests_handled,
                "cascade_failures": self.metrics.cascade_failures,
                "chaos_events_triggered": self.metrics.chaos_events_triggered,
                "services_built": self.metrics.services_built,
                "connections_created": self.metrics.connections_created,
                "average_uptime": self.metrics.average_uptime
            },
            "entropy": self.entropy,
            "current_player_index": self.current_player_index
        }
    
    def to_json(self) -> str:
        """Convert game state to JSON string"""
        return json.dumps(self.to_dict(), indent=2)


def create_initial_game_state(player_names: List[str]) -> GameState:
    """Create initial game state with given players"""
    game_state = GameState()
    
    # Create players
    for i, name in enumerate(player_names):
        player = Player(id=i, name=name)
        game_state.players.append(player)
    
    # Place starting services for each player
    starting_positions = [
        HexCoordinate(1, 1),
        HexCoordinate(1, 6),
        HexCoordinate(4, 1),
        HexCoordinate(4, 6)
    ]
    
    starting_services = [
        ServiceType.COMPUTE,
        ServiceType.DATABASE,
        ServiceType.LOAD_BALANCER
    ]
    
    for i, player in enumerate(game_state.players):
        if i < len(starting_positions):
            base_coord = starting_positions[i]
            
            for j, service_type in enumerate(starting_services):
                coord = HexCoordinate(base_coord.row, base_coord.col + j)
                if game_state.grid.is_valid_coordinate(coord):
                    costs = ServiceCosts.get_costs(service_type)
                    service = Service(
                        id=str(uuid.uuid4()),
                        service_type=service_type,
                        location=coord,
                        owner_id=player.id,
                        current_capacity=costs.capacity,
                        max_capacity=costs.capacity
                    )
                    game_state.add_service(service)
    
    game_state.log_action("game_start", -1, {"players": player_names})
    return game_state