import streamlit as st
import streamlit_shadcn_ui as ui
import plotly.express as px
import plotly.graph_objects as go
from globals import COLORS

def create_parameter_analysis_tab(analyzer):
    """Create parameter analysis tab content"""
    st.header("Parameter Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        create_custom_parameter_testing_section(analyzer)
    
    with col2:
        create_expected_value_calculator_section(analyzer)

def create_custom_parameter_testing_section(analyzer):
    """Create custom parameter testing section"""
    st.subheader("Custom Parameter Testing")
    
    test_x = st.slider("Start Value", 10000, 1000000, 200000, 20000)
    test_y = st.slider("End Value", 10000, 1000000, 600000, 20000)
    
    # Custom styled button
    st.markdown('<div class="success-button">', unsafe_allow_html=True)
    if st.button("Calculate Expected Value", key="calc_button"):
        rate, _, _ = analyzer.find_rate(test_x, test_y)
        value, x_count, y_count = analyzer.find_value(test_x, test_y)
        
        # Create completion pie chart
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("Expected Value")
            st.markdown(f"{round(value, 4)}")

        with col2:
            st.subheader("Rate of transition")
            st.markdown(f"### {round(rate, 4)}")

        with col3:
            st.markdown("**Rate of transition**")
            create_completion_pie_chart(y_count, x_count, test_x, test_y)
        
    st.markdown('</div>', unsafe_allow_html=True)

def create_completion_pie_chart(y_count, x_count, x_value, y_value):
    """Create a pie chart showing completion ratio of y/x"""
    if x_count == 0:
        st.error("Cannot create pie chart: X value cannot be zero")
        return
    
    # Calculate completion ratio
    completion_ratio = min(y_count / x_count, 1.0)  # Cap at 100%
    remaining_ratio = 1.0 - completion_ratio
    
    # Prepare data for pie chart
    labels = [f"{y_value} attained", f"{y_value} not attained"]
    values = [completion_ratio, remaining_ratio]
    colors = [COLORS['primaryColor'], COLORS['secondaryBackgroundColor']]
    
    # Create pie chart
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,  # Creates a donut chart
        marker_colors=colors,
        textinfo='none',
        textfont_size=12,
        hovertemplate='<b>%{label}</b><br>Value: %{value:.2%}<br>Count: %{customdata}<extra></extra>',
        customdata=[f'{y_count:,}', f'{x_count - y_count:,}' if y_count < x_count else '0'],
    )])
    
    # Update layout
    fig.update_layout(
        showlegend=False,
        height=150,
        margin=dict(l=20, r=20, t=20, b=20),  # Reduce margins
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
        annotations=[
            dict(
                text=f'{completion_ratio:.1%}',
                x=0.5, y=0.5,
                font_size=12,
                showarrow=False
            )
        ]
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_expected_value_calculator_section(analyzer):
    """Create expected value calculator section"""
    st.subheader("Expected Value Calculator")
    
    calc_stop_loss = st.slider("Stop Loss for Calculation", 0.0, 1.0, 0.3, 0.1)
    calc_multiplier = st.slider("Multiplier", 0.1, 5.0, 1.0, 0.1)
    calc_rate = st.slider("Rate", 0.0, 1.0, 0.5, 0.01)
    
    expected_val = analyzer.expected_value(calc_stop_loss, calc_multiplier, calc_rate)
    st.metric("Expected Value", f"{expected_val:.4f}")