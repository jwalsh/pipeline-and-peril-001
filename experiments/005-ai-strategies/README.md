# Experiment 005: AI Strategy Comparison

## Hypothesis

Different AI strategies create emergent gameplay patterns that can inform both game balance and player education. Understanding optimal strategies helps calibrate difficulty and tutorial design.

## Research Questions

1. **RQ1**: Which AI strategies consistently outperform others?
2. **RQ2**: How do strategies interact in mixed games?
3. **RQ3**: Are there dominant strategies that need balancing?
4. **RQ4**: Do strategies adapt effectively to different game states?

## Methodology

### Strategy Definitions

#### 1. Aggressive Expander
```python
strategy_aggressive = {
    "priority": "maximize_services",
    "resource_threshold": 0.3,  # Build when resources > 30%
    "service_preference": ["load_balancer", "compute", "api_gateway"],
    "connection_rate": 0.2,  # 20% chance to connect vs build
    "risk_tolerance": 0.8  # High risk tolerance
}
```

#### 2. Defensive Redundancy
```python
strategy_defensive = {
    "priority": "maximize_uptime",
    "resource_threshold": 0.5,
    "service_preference": ["cache", "queue", "database"],
    "connection_rate": 0.6,  # Prefer connections
    "risk_tolerance": 0.2  # Low risk tolerance
}
```

#### 3. Balanced Optimizer
```python
strategy_balanced = {
    "priority": "optimize_efficiency",
    "resource_threshold": 0.4,
    "service_preference": "adaptive",  # Based on game state
    "connection_rate": 0.4,
    "risk_tolerance": 0.5
}
```

#### 4. Chaos Specialist
```python
strategy_chaos = {
    "priority": "survive_chaos",
    "resource_threshold": 0.6,  # Hoard resources
    "service_preference": ["queue", "cache", "database"],
    "connection_rate": 0.3,
    "risk_tolerance": 0.3,
    "chaos_preparation": True  # Special chaos handling
}
```

#### 5. Economic Optimizer
```python
strategy_economic = {
    "priority": "maximize_roi",
    "resource_threshold": 0.25,
    "service_preference": "cost_efficient",  # Best capacity/cost ratio
    "connection_rate": 0.35,
    "risk_tolerance": 0.6
}
```

#### 6. Adaptive Learner
```python
strategy_adaptive = {
    "priority": "learn_and_adapt",
    "learning_rate": 0.1,
    "exploration_rate": 0.2,
    "strategy_switching": True,
    "memory_length": 10  # Remember last 10 rounds
}
```

### Tournament Structure

#### Round Robin (All vs All)
- Each strategy plays against every other strategy
- 100 games per matchup
- Total: 15 matchups × 100 = 1,500 games

#### Mixed Games
- 4 players with different strategies
- Test all unique combinations
- 100 games per combination
- Total: C(6,4) × 100 = 1,500 games

#### Evolution Tournament
- Start with equal distribution
- Winners reproduce, losers eliminated
- 20 generations × 100 games = 2,000 games

### Metrics

#### Performance Metrics
- Win rate
- Average game length
- Average final uptime
- Services built per game
- Resource efficiency

#### Behavioral Metrics
- Decision diversity index
- Adaptation rate
- Strategy stability
- Counter-strategy effectiveness

## Expected Outcomes

### Strategy Rankings (Predicted)
1. **Adaptive Learner** - 28% win rate
2. **Balanced Optimizer** - 24% win rate
3. **Economic Optimizer** - 20% win rate
4. **Aggressive Expander** - 12% win rate
5. **Defensive Redundancy** - 10% win rate
6. **Chaos Specialist** - 6% win rate (but high in chaos-heavy games)

### Rock-Paper-Scissors Dynamics
- Aggressive beats Economic
- Economic beats Defensive
- Defensive beats Aggressive
- Balanced has no hard counters
- Adaptive learns counters over time

## Implementation

```python
class StrategyTournament:
    def __init__(self, strategies, games_per_match=100):
        self.strategies = strategies
        self.games_per_match = games_per_match
        self.results = defaultdict(lambda: defaultdict(int))
    
    def run_match(self, strategy_a, strategy_b):
        wins_a, wins_b = 0, 0
        
        for _ in range(self.games_per_match):
            game = Game()
            game.add_player(AIPlayer(strategy_a))
            game.add_player(AIPlayer(strategy_b))
            
            winner = game.simulate()
            if winner.strategy == strategy_a:
                wins_a += 1
            else:
                wins_b += 1
        
        return wins_a, wins_b
    
    def run_tournament(self):
        for s1 in self.strategies:
            for s2 in self.strategies:
                if s1 != s2:
                    wins_1, wins_2 = self.run_match(s1, s2)
                    self.results[s1.name][s2.name] = wins_1
                    self.results[s2.name][s1.name] = wins_2
        
        return self.calculate_rankings()
```

## Analysis Plan

### 1. Head-to-Head Matrix
| | Aggr | Def | Bal | Chaos | Econ | Adapt |
|-|------|-----|-----|-------|------|-------|
| **Aggressive** | - | W | L | W | L | L |
| **Defensive** | L | - | L | W | W | L |
| **Balanced** | W | W | - | W | D | L |
| **Chaos** | L | L | L | - | L | L |
| **Economic** | W | L | D | W | - | L |
| **Adaptive** | W | W | W | W | W | - |

### 2. Statistical Analysis
- Chi-square test for strategy independence
- ANOVA for performance differences
- Regression analysis for success predictors
- Cluster analysis for strategy groupings

### 3. Evolutionary Stability
- Test if strategies reach equilibrium
- Identify evolutionary stable strategies (ESS)
- Calculate invasion barriers

### 4. Recommendations
- Difficulty levels based on strategy
- Tutorial scenarios for each strategy
- Balancing adjustments needed
- New strategy opportunities

## Output Files

```
outputs/
├── tournament_results.json     # Raw match results
├── strategy_rankings.csv       # Final rankings
├── head_to_head_matrix.png    # Visualization
├── evolution_timeline.png      # Strategy evolution
├── performance_analysis.html   # Detailed analysis
└── recommendations.md          # Game design recommendations
```