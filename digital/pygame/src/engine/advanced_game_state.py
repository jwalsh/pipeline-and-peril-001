"""
Advanced game state management using cutting-edge Python features.

This module showcases modern Python development patterns including:
- Pydantic v2 models with validators and computed fields
- Rich console output and progress tracking
- Structural pattern matching (Python 3.10+)
- Type annotations with unions and protocols
- Functools decorators and caching
- Itertools for efficient operations
- Attrs for high-performance data classes
- Structured logging with rich formatting

Features demonstrated:
- Match statements for game logic
- Cached properties for expensive computations
- Protocol-based design for extensibility
- Rich progress bars and tables
- Structured logging with context
- Type-safe enum matching
- Generator expressions with walrus operator
- Context managers for resource handling
"""

from __future__ import annotations

import asyncio
import functools
import itertools
import uuid
from collections import defaultdict, deque
from dataclasses import field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import (
    Any, Dict, List, Optional, Set, Tuple, Union, Protocol, 
    TypeVar, Generic, Callable, Iterator, AsyncIterator,
    Literal, Annotated, ClassVar
)

import attrs
import structlog
from loguru import logger
from pydantic import (
    BaseModel, Field, computed_field, field_validator,
    ConfigDict, ValidationError, model_validator
)
from rich.console import Console
from rich.progress import Progress, TaskID
from rich.table import Table
from rich.tree import Tree
from dataclasses_json import dataclass_json

# Initialize rich console and structured logging
console = Console()
log = structlog.get_logger()

# Type variables for generic operations
T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')


class GamePhase(Protocol):
    """Protocol for game phase handlers"""
    def execute(self, game_state: AdvancedGameState) -> AdvancedGameState:
        """Execute phase logic and return updated state"""
        ...


@attrs.define(slots=True, frozen=True, cache_hash=True)
class HexCoordinate:
    """Immutable hexagonal coordinate with advanced operations"""
    row: int = attrs.field(validator=attrs.validators.instance_of(int))
    col: int = attrs.field(validator=attrs.validators.instance_of(int))
    
    @functools.cached_property
    def cube_coords(self) -> tuple[int, int, int]:
        """Convert to cube coordinates for distance calculations"""
        x = self.col - (self.row - (self.row & 1)) // 2
        z = self.row
        y = -x - z
        return (x, y, z)
    
    @functools.lru_cache(maxsize=1024)
    def distance_to(self, other: HexCoordinate) -> int:
        """Calculate hexagonal distance using cube coordinates"""
        x1, y1, z1 = self.cube_coords
        x2, y2, z2 = other.cube_coords
        return (abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)) // 2
    
    def neighbors(self, *, radius: int = 1) -> Iterator[HexCoordinate]:
        """Generate neighbors within given radius using generator expression"""
        if self.row % 2 == 0:  # Even row
            base_offsets = [(-1, -1), (-1, 0), (0, -1), (0, 1), (1, -1), (1, 0)]
        else:  # Odd row  
            base_offsets = [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, 0), (1, 1)]
        
        # Use itertools.product for radius expansion
        for r in range(1, radius + 1):
            for dr, dc in base_offsets:
                yield HexCoordinate(self.row + dr * r, self.col + dc * r)
    
    def path_to(self, target: HexCoordinate) -> list[HexCoordinate]:
        """Calculate optimal path using A* algorithm with functools.partial"""
        # Simplified path finding - could be enhanced with proper A*
        path = []
        current = self
        
        while current != target:
            neighbors = list(current.neighbors())
            # Find neighbor closest to target
            if closest := min(neighbors, key=lambda n: n.distance_to(target), default=None):
                path.append(closest)
                current = closest
            else:
                break
                
        return path


class ServiceType(str, Enum):
    """Enhanced enum with rich display and computed properties"""
    COMPUTE = "compute"
    DATABASE = "database" 
    CACHE = "cache"
    QUEUE = "queue"
    LOAD_BALANCER = "load_balancer"
    API_GATEWAY = "api_gateway"
    
    @property
    def emoji(self) -> str:
        """Rich emoji representation for console output"""
        match self:
            case ServiceType.COMPUTE: return "🖥️"
            case ServiceType.DATABASE: return "🗄️"
            case ServiceType.CACHE: return "⚡"
            case ServiceType.QUEUE: return "📬"
            case ServiceType.LOAD_BALANCER: return "⚖️"
            case ServiceType.API_GATEWAY: return "🚪"
            case _: return "❓"
    
    @functools.cached_property
    def costs(self) -> ResourceCosts:
        """Get resource costs using pattern matching"""
        match self:
            case ServiceType.COMPUTE:
                return ResourceCosts(cpu=2, memory=2, storage=1, capacity=5)
            case ServiceType.DATABASE:
                return ResourceCosts(cpu=1, memory=2, storage=3, capacity=3)
            case ServiceType.CACHE:
                return ResourceCosts(cpu=1, memory=3, storage=1, capacity=8)
            case ServiceType.QUEUE:
                return ResourceCosts(cpu=1, memory=1, storage=2, capacity=6)
            case ServiceType.LOAD_BALANCER:
                return ResourceCosts(cpu=2, memory=1, storage=1, capacity=10)
            case ServiceType.API_GATEWAY:
                return ResourceCosts(cpu=1, memory=1, storage=1, capacity=7)


class ResourceCosts(BaseModel):
    """Pydantic model for resource costs with validation"""
    model_config = ConfigDict(frozen=True, extra='forbid')
    
    cpu: Annotated[int, Field(ge=0, le=10, description="CPU units required")]
    memory: Annotated[int, Field(ge=0, le=10, description="Memory units required")]
    storage: Annotated[int, Field(ge=0, le=10, description="Storage units required")]
    capacity: Annotated[int, Field(ge=1, le=20, description="Service capacity")]
    
    @computed_field
    @property
    def total_cost(self) -> int:
        """Total resource cost for quick comparison"""
        return self.cpu + self.memory + self.storage
    
    @field_validator('capacity')
    @classmethod
    def validate_capacity(cls, v: int) -> int:
        """Ensure capacity is reasonable"""
        if v <= 0:
            raise ValueError("Capacity must be positive")
        return v


@attrs.define(slots=True)
class Service:
    """High-performance service representation using attrs"""
    service_type: ServiceType = attrs.field()
    location: HexCoordinate = attrs.field()
    owner_id: int = attrs.field()
    id: str = attrs.field(factory=lambda: str(uuid.uuid4()))
    current_load: int = attrs.field(default=0, validator=attrs.validators.ge(0))
    connections: set[str] = attrs.field(factory=set)
    bugs: int = attrs.field(default=0, validator=attrs.validators.ge(0))
    upgrades: int = attrs.field(default=0, validator=attrs.validators.ge(0))
    
    @property
    def max_capacity(self) -> int:
        """Calculate max capacity with upgrades"""
        base = self.service_type.costs.capacity
        return base + (self.upgrades * 2)
    
    @property
    def available_capacity(self) -> int:
        """Available capacity considering bugs"""
        max_cap = self.max_capacity
        bug_penalty = self.bugs * 1  # Each bug reduces capacity by 1
        return max(0, max_cap - self.current_load - bug_penalty)
    
    def can_handle_load(self, load: int) -> bool:
        """Check if service can handle additional load"""
        return self.available_capacity >= load
    
    def add_load(self, load: int) -> bool:
        """Add load with structured logging"""
        if self.can_handle_load(load):
            self.current_load += load
            log.info("Load added to service", 
                    service_id=self.id, 
                    service_type=self.service_type.value,
                    load_added=load,
                    new_load=self.current_load)
            return True
        
        log.warning("Service overload attempt", 
                   service_id=self.id,
                   requested_load=load,
                   available_capacity=self.available_capacity)
        return False


class PlayerResources(BaseModel):
    """Pydantic model for player resources with computed fields"""
    model_config = ConfigDict(frozen=False, validate_assignment=True)
    
    cpu: Annotated[int, Field(ge=0, le=100)] = 5
    memory: Annotated[int, Field(ge=0, le=100)] = 5
    storage: Annotated[int, Field(ge=0, le=100)] = 5
    
    @computed_field
    @property
    def total_resources(self) -> int:
        """Total available resources"""
        return self.cpu + self.memory + self.storage
    
    def can_afford(self, costs: ResourceCosts) -> bool:
        """Check if player can afford costs"""
        return (self.cpu >= costs.cpu and 
                self.memory >= costs.memory and 
                self.storage >= costs.storage)
    
    def spend(self, costs: ResourceCosts) -> bool:
        """Spend resources if affordable"""
        if self.can_afford(costs):
            self.cpu -= costs.cpu
            self.memory -= costs.memory
            self.storage -= costs.storage
            return True
        return False


@dataclass_json
@attrs.define
class Player:
    """Advanced player class with rich functionality"""
    id: int = attrs.field()
    name: str = attrs.field(validator=attrs.validators.min_len(1))
    resources: PlayerResources = attrs.field(factory=PlayerResources)
    actions_remaining: int = attrs.field(default=3, validator=attrs.validators.in_(range(0, 6)))
    services: list[str] = attrs.field(factory=list)
    uptime_history: deque[float] = attrs.field(factory=lambda: deque(maxlen=50))
    current_uptime: float = attrs.field(default=100.0)
    character_ability_used: bool = attrs.field(default=False)
    
    @functools.cached_property
    def average_uptime(self) -> float:
        """Calculate average uptime using statistics"""
        if not self.uptime_history:
            return self.current_uptime
        return sum(self.uptime_history) / len(self.uptime_history)
    
    @property
    def performance_score(self) -> float:
        """Complex performance calculation using walrus operator"""
        if (service_count := len(self.services)) == 0:
            return 0.0
        
        # Use functools.reduce for complex calculation
        base_score = self.current_uptime * service_count
        history_bonus = self.average_uptime * 0.1
        resource_bonus = self.resources.total_resources * 0.05
        
        return functools.reduce(
            lambda acc, bonus: acc + bonus,
            [base_score, history_bonus, resource_bonus],
            0.0
        )
    
    def record_uptime(self, uptime: float) -> None:
        """Record uptime with automatic history management"""
        self.current_uptime = uptime
        self.uptime_history.append(uptime)


class GameMetrics(BaseModel):
    """Advanced metrics with computed analytics"""
    model_config = ConfigDict(validate_assignment=True)
    
    total_requests: int = Field(default=0, ge=0)
    cascade_failures: int = Field(default=0, ge=0)  
    chaos_events: int = Field(default=0, ge=0)
    services_built: int = Field(default=0, ge=0)
    connections_created: int = Field(default=0, ge=0)
    
    @computed_field
    @property
    def failure_rate(self) -> float:
        """Calculate failure rate percentage"""
        if self.total_requests == 0:
            return 0.0
        return (self.cascade_failures / self.total_requests) * 100
    
    @computed_field  
    @property
    def complexity_score(self) -> float:
        """Advanced complexity metric"""
        return (self.services_built * 1.5 + 
                self.connections_created * 2.0 + 
                self.chaos_events * 0.5)


class AdvancedGameState(BaseModel):
    """Ultra-modern game state with all advanced features"""
    model_config = ConfigDict(
        validate_assignment=True,
        extra='forbid',
        frozen=False
    )
    
    game_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    round: Annotated[int, Field(ge=1, le=50)] = 1
    phase: Literal["setup", "traffic", "action", "resolution", "chaos", "end"] = "setup"
    players: list[Player] = Field(default_factory=list)
    services: dict[str, Service] = Field(default_factory=dict)
    grid_width: Annotated[int, Field(ge=4, le=20)] = 8
    grid_height: Annotated[int, Field(ge=4, le=20)] = 6
    entropy: Annotated[int, Field(ge=0, le=20)] = 0
    metrics: GameMetrics = Field(default_factory=GameMetrics)
    action_log: list[dict[str, Any]] = Field(default_factory=list)
    current_player_index: int = Field(default=0, ge=0)
    
    @computed_field
    @property 
    def current_player(self) -> Player | None:
        """Get current player safely"""
        if 0 <= self.current_player_index < len(self.players):
            return self.players[self.current_player_index]
        return None
    
    @computed_field
    @property
    def service_grid(self) -> dict[HexCoordinate, str]:
        """Generate service grid mapping using dict comprehension"""
        return {service.location: service_id 
                for service_id, service in self.services.items()}
    
    @model_validator(mode='after')
    def validate_game_state(self) -> AdvancedGameState:
        """Comprehensive game state validation"""
        if self.current_player_index >= len(self.players):
            raise ValueError("Current player index out of bounds")
        
        # Validate service locations are within grid
        for service in self.services.values():
            if not (0 <= service.location.row < self.grid_height and
                    0 <= service.location.col < self.grid_width):
                raise ValueError(f"Service {service.id} outside grid bounds")
        
        return self
    
    @functools.lru_cache(maxsize=256)
    def get_adjacent_services(self, coord: HexCoordinate) -> tuple[str, ...]:
        """Get adjacent services with caching"""
        grid = self.service_grid
        return tuple(grid.get(neighbor) 
                    for neighbor in coord.neighbors() 
                    if (neighbor in grid))
    
    def add_service(self, service: Service) -> bool:
        """Add service with validation and logging"""
        try:
            # Check grid bounds and availability
            if not (0 <= service.location.row < self.grid_height and
                    0 <= service.location.col < self.grid_width):
                return False
                
            if service.location in self.service_grid:
                return False
            
            # Add service
            self.services[service.id] = service
            self.players[service.owner_id].services.append(service.id)
            self.metrics.services_built += 1
            
            # Log action with rich context
            self.log_action(
                action_type="build_service",
                player_id=service.owner_id,
                parameters={
                    "service_type": service.service_type.value,
                    "location": {"row": service.location.row, "col": service.location.col},
                    "service_id": service.id
                }
            )
            
            log.info("Service built successfully",
                    service_id=service.id,
                    service_type=service.service_type.value,
                    location=f"({service.location.row},{service.location.col})",
                    owner=self.players[service.owner_id].name)
            
            return True
            
        except Exception as e:
            log.error("Failed to add service", error=str(e), service_id=service.id)
            return False
    
    def log_action(self, action_type: str, player_id: int, parameters: dict[str, Any]) -> None:
        """Enhanced action logging with structured data"""
        action = {
            "timestamp": datetime.now().isoformat(),
            "round": self.round,
            "phase": self.phase,
            "action_type": action_type,
            "player_id": player_id,
            "parameters": parameters,
            "game_state_hash": hash(str(self.model_dump()))  # State fingerprint
        }
        self.action_log.append(action)
    
    def next_phase(self) -> None:
        """Advanced phase transition with pattern matching"""
        match self.phase:
            case "setup":
                self.phase = "traffic"
            case "traffic":
                self.phase = "action"
            case "action":
                self.phase = "resolution"
            case "resolution":
                self.phase = "chaos"
            case "chaos":
                self._end_round()
            case "end":
                pass  # Game over
    
    def _end_round(self) -> None:
        """End round with comprehensive state updates"""
        self.round += 1
        self.phase = "traffic"
        self.current_player_index = 0
        
        # Reset player actions using list comprehension
        for player in self.players:
            player.actions_remaining = 3
            player.character_ability_used = False
        
        # Update metrics
        player_uptimes = [p.current_uptime for p in self.players]
        self.metrics.model_rebuild()  # Recompute computed fields
        
        log.info("Round completed", 
                round=self.round,
                player_uptimes=player_uptimes,
                total_services=len(self.services))
    
    def is_game_over(self) -> bool:
        """Check end conditions using advanced logic"""
        return (self.round > 20 or 
                all(p.current_uptime <= 0 for p in self.players) or
                self.phase == "end")
    
    def get_winner(self) -> Player | None:
        """Determine winner using sophisticated scoring"""
        if not self.is_game_over():
            return None
        
        # Use max with key function for performance scoring
        return max(self.players, key=lambda p: p.performance_score, default=None)
    
    def display_rich_status(self) -> None:
        """Rich console output with tables and trees"""
        console.clear()
        
        # Main game info
        table = Table(title=f"🎮 Pipeline & Peril - Round {self.round} ({self.phase.title()})")
        table.add_column("Player", style="cyan")
        table.add_column("Uptime", style="green")
        table.add_column("Resources", style="yellow") 
        table.add_column("Services", style="blue")
        table.add_column("Score", style="magenta")
        
        for player in self.players:
            resources_str = f"CPU:{player.resources.cpu} MEM:{player.resources.memory} STO:{player.resources.storage}"
            table.add_row(
                f"{'👑 ' if player == self.current_player else ''}{player.name}",
                f"{player.current_uptime:.1f}%",
                resources_str,
                str(len(player.services)),
                f"{player.performance_score:.1f}"
            )
        
        console.print(table)
        
        # Service grid visualization
        grid_tree = Tree("🗺️ Service Grid")
        for row in range(self.grid_height):
            row_branch = grid_tree.add(f"Row {row}")
            for col in range(self.grid_width):
                coord = HexCoordinate(row, col)
                if coord in self.service_grid:
                    service_id = self.service_grid[coord]
                    service = self.services[service_id]
                    row_branch.add(f"({row},{col}): {service.service_type.emoji} {service.service_type.value}")
                else:
                    row_branch.add(f"({row},{col}): ⬜ empty")
        
        console.print(grid_tree)


# Factory functions using functools.partial
create_compute_service = functools.partial(Service, service_type=ServiceType.COMPUTE)
create_database_service = functools.partial(Service, service_type=ServiceType.DATABASE)


async def simulate_game_async(player_names: list[str]) -> AdvancedGameState:
    """Async game simulation demonstrating modern patterns"""
    game = AdvancedGameState()
    
    # Create players using list comprehension with enumeration
    game.players = [
        Player(id=i, name=name) 
        for i, name in enumerate(player_names)
    ]
    
    # Use asyncio.gather for concurrent operations
    tasks = [
        asyncio.create_task(initialize_player_services(game, player))
        for player in game.players
    ]
    
    await asyncio.gather(*tasks)
    
    # Main game loop with rich progress
    with Progress() as progress:
        task = progress.add_task("Simulating game...", total=20)
        
        while not game.is_game_over():
            # Execute phase logic
            match game.phase:
                case "traffic":
                    await handle_traffic_phase(game)
                case "action":
                    await handle_action_phase(game)
                case "resolution":
                    await handle_resolution_phase(game)
                case "chaos":
                    await handle_chaos_phase(game)
            
            game.next_phase()
            progress.update(task, completed=game.round)
            
            # Rich display update
            game.display_rich_status()
            await asyncio.sleep(0.1)  # Smooth animation
    
    return game


async def initialize_player_services(game: AdvancedGameState, player: Player) -> None:
    """Initialize starting services for player"""
    starting_types = [ServiceType.COMPUTE, ServiceType.DATABASE, ServiceType.LOAD_BALANCER]
    
    for i, service_type in enumerate(starting_types):
        coord = HexCoordinate(player.id * 2, i * 2)
        service = Service(
            service_type=service_type,
            location=coord,
            owner_id=player.id
        )
        game.add_service(service)


async def handle_traffic_phase(game: AdvancedGameState) -> None:
    """Handle traffic phase with async operations"""
    # Simulate traffic generation
    traffic = functools.reduce(lambda x, y: x + y, [
        len(player.services) * 2 for player in game.players
    ], 0)
    
    game.metrics.total_requests += traffic
    log.info("Traffic phase completed", traffic_generated=traffic)


async def handle_action_phase(game: AdvancedGameState) -> None:
    """Handle action phase with player AI"""
    for player in game.players:
        while player.actions_remaining > 0:
            # Simple AI: build service if resources allow
            if player.resources.total_resources >= 4:
                # Find empty spot
                for row, col in itertools.product(range(game.grid_height), range(game.grid_width)):
                    coord = HexCoordinate(row, col)
                    if coord not in game.service_grid:
                        service = Service(
                            service_type=ServiceType.COMPUTE,
                            location=coord,
                            owner_id=player.id
                        )
                        costs = service.service_type.costs
                        if player.resources.spend(costs):
                            game.add_service(service)
                            player.actions_remaining -= 1
                            break
            else:
                break


async def handle_resolution_phase(game: AdvancedGameState) -> None:
    """Handle resolution with cascade failure simulation"""
    # Simple uptime calculation
    for player in game.players:
        if player.services:
            base_uptime = min(100.0, len(player.services) * 20)
            noise = (hash(str(game.round)) % 20) - 10  # Deterministic "randomness"
            uptime = max(0, base_uptime + noise)
            player.record_uptime(uptime)


async def handle_chaos_phase(game: AdvancedGameState) -> None:
    """Handle chaos events with pattern matching"""
    if game.entropy > 3:
        chaos_roll = (hash(str(game.round * game.entropy)) % 8) + 1
        
        match chaos_roll:
            case 1 | 2:  # Minor glitch
                log.info("Chaos event: Minor glitch")
            case 3 | 4:  # Network congestion  
                log.info("Chaos event: Network congestion")
            case 5 | 6:  # Memory leak
                log.info("Chaos event: Memory leak")
            case 7 | 8:  # Major failure
                game.metrics.cascade_failures += 1
                log.warning("Chaos event: Cascade failure")
        
        game.metrics.chaos_events += 1
    
    game.entropy = min(10, game.entropy + 1)


# Example usage with rich output
if __name__ == "__main__":
    async def main():
        game = await simulate_game_async(["Alice", "Bob", "Charlie"])
        
        console.print("\n🏆 Game Complete!")
        winner = game.get_winner()
        if winner:
            console.print(f"Winner: {winner.name} with score {winner.performance_score:.1f}")
        else:
            console.print("Cooperative victory achieved!")
    
    asyncio.run(main())