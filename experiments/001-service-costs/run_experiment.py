#!/usr/bin/env python3
"""
Run service cost optimization experiment for Pipeline & Peril.

This script simulates games with different service cost configurations
to find the optimal balance for gameplay.
"""

import argparse
import json
import logging
import random
import sys
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import yaml

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent / "digital" / "pygame"))

from src.engine.simple_game_state import (
    GameState, Player, Service, ServiceType, HexCoordinate
)


@dataclass
class ExperimentConfig:
    """Configuration for a single experiment run"""
    service_costs: Dict[str, Dict[str, int]]
    games: int
    players: int
    strategy: str
    grid_width: int = 8
    grid_height: int = 6
    max_rounds: int = 20
    victory_threshold: float = 0.8
    seed: Optional[int] = None


@dataclass
class GameResult:
    """Result from a single game simulation"""
    game_id: str
    rounds: int
    winner: Optional[str]
    services_built: int
    avg_uptime: float
    resource_starvation_events: int
    chaos_events: int
    cooperative_victory: bool
    service_usage: Dict[str, int]
    final_scores: Dict[str, float]
    

class ServiceCostExperiment:
    """Main experiment runner for service cost optimization"""
    
    def __init__(self, config: ExperimentConfig):
        self.config = config
        if config.seed:
            random.seed(config.seed)
        self.setup_logging()
        
    def setup_logging(self):
        """Configure logging for the experiment"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
    def run_single_game(self) -> GameResult:
        """Run a single game with the configured costs"""
        game = GameState()
        
        # Initialize players
        game.players = [
            Player(id=i, name=f"Player_{i}")
            for i in range(self.config.players)
        ]
        
        # Apply custom service costs
        self.apply_service_costs(game)
        
        # Game simulation variables
        rounds = 0
        services_built = 0
        resource_starvation = 0
        chaos_events = 0
        service_usage = {st.value: 0 for st in ServiceType}
        
        # Run game simulation
        while rounds < self.config.max_rounds:
            rounds += 1
            
            # Simulate round phases
            services_built += self.simulate_action_phase(game, service_usage)
            resource_starvation += self.check_resource_starvation(game)
            chaos_events += self.simulate_chaos_phase(game, rounds)
            
            # Update player uptimes
            self.update_uptimes(game)
            
            # Check victory conditions
            avg_uptime = sum(p.current_uptime for p in game.players) / len(game.players)
            if rounds >= 10 and avg_uptime >= self.config.victory_threshold * 100:
                # Cooperative victory
                return self.create_result(
                    game, rounds, None, services_built,
                    avg_uptime, resource_starvation, chaos_events,
                    True, service_usage
                )
            
            # Check for elimination
            active_players = [p for p in game.players if p.current_uptime > 0]
            if len(active_players) <= 1:
                winner = active_players[0].name if active_players else None
                return self.create_result(
                    game, rounds, winner, services_built,
                    avg_uptime, resource_starvation, chaos_events,
                    False, service_usage
                )
        
        # Game ended by round limit
        winner = max(game.players, key=lambda p: p.current_uptime).name
        avg_uptime = sum(p.current_uptime for p in game.players) / len(game.players)
        
        return self.create_result(
            game, rounds, winner, services_built,
            avg_uptime, resource_starvation, chaos_events,
            False, service_usage
        )
    
    def apply_service_costs(self, game: GameState):
        """Apply custom service costs from configuration"""
        # This would modify the service creation to use custom costs
        # For simplicity, we track them separately
        pass
    
    def simulate_action_phase(self, game: GameState, usage: Dict[str, int]) -> int:
        """Simulate player actions and return services built"""
        services_built = 0
        
        for player in game.players:
            # Simple AI: try to build services based on strategy
            if self.can_afford_any_service(player):
                service_type = self.choose_service_type(player, game)
                if service_type and self.try_build_service(game, player, service_type):
                    services_built += 1
                    usage[service_type.value] += 1
                    
        return services_built
    
    def can_afford_any_service(self, player: Player) -> bool:
        """Check if player can afford any service"""
        # Check against configured costs
        for service_type in ServiceType:
            costs = self.config.service_costs.get(service_type.value, {})
            if (player.cpu >= costs.get('cpu', 0) and
                player.memory >= costs.get('memory', 0) and
                player.storage >= costs.get('storage', 0)):
                return True
        return False
    
    def choose_service_type(self, player: Player, game: GameState) -> Optional[ServiceType]:
        """Choose which service type to build based on strategy"""
        affordable = []
        
        for service_type in ServiceType:
            costs = self.config.service_costs.get(service_type.value, {})
            if (player.cpu >= costs.get('cpu', 0) and
                player.memory >= costs.get('memory', 0) and
                player.storage >= costs.get('storage', 0)):
                affordable.append(service_type)
        
        if not affordable:
            return None
            
        # Strategy-based selection
        if self.config.strategy == "balanced":
            return random.choice(affordable)
        elif self.config.strategy == "aggressive":
            # Prefer high-capacity services
            return max(affordable, 
                      key=lambda st: self.config.service_costs[st.value].get('capacity', 1))
        else:
            return affordable[0]
    
    def try_build_service(self, game: GameState, player: Player, 
                         service_type: ServiceType) -> bool:
        """Try to build a service, return success"""
        # Find empty location
        for row in range(game.grid_height):
            for col in range(game.grid_width):
                coord = HexCoordinate(row, col)
                if self.is_location_empty(game, coord):
                    # Build service
                    service = Service(
                        id=f"svc_{len(game.services)}",
                        service_type=service_type,
                        location=coord,
                        owner_id=player.id
                    )
                    
                    # Deduct costs
                    costs = self.config.service_costs[service_type.value]
                    player.cpu -= costs.get('cpu', 0)
                    player.memory -= costs.get('memory', 0)
                    player.storage -= costs.get('storage', 0)
                    
                    game.add_service(service)
                    return True
        return False
    
    def is_location_empty(self, game: GameState, coord: HexCoordinate) -> bool:
        """Check if a grid location is empty"""
        for service in game.services.values():
            if service.location == coord:
                return False
        return True
    
    def check_resource_starvation(self, game: GameState) -> int:
        """Count players with very low resources"""
        starvation_count = 0
        for player in game.players:
            total_resources = player.cpu + player.memory + player.storage
            if total_resources < 3:  # Less than minimum to build anything
                starvation_count += 1
        return starvation_count
    
    def simulate_chaos_phase(self, game: GameState, round_num: int) -> int:
        """Simulate chaos events"""
        # Simple chaos simulation based on round
        if round_num > 5 and random.random() < 0.3:
            return 1
        return 0
    
    def update_uptimes(self, game: GameState):
        """Update player uptimes based on services"""
        for player in game.players:
            service_count = len(player.services)
            
            # Base uptime from services
            base_uptime = min(100, service_count * 15 + 40)
            
            # Add some randomness
            variance = random.uniform(-5, 5)
            
            # Update uptime
            player.current_uptime = max(0, min(100, base_uptime + variance))
    
    def create_result(self, game: GameState, rounds: int, winner: Optional[str],
                     services_built: int, avg_uptime: float, 
                     resource_starvation: int, chaos_events: int,
                     coop_victory: bool, service_usage: Dict[str, int]) -> GameResult:
        """Create a GameResult from the game state"""
        final_scores = {
            p.name: p.current_uptime for p in game.players
        }
        
        return GameResult(
            game_id=game.game_id,
            rounds=rounds,
            winner=winner,
            services_built=services_built,
            avg_uptime=avg_uptime,
            resource_starvation_events=resource_starvation,
            chaos_events=chaos_events,
            cooperative_victory=coop_victory,
            service_usage=service_usage,
            final_scores=final_scores
        )
    
    def run_experiment(self) -> List[GameResult]:
        """Run the complete experiment"""
        results = []
        
        self.logger.info(f"Starting experiment with {self.config.games} games")
        start_time = time.time()
        
        for i in range(self.config.games):
            if i % 100 == 0:
                self.logger.info(f"Progress: {i}/{self.config.games} games")
            
            result = self.run_single_game()
            results.append(result)
        
        elapsed = time.time() - start_time
        self.logger.info(f"Experiment complete in {elapsed:.2f} seconds")
        self.logger.info(f"Average time per game: {elapsed/self.config.games:.3f} seconds")
        
        return results
    
    def save_results(self, results: List[GameResult], output_path: str):
        """Save results to JSON file"""
        data = {
            "config": asdict(self.config),
            "results": [asdict(r) for r in results],
            "summary": self.calculate_summary(results)
        }
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        self.logger.info(f"Results saved to {output_path}")
    
    def calculate_summary(self, results: List[GameResult]) -> Dict:
        """Calculate summary statistics"""
        total_games = len(results)
        avg_rounds = sum(r.rounds for r in results) / total_games
        coop_wins = sum(1 for r in results if r.cooperative_victory)
        avg_services = sum(r.services_built for r in results) / total_games
        avg_uptime = sum(r.avg_uptime for r in results) / total_games
        
        # Service usage statistics
        total_usage = {}
        for r in results:
            for service, count in r.service_usage.items():
                total_usage[service] = total_usage.get(service, 0) + count
        
        return {
            "total_games": total_games,
            "average_rounds": avg_rounds,
            "cooperative_wins": coop_wins,
            "cooperative_win_rate": coop_wins / total_games,
            "average_services_built": avg_services,
            "average_uptime": avg_uptime,
            "service_usage": total_usage,
            "most_used_service": max(total_usage.items(), key=lambda x: x[1])[0] if total_usage else None
        }


def load_config(config_path: str) -> ExperimentConfig:
    """Load configuration from YAML file"""
    with open(config_path, 'r') as f:
        data = yaml.safe_load(f)
    
    return ExperimentConfig(
        service_costs=data['service_costs'],
        games=data['simulation']['games'],
        players=data['simulation']['players'],
        strategy=data['simulation']['strategy'],
        grid_width=data['simulation'].get('grid_width', 8),
        grid_height=data['simulation'].get('grid_height', 6),
        max_rounds=data['simulation'].get('max_rounds', 20),
        victory_threshold=data['simulation'].get('victory_threshold', 0.8)
    )


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Run service cost optimization experiment"
    )
    parser.add_argument('--config', required=True, help='Path to config YAML')
    parser.add_argument('--games', type=int, help='Override number of games')
    parser.add_argument('--seed', type=int, default=42, help='Random seed')
    parser.add_argument('--output', required=True, help='Output JSON path')
    parser.add_argument('--log', help='Log file path')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Override games if specified
    if args.games:
        config.games = args.games
    
    # Set seed
    config.seed = args.seed
    
    # Setup logging
    if args.log:
        logging.basicConfig(filename=args.log, level=logging.INFO)
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Run experiment
    experiment = ServiceCostExperiment(config)
    results = experiment.run_experiment()
    
    # Save results
    experiment.save_results(results, args.output)
    
    # Print summary
    summary = experiment.calculate_summary(results)
    print(f"\n📊 Experiment Summary:")
    print(f"  Games played: {summary['total_games']}")
    print(f"  Avg rounds: {summary['average_rounds']:.1f}")
    print(f"  Coop win rate: {summary['cooperative_win_rate']:.1%}")
    print(f"  Avg services: {summary['average_services_built']:.1f}")
    print(f"  Avg uptime: {summary['average_uptime']:.1f}%")


if __name__ == "__main__":
    main()