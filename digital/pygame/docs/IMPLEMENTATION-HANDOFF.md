# Pipeline & Peril PyGame - Implementation Handoff

## Quick Summary for Implementation Agent

You are tasked with implementing a PyGame version of Pipeline & Peril, a board game about distributed systems. This document provides a quick reference for what needs to be built.

## Core Game Concept

- **Theme**: Players build and maintain distributed systems while fighting entropy
- **Mechanics**: Dice-based actions on a hexagonal grid
- **Goal**: Keep system uptime above threshold while handling traffic

## What You're Building

### 1. Game Engine
- Turn-based game with 4 phases: Traffic → Action → Resolution → Chaos
- 6 types of services (Compute, Database, Cache, Queue, Load Balancer, API Gateway)
- 8×6 hexagonal grid for service placement
- Resource management (CPU, Memory, Storage)
- Dice system using standard RPG dice (d4, d6, d8, d10, d12, d20)

### 2. Autonomous Play System
- AI players that can complete games without human input
- Multiple strategy profiles (aggressive, defensive, balanced)
- Ability to run thousands of games for statistics

### 3. Data Collection
- Log every action and state change
- Export games as JSON/CSV
- Statistical analysis of outcomes
- Replay functionality

### 4. Integration Points
- REST API for external control
- Ollama integration for LLM agents
- Structured input/output for AI agents

## Key Implementation Priorities

1. **Start Simple**: Get basic game loop working with random AI
2. **Rules First**: Implement all game rules before visualization
3. **Test Everything**: Each rule needs unit tests
4. **Performance Matters**: Must handle 1000+ games for analysis
5. **Clean API**: External agents need clear interfaces

## Critical Game Rules to Implement

### Turn Flow
1. Roll 2d10 for incoming requests
2. Each player takes 3 actions
3. Process requests through services
4. Check for cascade failures
5. Roll d8 for chaos events (if entropy > 3)

### Victory Conditions
- Cooperative: >80% uptime for 10 rounds
- Competitive: Highest (uptime × requests)
- Last player standing with >50% uptime

## Required Files to Create

1. `digital/pygame/src/engine/game_state.py` - Core state management
2. `digital/pygame/src/engine/rules_engine.py` - Game rules implementation
3. `digital/pygame/src/players/ai_player.py` - Autonomous player logic
4. `digital/pygame/scripts/run_autonomous.py` - Entry point for testing
5. `digital/pygame/src/integration/ollama_client.py` - LLM integration

## Testing Checklist

- [ ] Can complete full game without errors
- [ ] AI makes only legal moves
- [ ] Cascade failures work correctly
- [ ] Can run 1000 games automatically
- [ ] Statistics match expected distributions
- [ ] External API responds correctly
- [ ] Ollama agents can play

## Example Commands

```bash
# Run 100 autonomous games
python scripts/run_autonomous.py --games 100

# Run with specific configuration
python scripts/run_autonomous.py \
  --games 50 \
  --players "aggressive,defensive,balanced,aggressive" \
  --scenario high_chaos

# Export results
python scripts/analyze_games.py \
  --input data/logs/ \
  --export csv
```

Good luck with the implementation!
