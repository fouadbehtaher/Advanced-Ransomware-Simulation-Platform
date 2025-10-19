"""Test suite for analysis functionality"""
import pytest
from arsp.analysis import BehavioralAnalyzer, Reporter
from arsp.simulation import ScenarioBuilder, SimulationEngine


class TestBehavioralAnalyzer:
    """Test behavioral analyzer"""
    
    def test_analyzer_initialization(self):
        """Test analyzer initialization"""
        analyzer = BehavioralAnalyzer()
        assert analyzer is not None
    
    def test_analyze_results(self):
        """Test analysis of simulation results"""
        # Create mock simulation results
        results = {
            "scenario_name": "test",
            "steps": [
                {"action": "encrypt", "status": "success"},
                {"action": "enumerate", "status": "success"}
            ]
        }
        
        analyzer = BehavioralAnalyzer()
        analysis = analyzer.analyze(results)
        
        assert analysis is not None
        assert "behavior_patterns" in analysis
        assert "risk_assessment" in analysis
        assert "recommendations" in analysis
    
    def test_risk_assessment(self):
        """Test risk assessment"""
        results = {
            "scenario_name": "test",
            "steps": [
                {"action": "encrypt", "status": "success"},
                {"action": "exfiltrate", "status": "success"}
            ]
        }
        
        analyzer = BehavioralAnalyzer()
        analysis = analyzer.analyze(results)
        risk = analysis["risk_assessment"]
        
        assert "level" in risk
        assert "score" in risk
        assert risk["score"] >= 0


class TestReporter:
    """Test report generation"""
    
    def test_reporter_initialization(self):
        """Test reporter initialization"""
        reporter = Reporter()
        assert reporter is not None
    
    def test_generate_json_report(self):
        """Test JSON report generation"""
        results = {"scenario_name": "test", "status": "completed"}
        reporter = Reporter()
        
        report_path = reporter.generate_report(results, format="json")
        assert report_path is not None
        
        import os
        assert os.path.exists(report_path)
    
    def test_generate_text_report(self):
        """Test text report generation"""
        results = {"scenario_name": "test", "status": "completed"}
        reporter = Reporter()
        
        report_path = reporter.generate_report(results, format="text")
        assert report_path is not None
        
        import os
        assert os.path.exists(report_path)
