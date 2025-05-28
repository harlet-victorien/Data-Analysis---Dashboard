import streamlit as st
from tabs_pages.data_overview import create_data_overview_tab
from tabs_pages.parameter_analysis import create_parameter_analysis_tab
from tabs_pages.optimization import create_optimization_tab
from tabs_pages.visualizations import create_visualizations_tab
from config import get_custom_css

def create_tabs(analyzer, config):
    """Create main tabs for the application"""
    
    # Apply custom CSS
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Data Overview", 
        "🎯 Parameter Analysis", 
        "🔍 Optimization", 
        "📈 Visualizations"
    ])
    
    with tab1:
        create_data_overview_tab(analyzer)
    
    with tab2:
        create_parameter_analysis_tab(analyzer)
    
    with tab3:
        create_optimization_tab(analyzer, config)
    
    with tab4:
        create_visualizations_tab(analyzer, config)

    
    # Footer
    create_footer()

def create_footer():
    """Create application footer"""
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
            <p>Investment Analyzer Dashboard | Built with Streamlit</p>
        </div>
        """, 
        unsafe_allow_html=True
    )