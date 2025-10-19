"""
Scenario definitions for ransomware simulations

Provides scenario templates and configuration for different ransomware behaviors.
"""
from typing import List, Dict, Any, Optional
from enum import Enum
from dataclasses import dataclass, field
import json


class ScenarioType(Enum):
    """Types of ransomware simulation scenarios"""
    ENCRYPTION = "encryption"
    EXFILTRATION = "exfiltration"
    ENUMERATION = "enumeration"
    PERSISTENCE = "persistence"
    LATERAL_MOVEMENT = "lateral_movement"
    COMMAND_CONTROL = "command_control"
    FULL_ATTACK_CHAIN = "full_attack_chain"


@dataclass
class Scenario:
    """Ransomware simulation scenario configuration"""
    
    name: str
    description: str
    scenario_type: ScenarioType
    steps: List[Dict[str, Any]] = field(default_factory=list)
    parameters: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_step(self, step: Dict[str, Any]) -> None:
        """Add a step to the scenario"""
        self.steps.append(step)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert scenario to dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "scenario_type": self.scenario_type.value,
            "steps": self.steps,
            "parameters": self.parameters,
            "metadata": self.metadata,
        }
    
    def to_json(self) -> str:
        """Convert scenario to JSON string"""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Scenario':
        """Create scenario from dictionary"""
        return cls(
            name=data["name"],
            description=data["description"],
            scenario_type=ScenarioType(data["scenario_type"]),
            steps=data.get("steps", []),
            parameters=data.get("parameters", {}),
            metadata=data.get("metadata", {}),
        )
    
    @classmethod
    def from_json(cls, json_str: str) -> 'Scenario':
        """Create scenario from JSON string"""
        data = json.loads(json_str)
        return cls.from_dict(data)


class ScenarioBuilder:
    """Builder for creating ransomware simulation scenarios"""
    
    @staticmethod
    def create_encryption_scenario(name: str = "Basic Encryption") -> Scenario:
        """Create a basic file encryption scenario"""
        scenario = Scenario(
            name=name,
            description="Simulates basic file encryption behavior",
            scenario_type=ScenarioType.ENCRYPTION,
        )
        
        scenario.add_step({
            "name": "enumerate_files",
            "action": "enumerate",
            "parameters": {
                "extensions": [".txt", ".doc", ".pdf", ".jpg"],
                "max_depth": 3
            }
        })
        
        scenario.add_step({
            "name": "encrypt_files",
            "action": "encrypt",
            "parameters": {
                "algorithm": "AES-256",
                "extension": ".encrypted"
            }
        })
        
        scenario.add_step({
            "name": "create_ransom_note",
            "action": "create_note",
            "parameters": {
                "filename": "README_RANSOM.txt",
                "content": "Your files have been encrypted (simulation)"
            }
        })
        
        return scenario
    
    @staticmethod
    def create_exfiltration_scenario(name: str = "Data Exfiltration") -> Scenario:
        """Create a data exfiltration scenario"""
        scenario = Scenario(
            name=name,
            description="Simulates data exfiltration behavior",
            scenario_type=ScenarioType.EXFILTRATION,
        )
        
        scenario.add_step({
            "name": "identify_sensitive_files",
            "action": "enumerate",
            "parameters": {
                "patterns": ["*.key", "*.pem", "*.cert", "credentials*"],
                "keywords": ["password", "secret", "api_key"]
            }
        })
        
        scenario.add_step({
            "name": "stage_files",
            "action": "stage",
            "parameters": {
                "staging_dir": "/tmp/staged_data"
            }
        })
        
        scenario.add_step({
            "name": "simulate_exfiltration",
            "action": "exfiltrate",
            "parameters": {
                "method": "simulated",
                "compression": True
            }
        })
        
        return scenario
    
    @staticmethod
    def create_full_attack_chain(name: str = "Full Attack Chain") -> Scenario:
        """Create a comprehensive attack chain scenario"""
        scenario = Scenario(
            name=name,
            description="Simulates complete ransomware attack chain",
            scenario_type=ScenarioType.FULL_ATTACK_CHAIN,
        )
        
        # Enumeration phase
        scenario.add_step({
            "name": "system_enumeration",
            "action": "enumerate",
            "parameters": {"scope": "system"}
        })
        
        # Persistence phase
        scenario.add_step({
            "name": "establish_persistence",
            "action": "persist",
            "parameters": {"method": "simulated"}
        })
        
        # Exfiltration phase
        scenario.add_step({
            "name": "exfiltrate_data",
            "action": "exfiltrate",
            "parameters": {"priority": "high_value"}
        })
        
        # Encryption phase
        scenario.add_step({
            "name": "encrypt_files",
            "action": "encrypt",
            "parameters": {"scope": "all_files"}
        })
        
        # Ransom demand
        scenario.add_step({
            "name": "display_ransom",
            "action": "create_note",
            "parameters": {"type": "full_screen"}
        })
        
        return scenario
