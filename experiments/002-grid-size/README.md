# Experiment 002: Grid Size Impact Analysis

## Hypothesis

The hexagonal grid size significantly impacts gameplay dynamics. Smaller grids lead to more conflict and resource competition, while larger grids may reduce player interaction and extend game length unnecessarily.

## Research Questions

1. **RQ1**: What is the optimal grid size for 2-6 players?
2. **RQ2**: How does grid size affect average game duration?
3. **RQ3**: Does grid size influence service placement strategy?
4. **RQ4**: What is the relationship between grid area and cascade failure frequency?

## Methodology

### Independent Variables
- Grid dimensions: Width × Height
  - Small: 6×4 (24 hexes)
  - Medium: 8×6 (48 hexes) - baseline
  - Large: 10×8 (80 hexes)
  - Extra Large: 12×10 (120 hexes)

### Dependent Variables
- Game duration (rounds)
- Service density (services/hex)
- Cascade failure frequency
- Player interaction events
- Territory control metrics

### Control Variables
- Service costs: baseline
- Player count: 4
- AI strategy: balanced
- Starting resources: 5/5/5

## Expected Outcomes

| Grid Size | Expected Rounds | Service Density | Player Conflict |
|-----------|----------------|-----------------|-----------------|
| 6×4       | 8-10           | High (0.6-0.8)  | Very High       |
| 8×6       | 10-15          | Medium (0.4-0.6)| Medium          |
| 10×8      | 15-20          | Low (0.2-0.4)   | Low             |
| 12×10     | 20-25          | Very Low (<0.2) | Very Low        |

## Implementation

```yaml
# inputs/grid_6x4.yaml
grid:
  width: 6
  height: 4
  
simulation:
  games: 500
  players: 4
```

## Analysis Plan

1. **Spatial Analysis**
   - Heat maps of service placement
   - Clustering coefficient calculation
   - Path length distribution

2. **Performance Metrics**
   - Time to first conflict
   - Resource contention rate
   - Expansion patterns

3. **Optimization**
   - Player count to grid size ratio
   - Minimum viable grid dimensions