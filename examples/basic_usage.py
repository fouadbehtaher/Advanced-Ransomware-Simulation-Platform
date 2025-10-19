#!/usr/bin/env python3
"""Example usage script for ARSP"""
import sys
from arsp.core.config import Config
from arsp.simulation import SimulationEngine, ScenarioBuilder
from arsp.analysis import BehavioralAnalyzer, Reporter
from arsp.isolation import Sandbox
from arsp.monitoring import SystemMonitor

def main():
    print("=" * 70)
    print("Advanced Ransomware Simulation Platform - Example")
    print("=" * 70)
    print()
    
    config = Config()
    print("1. Configuration loaded")
    
    sandbox = Sandbox(config)
    sandbox_path = sandbox.create("example_simulation")
    sandbox.populate()
    print(f"2. Sandbox created at: {sandbox_path}")
    
    scenario = ScenarioBuilder.create_encryption_scenario("Example Encryption")
    print(f"3. Scenario created: {scenario.name}")
    
    monitor = SystemMonitor(config)
    monitor.start(interval=1.0)
    print("4. Monitoring started")
    
    engine = SimulationEngine(config)
    results = engine.execute(scenario, str(sandbox_path))
    print(f"5. Simulation completed: {results['status']}")
    
    monitor.stop()
    
    analyzer = BehavioralAnalyzer(config)
    analysis = analyzer.analyze(results)
    print(f"6. Analysis completed - Risk level: {analysis['risk_assessment']['level'].upper()}")
    
    reporter = Reporter(config)
    report_path = reporter.generate_report(results, analysis, format="text")
    print(f"7. Report generated: {report_path}")
    
    sandbox.cleanup(remove_all=True)
    print("8. Cleanup completed")
    print()
    print("=" * 70)
    print("Example completed successfully!")
    print("=" * 70)
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
