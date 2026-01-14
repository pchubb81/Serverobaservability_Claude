#!/usr/bin/env python3
"""
Azure Server Performance Observability System
Main entry point for the agent-based analysis system
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime
from colorama import init, Fore, Style

from src.agents.main_agent import MainAgent
from src.utils.logger import setup_logger
from src.utils.sample_data_generator import generate_sample_data

# Initialize colorama for cross-platform colored output
init(autoreset=True)

def print_banner():
    """Print application banner"""
    banner = f"""
{Fore.CYAN}================================================================
  Azure Server Performance Observability System
  AI-Powered Multi-Service Analysis & Bottleneck Detection
================================================================{Style.RESET_ALL}
"""
    print(banner)

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Azure Server Performance Observability System'
    )

    parser.add_argument(
        '--data-dir',
        type=str,
        default='./data/samples',
        help='Directory containing CSV/Excel files (default: ./data/samples)'
    )

    parser.add_argument(
        '--sample-data',
        action='store_true',
        help='Generate and use sample data for testing'
    )

    parser.add_argument(
        '--output-dir',
        type=str,
        default='./output',
        help='Directory for output reports (default: ./output)'
    )

    parser.add_argument(
        '--report-type',
        choices=['executive', 'technical', 'both'],
        default='both',
        help='Type of report to generate (default: both)'
    )

    parser.add_argument(
        '--format',
        choices=['html', 'pdf', 'both'],
        default='html',
        help='Output format (default: html)'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    return parser.parse_args()

def main():
    """Main execution function"""
    print_banner()

    # Parse arguments
    args = parse_arguments()

    # Setup logger
    logger = setup_logger(verbose=args.verbose)

    try:
        # Generate sample data if requested
        if args.sample_data:
            logger.info("Generating sample Azure metrics data...")
            sample_dir = Path('./data/samples')
            sample_dir.mkdir(parents=True, exist_ok=True)
            generate_sample_data(sample_dir)
            args.data_dir = str(sample_dir)
            logger.info(f"Sample data generated in {sample_dir}")

        # Validate data directory
        data_path = Path(args.data_dir)
        if not data_path.exists():
            logger.error(f"Data directory not found: {data_path}")
            sys.exit(1)

        # Create output directory
        output_path = Path(args.output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Initialize main agent
        logger.info("Initializing Azure Observability Agent System...")
        main_agent = MainAgent(
            data_dir=str(data_path),
            output_dir=str(output_path),
            report_type=args.report_type,
            output_format=args.format
        )

        # Run analysis
        logger.info(f"{Fore.GREEN}Starting multi-service analysis...{Style.RESET_ALL}")
        results = main_agent.analyze()

        # Generate reports
        logger.info(f"{Fore.GREEN}Generating reports and visualizations...{Style.RESET_ALL}")
        report_paths = main_agent.generate_reports(results)

        # Print summary
        print(f"\n{Fore.GREEN}{'='*60}")
        print(f"Analysis Complete!{Style.RESET_ALL}")
        print(f"{'='*60}")
        print(f"\n{Fore.CYAN}Generated Reports:{Style.RESET_ALL}")
        for report_type, path in report_paths.items():
            print(f"  • {report_type}: {path}")

        print(f"\n{Fore.YELLOW}Key Findings:{Style.RESET_ALL}")
        if 'summary' in results:
            summary = results['summary']
            print(f"  • Total Services Analyzed: {summary.get('services_analyzed', 0)}")
            print(f"  • Bottlenecks Detected: {summary.get('bottlenecks_count', 0)}")
            print(f"  • Overall Health Score: {summary.get('health_score', 'N/A')}")

        logger.info(f"{Fore.GREEN}Analysis completed successfully!{Style.RESET_ALL}")

    except KeyboardInterrupt:
        logger.warning("\nAnalysis interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
