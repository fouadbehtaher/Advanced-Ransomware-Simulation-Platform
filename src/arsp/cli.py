"""
Command-line interface for ARSP

Provides CLI commands for managing simulations, analysis, and reporting.
"""
import click
import sys
from pathlib import Path

from arsp import __version__
from arsp.core.config import Config
from arsp.core.logger import Logger
from arsp.simulation import SimulationEngine, ScenarioBuilder, ScenarioType
from arsp.analysis import BehavioralAnalyzer, Reporter
from arsp.isolation import Sandbox
from arsp.monitoring import SystemMonitor, FileMonitor


@click.group()
@click.version_option(version=__version__)
@click.option('--config', '-c', type=click.Path(exists=True), help='Configuration file path')
@click.pass_context
def cli(ctx, config):
    """Advanced Ransomware Simulation Platform (ARSP)
    
    A secure framework for executing and analyzing ransomware behaviors.
    """
    ctx.ensure_object(dict)
    ctx.obj['config'] = Config(config) if config else Config()


@cli.command()
@click.option('--scenario', '-s', 
              type=click.Choice(['encryption', 'exfiltration', 'full-chain']),
              default='encryption',
              help='Scenario type to simulate')
@click.option('--sandbox', '-b', is_flag=True, help='Run in sandbox environment')
@click.option('--monitor', '-m', is_flag=True, help='Enable system monitoring')
@click.option('--output', '-o', type=click.Path(), help='Output path for results')
@click.pass_context
def simulate(ctx, scenario, sandbox, monitor, output):
    """Execute a ransomware simulation scenario"""
    config = ctx.obj['config']
    logger = Logger().get_logger("cli", config.get("monitoring.log_level"))
    
    click.echo(f"🚀 Starting ARSP simulation: {scenario}")
    click.echo("-" * 50)
    
    try:
        # Create scenario
        if scenario == 'encryption':
            sim_scenario = ScenarioBuilder.create_encryption_scenario()
        elif scenario == 'exfiltration':
            sim_scenario = ScenarioBuilder.create_exfiltration_scenario()
        elif scenario == 'full-chain':
            sim_scenario = ScenarioBuilder.create_full_attack_chain()
        else:
            click.echo(f"❌ Unknown scenario: {scenario}", err=True)
            sys.exit(1)
        
        # Setup sandbox if requested
        sandbox_path = None
        sandbox_env = None
        if sandbox:
            click.echo("📦 Creating sandbox environment...")
            sandbox_env = Sandbox(config)
            sandbox_path = sandbox_env.create()
            sandbox_env.populate()
            click.echo(f"   Sandbox: {sandbox_path}")
        
        # Setup monitoring if requested
        sys_monitor = None
        file_monitor = None
        if monitor:
            click.echo("👁️  Starting monitoring...")
            sys_monitor = SystemMonitor(config)
            sys_monitor.start(interval=1.0)
            
            if sandbox_path:
                file_monitor = FileMonitor(config)
                file_monitor.start(str(sandbox_path))
        
        # Execute simulation
        click.echo("⚡ Executing simulation...")
        engine = SimulationEngine(config)
        results = engine.execute(sim_scenario, str(sandbox_path) if sandbox_path else None)
        
        # Stop monitoring
        if sys_monitor:
            sys_monitor.stop()
            click.echo(f"   System monitoring: {len(sys_monitor.get_metrics())} samples collected")
        
        if file_monitor:
            file_monitor.stop()
            click.echo(f"   File monitoring: {len(file_monitor.get_events())} events recorded")
        
        # Display results
        click.echo("\n" + "=" * 50)
        click.echo("📊 SIMULATION RESULTS")
        click.echo("=" * 50)
        click.echo(f"Status: {results['status']}")
        click.echo(f"Duration: {results['duration_seconds']:.2f}s")
        click.echo(f"Steps executed: {len(results.get('steps', []))}")
        
        # Save results if output specified
        if output:
            import json
            output_path = Path(output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                json.dump(results, f, indent=2)
            click.echo(f"\n💾 Results saved to: {output}")
        
        # Cleanup
        if sandbox_env:
            click.echo("\n🧹 Cleaning up sandbox...")
            sandbox_env.cleanup(remove_all=False)
        
        click.echo("\n✅ Simulation completed successfully!")
        
    except Exception as e:
        logger.error(f"Simulation failed: {str(e)}")
        click.echo(f"\n❌ Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('results_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output path for analysis')
@click.option('--format', '-f', 
              type=click.Choice(['json', 'text', 'html']),
              default='text',
              help='Output format')
@click.pass_context
def analyze(ctx, results_file, output, format):
    """Analyze simulation results"""
    config = ctx.obj['config']
    logger = Logger().get_logger("cli", config.get("monitoring.log_level"))
    
    click.echo(f"🔍 Analyzing results: {results_file}")
    click.echo("-" * 50)
    
    try:
        # Load results
        import json
        with open(results_file, 'r') as f:
            results = json.load(f)
        
        # Analyze
        click.echo("🧠 Running behavioral analysis...")
        analyzer = BehavioralAnalyzer(config)
        analysis = analyzer.analyze(results)
        
        # Display summary
        click.echo("\n" + "=" * 50)
        click.echo("📊 ANALYSIS RESULTS")
        click.echo("=" * 50)
        
        risk = analysis.get('risk_assessment', {})
        click.echo(f"Risk Level: {risk.get('level', 'unknown').upper()}")
        click.echo(f"Risk Score: {risk.get('score', 0)}/100")
        
        patterns = analysis.get('behavior_patterns', [])
        click.echo(f"\nBehavioral Patterns: {len(patterns)}")
        for pattern in patterns:
            click.echo(f"  - {pattern['description']} (Severity: {pattern['severity']})")
        
        recommendations = analysis.get('recommendations', [])
        click.echo(f"\nRecommendations: {len(recommendations)}")
        for i, rec in enumerate(recommendations, 1):
            click.echo(f"  {i}. {rec}")
        
        # Save analysis if output specified
        if output:
            output_path = Path(output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                json.dump(analysis, f, indent=2)
            click.echo(f"\n💾 Analysis saved to: {output}")
        
        click.echo("\n✅ Analysis completed!")
        
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        click.echo(f"\n❌ Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('results_file', type=click.Path(exists=True))
@click.option('--analysis', '-a', type=click.Path(exists=True), 
              help='Optional analysis results file')
@click.option('--format', '-f',
              type=click.Choice(['json', 'text', 'html']),
              default='html',
              help='Report format')
@click.option('--output', '-o', type=click.Path(), help='Output path for report')
@click.pass_context
def report(ctx, results_file, analysis, format, output):
    """Generate report from simulation and analysis results"""
    config = ctx.obj['config']
    logger = Logger().get_logger("cli", config.get("monitoring.log_level"))
    
    click.echo(f"📝 Generating {format} report...")
    click.echo("-" * 50)
    
    try:
        # Load results
        import json
        with open(results_file, 'r') as f:
            results = json.load(f)
        
        analysis_data = None
        if analysis:
            with open(analysis, 'r') as f:
                analysis_data = json.load(f)
        
        # Generate report
        reporter = Reporter(config)
        report_path = reporter.generate_report(results, analysis_data, format)
        
        click.echo(f"\n✅ Report generated: {report_path}")
        
        if output:
            import shutil
            shutil.copy(report_path, output)
            click.echo(f"   Copied to: {output}")
        
    except Exception as e:
        logger.error(f"Report generation failed: {str(e)}")
        click.echo(f"\n❌ Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.pass_context
def info(ctx):
    """Display platform information"""
    config = ctx.obj['config']
    
    click.echo("=" * 50)
    click.echo("Advanced Ransomware Simulation Platform (ARSP)")
    click.echo("=" * 50)
    click.echo(f"Version: {__version__}")
    click.echo(f"Simulation Mode: {config.get('simulation.mode')}")
    click.echo(f"Sandbox Path: {config.get('simulation.sandbox_path')}")
    click.echo(f"Log Level: {config.get('monitoring.log_level')}")
    click.echo(f"Network Isolation: {config.get('security.enable_network_isolation')}")
    click.echo(f"Filesystem Isolation: {config.get('security.enable_filesystem_isolation')}")
    click.echo("=" * 50)


def main():
    """Main entry point"""
    cli(obj={})


if __name__ == '__main__':
    main()
