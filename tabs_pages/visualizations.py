import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from globals import COLORS

def create_visualizations_tab(analyzer, config):
    """Create visualizations tab content"""
    st.header("Visualizations")
    
    # Check if analyzer and config are valid
    if analyzer is None or config is None:
        st.error("Analyzer or configuration not available. Please check your data input.")
        return
    
    # Heatmap section
    create_heatmap_section(analyzer, config)
    
    # 3D Surface plot section
    create_3d_surface_section(analyzer, config)

def create_heatmap_section(analyzer, config):
    """Create parameter heatmap section"""
    st.subheader("Parameter Heatmap")
    st.markdown('<div class="visualization-button">', unsafe_allow_html=True)
    if st.button("Generate Parameter Heatmap", key="heatmap_button"):
        generate_parameter_heatmap(analyzer, config)
    st.markdown('</div>', unsafe_allow_html=True)

def create_3d_surface_section(analyzer, config):
    """Create 3D surface plot section"""
    st.subheader("3D Surface Plot")
    st.markdown('<div class="visualization-button">', unsafe_allow_html=True)
    if st.button("Generate 3D Surface Plot", key="3d_button"):
        generate_3d_surface_plot(analyzer, config)
    st.markdown('</div>', unsafe_allow_html=True)

def generate_parameter_heatmap(analyzer, config):
    """Generate parameter heatmap visualization"""
    try:
        with st.spinner("Generating heatmap..."):
            # Validate config parameters
            required_keys = ['x_min', 'x_max', 'y_min', 'y_max', 'step']
            for key in required_keys:
                if key not in config:
                    st.error(f"Missing required configuration parameter: {key}")
                    return
            
            # Create a smaller grid for faster computation with bounds checking
            step_size = max(config['step'] * 2, 10000)  # Ensure minimum step size
            
            # Calculate values for heatmap
            heatmap_data = []
            total_points = 0
            
            # First, count total points for progress bar
            for x in range(int(config['x_min']), int(config['x_max']) + 1, int(step_size)):
                for y in range(x + int(step_size), int(config['y_max']) + 1, int(step_size)):
                    total_points += 1
            
            # Limit the number of points to avoid memory issues
            if total_points > 10000:
                st.warning("Large dataset detected. Reducing resolution for better performance.")
                step_size = step_size * 2
                total_points = 0
                for x in range(int(config['x_min']), int(config['x_max']) + 1, int(step_size)):
                    for y in range(x + int(step_size), int(config['y_max']) + 1, int(step_size)):
                        total_points += 1
            
            progress_bar = st.progress(0)
            error_count = 0
            max_errors = 10
            processed = 0
            
            for x in range(int(config['x_min']), int(config['x_max']) + 1, int(step_size)):
                for y in range(x + int(step_size), int(config['y_max']) + 1, int(step_size)):
                    try:
                        result = analyzer.find_value(x, y)
                        # Handle tuple returns from find_value
                        if hasattr(result, '__len__') and not isinstance(result, str):
                            value = result[0] if len(result) > 0 else np.nan
                        else:
                            value = result
                        
                        # Convert to scalar and check if valid
                        value = float(value)
                        if np.isfinite(value):
                            heatmap_data.append([x, y, value])
                    except Exception as e:
                        error_count += 1
                        if error_count <= max_errors:
                            print(f"Error calculating value at ({x}, {y}): {str(e)}")
                    
                    processed += 1
                    if processed % 10 == 0:  # Update progress every 10 points
                        progress_bar.progress(processed / total_points)
            
            progress_bar.empty()
            
            # Show error summary if there were errors
            if error_count > 0:
                if error_count > max_errors:
                    st.warning(f"Encountered {error_count} calculation errors. Check console for details.")
                else:
                    st.warning(f"Encountered {error_count} calculation errors.")
            
            if not heatmap_data:
                st.error("No valid data points generated for heatmap.")
                return
            
            # Convert to DataFrame and create pivot table
            df_heatmap = pd.DataFrame(heatmap_data, columns=['X', 'Y', 'Value'])
            
            if df_heatmap.empty:
                st.error("No data available for heatmap.")
                return
            
            pivot_table = df_heatmap.pivot(index='Y', columns='X', values='Value')
              # Create heatmap
            fig = px.imshow(
                pivot_table.values,
                x=pivot_table.columns,
                y=pivot_table.index,
                color_continuous_scale='viridis',
                title="Expected Value Heatmap",
                aspect='auto'
            )
            fig.update_layout(
                xaxis_title="X Parameter",
                yaxis_title="Y Parameter",
                height=600,
                plot_bgcolor=COLORS['transparent'],  # Transparent background
                paper_bgcolor=COLORS['transparent'],
                font_color=COLORS['textColor']
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Show statistics
            st.subheader("Heatmap Statistics")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Min Value", f"{df_heatmap['Value'].min():.4f}")
            with col2:
                st.metric("Max Value", f"{df_heatmap['Value'].max():.4f}")
            with col3:
                st.metric("Mean Value", f"{df_heatmap['Value'].mean():.4f}")
            with col4:
                st.metric("Valid Points", f"{len(df_heatmap)}/{total_points}")
                
    except Exception as e:
        st.error(f"Error generating heatmap: {str(e)}")

def generate_3d_surface_plot(analyzer, config):
    """Generate 3D surface plot visualization"""
    try:
        with st.spinner("Generating 3D visualization..."):
            # Validate config parameters
            required_keys = ['x_min', 'x_max', 'y_min', 'y_max', 'step']
            for key in required_keys:
                if key not in config:
                    st.error(f"Missing required configuration parameter: {key}")
                    return
            
            # Create data for 3D plot with larger step size for performance
            step_size = max(config['step'] * 3, 20000)  # Ensure minimum step size
            
            # Calculate total points and prepare data structure
            surface_data = []
            total_points = 0
            
            # First, count total points for progress bar
            for x in range(int(config['x_min']), int(config['x_max']) + 1, int(step_size)):
                for y in range(x + int(step_size), int(config['y_max']) + 1, int(step_size)):
                    total_points += 1
            
            # Limit the number of points for 3D plot
            if total_points > 5000:
                st.warning("Large dataset detected. Reducing resolution for 3D plot.")
                step_size = step_size * 2
                total_points = 0
                for x in range(int(config['x_min']), int(config['x_max']) + 1, int(step_size)):
                    for y in range(x + int(step_size), int(config['y_max']) + 1, int(step_size)):
                        total_points += 1
            
            progress_bar = st.progress(0)
            processed = 0
            error_count = 0
            max_errors = 10
            
            for x in range(int(config['x_min']), int(config['x_max']) + 1, int(step_size)):
                for y in range(x + int(step_size), int(config['y_max']) + 1, int(step_size)):
                    try:
                        result = analyzer.find_value(x, y)
                        # Handle tuple returns from find_value
                        if hasattr(result, '__len__') and not isinstance(result, str):
                            value = result[0] if len(result) > 0 else np.nan
                        else:
                            value = result
                        
                        # Convert to scalar and check if valid
                        value = float(value)
                        if np.isfinite(value):
                            surface_data.append([x, y, value])
                    except Exception as e:
                        error_count += 1
                        if error_count <= max_errors:
                            print(f"Error calculating value at ({x}, {y}): {str(e)}")
                    
                    processed += 1
                    if processed % 10 == 0:  # Update progress every 10 points
                        progress_bar.progress(processed / total_points)
            
            progress_bar.empty()
            
            # Show error summary if there were errors
            if error_count > 0:
                if error_count > max_errors:
                    st.warning(f"Encountered {error_count} calculation errors in 3D plot. Check console for details.")
                else:
                    st.warning(f"Encountered {error_count} calculation errors in 3D plot.")
            
            # Check if we have valid data
            if not surface_data:
                st.error("No valid data points generated for 3D plot.")
                return
            
            # Convert to DataFrame for easier handling
            df_surface = pd.DataFrame(surface_data, columns=['X', 'Y', 'Z'])
            
            # Create 3D scatter plot instead of surface for irregular grid
            fig = go.Figure(data=[go.Scatter3d(
                x=df_surface['X'],
                y=df_surface['Y'], 
                z=df_surface['Z'],
                mode='markers',
                marker=dict(
                    size=5,
                    color=df_surface['Z'],
                    colorscale='viridis',
                    showscale=True,
                    colorbar=dict(title="Expected Value")
                )            )])
            
            fig.update_layout(
                title="3D Scatter Plot of Expected Values",
                scene=dict(
                    xaxis_title="X Parameter",
                    yaxis_title="Y Parameter",
                    zaxis_title="Expected Value",
                    camera=dict(
                        eye=dict(x=1.2, y=1.2, z=0.8)
                    ),
                    bgcolor=COLORS['transparent']  # Transparent background
                ),
                height=1100,
                plot_bgcolor=COLORS['transparent'],  # Transparent background
                paper_bgcolor=COLORS['transparent'],
                font_color=COLORS['textColor']
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Show statistics
            st.subheader("3D Plot Statistics")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Min Value", f"{df_surface['Z'].min():.4f}")
            with col2:
                st.metric("Max Value", f"{df_surface['Z'].max():.4f}")
            with col3:
                st.metric("Mean Value", f"{df_surface['Z'].mean():.4f}")
            with col4:
                st.metric("Valid Points", f"{len(df_surface)}/{total_points}")
                    
    except Exception as e:
        st.error(f"Error generating 3D plot: {str(e)}")
