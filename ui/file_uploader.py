"""
CSV file upload interface.

Handles multiple file uploads and shows basic validation.
"""

import streamlit as st
import pandas as pd
from typing import Dict, List


def render_upload_section() -> Dict[str, pd.DataFrame]:
    """
    Show file uploader and load CSV files.
    
    Returns:
        Dictionary of {filename: dataframe}
    """
    
    st.subheader("📁 Upload Your Data")
    
    # File uploader widget
    uploaded_files = st.file_uploader(
        "Choose CSV files",
        type=['csv'],
        accept_multiple_files=True,
        help="Upload one or more CSV files to analyze"
    )
    
    loaded_data = {}
    
    if uploaded_files:
        for file in uploaded_files:
            try:
                # Try reading the CSV
                # Try common encodings in case of issues
                encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
                df = None
                
                for encoding in encodings:
                    try:
                        file.seek(0)  # reset file pointer
                        df = pd.read_csv(file, encoding=encoding)
                        break  # success!
                    except UnicodeDecodeError:
                        continue  # try next encoding
                
                if df is None:
                    st.error(f"Could not read {file.name} - encoding issue")
                    continue
                
                loaded_data[file.name] = df
                
            except Exception as e:
                st.error(f"Failed to load {file.name}: {str(e)}")
        
        # Show single summary message
        if loaded_data:
            st.success(f"✓ {len(loaded_data)} table(s) loaded successfully")
    
    else:
        st.info("👆 Upload CSV files to get started")
    
    return loaded_data


def show_data_summary(dataframes: Dict[str, pd.DataFrame]):
    """
    Display summary statistics for uploaded data.
    
    Shows things like row counts, column types, missing values.
    """
    
    if not dataframes:
        return
    
    # Header with help section
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("📊 Data Summary")
    
    with col2:
        # Show help once for all tables
        with st.expander("📝 NULL Help"):
            st.write("""
            **Auto-handled by LLM:**
            - Aggregations skip NULLs
            - JOINs work with NULLs
            - Queries use IS NULL logic
            
            **Guidelines:**
            - >30% missing → Consider dropping
            - <10% missing → Safe to use
            """)
    
    # Show each table's summary
    for filename, df in dataframes.items():
        with st.expander(f"{filename} - Details"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Rows", f"{len(df):,}")
            
            with col2:
                st.metric("Columns", len(df.columns))
            
            with col3:
                missing = df.isnull().sum().sum()
                missing_pct = (missing / (len(df) * len(df.columns))) * 100
                st.metric("Missing Values", f"{missing:,}", f"{missing_pct:.1f}%")
            
            # Show column info with missing values
            st.write("**Column Details:**")
            col_info = pd.DataFrame({
                'Column': df.columns,
                'Type': df.dtypes.astype(str),
                'Non-Null': df.count().values,
                'Missing': df.isnull().sum().values,
                'Missing %': (df.isnull().sum() / len(df) * 100).round(1).astype(str) + '%'
            })
            st.dataframe(col_info, width='stretch', hide_index=True)
            
            # Show missing value recommendations if there are any
            if missing > 0:
                st.divider()
                st.write("**💡 Recommendations:**")
                
                # Analyze missing patterns
                high_missing_cols = df.isnull().sum()[df.isnull().sum() > len(df) * 0.3].index.tolist()
                medium_missing_cols = df.isnull().sum()[(df.isnull().sum() > 0) & (df.isnull().sum() <= len(df) * 0.3)].index.tolist()
                
                if high_missing_cols:
                    st.warning(f"⚠️ **High missing** (>30%): `{', '.join(high_missing_cols)}`")
                    st.caption("Consider dropping these columns")
                
                if medium_missing_cols:
                    st.info(f"ℹ️ **Some missing**: `{', '.join(medium_missing_cols)}`")
                    st.caption("LLM will handle these automatically")


