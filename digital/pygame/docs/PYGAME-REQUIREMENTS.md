# Pipeline & Peril - Digital Playtesting Requirements

## Executive Summary

This document outlines the requirements for a PyGame-based digital version of Pipeline & Peril, designed specifically for rapid playtesting, rules validation, and game balance evaluation. The system will support both autonomous AI-driven gameplay and human interaction, with optional integration to LLM agents via Ollama.

## Project Overview

### Purpose
Create a digital playtesting environment to:
- Validate game mechanics and balance
- Test edge cases and rule interactions
- Gather statistical data on game outcomes
- Evaluate different strategies
- Accelerate iteration on game design

### Scope
- Core game engine with complete rules implementation
- Autonomous AI players with configurable strategies
- Data collection and analytics
- Optional human player interface
- Optional LLM agent integration

## System Requirements

### Functional Requirements

#### FR1: Game Engine Core
- FR1.1: Complete implementation of all game rules
- FR1.2: Turn-based state machine
- FR1.3: Dice rolling system (d4, d6, d8, d10, d12, d20)
- FR1.4: Service placement and connection logic
- FR1.5: Resource management (CPU, Memory, Storage)
- FR1.6: Traffic routing and load distribution
- FR1.7: Cascade failure simulation
- FR1.8: Chaos event system
- FR1.9: Win/loss condition checking

#### FR2: Autonomous Play
- FR2.1: AI players with configurable strategies
- FR2.2: Default action selection based on game state
- FR2.3: Automatic dice roll resolution
- FR2.4: Strategy profiles (aggressive, defensive, balanced)
- FR2.5: No-human-input game completion

#### FR3: Data Collection
- FR3.1: Log all game actions and state changes
- FR3.2: Track metrics (uptime, rounds, failures, resources)
- FR3.3: Export game data as JSON/CSV
- FR3.4: Replay functionality from logs
- FR3.5: Statistical analysis tools

#### FR4: Visualization
- FR4.1: Board state rendering
- FR4.2: Service connection visualization
- FR4.3: Resource tracking display
- FR4.4: Metrics dashboard
- FR4.5: Animation for state changes (optional)

#### FR5: Integration Interfaces
- FR5.1: REST API for external agent control
- FR5.2: Ollama integration for LLM agents
- FR5.3: Structured input/output format
- FR5.4: WebSocket support for real-time play
- FR5.5: Plugin architecture for custom agents

### Non-Functional Requirements

#### NFR1: Performance
- NFR1.1: Complete 1000 autonomous games in < 1 hour
- NFR1.2: < 100ms response time for any action
- NFR1.3: < 500MB memory usage
- NFR1.4: Support parallel game execution

#### NFR2: Usability
- NFR2.1: Single command to run autonomous games
- NFR2.2: Clear visualization of game state
- NFR2.3: Helpful error messages
- NFR2.4: Comprehensive logging

## Game Rules Specification

### Setup Phase
1. Initialize 8x6 hex grid
2. Place 3 starting services (1 Compute, 1 Database, 1 Load Balancer)
3. Each player starts with:
   - 5 CPU, 5 Memory, 5 Storage
   - 3 action tokens
   - Character ability
4. Set uptime to 100%
5. Set entropy to 0

### Turn Structure

#### 1. Traffic Phase
- Roll 2d10 for incoming requests
- Distribute requests to entry points (Load Balancers/API Gateways)
- Check for overload conditions

#### 2. Action Phase (3 actions per player)
Available actions:
- Build Service (cost varies by type)
- Create Connection (1 resource)
- Upgrade Service (2 resources)
- Debug Service (roll d20, DC based on bug severity)
- Deploy Redundancy (copy service)
- Gather Resources (gain 1d6 resources)
- Use Tool Card
- Activate Character Ability

#### 3. Resolution Phase
- Services process requests
- Check for cascade failures
- Calculate uptime changes
- Resolve any triggered events

#### 4. Chaos Phase
- Roll d8 for chaos event (if entropy > 3)
- Apply chaos effects
- Increase entropy by 1 (max 10)

### Service Types and Properties

| Service Type   | CPU | Memory | Storage | Capacity | Special                    |
|----------------|-----|--------|---------|----------|----------------------------|
| Compute        |   2 |      2 |       1 |        5 | Process any request        |
| Database       |   1 |      2 |       3 |        3 | Required for data requests |
| Cache          |   1 |      3 |       1 |        8 | Speed up connected services|
| Queue          |   1 |      1 |       2 |        6 | Buffer overflow            |
| Load Balancer  |   2 |      1 |       1 |       10 | Distribute traffic         |
| API Gateway    |   1 |      1 |       1 |        7 | External entry point       |

### Victory Conditions
- **Cooperative**: Maintain >80% uptime for 10 rounds
- **Competitive**: Highest (uptime × requests handled)
- **Survival**: Last player with >50% uptime

## Acceptance Criteria

### Core Gameplay
- [ ] Can complete a full 10-round game without errors
- [ ] All 6 service types function correctly
- [ ] Cascade failures propagate properly
- [ ] Resource costs are deducted correctly
- [ ] Dice rolls produce expected distributions

### Autonomous Play
- [ ] AI players complete turns within 1 second
- [ ] AI makes legal moves only
- [ ] Different strategies produce different outcomes
- [ ] Can run 1000 games unattended
- [ ] Games complete in reasonable time (5-15 rounds)

### Data Collection
- [ ] Every action is logged with timestamp
- [ ] Can reconstruct game state from logs
- [ ] Statistical summaries are accurate
- [ ] Export formats are valid JSON/CSV
- [ ] No data loss during long runs

### Integration
- [ ] REST API responds to all endpoints
- [ ] Ollama agents can play complete games
- [ ] Structured output matches specification
- [ ] WebSocket connections remain stable
- [ ] External agents receive valid game states
