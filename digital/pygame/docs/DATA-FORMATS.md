# Pipeline & Peril - Structured Data Formats

## Game State Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "GameState",
  "type": "object",
  "required": ["game_id", "round", "phase", "players", "grid", "metrics"],
  "properties": {
    "game_id": {
      "type": "string",
      "format": "uuid"
    },
    "round": {
      "type": "integer",
      "minimum": 1,
      "maximum": 20
    },
    "phase": {
      "type": "string",
      "enum": ["setup", "traffic", "action", "resolution", "chaos", "end"]
    },
    "players": {
      "type": "array",
      "items": {
        "$ref": "#/definitions/Player"
      }
    },
    "grid": {
      "$ref": "#/definitions/Grid"
    },
    "metrics": {
      "$ref": "#/definitions/Metrics"
    }
  }
}
```

## Action Format

```json
{
  "action_type": "build_service",
  "player_id": 1,
  "parameters": {
    "service_type": "cache",
    "location": {"row": 3, "col": 4}
  },
  "dice_rolls": [{"die": "d20", "result": 15}],
  "timestamp": "2025-09-10T22:45:00Z"
}
```

## Ollama Integration Format

### Request
```json
{
  "model": "llama2",
  "prompt": "You are playing Pipeline & Peril...",
  "format": {
    "type": "object",
    "required": ["action_type", "parameters", "reasoning"],
    "properties": {
      "action_type": {"type": "string"},
      "parameters": {"type": "object"},
      "reasoning": {"type": "string"}
    }
  }
}
```

### Response
```json
{
  "action_type": "build_service",
  "parameters": {
    "service_type": "cache",
    "location": {"row": 3, "col": 4}
  },
  "reasoning": "Building a cache to improve performance..."
}
```

## Service Costs

| Service       | CPU | Memory | Storage | Capacity |
|---------------|-----|--------|---------|----------|
| Compute       |   2 |      2 |       1 |        5 |
| Database      |   1 |      2 |       3 |        3 |
| Cache         |   1 |      3 |       1 |        8 |
| Queue         |   1 |      1 |       2 |        6 |
| Load Balancer |   2 |      1 |       1 |       10 |
| API Gateway   |   1 |      1 |       1 |        7 |

## Chaos Events

1. **Minor Glitch**: Random service loses 1 capacity
2. **Network Congestion**: +1 latency all connections
3. **Memory Leak**: All services need +1 memory
4. **DDoS Attack**: Roll 2d10 extra traffic
5. **Database Corruption**: Random DB gets d8 bug
6. **Cascading Failure**: 2x load on failure cascade
7. **Security Breach**: API gateways shut down
8. **The Static Strikes**: Entropy +2, all lose 1 resource
9. **System Meltdown**: Damage = current entropy

## Configuration Examples

### Strategy Configuration
```yaml
name: "Aggressive Expander"
decision_weights:
  build_service: 0.4
  create_connection: 0.25
  upgrade_service: 0.1
  debug_service: 0.1
  gather_resources: 0.1
  use_tool_card: 0.05
service_preferences:
  load_balancer: 3.0
  compute: 2.0
  cache: 1.0
```

### Scenario Configuration
```yaml
name: "High Chaos"
initial_state:
  starting_entropy: 5
  starting_resources:
    cpu: 3
    memory: 3
    storage: 3
modifiers:
  traffic_multiplier: 1.5
  chaos_frequency: 2.0
victory_conditions:
  rounds: 15
  minimum_uptime: 70
```
