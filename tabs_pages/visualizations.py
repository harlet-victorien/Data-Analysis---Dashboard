import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def create_visualizations_tab(analyzer, config):
    """Create visualizations tab content"""
    st.header("Visualizations")
    
    # Heatmap section
    create_heatmap_section(analyzer, config)
    
    # 3D Surface plot section
    create_3d_surface_section(analyzer, config)

def create_heatmap_section(analyzer, config):
    """Create parameter heatmap section"""
    st.markdown('<div class="visualization-button">', unsafe_allow_html=True)
    if st.button("Generate Parameter Heatmap", key="heatmap_button"):
        generate_parameter_heatmap(analyzer, config)
    st.markdown('</div>', unsafe_allow_html=True)

def create_3d_surface_section(analyzer, config):
    """Create 3D surface plot section"""
    st.markdown('<div class="visualization-button">', unsafe_allow_html=True)
    if st.button("Generate 3D Surface Plot", key="3d_button"):
        generate_3d_surface_plot(analyzer, config)
    st.markdown('</div>', unsafe_allow_html=True)

def generate_parameter_heatmap(analyzer, config):
    """Generate parameter heatmap visualization"""
    with st.spinner("Generating heatmap..."):
        # Create a smaller grid for faster computation
        x_range = np.arange(config['x_min'], config['x_max'] + config['step'], config['step'] * 2)
        y_range = np.arange(config['y_min'], config['y_max'] + config['step'], config['step'] * 2)
        
        # Calculate values for heatmap
        heatmap_data = []
        for x in x_range:
            for y in y_range:
                value = analyzer.find_value(x, y)
                heatmap_data.append([x, y, value])
        
        # Convert to DataFrame and create pivot table
        df_heatmap = pd.DataFrame(heatmap_data, columns=['X', 'Y', 'Value'])
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

def generate_3d_surface_plot(analyzer, config):
    """Generate 3D surface plot visualization"""
    with st.spinner("Generating 3D visualization..."):
        # Create data for 3D plot
        x_range = np.arange(config['x_min'], config['x_max'] + config['step'], config['step'] * 3)
        y_range = np.arange(config['y_min'], config['y_max'] + config['step'], config['step'] * 3)
        
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