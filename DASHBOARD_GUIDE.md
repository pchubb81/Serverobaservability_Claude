# Interactive Dashboard Guide

## Quick Start

Launch the dashboard with one command:

```bash
# Option 1: Direct command
streamlit run streamlit_app.py

# Option 2: Use launcher script
./launch_dashboard.sh     # Linux/Mac
launch_dashboard.bat      # Windows
```

The dashboard will automatically open in your browser at `http://localhost:8501`

## Dashboard Overview

### 🎯 Control Panel (Left Sidebar)

The sidebar contains all configuration and control options:

#### 1. Data Source Selection
- **Use Sample Data**: Generate synthetic Azure metrics for testing
  - Click "Generate Fresh Sample Data" to create new test data
  - Data includes 24 hours of metrics with realistic anomalies
- **Upload Custom Data**: Point to your own CSV/Excel files
  - Specify directory containing your Azure metrics files

#### 2. Analysis Settings
- **Custom Thresholds** (Optional):
  - Enable checkbox to adjust detection thresholds
  - Sliders for CPU, Memory, DTU, Query Time, etc.
  - Changes apply to next analysis run
  - Great for sensitivity tuning

#### 3. Run Analysis
- Click "🚀 Run Analysis" button
- System loads agents and processes data
- Results appear in main area
- Typically completes in 2-5 seconds

#### 4. Export
- Download analysis results as JSON
- Includes metrics, health scores, anomalies, insights
- Timestamped filename for record-keeping

### 📊 Main Dashboard Area

When no analysis is loaded, you'll see:
- Getting started guide
- Supported Azure services list
- Step-by-step instructions

After running analysis, you get:

#### System Overview
Four key metrics at the top:
- **Overall Health Score**: 0-100 scale (80+ is healthy)
- **Services Analyzed**: Number of Azure services processed
- **Anomalies Detected**: Total issues found
- **Bottlenecks**: Cross-service performance limiters

#### Health Gauges
Five gauges showing health score for each service:
- Color-coded (green=healthy, yellow=warning, red=critical)
- Needle position shows current score
- Delta shows distance from healthy threshold (80)

## Interactive Tabs

### 🔍 Service Details Tab

**Purpose**: Deep dive into individual service metrics

**Features**:
1. **Service Selector**: Dropdown to choose AKS, SQL, Blob, API, or Redis
2. **Metrics Table**: All key metrics for selected service
   - CPU/Memory usage, response times, connection counts, etc.
   - Values formatted for readability
3. **Health Status**: Current health score and anomaly count
4. **Anomaly List**: All detected issues
   - Color-coded by severity (critical/high/medium)
   - Detailed descriptions
   - Affected resources listed

**Use Cases**:
- Investigate specific service issues
- Review detailed metric values
- Understand why health score is low
- Identify which pods/databases/endpoints are affected

### 🔗 Correlations Tab

**Purpose**: See how services affect each other

**Features**:
1. **Correlation Cards**: Each shows:
   - Connected services (e.g., "API ↔️ Redis")
   - Correlation description
   - Correlation coefficient (-1 to 1)
2. **Severity Indication**: How strong the relationship is

**Interpreting Correlations**:
- Coefficient close to 1: Strong positive correlation
- Coefficient close to -1: Strong negative correlation (inverse)
- Above 0.7: High priority to investigate

**Example**:
```
API ↔️ RedisCache
Low Redis cache hit rate correlates with higher API response times (r=0.85)
```
This means: Fix Redis cache issues, and API performance will improve.

### ⚠️ Bottlenecks Tab

**Purpose**: Identify and resolve root causes

**Features**:
1. **Expandable Cards**: Click to open details
2. **Each Bottleneck Shows**:
   - Service and bottleneck type
   - Detailed description
   - Impact assessment (which services affected)
   - Actionable recommendations (ordered by priority)

**Types of Bottlenecks**:
- **Resource Contention**: Infrastructure limiting everything
- **Cascade Bottleneck**: One service slowing others
- **Performance Degradation**: Service-specific issues

**How to Use**:
1. Read the description to understand the problem
2. Check the impact to see scope
3. Follow recommendations in order
4. Re-run analysis after fixes to verify improvement

### 📈 Time Series Tab

**Purpose**: Explore metrics over time

**Features**:
1. **Service Selector**: Choose which service to analyze
2. **Metric Selector**: Pick specific metric to plot
   - Options change based on selected service
   - Only numeric metrics shown
3. **Date Range Filters**:
   - Start date picker
   - End date picker
   - Instantly filters chart
4. **Interactive Chart**:
   - Hover for exact values
   - Zoom by dragging
   - Pan by holding shift and dragging
   - Reset with home button
5. **Statistics Panel**:
   - Mean, Median, P95, Max
   - Calculated for filtered date range

**Use Cases**:
- Identify when issues started
- Spot patterns (daily spikes, gradual degradation)
- Correlate with known events
- Verify if problems persist or resolved

**Example Workflow**:
1. User reports API slowness yesterday afternoon
2. Select "API" service
3. Select "response_time_ms" metric
4. Set date range to yesterday
5. See spike at 2 PM matching user report
6. Switch to "RedisCache" service
7. Check "cache_hit_rate" for same time
8. See corresponding drop in cache performance

### 💡 Insights Tab

**Purpose**: Get actionable recommendations

**Features**:
1. **Organized by Service**: Insights grouped by source
2. **Color-Coded**:
   - 🔴 Red box: Critical issues
   - ⚠️ Yellow box: Warnings
   - ✅ Green box: Positive findings
   - ℹ️ Blue box: Informational
3. **Plain Language**: No jargon, clear actions

**Types of Insights**:
- Performance warnings ("CPU usage is high - consider scaling")
- Optimization suggestions ("Enable caching to improve response times")
- Positive feedback ("No deadlocks detected - excellent transaction management")
- Configuration advice ("Review connection pooling settings")

## Advanced Features

### Custom Threshold Tuning

Why adjust thresholds?
- Your environment may have different "normal" values
- Reduce false positives
- Make detection more sensitive

How to use:
1. Enable "Custom Thresholds" checkbox in sidebar
2. Adjust sliders to your desired values
3. Run analysis
4. Observe if anomaly detection improves

Example:
- Default CPU threshold: 80%
- Your environment typically runs at 70-75%
- Lower threshold to 60% to detect issues earlier

### Generating Fresh Sample Data

Useful when:
- Testing dashboard features
- Demonstrating to stakeholders
- Learning the system

What it does:
- Creates 5 CSV/Excel files in `data/samples/`
- 24 hours of realistic metrics
- Includes injected anomalies (high CPU, slow queries, etc.)
- Different intervals per service (realistic timing)

### Exporting Results

Downloaded JSON includes:
```json
{
  "AKS": {
    "metrics": { ... },
    "health_score": 75.2,
    "anomalies": [ ... ],
    "insights": [ ... ]
  },
  "SQLServer": { ... },
  ...
}
```

Use cases:
- Keep historical records
- Share with team members
- Feed into other tools
- Compliance/auditing

## Tips & Tricks

### Performance Optimization

**For Large Datasets**:
- Time-series charts may be slow with >10,000 data points
- Use date range filters to reduce points
- Consider downsampling data before loading

**Dashboard Responsiveness**:
- Analysis runs on-demand (not continuous)
- Click "Run Analysis" only when needed
- Results cached until next run

### Keyboard Shortcuts

When using charts:
- **Scroll**: Zoom in/out
- **Shift + Drag**: Pan around chart
- **Double Click**: Reset zoom
- **Hover**: See exact values

### Comparing Runs

To compare before/after:
1. Run analysis, export results
2. Make changes to your infrastructure
3. Generate fresh data or wait for new data
4. Run analysis again, export results
5. Compare JSON files

### Understanding Health Scores

Score interpretation:
- **90-100**: Excellent - system is optimal
- **80-89**: Healthy - minor issues, monitor
- **60-79**: Warning - attention needed soon
- **40-59**: Degraded - significant issues
- **0-39**: Critical - immediate action required

Scores are **weighted**:
- Infrastructure (AKS): 1.5x weight
- Database (SQL): 1.3x weight
- Cache (Redis): 1.2x weight
- Application (API/Blob): 1.0x weight

This means AKS issues have bigger impact on overall score.

## Troubleshooting

### "No data found for [service]"
**Solution**:
- Check data directory path in sidebar
- Verify file naming matches patterns (see QUICKSTART.md)
- Ensure CSV/Excel files have required columns

### Charts not rendering
**Solution**:
- Check browser console for errors
- Ensure internet connection (needs CDN)
- Try different browser (Chrome recommended)
- Clear browser cache

### Analysis takes too long
**Solution**:
- Check data file sizes (>100MB can be slow)
- Reduce date range if using filters
- Ensure no other heavy processes running

### Custom thresholds not applying
**Solution**:
- Enable "Custom Thresholds" checkbox first
- Adjust sliders
- Click "Run Analysis" again (changes don't apply retroactively)

### Dashboard crashes or freezes
**Solution**:
- Refresh browser page
- Restart dashboard: Ctrl+C in terminal, then relaunch
- Check terminal for error messages
- Verify Python dependencies installed

## Best Practices

1. **Start with Sample Data**
   - Familiarize yourself with dashboard features
   - Understand what good/bad looks like
   - Test threshold adjustments

2. **Regular Analysis**
   - Run daily on fresh data
   - Export results for trending
   - Look for patterns over time

3. **Threshold Tuning**
   - Start with defaults
   - Adjust if too many/few alerts
   - Document your custom thresholds

4. **Investigate Systematically**
   - Start with Bottlenecks tab
   - Check Correlations for root causes
   - Drill into Service Details
   - Use Time Series to confirm timing

5. **Action on Insights**
   - Prioritize critical issues
   - Follow recommendations in order
   - Re-analyze after changes
   - Track improvements over time

## Next Steps

1. **Launch Dashboard**: `streamlit run streamlit_app.py`
2. **Generate Sample Data**: Click button in sidebar
3. **Run Analysis**: Click "Run Analysis"
4. **Explore Tabs**: Try each tab to understand features
5. **Try Custom Thresholds**: Adjust and see how detection changes
6. **Use Time Series**: Practice filtering and zooming
7. **Load Your Data**: Switch to custom data and analyze real metrics

For detailed technical documentation, see `CLAUDE.md`
