# Experiment 001: Service Cost Optimization

## Hypothesis

The current service costs may not be optimally balanced for engaging gameplay. By systematically varying the resource costs of each service type, we can identify the configuration that produces:
- Appropriate game length (10-15 rounds)
- Balanced win rates across strategies
- Meaningful resource management decisions

## Research Questions

1. **RQ1**: How do service costs affect average game duration?
2. **RQ2**: Which cost configurations lead to the most balanced outcomes?
3. **RQ3**: Is there a correlation between total resource cost and service usage frequency?
4. **RQ4**: Do certain cost ratios (CPU:Memory:Storage) produce better gameplay?

## Methodology

### Independent Variables
- Service costs for each type (6 service types × 3 resource types = 18 variables)
- Cost scaling factor: 0.5x to 2.0x baseline in 0.1x increments

### Dependent Variables
- Game duration (rounds)
- Winner distribution
- Service build frequency
- Resource starvation events
- Player satisfaction proxy (game completion rate)

### Control Variables
- Grid size: 8×6 (fixed)
- Player count: 4 (fixed)
- Starting resources: 5 CPU, 5 Memory, 5 Storage (fixed)
- AI strategies: Balanced (fixed)

### Experimental Design

1. **Baseline Measurement**: 1000 games with current costs
2. **Individual Variation**: Vary each service type independently
3. **Combined Variation**: Test promising combinations
4. **Validation**: 5000 games with optimal configuration

## Implementation

### Input Configuration

```yaml
# inputs/baseline.yaml
service_costs:
  compute:
    cpu: 2
    memory: 2
    storage: 1
  database:
    cpu: 1
    memory: 2
    storage: 3
  # ... etc

simulation:
  games: 1000
  players: 4
  strategy: balanced
```

### Variations

We test 16 variations per service type:
- Scale factors: [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]
- Total experiments: 6 services × 16 variations = 96 configurations
- Games per configuration: 100
- Total games: 9,600 + 1,000 baseline + 5,000 validation = 15,600

## Expected Outcomes

### Success Metrics
- [ ] Identify cost configuration with game length 12±2 rounds
- [ ] Achieve <10% variance in win rates across strategies
- [ ] All service types used in >80% of games
- [ ] Resource starvation in <5% of games

### Risk Factors
- Computational time: ~15 minutes for full experiment
- Statistical power: May need more games for significance
- Interaction effects: Service costs may not be independent

## Analysis Plan

1. **Descriptive Statistics**
   - Mean, median, std dev for each configuration
   - Distribution plots for game length

2. **Inferential Statistics**
   - ANOVA to test significance of cost variations
   - Post-hoc Tukey HSD for pairwise comparisons
   - Linear regression for cost-duration relationship

3. **Optimization**
   - Grid search for optimal combination
   - Validation on held-out test set

## Usage

```bash
# Run the complete experiment
make all

# Run just the baseline
make baseline

# Run variations
make variations

# Generate analysis
make analyze

# Clean outputs
make clean
```

## Results Summary

Results will be stored in:
- `outputs/results.json` - Raw simulation data
- `outputs/analysis.html` - Statistical analysis report
- `outputs/optimal_config.yaml` - Best configuration found
- `outputs/visualizations/` - Plots and charts

## Reproducibility

Random seed is fixed at 42 for all simulations. Results should be identical across runs on the same platform.