#!/usr/bin/env python3
"""
Rich Console Demo for Pipeline & Peril
Beautiful terminal output for screenshots
"""

import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from rich.tree import Tree
from rich.text import Text
from rich.align import Align
from rich.layout import Layout
from rich.live import Live

from src.engine.simple_game_state import GameState, Player, Service, ServiceType, HexCoordinate

console = Console()

def create_rich_demo():
    """Create rich demo game with interesting state"""
    game = GameState()
    
    # Add players with varied stats
    game.players = [
        Player(id=0, name="🤖 AlphaBot", cpu=8, memory=6, storage=4, current_uptime=95.2),
        Player(id=1, name="🧠 BetaAI", cpu=3, memory=9, storage=7, current_uptime=88.7),
        Player(id=2, name="⚡ GammaSpeed", cpu=6, memory=4, storage=8, current_uptime=92.1),
        Player(id=3, name="🛡️ DefenseBot", cpu=2, memory=8, storage=9, current_uptime=97.8)
    ]
    
    # Add variety of services
    services = [
        Service("svc1", ServiceType.COMPUTE, HexCoordinate(1, 1), 0),
        Service("svc2", ServiceType.DATABASE, HexCoordinate(1, 2), 0),
        Service("svc3", ServiceType.LOAD_BALANCER, HexCoordinate(2, 1), 1),
        Service("svc4", ServiceType.CACHE, HexCoordinate(3, 3), 2),
        Service("svc5", ServiceType.API_GATEWAY, HexCoordinate(0, 4), 3),
        Service("svc6", ServiceType.QUEUE, HexCoordinate(4, 2), 1),
        Service("svc7", ServiceType.COMPUTE, HexCoordinate(2, 5), 2),
        Service("svc8", ServiceType.DATABASE, HexCoordinate(5, 1), 3),
    ]
    
    for service in services:
        game.add_service(service)
    
    game.round = 7
    return game

def display_title():
    """Display fancy title"""
    title = Text("🎮 Pipeline & Peril", style="bold magenta")
    subtitle = Text("Digital Playtesting System - Live Demo", style="dim cyan")
    
    title_panel = Panel(
        Align.center(f"{title}\n{subtitle}"),
        title="Game Engine Showcase",
        border_style="bright_blue"
    )
    console.print(title_panel)

def display_player_table(game):
    """Display players in a rich table"""
    table = Table(title=f"🏆 Round {game.round} Status", show_header=True, header_style="bold cyan")
    table.add_column("Player", style="white", min_width=12)
    table.add_column("CPU", style="red", justify="center")
    table.add_column("Memory", style="yellow", justify="center") 
    table.add_column("Storage", style="green", justify="center")
    table.add_column("Services", style="blue", justify="center")
    table.add_column("Uptime", style="magenta", justify="center")
    table.add_column("Status", style="bright_green")
    
    for player in game.players:
        # Determine status
        if player.current_uptime > 95:
            status = "🟢 Excellent"
        elif player.current_uptime > 85:
            status = "🟡 Good"
        else:
            status = "🔴 Critical"
        
        table.add_row(
            player.name,
            f"{player.cpu}💾",
            f"{player.memory}🧠", 
            f"{player.storage}💿",
            f"{len(player.services)}🏗️",
            f"{player.current_uptime:.1f}%",
            status
        )
    
    return table

def display_service_grid(game):
    """Display service grid as a tree"""
    tree = Tree("🗺️ Service Grid Layout")
    
    # Group services by type
    service_types = {}
    for service in game.services.values():
        if service.service_type not in service_types:
            service_types[service.service_type] = []
        service_types[service.service_type].append(service)
    
    for service_type, services in service_types.items():
        type_branch = tree.add(f"{service_type.value.replace('_', ' ').title()} ({len(services)})")
        for service in services:
            owner_name = game.players[service.owner_id].name
            type_branch.add(f"[{service.location.row},{service.location.col}] - {owner_name}")
    
    return tree

def display_metrics(game):
    """Display game metrics"""
    metrics_text = Text()
    metrics_text.append("📊 Game Metrics\n", style="bold blue")
    metrics_text.append(f"Round: {game.round}/20\n")
    metrics_text.append(f"Phase: Action\n", style="yellow")
    metrics_text.append(f"Total Services: {len(game.services)}\n")
    metrics_text.append(f"Grid Size: {game.grid_width}×{game.grid_height}\n")
    
    avg_uptime = sum(p.current_uptime for p in game.players) / len(game.players)
    metrics_text.append(f"Average Uptime: {avg_uptime:.1f}%\n")
    
    if avg_uptime > 90:
        metrics_text.append("🎯 System Stable", style="bold green")
    elif avg_uptime > 80:
        metrics_text.append("⚠️ Monitor Closely", style="bold yellow")
    else:
        metrics_text.append("🚨 Critical Issues", style="bold red")
    
    return Panel(metrics_text, title="Live Metrics", border_style="green")

def display_feature_showcase():
    """Display modern Python features"""
    features_table = Table(title="🚀 Modern Python Features Demo", show_header=True)
    features_table.add_column("Feature", style="cyan")
    features_table.add_column("Usage", style="yellow")
    features_table.add_column("Benefit", style="green")
    
    features = [
        ("Rich Console", "Beautiful CLI output", "Professional UX"),
        ("Dataclasses", "Clean data structures", "Type safety"),
        ("Enums", "Service types", "Code clarity"),
        ("f-strings", "String formatting", "Readability"),
        ("Type Hints", "Function annotations", "IDE support"),
        ("uv Package Manager", "Fast dependencies", "Quick setup")
    ]
    
    for feature, usage, benefit in features:
        features_table.add_row(feature, usage, benefit)
    
    return features_table

def display_game_info():
    """Display game concept info"""
    info_text = Text()
    info_text.append("🎯 Game Concept\n", style="bold blue")
    info_text.append("Build and maintain distributed systems\n")
    info_text.append("while fighting entropy and chaos events.\n\n")
    
    info_text.append("🏗️ Core Mechanics\n", style="bold yellow")
    info_text.append("• Place services on hexagonal grid\n")
    info_text.append("• Manage CPU, Memory, Storage\n")
    info_text.append("• Handle traffic and prevent failures\n")
    info_text.append("• Survive chaos events\n\n")
    
    info_text.append("🤖 AI Features\n", style="bold green")
    info_text.append("• Autonomous gameplay\n")
    info_text.append("• Statistical analysis\n") 
    info_text.append("• Strategy testing\n")
    info_text.append("• LLM integration ready\n")
    
    return Panel(info_text, title="About Pipeline & Peril", border_style="magenta")

def run_live_demo():
    """Run live updating demo"""
    game = create_rich_demo()
    
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main"),
        Layout(name="footer", size=8)
    )
    
    layout["main"].split_row(
        Layout(name="left"),
        Layout(name="right")
    )
    
    layout["footer"].split_row(
        Layout(name="features"),
        Layout(name="info")
    )
    
    with Live(layout, refresh_per_second=2) as live:
        for i in range(20):
            # Update header
            header_text = Text(f"🎮 Pipeline & Peril - Live Demo (Update {i+1}/20)", style="bold magenta")
            layout["header"].update(Panel(Align.center(header_text), border_style="bright_blue"))
            
            # Update main content
            layout["left"].update(display_player_table(game))
            layout["right"].update(Columns([display_service_grid(game), display_metrics(game)]))
            
            # Update footer
            layout["features"].update(display_feature_showcase())
            layout["info"].update(display_game_info())
            
            # Simulate game changes
            if i % 3 == 0:
                # Update uptimes
                for player in game.players:
                    import random
                    player.current_uptime += random.uniform(-2, 3)
                    player.current_uptime = max(75, min(100, player.current_uptime))
            
            time.sleep(1)

def main():
    """Main demo function"""
    console.clear()
    
    # Static display for screenshots
    display_title()
    console.print()
    
    game = create_rich_demo()
    
    # Display components
    console.print(display_player_table(game))
    console.print()
    
    columns = Columns([
        display_service_grid(game), 
        display_metrics(game)
    ])
    console.print(columns)
    console.print()
    
    footer_columns = Columns([
        display_feature_showcase(),
        display_game_info()
    ])
    console.print(footer_columns)
    
    console.print()
    console.print(Panel(
        Align.center(Text("Repository: github.com/jwalsh/pipeline-and-peril-001", style="bold cyan")),
        title="🚀 Get Started",
        border_style="bright_green"
    ))
    
    # Optionally run live demo
    user_input = input("\nRun live demo? (y/N): ")
    if user_input.lower() == 'y':
        console.clear()
        run_live_demo()

if __name__ == "__main__":
    main()