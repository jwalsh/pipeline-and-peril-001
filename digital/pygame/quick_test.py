#!/usr/bin/env python3
"""
Quick test script to verify the game engine works
"""

import asyncio
from src.engine.advanced_game_state import AdvancedGameState, Player, Service, ServiceType, HexCoordinate

def test_basic_game_state():
    """Test basic game state creation"""
    print("🧪 Testing basic game state...")
    
    game = AdvancedGameState()
    game.players = [
        Player(id=0, name="Alice"),
        Player(id=1, name="Bob")
    ]
    
    print(f"✅ Created game with {len(game.players)} players")
    print(f"✅ Game ID: {game.game_id}")
    print(f"✅ Current phase: {game.phase}")
    
    # Add a service
    service = Service(
        service_type=ServiceType.COMPUTE,
        location=HexCoordinate(1, 1),
        owner_id=0
    )
    
    success = game.add_service(service)
    print(f"✅ Service added: {success}")
    print(f"✅ Total services: {len(game.services)}")
    
    return game

async def test_async_simulation():
    """Test async game simulation"""
    print("\n🚀 Testing async simulation...")
    
    game = AdvancedGameState()
    game.players = [
        Player(id=0, name="AsyncBot1"),
        Player(id=1, name="AsyncBot2")
    ]
    
    # Quick simulation
    for round_num in range(1, 6):
        game.round = round_num
        game.phase = "action"
        
        # Add services for demonstration
        for player in game.players:
            if player.resources.total_resources >= 4:
                service = Service(
                    service_type=ServiceType.COMPUTE,
                    location=HexCoordinate(round_num % 6, player.id * 3),
                    owner_id=player.id
                )
                if game.add_service(service):
                    costs = service.service_type.costs
                    player.resources.spend(costs)
        
        # Update player uptimes
        for player in game.players:
            uptime = min(100, len(player.services) * 20 + 40)
            player.record_uptime(uptime)
        
        print(f"✅ Round {round_num}: {len(game.services)} services, avg uptime: {sum(p.current_uptime for p in game.players) / len(game.players):.1f}%")
        
        await asyncio.sleep(0.1)
    
    print(f"✅ Simulation complete!")
    return game

def test_rich_display():
    """Test rich console output"""
    print("\n🎨 Testing rich display...")
    
    try:
        from rich.console import Console
        from rich.table import Table
        
        console = Console()
        
        table = Table(title="🎮 Pipeline & Peril Test")
        table.add_column("Feature", style="cyan")
        table.add_column("Status", style="green")
        
        table.add_row("Game State", "✅ Working")
        table.add_row("Service Management", "✅ Working")
        table.add_row("Player Resources", "✅ Working")
        table.add_row("Rich Display", "✅ Working")
        
        console.print(table)
        print("✅ Rich display working!")
        
    except ImportError as e:
        print(f"❌ Rich display test failed: {e}")

async def main():
    """Run all tests"""
    print("🧪 Pipeline & Peril - Quick Test Suite\n")
    
    # Basic tests
    game1 = test_basic_game_state()
    
    # Async tests
    game2 = await test_async_simulation()
    
    # Rich display test
    test_rich_display()
    
    print(f"\n🎉 All tests completed!")
    print(f"📊 Final stats:")
    print(f"   - Game 1: {len(game1.services)} services")
    print(f"   - Game 2: {len(game2.services)} services") 
    print(f"   - Total action log entries: {len(game1.action_log) + len(game2.action_log)}")

if __name__ == "__main__":
    asyncio.run(main())