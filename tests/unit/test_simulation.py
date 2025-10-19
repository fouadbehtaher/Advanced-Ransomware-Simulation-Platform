"""Test suite for simulation functionality"""
import pytest
from arsp.simulation import SimulationEngine, Scenario, ScenarioType, ScenarioBuilder
from arsp.core.config import Config


class TestScenario:
    """Test scenario creation and management"""
    
    def test_scenario_creation(self):
        """Test basic scenario creation"""
        scenario = Scenario(
            name="Test Scenario",
            description="Test description",
            scenario_type=ScenarioType.ENCRYPTION
        )
        assert scenario.name == "Test Scenario"
        assert scenario.scenario_type == ScenarioType.ENCRYPTION
    
    def test_scenario_add_step(self):
        """Test adding steps to scenario"""
        scenario = Scenario(
            name="Test",
            description="Test",
            scenario_type=ScenarioType.ENCRYPTION
        )
        scenario.add_step({"name": "step1", "action": "test"})
        assert len(scenario.steps) == 1
    
    def test_scenario_to_dict(self):
        """Test scenario serialization"""
        scenario = Scenario(
            name="Test",
            description="Test",
            scenario_type=ScenarioType.ENCRYPTION
        )
        data = scenario.to_dict()
        assert data["name"] == "Test"
        assert data["scenario_type"] == "encryption"


class TestScenarioBuilder:
    """Test scenario builder"""
    
    def test_create_encryption_scenario(self):
        """Test encryption scenario creation"""
        scenario = ScenarioBuilder.create_encryption_scenario()
        assert scenario.scenario_type == ScenarioType.ENCRYPTION
        assert len(scenario.steps) > 0
    
    def test_create_exfiltration_scenario(self):
        """Test exfiltration scenario creation"""
        scenario = ScenarioBuilder.create_exfiltration_scenario()
        assert scenario.scenario_type == ScenarioType.EXFILTRATION
        assert len(scenario.steps) > 0
    
    def test_create_full_attack_chain(self):
        """Test full attack chain scenario"""
        scenario = ScenarioBuilder.create_full_attack_chain()
        assert scenario.scenario_type == ScenarioType.FULL_ATTACK_CHAIN
        assert len(scenario.steps) >= 4


class TestSimulationEngine:
    """Test simulation engine"""
    
    def test_engine_initialization(self):
        """Test engine initialization"""
        engine = SimulationEngine()
        assert engine is not None
    
    def test_engine_execute(self):
        """Test simulation execution"""
        config = Config()
        engine = SimulationEngine(config)
        scenario = ScenarioBuilder.create_encryption_scenario()
        
        results = engine.execute(scenario)
        
        assert results is not None
        assert "status" in results
        assert "duration_seconds" in results
    
    def test_engine_status(self):
        """Test engine status tracking"""
        engine = SimulationEngine()
        status = engine.get_status()
        assert status is not None
