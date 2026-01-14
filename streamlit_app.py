"""
Interactive Streamlit Dashboard for Azure Performance Observability
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import json

from src.agents.aks_agent import AKSAgent
from src.agents.sql_agent import SQLAgent
from src.agents.blob_agent import BlobAgent
from src.agents.api_agent import APIAgent
from src.agents.redis_agent import RedisAgent
from src.analyzers.correlation_engine import CorrelationEngine
from src.utils.sample_data_generator import generate_sample_data

# Page configuration
st.set_page_config(
    page_title="Azure Performance Observability",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #0e639c;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .status-healthy { color: #4CAF50; font-weight: bold; }
    .status-warning { color: #FFC107; font-weight: bold; }
    .status-critical { color: #F44336; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
    st.session_state.results = None
    st.session_state.agents = {}
    st.session_state.data_dir = './data/samples'

def load_agents(data_dir: str):
    """Load all agents"""
    agents = {
        'AKS': AKSAgent(data_dir),
        'SQLServer': SQLAgent(data_dir),
        'BlobStorage': BlobAgent(data_dir),
        'API': APIAgent(data_dir),
        'RedisCache': RedisAgent(data_dir)
    }
    return agents

def run_analysis(agents, custom_thresholds=None):
    """Run analysis with optional custom thresholds"""
    results = {}

    # Apply custom thresholds if provided
    if custom_thresholds:
        for agent_name, agent in agents.items():
            if agent_name in custom_thresholds:
                agent.thresholds.update(custom_thresholds[agent_name])

    # Load and analyze each service
    for agent_name, agent in agents.items():
        if agent.load_data():
            result = agent.analyze()
            results[agent_name] = result
        else:
            results[agent_name] = {}

    # Correlation analysis
    correlation_engine = CorrelationEngine()
    correlation_results = correlation_engine.analyze_correlations(results)
    results['correlation_analysis'] = correlation_results

    return results

def create_health_gauge(score: float, title: str):
    """Create health score gauge"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 20}},
        delta={'reference': 80},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "green" if score >= 80 else "orange" if score >= 60 else "red"},
            'steps': [
                {'range': [0, 40], 'color': '#ffcccc'},
                {'range': [40, 60], 'color': '#ffffcc'},
                {'range': [60, 80], 'color': '#e6f3ff'},
                {'range': [80, 100], 'color': '#ccffcc'}
            ],
            'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 70}
        }
    ))
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20))
    return fig

def filter_time_series(df: pd.DataFrame, start_date, end_date):
    """Filter dataframe by date range"""
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        mask = (df['timestamp'] >= pd.to_datetime(start_date)) & (df['timestamp'] <= pd.to_datetime(end_date))
        return df[mask]
    return df

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/azure-1.png", width=80)
    st.title("⚙️ Control Panel")

    st.markdown("---")

    # Data source selection
    st.subheader("📁 Data Source")
    data_source = st.radio(
        "Choose data source:",
        ["Use Sample Data", "Upload Custom Data"]
    )

    if data_source == "Use Sample Data":
        if st.button("🔄 Generate Fresh Sample Data", type="primary"):
            with st.spinner("Generating sample Azure metrics..."):
                sample_dir = Path('./data/samples')
                sample_dir.mkdir(parents=True, exist_ok=True)
                generate_sample_data(sample_dir)
                st.session_state.data_dir = str(sample_dir)
                st.success("✅ Sample data generated!")
    else:
        uploaded_dir = st.text_input("Data directory path:", "./data/samples")
        st.session_state.data_dir = uploaded_dir

    st.markdown("---")

    # Analysis controls
    st.subheader("🔧 Analysis Settings")

    enable_custom_thresholds = st.checkbox("Custom Thresholds", value=False)

    custom_thresholds = {}
    if enable_custom_thresholds:
        st.markdown("**AKS Thresholds**")
        custom_thresholds['AKS'] = {
            'cpu_usage_percent': st.slider("CPU %", 0, 100, 80),
            'memory_usage_percent': st.slider("Memory %", 0, 100, 85)
        }

        st.markdown("**SQL Server Thresholds**")
        custom_thresholds['SQLServer'] = {
            'dtu_percent': st.slider("DTU %", 0, 100, 80),
            'avg_query_time_ms': st.slider("Query Time (ms)", 0, 1000, 300)
        }

    st.markdown("---")

    # Run analysis button
    if st.button("🚀 Run Analysis", type="primary", use_container_width=True):
        with st.spinner("Loading agents..."):
            st.session_state.agents = load_agents(st.session_state.data_dir)

        with st.spinner("Analyzing services..."):
            thresholds = custom_thresholds if enable_custom_thresholds else None
            st.session_state.results = run_analysis(st.session_state.agents, thresholds)
            st.session_state.data_loaded = True

        st.success("✅ Analysis complete!")

    # Export results
    if st.session_state.data_loaded:
        st.markdown("---")
        st.subheader("💾 Export")

        if st.button("Download JSON Results", use_container_width=True):
            # Prepare results for export (remove non-serializable items)
            export_data = {}
            for key, value in st.session_state.results.items():
                if key != 'correlation_analysis' and isinstance(value, dict):
                    export_data[key] = {
                        'metrics': value.get('metrics', {}),
                        'health_score': value.get('health_score'),
                        'anomalies': value.get('anomalies', []),
                        'insights': value.get('insights', [])
                    }

            st.download_button(
                label="📥 Download",
                data=json.dumps(export_data, indent=2),
                file_name=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

# ============================================
# MAIN CONTENT
# ============================================

st.markdown('<h1 class="main-header">📊 Azure Performance Observability Dashboard</h1>', unsafe_allow_html=True)

if not st.session_state.data_loaded:
    st.info("👈 Configure settings in the sidebar and click 'Run Analysis' to begin")

    # Show getting started guide
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        ### 🎯 Step 1: Choose Data
        - Use sample data for testing
        - Or provide your own CSV/Excel files
        """)

    with col2:
        st.markdown("""
        ### ⚙️ Step 2: Configure
        - Adjust thresholds (optional)
        - Set analysis parameters
        """)

    with col3:
        st.markdown("""
        ### 🚀 Step 3: Analyze
        - Click 'Run Analysis'
        - Explore interactive results
        """)

    st.markdown("---")
    st.markdown("### 📋 Supported Azure Services")

    services_df = pd.DataFrame({
        'Service': ['AKS', 'SQL Server', 'Blob Storage', 'API', 'Redis Cache'],
        'Metrics Analyzed': [
            'CPU, Memory, Pod Health',
            'DTU, Queries, Connections',
            'Latency, Throughput, Errors',
            'Response Time, Error Rate',
            'Hit Rate, Memory, Evictions'
        ],
        'Status': ['✅ Ready', '✅ Ready', '✅ Ready', '✅ Ready', '✅ Ready']
    })

    st.dataframe(services_df, use_container_width=True, hide_index=True)

else:
    # Extract results
    results = st.session_state.results
    correlation_analysis = results.get('correlation_analysis', {})
    system_health = correlation_analysis.get('system_health', {})

    # ============================================
    # OVERVIEW SECTION
    # ============================================
    st.header("🎯 System Overview")

    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        score = system_health.get('overall_score', 0)
        st.metric(
            label="Overall Health Score",
            value=f"{score:.1f}",
            delta=f"{score - 80:.1f}" if score < 80 else "Healthy"
        )

    with col2:
        services_analyzed = sum(1 for r in results.values() if isinstance(r, dict) and r.get('metrics'))
        st.metric(
            label="Services Analyzed",
            value=services_analyzed
        )

    with col3:
        total_anomalies = sum(len(r.get('anomalies', [])) for r in results.values() if isinstance(r, dict))
        st.metric(
            label="Anomalies Detected",
            value=total_anomalies,
            delta="Critical" if total_anomalies > 10 else "Normal",
            delta_color="inverse"
        )

    with col4:
        bottlenecks = len(correlation_analysis.get('bottlenecks', []))
        st.metric(
            label="Bottlenecks",
            value=bottlenecks,
            delta="Needs Attention" if bottlenecks > 0 else "None",
            delta_color="inverse"
        )

    # Health gauges
    st.markdown("### 📊 Health Scores by Service")
    gauge_cols = st.columns(5)

    service_names = ['AKS', 'SQLServer', 'BlobStorage', 'API', 'RedisCache']
    for idx, service in enumerate(service_names):
        if service in results and results[service]:
            with gauge_cols[idx]:
                score = results[service].get('health_score', 100)
                fig = create_health_gauge(score, service)
                st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ============================================
    # TABS FOR DETAILED VIEWS
    # ============================================
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔍 Service Details",
        "🔗 Correlations",
        "⚠️ Bottlenecks",
        "📈 Time Series",
        "💡 Insights"
    ])

    # TAB 1: Service Details
    with tab1:
        st.header("Service-Level Analysis")

        selected_service = st.selectbox(
            "Select service to analyze:",
            service_names,
            key="service_selector"
        )

        if selected_service in results and results[selected_service]:
            service_data = results[selected_service]

            col1, col2 = st.columns([2, 1])

            with col1:
                st.subheader(f"📊 {selected_service} Metrics")

                metrics = service_data.get('metrics', {})
                if metrics:
                    # Display metrics in a nice format
                    metrics_df = pd.DataFrame([
                        {'Metric': k.replace('_', ' ').title(), 'Value': f"{v:.2f}" if isinstance(v, float) else str(v)}
                        for k, v in metrics.items()
                    ])
                    st.dataframe(metrics_df, use_container_width=True, hide_index=True)

            with col2:
                st.subheader("🎯 Health Status")
                health_score = service_data.get('health_score', 0)

                if health_score >= 80:
                    st.success(f"✅ Healthy: {health_score:.1f}")
                elif health_score >= 60:
                    st.warning(f"⚠️ Warning: {health_score:.1f}")
                else:
                    st.error(f"🔴 Critical: {health_score:.1f}")

                anomaly_count = len(service_data.get('anomalies', []))
                st.metric("Anomalies", anomaly_count)

            # Anomalies
            st.subheader("🚨 Detected Anomalies")
            anomalies = service_data.get('anomalies', [])

            if anomalies:
                for anomaly in anomalies:
                    severity = anomaly.get('severity', 'medium')

                    if severity == 'critical':
                        st.error(f"**{anomaly.get('type')}** - {anomaly.get('description')}")
                    elif severity == 'high':
                        st.warning(f"**{anomaly.get('type')}** - {anomaly.get('description')}")
                    else:
                        st.info(f"**{anomaly.get('type')}** - {anomaly.get('description')}")
            else:
                st.success("No anomalies detected for this service!")

    # TAB 2: Correlations
    with tab2:
        st.header("Cross-Service Correlations")

        correlations = correlation_analysis.get('correlations', [])

        if correlations:
            for corr in correlations:
                services = corr.get('services', [])
                correlation_val = corr.get('correlation', 0)

                col1, col2 = st.columns([3, 1])

                with col1:
                    st.markdown(f"**{' ↔️ '.join(services)}**")
                    st.write(corr.get('description', ''))

                with col2:
                    st.metric("Correlation", f"{correlation_val:.3f}")

                st.markdown("---")
        else:
            st.info("No significant correlations detected between services.")

    # TAB 3: Bottlenecks
    with tab3:
        st.header("Performance Bottlenecks")

        bottlenecks = correlation_analysis.get('bottlenecks', [])

        if bottlenecks:
            for bn in bottlenecks:
                with st.expander(f"🔴 {bn.get('service')} - {bn.get('type')}", expanded=True):
                    st.write(f"**Description:** {bn.get('description')}")
                    st.write(f"**Impact:** {bn.get('impact')}")

                    st.markdown("**Recommendations:**")
                    recommendations = bn.get('recommendations', [])
                    for rec in recommendations:
                        st.markdown(f"- {rec}")
        else:
            st.success("🎉 No bottlenecks detected! System is performing well.")

    # TAB 4: Time Series
    with tab4:
        st.header("Time Series Analysis")

        # Service and metric selection
        col1, col2 = st.columns(2)

        with col1:
            ts_service = st.selectbox(
                "Select service:",
                service_names,
                key="ts_service"
            )

        with col2:
            # Get available metrics for selected service
            if ts_service in results and results[ts_service].get('time_series_data'):
                df = pd.DataFrame(results[ts_service]['time_series_data'])
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

                ts_metric = st.selectbox(
                    "Select metric:",
                    numeric_cols,
                    key="ts_metric"
                )

        # Date range filter
        if ts_service in results and results[ts_service].get('time_series_data'):
            df = pd.DataFrame(results[ts_service]['time_series_data'])

            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'])

                min_date = df['timestamp'].min().date()
                max_date = df['timestamp'].max().date()

                col1, col2 = st.columns(2)
                with col1:
                    start_date = st.date_input("Start date", min_date, min_value=min_date, max_value=max_date)
                with col2:
                    end_date = st.date_input("End date", max_date, min_value=min_date, max_value=max_date)

                # Filter data
                filtered_df = filter_time_series(df, start_date, end_date)

                # Plot
                if ts_metric in filtered_df.columns:
                    fig = px.line(
                        filtered_df,
                        x='timestamp',
                        y=ts_metric,
                        title=f"{ts_service}: {ts_metric.replace('_', ' ').title()} Over Time"
                    )
                    fig.update_layout(height=500)
                    st.plotly_chart(fig, use_container_width=True)

                    # Statistics
                    st.subheader("📊 Statistics")
                    col1, col2, col3, col4 = st.columns(4)

                    with col1:
                        st.metric("Mean", f"{filtered_df[ts_metric].mean():.2f}")
                    with col2:
                        st.metric("Median", f"{filtered_df[ts_metric].median():.2f}")
                    with col3:
                        st.metric("P95", f"{filtered_df[ts_metric].quantile(0.95):.2f}")
                    with col4:
                        st.metric("Max", f"{filtered_df[ts_metric].max():.2f}")

    # TAB 5: Insights
    with tab5:
        st.header("💡 Actionable Insights")

        for service in service_names:
            if service in results and results[service]:
                insights = results[service].get('insights', [])

                if insights:
                    st.subheader(f"{service}")

                    for insight in insights:
                        if '⚠️' in insight or '🔴' in insight:
                            st.warning(insight)
                        elif '✅' in insight:
                            st.success(insight)
                        else:
                            st.info(insight)

                    st.markdown("---")
