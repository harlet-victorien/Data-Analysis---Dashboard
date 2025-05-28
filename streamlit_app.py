import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from tim import InvestmentAnalyzer
import io

# Configure the page
st.set_page_config(
    page_title="Investment Analyzer Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("📈 Investment Analyzer Dashboard")
st.markdown("""
This app analyzes investment data from CSV files and helps find optimal parameters for investment strategies.
Upload a CSV file or use the default test.csv to get started.
""")

# Sidebar for configuration
st.sidebar.header("Configuration")

# File upload
uploaded_file = st.sidebar.file_uploader(
    "Choose a CSV file", 
    type="csv",
    help="Upload a CSV file with investment data"
)

# Use default file if no file uploaded
if uploaded_file is None:
    file_path = "test.csv"
    st.sidebar.info("Using default test.csv file")
else:
    # Save uploaded file temporarily
    file_path = f"temp_{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

# Configuration parameters
st.sidebar.subheader("Analysis Parameters")
stop_loss = st.sidebar.slider("Stop Loss", 0.0, 1.0, 0.3, 0.1, help="Stop loss percentage")
with_scam = st.sidebar.checkbox("Include Scam Data", False, help="Include scam data in analysis")

# Parameter ranges for optimization
st.sidebar.subheader("Optimization Ranges")
x_min = st.sidebar.number_input("X Min", value=20000, step=10000)
x_max = st.sidebar.number_input("X Max", value=1000000, step=10000)
y_min = st.sidebar.number_input("Y Min", value=20000, step=10000)
y_max = st.sidebar.number_input("Y Max", value=1000000, step=10000)
step = st.sidebar.number_input("Step Size", value=10000, step=1000)

# Create analyzer instance
try:
    analyzer = InvestmentAnalyzer(file_path, stop_loss=stop_loss, with_scam=with_scam)
    st.success(f"✅ Data loaded successfully! Found {len(analyzer.data)} data points.")
except Exception as e:
    st.error(f"❌ Error loading data: {str(e)}")
    st.stop()

# Main content area with tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Data Overview", "🎯 Parameter Analysis", "🔍 Optimization", "📈 Visualizations"])

with tab1:
    st.header("Data Overview")
    
    # Display basic statistics
    col1, col2, col3 = st.columns(3)
    
    values = [item[0] for item in analyzer.data]
    scams = [item[1] for item in analyzer.data]
    
    with col1:
        st.metric("Total Data Points", len(analyzer.data))
        st.metric("Average Value", f"{np.mean(values):.2f}")
    
    with col2:
        st.metric("Scam Count", sum(scams))
        st.metric("Scam Percentage", f"{(sum(scams)/len(scams)*100):.1f}%")
    
    with col3:
        st.metric("Max Value", max(values))
        st.metric("Min Value", min(values))
    
    # Data distribution
    st.subheader("Value Distribution")
    fig = px.histogram(x=values, nbins=50, title="Distribution of Investment Values")
    fig.update_layout(xaxis_title="Value", yaxis_title="Frequency")
    st.plotly_chart(fig, use_container_width=True)
    
    # Show raw data sample
    st.subheader("Data Sample")
    df = pd.DataFrame(analyzer.data, columns=['Value', 'Is_Scam'])
    st.dataframe(df.head(20), use_container_width=True)

with tab2:
    st.header("Parameter Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Custom Parameter Testing")
        test_x = st.number_input("Test X Value", value=100000, step=10000)
        test_y = st.number_input("Test Y Value", value=100000, step=10000)
        
        if st.button("Calculate Expected Value", type="secondary"):
            rate = analyzer.find_rate(test_x, test_y)
            value = analyzer.find_value(test_x, test_y)
            
            st.success(f"Rate: {rate:.4f}")
            st.success(f"Expected Value: {value:.2f}")
    
    with col2:
        st.subheader("Expected Value Calculator")
        calc_stop_loss = st.slider("Stop Loss for Calculation", 0.0, 1.0, 0.3, 0.1)
        calc_multiplier = st.slider("Multiplier", 0.1, 5.0, 1.0, 0.1)
        calc_rate = st.slider("Rate", 0.0, 1.0, 0.5, 0.01)
        
        expected_val = analyzer.expected_value(calc_stop_loss, calc_multiplier, calc_rate)
        st.metric("Expected Value", f"{expected_val:.4f}")

with tab3:
    st.header("Parameter Optimization")
    
    # Run optimization button
    if st.button("🚀 Run Optimization", type="primary"):
        with st.spinner("Running optimization... This may take a moment."):
            try:
                optimal_x, optimal_y, optimal_value, x_count, y_count = analyzer.find_optimal_parameters(
                    x_range=(x_min, x_max),
                    y_range=(y_min, y_max),
                    step=step,
                    visualize=False
                )
                
                # Display results
                st.success("✅ Optimization completed!")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Optimal X", f"{optimal_x:,}")
                    st.metric("X Count", x_count)
                
                with col2:
                    st.metric("Optimal Y", f"{optimal_y:,}")
                    st.metric("Y Count", y_count)
                
                with col3:
                    st.metric("Optimal Value", f"{optimal_value:.4f}")
                
                # Store results in session state for visualization
                st.session_state.optimization_results = {
                    'optimal_x': optimal_x,
                    'optimal_y': optimal_y,
                    'optimal_value': optimal_value,
                    'x_count': x_count,
                    'y_count': y_count
                }
                
            except Exception as e:
                st.error(f"❌ Optimization failed: {str(e)}")

with tab4:
    st.header("Visualizations")
    
    if st.button("Generate Parameter Heatmap"):
        with st.spinner("Generating visualizations..."):
            # Create a smaller grid for faster computation
            x_range = np.arange(x_min, x_max + step, step * 2)  # Use larger step for faster computation
            y_range = np.arange(y_min, y_max + step, step * 2)
            
            # Calculate values for heatmap
            heatmap_data = []
            for x in x_range:
                for y in y_range:
                    value = analyzer.find_value(x, y)
                    heatmap_data.append([x, y, value])
            
            # Convert to DataFrame
            df_heatmap = pd.DataFrame(heatmap_data, columns=['X', 'Y', 'Value'])
            
            # Create pivot table for heatmap
            pivot_table = df_heatmap.pivot(index='Y', columns='X', values='Value')
            
            # Create heatmap
            fig = px.imshow(
                pivot_table.values,
                x=pivot_table.columns,
                y=pivot_table.index,
                color_continuous_scale='viridis',
                title="Expected Value Heatmap"
            )
            fig.update_layout(
                xaxis_title="X Parameter",
                yaxis_title="Y Parameter"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # 3D Surface Plot
    if st.button("Generate 3D Surface Plot"):
        with st.spinner("Generating 3D visualization..."):
            # Create data for 3D plot
            x_range = np.arange(x_min, x_max + step, step * 3)
            y_range = np.arange(y_min, y_max + step, step * 3)
            
            X, Y = np.meshgrid(x_range, y_range)
            Z = np.zeros_like(X)
            
            for i, x in enumerate(x_range):
                for j, y in enumerate(y_range):
                    Z[j, i] = analyzer.find_value(x, y)
            
            fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='viridis')])
            fig.update_layout(
                title="3D Surface Plot of Expected Values",
                scene=dict(
                    xaxis_title="X Parameter",
                    yaxis_title="Y Parameter",
                    zaxis_title="Expected Value"
                )
            )
            st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Investment Analyzer Dashboard | Built with Streamlit</p>
    </div>
    """, 
    unsafe_allow_html=True
)