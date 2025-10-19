"""
Report generation for simulation and analysis results

Generates comprehensive reports in various formats.
"""
from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime
import json

from arsp.core.config import Config
from arsp.core.logger import Logger


class Reporter:
    """Generate reports from simulation and analysis results"""
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize reporter
        
        Args:
            config: Optional configuration object
        """
        self.config = config or Config()
        self.logger = Logger().get_logger(
            "reporter",
            self.config.get("monitoring.log_level", "INFO"),
            self.config.get("monitoring.log_path")
        )
        
        self.output_path = Path(self.config.get("reporting.output_path", "./reports"))
        self.output_path.mkdir(parents=True, exist_ok=True)
    
    def generate_report(
        self,
        simulation_results: Dict[str, Any],
        analysis_results: Optional[Dict[str, Any]] = None,
        format: str = "json"
    ) -> str:
        """
        Generate comprehensive report
        
        Args:
            simulation_results: Simulation execution results
            analysis_results: Optional analysis results
            format: Report format (json, text, html)
            
        Returns:
            Path to generated report file
        """
        self.logger.info(f"Generating report in {format} format")
        
        report_data = {
            "report_metadata": {
                "generated_at": datetime.now().isoformat(),
                "platform_version": "0.1.0",
                "report_type": "simulation_analysis",
            },
            "simulation": simulation_results,
        }
        
        if analysis_results:
            report_data["analysis"] = analysis_results
        
        # Generate report based on format
        if format == "json":
            report_path = self._generate_json_report(report_data)
        elif format == "text":
            report_path = self._generate_text_report(report_data)
        elif format == "html":
            report_path = self._generate_html_report(report_data)
        else:
            raise ValueError(f"Unsupported report format: {format}")
        
        self.logger.info(f"Report generated: {report_path}")
        return str(report_path)
    
    def _generate_json_report(self, data: Dict[str, Any]) -> Path:
        """Generate JSON report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.output_path / f"report_{timestamp}.json"
        
        with open(report_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        return report_path
    
    def _generate_text_report(self, data: Dict[str, Any]) -> Path:
        """Generate plain text report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.output_path / f"report_{timestamp}.txt"
        
        lines = []
        lines.append("=" * 80)
        lines.append("ADVANCED RANSOMWARE SIMULATION PLATFORM - REPORT")
        lines.append("=" * 80)
        lines.append("")
        
        # Metadata
        metadata = data.get("report_metadata", {})
        lines.append(f"Generated: {metadata.get('generated_at', 'N/A')}")
        lines.append(f"Platform Version: {metadata.get('platform_version', 'N/A')}")
        lines.append("")
        
        # Simulation results
        sim = data.get("simulation", {})
        lines.append("SIMULATION RESULTS")
        lines.append("-" * 80)
        lines.append(f"Scenario: {sim.get('scenario_name', 'N/A')}")
        lines.append(f"Type: {sim.get('scenario_type', 'N/A')}")
        lines.append(f"Status: {sim.get('status', 'N/A')}")
        lines.append(f"Duration: {sim.get('duration_seconds', 0):.2f} seconds")
        lines.append("")
        
        # Steps
        steps = sim.get("steps", [])
        lines.append(f"Steps Executed: {len(steps)}")
        for i, step in enumerate(steps, 1):
            lines.append(f"  {i}. {step.get('name', 'unknown')} - {step.get('status', 'unknown')}")
        lines.append("")
        
        # Analysis results
        if "analysis" in data:
            analysis = data["analysis"]
            lines.append("BEHAVIORAL ANALYSIS")
            lines.append("-" * 80)
            
            # Risk assessment
            risk = analysis.get("risk_assessment", {})
            lines.append(f"Risk Level: {risk.get('level', 'N/A').upper()}")
            lines.append(f"Risk Score: {risk.get('score', 0)}/100")
            lines.append("")
            
            # Patterns
            patterns = analysis.get("behavior_patterns", [])
            lines.append(f"Behavioral Patterns Detected: {len(patterns)}")
            for pattern in patterns:
                lines.append(f"  - {pattern.get('description', 'N/A')} (Severity: {pattern.get('severity', 'N/A')})")
            lines.append("")
            
            # Recommendations
            recommendations = analysis.get("recommendations", [])
            lines.append("RECOMMENDATIONS:")
            for i, rec in enumerate(recommendations, 1):
                lines.append(f"  {i}. {rec}")
        
        lines.append("")
        lines.append("=" * 80)
        
        with open(report_path, 'w') as f:
            f.write('\n'.join(lines))
        
        return report_path
    
    def _generate_html_report(self, data: Dict[str, Any]) -> Path:
        """Generate HTML report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.output_path / f"report_{timestamp}.html"
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>ARSP Simulation Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #2c3e50; }}
        h2 {{ color: #34495e; border-bottom: 2px solid #3498db; padding-bottom: 5px; }}
        .metadata {{ background-color: #ecf0f1; padding: 10px; border-radius: 5px; }}
        .status {{ font-weight: bold; }}
        .critical {{ color: #e74c3c; }}
        .high {{ color: #e67e22; }}
        .medium {{ color: #f39c12; }}
        .low {{ color: #27ae60; }}
        table {{ border-collapse: collapse; width: 100%; margin: 10px 0; }}
        th, td {{ border: 1px solid #bdc3c7; padding: 8px; text-align: left; }}
        th {{ background-color: #3498db; color: white; }}
    </style>
</head>
<body>
    <h1>Advanced Ransomware Simulation Platform - Report</h1>
    <div class="metadata">
        <p><strong>Generated:</strong> {data.get('report_metadata', {}).get('generated_at', 'N/A')}</p>
        <p><strong>Platform Version:</strong> {data.get('report_metadata', {}).get('platform_version', 'N/A')}</p>
    </div>
    
    <h2>Simulation Results</h2>
    <p><strong>Scenario:</strong> {data.get('simulation', {}).get('scenario_name', 'N/A')}</p>
    <p><strong>Status:</strong> <span class="status">{data.get('simulation', {}).get('status', 'N/A')}</span></p>
    <p><strong>Duration:</strong> {data.get('simulation', {}).get('duration_seconds', 0):.2f} seconds</p>
    
    <h2>Analysis Results</h2>
"""
        
        if "analysis" in data:
            analysis = data["analysis"]
            risk = analysis.get("risk_assessment", {})
            risk_level = risk.get('level', 'unknown')
            
            html += f"""
    <p><strong>Risk Level:</strong> <span class="{risk_level}">{risk_level.upper()}</span></p>
    <p><strong>Risk Score:</strong> {risk.get('score', 0)}/100</p>
    
    <h3>Recommendations</h3>
    <ul>
"""
            for rec in analysis.get("recommendations", []):
                html += f"        <li>{rec}</li>\n"
            
            html += "    </ul>\n"
        
        html += """
</body>
</html>
"""
        
        with open(report_path, 'w') as f:
            f.write(html)
        
        return report_path
