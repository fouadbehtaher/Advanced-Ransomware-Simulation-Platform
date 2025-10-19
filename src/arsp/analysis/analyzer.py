"""
Behavioral analysis for simulation results

Analyzes simulation data to identify patterns and behaviors.
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path

from arsp.core.config import Config
from arsp.core.logger import Logger


class BehavioralAnalyzer:
    """Analyze ransomware simulation behaviors"""
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize behavioral analyzer
        
        Args:
            config: Optional configuration object
        """
        self.config = config or Config()
        self.logger = Logger().get_logger(
            "analyzer",
            self.config.get("monitoring.log_level", "INFO"),
            self.config.get("monitoring.log_path")
        )
    
    def analyze(self, simulation_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze simulation results
        
        Args:
            simulation_results: Results from simulation execution
            
        Returns:
            Analysis results dictionary
        """
        self.logger.info("Starting behavioral analysis")
        
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "simulation_name": simulation_results.get("scenario_name", "unknown"),
            "behavior_patterns": self._identify_patterns(simulation_results),
            "risk_assessment": self._assess_risk(simulation_results),
            "iocs": self._extract_iocs(simulation_results),
            "recommendations": self._generate_recommendations(simulation_results),
        }
        
        self.logger.info("Behavioral analysis completed")
        return analysis
    
    def _identify_patterns(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify behavioral patterns from simulation"""
        patterns = []
        
        steps = results.get("steps", [])
        
        # Detect encryption patterns
        encryption_steps = [s for s in steps if s.get("action") == "encrypt"]
        if encryption_steps:
            patterns.append({
                "pattern": "encryption_behavior",
                "severity": "high",
                "description": "File encryption activity detected",
                "count": len(encryption_steps),
            })
        
        # Detect enumeration patterns
        enum_steps = [s for s in steps if s.get("action") == "enumerate"]
        if enum_steps:
            patterns.append({
                "pattern": "enumeration_behavior",
                "severity": "medium",
                "description": "System/file enumeration detected",
                "count": len(enum_steps),
            })
        
        # Detect exfiltration patterns
        exfil_steps = [s for s in steps if s.get("action") == "exfiltrate"]
        if exfil_steps:
            patterns.append({
                "pattern": "exfiltration_behavior",
                "severity": "critical",
                "description": "Data exfiltration activity detected",
                "count": len(exfil_steps),
            })
        
        return patterns
    
    def _assess_risk(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Assess risk level of observed behaviors"""
        risk_score = 0
        risk_factors = []
        
        steps = results.get("steps", [])
        
        # Risk scoring
        for step in steps:
            action = step.get("action", "")
            
            if action == "encrypt":
                risk_score += 30
                risk_factors.append("File encryption capability")
            elif action == "exfiltrate":
                risk_score += 40
                risk_factors.append("Data exfiltration capability")
            elif action == "persist":
                risk_score += 20
                risk_factors.append("Persistence mechanism")
            elif action == "enumerate":
                risk_score += 10
                risk_factors.append("System enumeration")
        
        # Determine risk level
        if risk_score >= 70:
            risk_level = "critical"
        elif risk_score >= 50:
            risk_level = "high"
        elif risk_score >= 30:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        return {
            "score": min(risk_score, 100),
            "level": risk_level,
            "factors": risk_factors,
        }
    
    def _extract_iocs(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract Indicators of Compromise (IOCs)"""
        iocs = []
        
        # File-based IOCs
        steps = results.get("steps", [])
        for step in steps:
            if step.get("action") == "create_note":
                iocs.append({
                    "type": "file",
                    "value": step.get("parameters", {}).get("filename", "unknown"),
                    "description": "Ransom note file",
                })
        
        # Pattern-based IOCs
        if any(s.get("action") == "encrypt" for s in steps):
            iocs.append({
                "type": "behavior",
                "value": "mass_file_encryption",
                "description": "Mass file encryption pattern",
            })
        
        return iocs
    
    def _generate_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """Generate security recommendations based on analysis"""
        recommendations = []
        
        steps = results.get("steps", [])
        
        if any(s.get("action") == "encrypt" for s in steps):
            recommendations.append(
                "Implement file integrity monitoring and backup solutions"
            )
            recommendations.append(
                "Deploy anti-ransomware solutions with behavioral detection"
            )
        
        if any(s.get("action") == "exfiltrate" for s in steps):
            recommendations.append(
                "Enhance network segmentation and data loss prevention (DLP) controls"
            )
            recommendations.append(
                "Monitor for unusual outbound network traffic patterns"
            )
        
        if any(s.get("action") == "enumerate" for s in steps):
            recommendations.append(
                "Implement least privilege access controls"
            )
            recommendations.append(
                "Enable detailed audit logging for file and system access"
            )
        
        if not recommendations:
            recommendations.append(
                "Continue regular security assessments and simulations"
            )
        
        return recommendations
