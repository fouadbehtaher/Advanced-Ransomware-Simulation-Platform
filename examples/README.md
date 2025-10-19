# ARSP Examples

This directory contains example scripts demonstrating how to use the Advanced Ransomware Simulation Platform.

## Available Examples

### basic_usage.py

A complete workflow example that demonstrates:

- Configuration initialization
- Sandbox environment creation
- Scenario creation and execution
- System monitoring
- Behavioral analysis
- Report generation
- Cleanup

**Run it:**

```bash
python examples/basic_usage.py
```

## Creating Your Own Simulations

### Example: Custom Scenario

```python
from arsp.simulation import Scenario, ScenarioType

# Create custom scenario
scenario = Scenario(
    name="Custom Test",
    description="My custom scenario",
    scenario_type=ScenarioType.ENCRYPTION
)

# Add custom steps
scenario.add_step({
    "name": "custom_step",
    "action": "encrypt",
    "parameters": {"algorithm": "AES-256"}
})
```

### Example: Using Pre-built Scenarios

```python
from arsp.simulation import ScenarioBuilder

# Use pre-built scenarios
encryption = ScenarioBuilder.create_encryption_scenario()
exfiltration = ScenarioBuilder.create_exfiltration_scenario()
full_chain = ScenarioBuilder.create_full_attack_chain()
```

## Security Reminder

Always run simulations in isolated sandbox environments. Never use on production systems or unauthorized infrastructure.
