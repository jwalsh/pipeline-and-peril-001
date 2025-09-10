# Experiment 004: Victory Condition Balance

## Hypothesis

Different victory conditions create distinct gameplay experiences. The current conditions may favor certain strategies or player counts over others.

## Research Questions

1. **RQ1**: Which victory conditions are most frequently achieved?
2. **RQ2**: How do victory conditions affect game length and strategy?
3. **RQ3**: Are cooperative victories properly balanced against competitive ones?
4. **RQ4**: Do victory conditions scale appropriately with player count?

## Methodology

### Victory Conditions Tested

| Type | Condition | Parameters |
|------|-----------|------------|
| Cooperative | Uptime Threshold | 70%, 75%, 80%, 85%, 90% |
| Cooperative | Duration | 8, 10, 12, 15 rounds |
| Competitive | Score Formula | uptime×services, uptime+services×10 |
| Survival | Last Standing | >40%, >50%, >60% uptime |
| Hybrid | Points System | Various point allocations |

### Variables
- **Independent**: Victory condition parameters
- **Dependent**: Win rate distribution, game satisfaction, strategic diversity
- **Control**: Grid size (8×6), service costs (baseline)

## Test Configurations

### Cooperative Variations
```yaml
victory_conditions:
  - type: cooperative
    uptime_threshold: [0.70, 0.75, 0.80, 0.85, 0.90]
    min_rounds: [8, 10, 12, 15]
    player_count_scaling: [true, false]
```

### Competitive Variations
```yaml
victory_conditions:
  - type: competitive
    scoring:
      - formula: "uptime * services_built"
      - formula: "uptime * requests_handled"
      - formula: "(uptime + 50) * (services + connections)"
```

### Hybrid System
```yaml
victory_conditions:
  - type: points
    targets:
      services: 10 points each
      uptime_95: 50 points
      no_failures: 30 points
      chaos_survived: 20 points
    win_threshold: 200 points
```

## Expected Outcomes

### Balance Targets
- Cooperative wins: 20-30% of games
- Competitive wins: 60-70% of games
- Draws/Timeouts: <10% of games
- Average game length: 12±3 rounds

### Player Count Scaling
| Players | Coop Win Rate | Avg Rounds |
|---------|---------------|------------|
| 2       | 35%           | 10         |
| 3       | 28%           | 12         |
| 4       | 22%           | 13         |
| 5       | 18%           | 15         |
| 6       | 15%           | 17         |

## Analysis Plan

1. **Win Distribution Analysis**
   - Chi-square test for condition preference
   - Logistic regression for win predictors

2. **Game Length Impact**
   - ANOVA across conditions
   - Survival analysis for game duration

3. **Strategy Emergence**
   - Cluster analysis of winning strategies
   - Diversity index calculation

4. **Player Satisfaction Proxy**
   - Completion rate
   - Rematch rate (simulated)
   - Decision complexity metrics

## Implementation

```python
def test_victory_condition(condition_config):
    results = {
        'wins_by_type': defaultdict(int),
        'game_lengths': [],
        'strategy_distribution': {},
        'satisfaction_score': 0
    }
    
    for _ in range(1000):
        game = simulate_game(victory_condition=condition_config)
        results['wins_by_type'][game.victory_type] += 1
        results['game_lengths'].append(game.rounds)
        results['strategy_distribution'][game.winning_strategy] += 1
    
    return analyze_results(results)
```