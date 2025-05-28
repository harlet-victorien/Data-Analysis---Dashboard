import streamlit as st

def create_optimization_tab(analyzer, config):
    """Create optimization tab content"""
    st.header("Parameter Optimization")
    st.write("Goes through all possible values of X and Y to find the optimal parameters for the best expected value.")
    
    # Custom styled optimization button
    st.markdown('<div class="optimization-button">', unsafe_allow_html=True)
    if st.button("🚀 Run Optimization", key="opt_button"):
        run_optimization(analyzer, config)
    st.markdown('</div>', unsafe_allow_html=True)

def run_optimization(analyzer, config):
    """Run the optimization process"""
    with st.spinner("Running optimization... This may take a moment."):
        try:
            optimal_x, optimal_y, optimal_value, x_count, y_count = analyzer.find_optimal_parameters(
                x_range=(config['x_min'], config['x_max']),
                y_range=(config['y_min'], config['y_max']),
                step=config['step'],
                visualize=False
            )
            
            # Display results
            st.success("✅ Optimization completed!")
            display_optimization_results(optimal_x, optimal_y, optimal_value, x_count, y_count)
            
            # Store results in session state for visualization
            store_optimization_results(optimal_x, optimal_y, optimal_value, x_count, y_count)
            
        except Exception as e:
            st.error(f"❌ Optimization failed: {str(e)}")

def display_optimization_results(optimal_x, optimal_y, optimal_value, x_count, y_count):
    """Display optimization results"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Optimal X", f"{optimal_x:,}")
        st.metric("X Count", x_count)
    
    with col2:
        st.metric("Optimal Y", f"{optimal_y:,}")
        st.metric("Y Count", y_count)
    
    with col3:
        st.metric("Optimal Value", f"{optimal_value:.4f}")

def store_optimization_results(optimal_x, optimal_y, optimal_value, x_count, y_count):
    """Store optimization results in session state"""
    st.session_state.optimization_results = {
        'optimal_x': optimal_x,
        'optimal_y': optimal_y,
        'optimal_value': optimal_value,
        'x_count': x_count,
        'y_count': y_count
    }