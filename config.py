import streamlit as st

def configure_page():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="Investment Analyzer Dashboard",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply custom CSS globally
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    
    # Title and description
    st.title("📈 MemeCoin Data Dashboard")
    

def get_custom_css():
    """Return custom CSS for styling all columns automatically"""
    return """
        <style>
        /* Auto-apply borders to all Streamlit columns */
        .stColumn > div {
            border: 1px solid #555555 !important;
            border-radius: 10px !important;
            background-color: #222222 !important;
            padding: 20px !important;
            margin: 10px !important;
            min-height: 100px !important;
        }
        
        /* Additional manual styling classes (keep for specific use cases) */
        .column-border {
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            padding: 20px;
            margin: 10px;
            background-color: #fafafa;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .column-border-left {
            border: 2px solid #4CAF50;
            border-radius: 10px;
            padding: 20px;
            margin: 10px;
            background-color: #f8fff9;
            box-shadow: 0 2px 4px rgba(76,175,80,0.2);
        }
        .column-border-right {
            border: 2px solid #2196F3;
            border-radius: 10px;
            padding: 20px;
            margin: 10px;
            background-color: #f8fbff;
            box-shadow: 0 2px 4px rgba(33,150,243,0.2);
        }
        

        
        /* Make sure content inside columns doesn't inherit the border */
        .stColumn > div > div {
            border: none !important;
            background: transparent !important;
            box-shadow: none !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        </style>
    """
