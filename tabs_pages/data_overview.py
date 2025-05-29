import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from globals import COLORS

def create_data_overview_tab(analyzer):
    """Create data overview tab content"""
    st.header("Data Overview")

    # Display basic statistics
    display_basic_statistics(analyzer)
    
    # Data distribution
    display_data_distribution(analyzer)
    
    # Show raw data sample
    display_data_sample(analyzer)

def display_basic_statistics(analyzer):
    """Display basic statistics about the data"""
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

def display_data_distribution(analyzer):
    """Display data distribution histogram"""
    st.subheader("Value Distribution")
    
    values = [item[0] for item in analyzer.data if item[0] < 2e6]
    fig = px.histogram(x=values, nbins=50, title="Distribution of Investment Values")
    fig.update_layout(
        xaxis_title="Value", 
        yaxis_title="Frequency",
        paper_bgcolor=COLORS['transparent'],  # Transparent background
        plot_bgcolor=COLORS['transparent'],
        font_color=COLORS['textColor']
    )
    st.plotly_chart(fig, use_container_width=True)

def display_data_sample(analyzer):
    """Display sample of raw data"""
    st.subheader("Data Sample")
    
    df = pd.DataFrame(analyzer.data, columns=['Value', 'Is_Scam'])
    st.dataframe(df.head(100), use_container_width=True)