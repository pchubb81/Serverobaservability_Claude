# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Azure Server Performance Observability System - An AI-powered agent-based system that analyzes CSV/Excel files containing Azure service metrics, performs cross-service correlation analysis, detects bottlenecks, and generates executive summaries and detailed technical reports with interactive visualizations.

## Core Architecture

### Agent-Based System

The system uses a hierarchical agent architecture:

1. **MainAgent** (`src/agents/main_agent.py`) - Orchestrates all sub-agents and coordinates the analysis pipeline
2. **Sub-Agents** - Specialized agents for each Azure service:
   - **AKSAgent** - Analyzes Kubernetes pod/node metrics
   - **SQLAgent** - Analyzes SQL Server performance (DTU, queries, connections)
   - **BlobAgent** - Analyzes Blob Storage latency and throughput
   - **APIAgent** - Analyzes API response times and error rates
   - **RedisAgent** - Analyzes Redis cache hit rates and memory usage

3. **BaseAgent** (`src/agents/base_agent.py`) - Abstract base class that all sub-agents inherit from, providing:
   - Data loading interface
   - Anomaly detection framework
   - Health score calculation
   - Trend identification

### Data Flow

```
CSV/Excel Files → Sub-Agents (load_data) → Sub-Agents (analyze) → MainAgent (orchestrate)
                                          ↓
                      CorrelationEngine (cross-service analysis)
                                          ↓
                      Report Generators (executive + technical)
                                          ↓
                      Dashboard Generator (interactive HTML)
```

### Key Components

#### Correlation Engine (`src/analyzers/correlation_engine.py`)

The correlation engine is the intelligence layer that:
- Merges time-series data across services using time-based alignment
- Calculates correlation coefficients between service metrics
- Identifies root causes in cascade failures (prioritizes infrastructure → database → cache → application)
- Detects bottlenecks by combining health scores, anomalies, and correlations
- Calculates weighted system health (infrastructure services weighted higher)

**Critical Correlation Patterns:**
- API response time ↔ Redis cache hit rate
- API response time ↔ SQL query time
- AKS CPU usage ↔ All service performance metrics

#### Visualization System

- **ChartGenerator** (`src/visualizers/chart_generator.py`) - Creates Plotly charts (gauges, time series, heatmaps, correlations)
- **DashboardGenerator** (`src/visualizers/dashboard_generator.py`) - Generates standalone HTML dashboards
- **ExecutiveReportGenerator** (`src/reporters/executive_report.py`) - Business-focused summary reports
- **TechnicalReportGenerator** (`src/reporters/technical_report.py`) - Engineering-focused detailed reports

## Common Development Commands

### Setup and Installation

```bash
# Install dependencies (includes Streamlit for interactive dashboard)
pip install -r requirements.txt

# Verify installation
python -c "import pandas, plotly, streamlit; print('Dependencies OK')"
```

### Running Analysis

#### Interactive Dashboard (Recommended for Development)

```bash
# Launch interactive web dashboard
streamlit run streamlit_app.py

# Dashboard will open at http://localhost:8501
# Features:
# - Real-time threshold adjustment
# - Interactive filtering and drill-down
# - On-demand analysis execution
# - Time-series exploration with date filters
# - Export results to JSON

# Use launcher scripts for convenience
./launch_dashboard.sh   # Linux/Mac
launch_dashboard.bat    # Windows
```

#### Command-Line Analysis

```bash
# Run with sample data (generates synthetic Azure metrics)
python main.py --sample-data

# Run with your own data
python main.py --data-dir ./path/to/your/csv_files

# Generate only executive summary
python main.py --data-dir ./data --report-type executive

# Generate only technical report
python main.py --data-dir ./data --report-type technical

# Enable verbose logging
python main.py --sample-data --verbose
```

### Testing

```bash
# Test with sample data generation
python -c "from src.utils.sample_data_generator import generate_sample_data; from pathlib import Path; generate_sample_data(Path('./test_data'))"

# Test individual agent
python -c "from src.agents.aks_agent import AKSAgent; agent = AKSAgent('./data/samples'); agent.load_data(); print(agent.analyze())"
```

### Data File Requirements

The system expects CSV/Excel files with specific naming patterns:
- AKS: Files matching `*aks*.csv`
- SQL Server: Files matching `*sql*.xlsx` or `*sql*.csv`
- Blob Storage: Files matching `*blob*.csv`
- API Performance: Files matching `*api*.xlsx` or `*api*.csv`
- Redis Cache: Files matching `*redis*.csv`

## Architecture Patterns

### Adding a New Azure Service Agent

1. Create new agent class inheriting from `BaseAgent` in `src/agents/`
2. Implement required methods: `load_data()`, `analyze()`, `detect_anomalies()`, `get_insights()`
3. Define service-specific thresholds in `__init__`
4. Add agent to `MainAgent.agents` dictionary
5. Update correlation engine to include new service correlations

Example structure:
```python
class NewServiceAgent(BaseAgent):
    def __init__(self, data_dir: str):
        super().__init__("ServiceName", data_dir)
        self.thresholds = {
            'metric_name': threshold_value
        }

    def load_data(self) -> bool:
        # Load CSV/Excel files
        # Parse timestamps
        # Return True if successful

    def analyze(self) -> Dict[str, Any]:
        # Calculate metrics
        # Detect anomalies
        # Generate insights
        # Calculate health score
        # Return comprehensive results dict
```

### Health Score Calculation

Health scores (0-100) are calculated using `calculate_health_score()` from BaseAgent:
- Compare metrics against thresholds
- 100: metric ≤ threshold
- 70: metric ≤ threshold * 1.5
- 40: metric ≤ threshold * 2
- 20: metric > threshold * 2

System-level health uses weighted averaging (defined in `CorrelationEngine._calculate_system_health`):
- AKS: 1.5x weight (infrastructure)
- SQLServer: 1.3x weight (critical data layer)
- RedisCache: 1.2x weight (caching layer)
- API/BlobStorage: 1.0x weight

### Anomaly Detection Patterns

Each agent detects service-specific anomalies using:
1. Threshold-based detection (values exceeding defined limits)
2. Statistical detection (values beyond mean + 3*std)
3. Rate-based detection (error rates, cache miss rates)
4. Time-based patterns (sustained degradation periods)

Anomalies include:
- `type`: Category of anomaly
- `severity`: critical/high/medium
- `count`: Number of occurrences
- `description`: Human-readable explanation
- `affected_*`: List of impacted resources

### Correlation Detection

The correlation engine uses `pd.merge_asof` for time-aligned joins with 5-minute tolerance. Correlations are flagged when:
- Absolute correlation coefficient > 0.5 (moderate correlation)
- Correlation > 0.7 triggers high severity
- Special handling for infrastructure cascades (AKS affecting all services)

## File Organization

```
src/
├── agents/          # All agent implementations
│   ├── base_agent.py       # Abstract base class
│   ├── main_agent.py       # Orchestrator
│   └── *_agent.py          # Service-specific agents
├── analyzers/       # Analysis engines
│   └── correlation_engine.py  # Cross-service correlation
├── visualizers/     # Visualization generation
│   ├── chart_generator.py     # Plotly charts
│   └── dashboard_generator.py # Static HTML dashboard
├── reporters/       # Report generation
│   ├── executive_report.py    # Executive summary
│   └── technical_report.py    # Technical details
└── utils/          # Utilities
    ├── logger.py              # Logging setup
    └── sample_data_generator.py  # Test data generation

# Top-level files
├── main.py                # CLI entry point
├── streamlit_app.py       # Interactive web dashboard (NEW)
├── launch_dashboard.sh    # Dashboard launcher (Linux/Mac)
└── launch_dashboard.bat   # Dashboard launcher (Windows)
```

## Key Design Decisions

### Why Agent-Based Architecture?

Each Azure service has unique metrics, thresholds, and analysis patterns. The agent-based design:
- Allows independent development and testing of service analyzers
- Enables easy addition of new Azure services
- Provides clear separation of concerns
- Supports parallel analysis of services

### Why Correlation Engine is Separate?

Cross-service analysis requires:
- Access to all service data simultaneously
- Complex time-series alignment
- Domain knowledge of service dependencies
- Root cause determination logic

Keeping this in a separate engine allows the MainAgent to remain simple and focused on orchestration.

### Sample Data Generation

The sample data generator (`src/utils/sample_data_generator.py`) creates realistic Azure metrics with:
- Normal operational patterns
- Injected anomalies (CPU spikes, query slowdowns, cache misses)
- Time-correlated events (simulating real cascade failures)
- 24 hours of data at appropriate intervals

This is essential for testing and demonstrating the system without real Azure data.

## Interactive Dashboard Architecture

The Streamlit dashboard (`streamlit_app.py`) provides a web-based interface for:

### Key Features

1. **Session State Management**: Uses `st.session_state` to persist:
   - Loaded agents
   - Analysis results
   - Data directory path
   - Custom thresholds

2. **Real-Time Analysis**:
   - Click "Run Analysis" to execute agents on-demand
   - Supports custom threshold adjustment via sidebar
   - Regenerate sample data without restarting

3. **Interactive Tabs**:
   - **Service Details**: Drill down into individual services, view metrics and anomalies
   - **Correlations**: Visualize cross-service relationships
   - **Bottlenecks**: View detected bottlenecks with recommendations
   - **Time Series**: Filter and explore metrics over time with date range selection
   - **Insights**: Aggregated actionable insights from all services

4. **Export Functionality**:
   - Download analysis results as JSON
   - Preserves metrics, health scores, anomalies, and insights

### Customizing the Dashboard

To add new features to the dashboard:

```python
# Add a new tab in streamlit_app.py
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🔍 Service Details",
    "🔗 Correlations",
    "⚠️ Bottlenecks",
    "📈 Time Series",
    "💡 Insights",
    "🆕 Your New Tab"  # Add here
])

with tab6:
    st.header("Your New Feature")
    # Add your custom visualization or analysis
```

To add new threshold controls:

```python
# In the sidebar section
st.markdown("**Your Service Thresholds**")
custom_thresholds['YourService'] = {
    'your_metric': st.slider("Your Metric", 0, 100, 50)
}
```

### Dashboard Performance Considerations

- **Large Datasets**: Time-series charts may be slow with >10,000 points. Consider downsampling.
- **Session State**: Results are kept in memory. Clear `st.session_state` for fresh start.
- **Caching**: Use `@st.cache_data` for expensive computations that don't change often.

## Extension Points

### Adding New Metrics to Existing Agents

1. Update the data loading in `load_data()` to parse new columns
2. Add metric calculations in `analyze()`
3. Update thresholds if needed
4. Add anomaly detection rules in `detect_anomalies()`
5. Generate insights in `get_insights()`

### Adding New Correlation Patterns

Edit `CorrelationEngine._detect_correlations()`:
1. Identify which services to correlate
2. Select relevant metrics from each service
3. Use `pd.merge_asof` for time alignment
4. Calculate correlation coefficient
5. Add to correlations list if threshold exceeded

### Custom Visualizations

Create new methods in `ChartGenerator`:
- Use Plotly's graph_objects or express modules
- Follow existing pattern: return `go.Figure`
- Use consistent color schemes from `self.default_colors`
- Set appropriate height and template

## Performance Considerations

- **Memory**: Large CSV files (>100MB) may require chunked reading
- **Correlation**: Time-series alignment with `merge_asof` is O(n log n)
- **Visualization**: Plotly charts embed data in HTML (large datasets = large files)
- **Parallelization**: Agents could run in parallel (currently sequential)

## Troubleshooting

### No data loaded for service X
- Check file naming pattern matches glob patterns
- Verify CSV/Excel files have required columns
- Check file permissions

### Correlation analysis returns empty
- Ensure multiple services have time_series_data
- Verify timestamps are parseable by pandas
- Check that timestamps overlap between services

### Charts not rendering in reports
- Ensure plotly is installed: `pip install plotly`
- Check browser console for JavaScript errors
- Verify include_plotlyjs='cdn' has internet access
