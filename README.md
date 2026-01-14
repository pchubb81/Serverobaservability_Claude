# Azure Server Performance Observability System

A comprehensive agent-based system for analyzing Azure service metrics from CSV/Excel files, providing performance insights, bottleneck detection, and generating executive and technical reports.

## Features

- **Multi-Service Analysis**: Analyzes metrics from AKS, SQL Server, Azure Blob, APIs, and Redis Cache
- **Intelligent Agent System**: Main orchestrator with specialized sub-agents for each Azure service
- **Bottleneck Detection**: Correlates data across all metrics to identify performance issues
- **Dual Reports**: Executive summaries and detailed technical reports
- **Rich Visualizations**: Interactive charts, graphs, and HTML dashboards

## Quick Start

### Option 1: Interactive Web Dashboard (Recommended)

```bash
# Install dependencies
pip install -r requirements.txt

# Launch interactive dashboard
streamlit run streamlit_app.py

# Or use the launcher script
./launch_dashboard.sh   # Linux/Mac
launch_dashboard.bat    # Windows
```

The dashboard provides:
- 🎯 Real-time service health monitoring
- 🔧 Adjustable threshold settings
- 📊 Interactive charts with drill-down
- 🔄 On-demand data refresh
- 💾 Export analysis results
- 📈 Time-series filtering

### Option 2: Command-Line Analysis

```bash
# Run analysis with sample data
python main.py --sample-data

# Run analysis with your own data
python main.py --data-dir ./your_data_directory

# Generate only executive summary
python main.py --data-dir ./data --report-type executive
```

## Project Structure

```
serverobservability/
├── src/
│   ├── agents/           # Main agent and sub-agents
│   ├── analyzers/        # Analysis engines
│   ├── visualizers/      # Chart and dashboard generators
│   ├── reporters/        # Report generators
│   └── utils/            # Utility functions
├── data/
│   └── samples/          # Sample Azure metrics data
├── output/               # Generated reports and dashboards
├── templates/            # HTML/report templates
└── main.py              # Entry point
```

## Azure Services Supported

- **AKS (Azure Kubernetes Service)**: Pod metrics, node health, resource utilization
- **SQL Server**: Query performance, connection pools, wait statistics
- **Azure Blob**: Throughput, latency, transaction counts
- **API Performance**: Response times, error rates, throughput
- **Redis Cache**: Hit rates, memory usage, command latency

## Output

The system provides two interfaces:

### 🌐 Interactive Web Dashboard
- Real-time service health monitoring
- Customizable threshold settings
- Drill-down into specific services and metrics
- Time-series analysis with date filtering
- Correlation and bottleneck visualization
- Export results to JSON

### 📄 Static Reports (via CLI)
1. **Executive Summary** (HTML): High-level insights, KPIs, and recommendations
2. **Technical Report** (HTML): Detailed metrics, correlation analysis, and bottlenecks
3. **Dashboard** (HTML): Static charts and visualizations
