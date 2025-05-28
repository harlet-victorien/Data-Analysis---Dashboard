import streamlit as st
from config import configure_page
from sidebar import create_sidebar
from tabs import create_tabs
from tim import InvestmentAnalyzer

def main():
    """Main application entry point"""
    # Configure page
    configure_page()
    
    # Create sidebar and get configuration
    config = create_sidebar()
    
    # Create analyzer instance
    try:
        analyzer = InvestmentAnalyzer(
            config['file_path'], 
            stop_loss=config['stop_loss'], 
            with_scam=config['with_scam']
        )
        st.success(f"✅ Data loaded successfully! Found {len(analyzer.data)} data points.")
        
        # Create tabs with analyzer and config
        create_tabs(analyzer, config)
        
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        st.stop()

if __name__ == "__main__":
    main()