#!/usr/bin/env python3
"""
🎮 Pipeline & Peril Demo Script

A showcase demonstration of the digital playtesting system featuring:
- Rich terminal output with live updates
- Modern Python patterns and async operations  
- Statistical analysis and visualization
- Multiple AI strategy testing

Run with: uv run python demo.py
"""

import asyncio
import time
from typing import List

from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, TaskID, BarColumn, TextColumn, TimeRemainingColumn
from rich.table import Table
from rich.text import Text
from rich.align import Align

from src.engine.advanced_game_state import (
    AdvancedGameState, Player, Service, ServiceType, HexCoordinate,
    simulate_game_async, console, log
)

# Initialize rich console
demo_console = Console()

class GameDemo:
    """Comprehensive demo showcasing all features"""
    
    def __init__(self):
        self.console = Console()
        self.games_completed = 0
        self.total_games = 10
        
    async def run_full_demo(self):
        """Run complete demonstration"""
        self.console.clear()
        
        with Live(self.create_layout(), refresh_per_second=4) as live:
            await self.demo_introduction(live)
            await self.demo_single_game(live)
            await self.demo_batch_analysis(live)
            await self.demo_conclusion(live)
    
    def create_layout(self) -> Layout:
        """Create rich layout for demo display"""
        layout = Layout()
        
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=3)
        )
        
        layout["main"].split_row(
            Layout(name="left"),
            Layout(name="right")
        )
        
        return layout
    
    def update_header(self, layout: Layout, title: str, subtitle: str = ""):
        """Update header with current demo section"""
        header_text = Text(title, style="bold magenta")
        if subtitle:
            header_text.append(f"\n{subtitle}", style="dim cyan")
        
        layout["header"].update(
            Panel(Align.center(header_text), title="🎮 Pipeline & Peril Demo")
        )
    
    def update_footer(self, layout: Layout, status: str):
        """Update footer with current status"""
        layout["footer"].update(
            Panel(Align.center(Text(status, style="bold green")), 
                  title="Status")
        )
    
    async def demo_introduction(self, live: Live):
        """Introduction and feature overview"""
        layout = live.layout
        
        self.update_header(layout, "Welcome to Pipeline & Peril!", 
                          "Digital Playtesting System Demonstration")
        
        # Feature showcase
        features_table = Table(title="🚀 Modern Python Features Demonstrated")
        features_table.add_column("Feature", style="cyan")
        features_table.add_column("Implementation", style="yellow")
        features_table.add_column("Benefit", style="green")
        
        features = [
            ("Pattern Matching", "match/case statements", "Clean game logic"),
            ("Pydantic v2", "@computed_field properties", "Type-safe validation"),
            ("Rich Console", "Live layouts & progress", "Beautiful CLI"),
            ("Async/Await", "Concurrent simulations", "High performance"),
            ("Functional Tools", "functools.lru_cache", "Optimized operations"),
            ("Structural Logging", "structlog + loguru", "Debug insights"),
        ]
        
        for feature, impl, benefit in features:
            features_table.add_row(feature, impl, benefit)
        
        layout["left"].update(Panel(features_table))
        
        # Game overview
        game_info = Text()
        game_info.append("🎯 Game Concept\n", style="bold blue")
        game_info.append("Pipeline & Peril simulates distributed systems management.\n\n")
        game_info.append("🏗️ Core Mechanics\n", style="bold blue")
        game_info.append("• Build services on hexagonal grid\n")
        game_info.append("• Manage CPU, Memory, Storage resources\n")
        game_info.append("• Handle traffic and prevent cascade failures\n")
        game_info.append("• Fight entropy and chaos events\n\n")
        game_info.append("🤖 AI Players\n", style="bold blue")
        game_info.append("• Autonomous gameplay for rapid testing\n")
        game_info.append("• Multiple strategy implementations\n")
        game_info.append("• Statistical analysis of outcomes\n")
        
        layout["right"].update(Panel(game_info, title="Game Overview"))
        
        self.update_footer(layout, "Press Ctrl+C to skip sections • Demo starting in 3 seconds...")
        await asyncio.sleep(3)
    
    async def demo_single_game(self, live: Live):
        """Demonstrate single game with live updates"""
        layout = live.layout
        
        self.update_header(layout, "Single Game Demonstration", 
                          "Watch AI players compete in real-time")
        
        # Create game state
        game = AdvancedGameState()
        game.players = [
            Player(id=0, name="🤖 AlphaBot"),
            Player(id=1, name="🧠 BetaAI"), 
            Player(id=2, name="⚡ GammaSpeed")
        ]
        
        # Progress tracking
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeRemainingColumn(),
        ) as progress:
            
            game_task = progress.add_task("Game Progress", total=20)
            
            # Game simulation loop
            for round_num in range(1, 21):
                game.round = round_num
                
                # Simulate phase progression
                phases = ["traffic", "action", "resolution", "chaos"]
                for phase in phases:
                    game.phase = phase
                    
                    # Update display
                    self.update_game_display(layout, game, progress)
                    
                    # Simulate phase processing
                    await self.simulate_phase(game, phase)
                    await asyncio.sleep(0.2)  # Smooth animation
                
                progress.update(game_task, completed=round_num)
                
                # Check game end conditions
                if round_num >= 10 and all(p.current_uptime > 80 for p in game.players):
                    self.update_footer(layout, "🎉 Cooperative Victory Achieved!")
                    break
        
        await asyncio.sleep(2)
    
    def update_game_display(self, layout: Layout, game: AdvancedGameState, progress: Progress):
        """Update game state display"""
        # Player status table
        players_table = Table(title=f"Round {game.round} - {game.phase.title()} Phase")
        players_table.add_column("Player", style="cyan")
        players_table.add_column("Uptime", style="green")
        players_table.add_column("Services", style="blue") 
        players_table.add_column("Resources", style="yellow")
        players_table.add_column("Score", style="magenta")
        
        for player in game.players:
            resources = f"{player.resources.cpu}💾 {player.resources.memory}🧠 {player.resources.storage}💿"
            players_table.add_row(
                player.name,
                f"{player.current_uptime:.1f}%",
                str(len(player.services)),
                resources,
                f"{player.performance_score:.1f}"
            )
        
        layout["left"].update(Panel(players_table))
        
        # Game metrics
        metrics_text = Text()
        metrics_text.append(f"🎮 Game Metrics\n", style="bold blue")
        metrics_text.append(f"Round: {game.round}/20\n")
        metrics_text.append(f"Phase: {game.phase.title()}\n")
        metrics_text.append(f"Entropy: {game.entropy}/10\n")
        metrics_text.append(f"Total Services: {len(game.services)}\n")
        metrics_text.append(f"Requests Handled: {game.metrics.total_requests}\n")
        metrics_text.append(f"Cascade Failures: {game.metrics.cascade_failures}\n")
        
        if game.entropy > 5:
            metrics_text.append(f"\n⚠️ High Entropy Warning!", style="bold red")
        
        layout["right"].update(Panel(metrics_text, title="Live Metrics"))
    
    async def simulate_phase(self, game: AdvancedGameState, phase: str):
        """Simulate game phase with realistic updates"""
        match phase:
            case "traffic":
                # Generate traffic
                traffic = len(game.services) * 2 + (game.round * 1)
                game.metrics.total_requests += traffic
                
            case "action":
                # Simulate AI actions
                for player in game.players:
                    if player.resources.total_resources >= 4:
                        # Build service
                        service = Service(
                            service_type=ServiceType.COMPUTE,
                            location=HexCoordinate(
                                row=game.round % game.grid_height,
                                col=(player.id * 2 + game.round) % game.grid_width
                            ),
                            owner_id=player.id
                        )
                        if game.add_service(service):
                            costs = service.service_type.costs
                            player.resources.spend(costs)
            
            case "resolution":
                # Update player uptimes
                for player in game.players:
                    base_uptime = min(100, len(player.services) * 15 + 25)
                    # Add some deterministic variance
                    variance = (hash(f"{game.round}{player.id}") % 20) - 10
                    uptime = max(0, min(100, base_uptime + variance))
                    player.record_uptime(uptime)
            
            case "chaos":
                # Increase entropy
                game.entropy = min(10, game.entropy + 1)
                if game.entropy > 3:
                    # Chaos event
                    game.metrics.chaos_events += 1
                    if game.entropy > 7:
                        game.metrics.cascade_failures += 1
    
    async def demo_batch_analysis(self, live: Live):
        """Demonstrate batch processing and analysis"""
        layout = live.layout
        
        self.update_header(layout, "Batch Analysis Demo", 
                          "Running multiple games for statistical analysis")
        
        # Results storage
        results = {
            "cooperative_wins": 0,
            "competitive_wins": {"🤖 AlphaBot": 0, "🧠 BetaAI": 0, "⚡ GammaSpeed": 0},
            "average_uptimes": [],
            "game_lengths": [],
            "service_counts": []
        }
        
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeRemainingColumn(),
        ) as progress:
            
            batch_task = progress.add_task("Batch Analysis", total=self.total_games)
            
            for game_num in range(self.total_games):
                # Create and run game
                game = await self.simulate_quick_game()
                
                # Collect statistics
                avg_uptime = sum(p.current_uptime for p in game.players) / len(game.players)
                results["average_uptimes"].append(avg_uptime)
                results["game_lengths"].append(game.round)
                results["service_counts"].append(len(game.services))
                
                # Determine winner
                if avg_uptime > 80:
                    results["cooperative_wins"] += 1
                else:
                    winner = max(game.players, key=lambda p: p.performance_score)
                    results["competitive_wins"][winner.name] += 1
                
                # Update display
                self.update_analysis_display(layout, results, game_num + 1)
                progress.update(batch_task, completed=game_num + 1)
                
                await asyncio.sleep(0.1)
        
        await asyncio.sleep(3)
    
    async def simulate_quick_game(self) -> AdvancedGameState:
        """Quick game simulation for batch analysis"""
        game = AdvancedGameState()
        game.players = [
            Player(id=0, name="🤖 AlphaBot"),
            Player(id=1, name="🧠 BetaAI"),
            Player(id=2, name="⚡ GammaSpeed")
        ]
        
        # Fast simulation
        for round_num in range(1, 21):
            game.round = round_num
            
            # Quick phase simulation
            game.metrics.total_requests += len(game.services) * 2
            
            # Add services
            for player in game.players:
                if player.resources.total_resources >= 4 and round_num % 3 == player.id:
                    service = Service(
                        service_type=ServiceType.COMPUTE,
                        location=HexCoordinate(
                            row=(round_num + player.id) % game.grid_height,
                            col=(round_num * 2 + player.id) % game.grid_width
                        ),
                        owner_id=player.id
                    )
                    if game.add_service(service):
                        costs = service.service_type.costs
                        player.resources.spend(costs)
            
            # Update uptimes
            for player in game.players:
                base = min(100, len(player.services) * 12 + 30)
                variance = (hash(f"{round_num}{player.id}") % 30) - 15
                uptime = max(0, min(100, base + variance))
                player.record_uptime(uptime)
            
            # Check victory
            avg_uptime = sum(p.current_uptime for p in game.players) / len(game.players)
            if round_num >= 10 and avg_uptime > 80:
                break
        
        return game
    
    def update_analysis_display(self, layout: Layout, results: dict, games_completed: int):
        """Update batch analysis display"""
        # Results table
        analysis_table = Table(title=f"Analysis Results ({games_completed}/{self.total_games} games)")
        analysis_table.add_column("Metric", style="cyan")
        analysis_table.add_column("Value", style="yellow")
        analysis_table.add_column("Insight", style="green")
        
        if results["average_uptimes"]:
            avg_uptime = sum(results["average_uptimes"]) / len(results["average_uptimes"])
            avg_length = sum(results["game_lengths"]) / len(results["game_lengths"])
            avg_services = sum(results["service_counts"]) / len(results["service_counts"])
            
            analysis_table.add_row(
                "Average Uptime", 
                f"{avg_uptime:.1f}%",
                "😊 Good" if avg_uptime > 75 else "⚠️ Needs Tuning"
            )
            analysis_table.add_row(
                "Average Game Length",
                f"{avg_length:.1f} rounds",
                "⚡ Quick" if avg_length < 15 else "🐌 Long"
            )
            analysis_table.add_row(
                "Services per Game",
                f"{avg_services:.1f}",
                "🏗️ Active Building"
            )
            analysis_table.add_row(
                "Cooperative Wins",
                f"{results['cooperative_wins']}/{games_completed}",
                "🤝 Balanced" if results['cooperative_wins'] > 0 else "⚔️ Competitive"
            )
        
        layout["left"].update(Panel(analysis_table))
        
        # Win distribution
        wins_text = Text()
        wins_text.append("🏆 Victory Distribution\n", style="bold blue")
        
        total_competitive = sum(results["competitive_wins"].values())
        for player, wins in results["competitive_wins"].items():
            if total_competitive > 0:
                percentage = (wins / total_competitive) * 100
                wins_text.append(f"{player}: {wins} wins ({percentage:.1f}%)\n")
            else:
                wins_text.append(f"{player}: {wins} wins\n")
        
        wins_text.append(f"\nCooperative Victories: {results['cooperative_wins']}\n")
        wins_text.append(f"Competitive Victories: {total_competitive}\n")
        
        layout["right"].update(Panel(wins_text, title="Victory Analytics"))
    
    async def demo_conclusion(self, live: Live):
        """Demo conclusion and next steps"""
        layout = live.layout
        
        self.update_header(layout, "Demo Complete!", 
                          "Pipeline & Peril Digital Playtesting System")
        
        # Summary
        summary_text = Text()
        summary_text.append("🎉 Demonstration Complete\n\n", style="bold green")
        summary_text.append("✅ Features Demonstrated:\n", style="bold blue")
        summary_text.append("• Modern Python 3.13+ patterns\n")
        summary_text.append("• Rich console UI with live updates\n")
        summary_text.append("• Async game simulation\n")
        summary_text.append("• Statistical batch analysis\n")
        summary_text.append("• Comprehensive logging\n")
        summary_text.append("• Type-safe validation\n\n")
        
        summary_text.append("🚀 Next Steps:\n", style="bold yellow")
        summary_text.append("• Run: uv run python demo.py\n")
        summary_text.append("• Test: uv run pytest tests/\n")
        summary_text.append("• Analyze: python scripts/analyze_balance.py\n")
        summary_text.append("• Extend: Add your own AI strategies\n")
        
        layout["left"].update(Panel(summary_text))
        
        # Repository info
        repo_text = Text()
        repo_text.append("📚 Repository Information\n", style="bold blue")
        repo_text.append("GitHub: github.com/jwalsh/pipeline-and-peril-001\n")
        repo_text.append("License: MIT\n")
        repo_text.append("Topics: board-game, pygame, python, distributed-systems, simulation\n\n")
        
        repo_text.append("🤝 Contributing:\n", style="bold green")
        repo_text.append("• Fork and create feature branches\n")
        repo_text.append("• Add comprehensive tests\n")
        repo_text.append("• Document decisions in git notes\n")
        repo_text.append("• Submit pull requests\n\n")
        
        repo_text.append("📞 Contact:\n", style="bold cyan")
        repo_text.append("@jwalsh on GitHub\n")
        
        layout["right"].update(Panel(repo_text, title="Project Info"))
        
        self.update_footer(layout, "Thank you for watching the demo! 🎮✨")
        await asyncio.sleep(5)


async def main():
    """Main demo entry point"""
    demo = GameDemo()
    
    try:
        await demo.run_full_demo()
    except KeyboardInterrupt:
        demo_console.print("\n[yellow]Demo interrupted by user[/yellow]")
    except Exception as e:
        demo_console.print(f"\n[red]Demo error: {e}[/red]")
    finally:
        demo_console.print("\n[green]Demo complete! Run 'uv run python demo.py' to see it again.[/green]")


if __name__ == "__main__":
    asyncio.run(main())