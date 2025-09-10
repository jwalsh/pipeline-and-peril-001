# Experiment 003: Chaos Event Frequency Tuning

## Hypothesis

The frequency and severity of chaos events significantly impact game tension and player engagement. Too frequent chaos creates frustration; too rare removes excitement.

## Research Questions

1. **RQ1**: What chaos frequency maintains optimal game tension?
2. **RQ2**: How do chaos events affect cooperative vs competitive play?
3. **RQ3**: What is the relationship between entropy buildup and game length?
4. **RQ4**: Do chaos events create meaningful decision points?

## Methodology

### Independent Variables
- Entropy threshold for chaos: [2, 3, 4, 5, 6]
- Chaos probability: [0.1, 0.2, 0.3, 0.4, 0.5]
- Entropy increment rate: [0.5, 1.0, 1.5, 2.0]
- Chaos severity multiplier: [0.5x, 1.0x, 1.5x, 2.0x]

### Dependent Variables
- Player satisfaction proxy (game completion rate)
- Recovery time from chaos events
- Cascade failure frequency
- Strategic diversity index

### Chaos Event Types

| Event | Severity | Effect |
|-------|----------|--------|
| Minor Glitch | Low | -1 capacity random service |
| Network Congestion | Medium | +1 latency all connections |
| Memory Leak | Medium | All services need +1 memory |
| DDoS Attack | High | Roll 2d10 extra traffic |
| Database Corruption | High | Random DB gets d8 bug |
| Cascading Failure | Critical | 2x load on failure cascade |
| Security Breach | Critical | API gateways shut down |
| The Static Strikes | Extreme | Entropy +2, all lose 1 resource |

## Expected Outcomes

### Optimal Configuration
- Entropy threshold: 3
- Chaos probability: 0.25
- Entropy increment: 1.0
- Events every 3-4 rounds

## Implementation

```python
# Chaos configuration testing
chaos_configs = [
    {"threshold": 3, "probability": 0.25, "increment": 1.0},
    {"threshold": 4, "probability": 0.30, "increment": 0.5},
    # ... more configurations
]

for config in chaos_configs:
    results = simulate_with_chaos(config, games=1000)
    analyze_chaos_impact(results)
```

## Metrics

- **Tension Score**: Measure of game excitement
- **Frustration Index**: Player abandonment rate
- **Recovery Rate**: Rounds to recover from chaos
- **Strategic Impact**: Change in optimal strategy