# Azure Server Performance Observability - Quick Start Guide

## What This System Does

This is an AI-powered agent-based system that:

1. **Analyzes Azure service metrics** from CSV/Excel files (AKS, SQL Server, Blob Storage, APIs, Redis Cache)
2. **Detects anomalies and bottlenecks** across all services using intelligent correlation
3. **Generates comprehensive reports**:
   - **Executive Summary** - High-level business insights for leadership
   - **Technical Report** - Detailed engineering analysis with metrics
   - **Interactive Dashboard** - Visual charts and real-time data exploration

## Installation

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Verify installation
python -c "import pandas, plotly; print('All dependencies installed successfully!')"
```

## Running Your First Analysis

### Option 1: Interactive Dashboard (BEST for Exploration)

```bash
# Launch the web dashboard
streamlit run streamlit_app.py

# Or use launcher scripts
./launch_dashboard.sh   # Linux/Mac
launch_dashboard.bat    # Windows
```

**Dashboard opens at: http://localhost:8501**

The interactive dashboard provides:
- 🔄 Real-time analysis with custom thresholds
- 🎯 Drill-down into specific services
- 📈 Time-series filtering and exploration
- 🔍 Interactive charts with zoom/pan
- 💾 Export results to JSON
- 🎨 Beautiful, responsive UI

**Dashboard Features:**
1. Generate sample data with one click
2. Adjust thresholds via sliders
3. Run analysis on-demand
4. Explore 5 interactive tabs:
   - Service Details (metrics + anomalies)
   - Correlations (cross-service relationships)
   - Bottlenecks (root cause analysis)
   - Time Series (date-filtered charts)
   - Insights (actionable recommendations)

See `DASHBOARD_GUIDE.md` for complete dashboard documentation.

### Option 2: Command-Line Analysis (Fast Batch Processing)

```bash
# Generate synthetic Azure metrics and run analysis
python main.py --sample-data

# View the generated reports in the output/ directory
```

### Option 3: Test with Sample Data (CLI)

```bash
# Generate synthetic Azure metrics and run analysis
python main.py --sample-data

# View the generated reports in the output/ directory
```

### Option 4: Analyze Your Own Data

```bash
# 1. Place your CSV/Excel files in a directory (e.g., ./my_data/)
#    Files should match these patterns:
#    - *aks*.csv - AKS metrics
#    - *sql*.xlsx or *sql*.csv - SQL Server metrics
#    - *blob*.csv - Blob Storage metrics
#    - *api*.xlsx or *api*.csv - API performance
#    - *redis*.csv - Redis Cache metrics

# 2. Run analysis
python main.py --data-dir ./my_data

# 3. Open reports in output/ directory
```

## What Gets Generated

After running, you'll find in the `output/` directory:

1. **executive_summary_[timestamp].html**
   - System health score and status
   - Critical issues requiring attention
   - Performance bottlenecks with recommendations
   - Service health overview

2. **technical_report_[timestamp].html**
   - Detailed metrics for each service
   - Anomaly breakdown by type and severity
   - Cross-service correlation analysis
   - Technical insights and recommendations

3. **dashboard_[timestamp].html**
   - Interactive visualizations
   - Time-series charts for all metrics
   - Anomaly heatmaps
   - Service correlation matrix

## Example: Understanding the Output

### Health Score Interpretation

- **80-100**: Healthy - System performing well
- **60-79**: Warning - Some issues detected
- **40-59**: Degraded - Significant performance issues
- **0-39**: Critical - Immediate attention required

### Common Bottlenecks Detected

The system automatically identifies:
- **Resource Contention** - AKS CPU/memory limiting other services
- **Cache Inefficiency** - Low Redis hit rates slowing APIs
- **Database Performance** - SQL query times affecting APIs
- **Network Latency** - Blob storage latency issues

### Reading Correlations

When the system says: "Redis cache hit rate correlates with API response times (r=0.85)"
- This means low cache performance directly impacts API speed
- The number (r=0.85) indicates strength (0.85 = very strong)
- Recommendations will prioritize fixing the root cause (Redis)

## Advanced Usage

### Generate Only Executive Summary

```bash
python main.py --data-dir ./data --report-type executive
```

### Generate Only Technical Report

```bash
python main.py --data-dir ./data --report-type technical
```

### Enable Verbose Logging

```bash
python main.py --sample-data --verbose
```

## Expected Data Format

Your CSV/Excel files should have these columns:

### AKS Metrics
- `timestamp`, `pod_name`, `node_name`, `cpu_usage_percent`, `memory_usage_mb`, `memory_limit_mb`

### SQL Server Metrics
- `timestamp`, `dtu_percent`, `cpu_percent`, `avg_query_time_ms`, `active_connections`, `blocked_connections`

### Blob Storage Metrics
- `timestamp`, `total_requests`, `successful_requests`, `avg_e2e_latency_ms`, `ingress_bytes`, `egress_bytes`

### API Performance Metrics
- `timestamp`, `endpoint`, `method`, `status_code`, `response_time_ms`, `cache_hit_ratio`

### Redis Cache Metrics
- `timestamp`, `memory_used_mb`, `memory_limit_mb`, `cache_hits_per_sec`, `cache_misses_per_sec`, `evicted_keys`

## Troubleshooting

### "No data found for [service]"
- Check your file naming matches the expected patterns
- Verify CSV/Excel files have required columns
- Ensure timestamps are in a parseable format

### Charts not showing in reports
- Ensure you have internet connection (charts use CDN)
- Try opening reports in a different browser
- Check browser console for JavaScript errors

### "Module not found" errors
- Run: `pip install -r requirements.txt`
- Verify you're using Python 3.8 or higher

## Project Structure

```
serverobservability/
├── main.py                 # Entry point - start here
├── src/
│   ├── agents/             # Service-specific analyzers
│   ├── analyzers/          # Correlation engine
│   ├── visualizers/        # Chart generation
│   └── reporters/          # Report generators
├── data/samples/           # Sample data (generated)
├── output/                 # Generated reports
└── CLAUDE.md              # Detailed development guide
```

## Next Steps

1. **Test with Sample Data**: Run `python main.py --sample-data` to see the system in action
2. **Analyze Your Data**: Prepare your Azure metrics files and run analysis
3. **Review Reports**: Open the HTML reports in your browser
4. **Take Action**: Follow recommendations in the executive summary
5. **Deep Dive**: Use technical report for detailed investigation

## Support

For detailed architecture and development information, see:
- `README.md` - Project overview
- `CLAUDE.md` - Development guide for extending the system

## Example Run

```bash
$ python main.py --sample-data

================================================================
  Azure Server Performance Observability System
  AI-Powered Multi-Service Analysis & Bottleneck Detection
================================================================

Generating sample Azure metrics data...
  + Generated AKS metrics: 1441 records
  + Generated SQL Server metrics: 289 records
  + Generated Blob Storage metrics: 481 records
  + Generated API Performance metrics: 1441 records
  + Generated Redis Cache metrics: 721 records

Analysis Complete!

Generated Reports:
  • Executive Summary: output/executive_summary_20260114_171246.html
  • Technical Report: output/technical_report_20260114_171246.html
  • Interactive Dashboard: output/dashboard_20260114_171246.html

Key Findings:
  • Total Services Analyzed: 5
  • Bottlenecks Detected: 2
  • Overall Health Score: 62.0
```

Now open the reports in your browser to see the insights!
