"""
Table viewer component - shows uploaded data in clean format.
"""

import streamlit as st
import pandas as pd
from typing import Dict


def render_table_viewer(tables: Dict[str, pd.DataFrame]):
    """
    Display all loaded tables with interactive preview.
    
    Args:
        tables: Dictionary of {table_name: dataframe}
    """
    
    if not tables:
        st.info("No tables loaded yet. Upload CSV files to see data here.")
        return
    
    st.subheader("📋 Loaded Tables")
    
    # Let user select which table to view
    table_names = list(tables.keys())
    
    selected_table = st.selectbox(
        "Select table to view:",
        table_names,
        key='table_viewer_select'
    )
    
    if selected_table:
        df = tables[selected_table]
        
        # Show table info
        st.write(f"**{selected_table}** - {len(df)} rows × {len(df.columns)} columns")
        
        # Interactive dataframe display
        st.dataframe(
            df,
            width='stretch',  # Updated from use_container_width
            height=400  # fixed height with scrolling
        )
        
        # Quick stats
        with st.expander("📈 Quick Statistics"):
            st.write(df.describe())
