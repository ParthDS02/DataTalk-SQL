"""
Auto-detect and show visualizations for query results.

Keeps it simple - just looks at the data and picks a chart that makes sense.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from typing import Optional


def try_visualize(df: pd.DataFrame):
    """
    Try to create a useful chart from the results.
    
    If the data doesn't fit any chart type, that's fine - just skip it.
    No need to force a chart on everything.
    
    Returns the plotly figure if created, None otherwise.
    """
    
    # Skip if empty or too few rows
    if df.empty or len(df) < 2:
        return None
    
    # Skip if too many rows (charts get messy)
    if len(df) > 1000:
        st.caption("💡 Dataset is large - showing table only. Try filtering for visualizations.")
        return None
    
    # Try to find a good chart
    chart = _pick_best_chart(df)
    
    if chart:
        st.write("**📊 Visualization:**")
        st.plotly_chart(chart, use_container_width=True)
        
        # Add download button for the chart
        try:
            import io
            buffer = io.BytesIO()
            chart.write_image(buffer, format='png', width=1200, height=600)
            buffer.seek(0)
            
            st.download_button(
                label="💾 Download Chart (PNG)",
                data=buffer,
                file_name="chart.png",
                mime="image/png",
                use_container_width=True
            )
        except Exception:
            # If kaleido not installed, show message
            st.caption("💡 Install 'kaleido' package to enable chart downloads")
        
        return chart
    
    return None


def _pick_best_chart(df: pd.DataFrame) -> Optional:
    """
    Look at the columns and pick the best chart type.
    
    Priority:
    1. Time series (date + number) → line chart
    2. Category + number → bar chart  
    3. Single category with few values → pie chart
    4. Two numbers → scatter plot
    """
    
    # Get column types
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    date_cols = df.select_dtypes(include=['datetime']).columns.tolist()
    text_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    # Try to detect date columns from strings (common case)
    if not date_cols:
        for col in text_cols:
            if _looks_like_date(df[col]):
                try:
                    df[col] = pd.to_datetime(df[col])
                    date_cols.append(col)
                    text_cols.remove(col)
                except:
                    pass  # not a date after all
    
    # Chart 1: Time series (best for trends)
    if date_cols and numeric_cols:
        return _make_line_chart(df, date_cols[0], numeric_cols[0])
    
    # Chart 2: Category breakdown (most common)
    if text_cols and numeric_cols:
        # check if few enough categories for bar chart
        if df[text_cols[0]].nunique() <= 20:
            return _make_bar_chart(df, text_cols[0], numeric_cols[0])
    
    # Chart 3: Pie chart for proportions
    if text_cols and numeric_cols:
        if df[text_cols[0]].nunique() <= 7:  # pie charts get messy with many slices
            return _make_pie_chart(df, text_cols[0], numeric_cols[0])
    
    # Chart 4: Scatter plot for correlations
    if len(numeric_cols) >= 2:
        return _make_scatter(df, numeric_cols[0], numeric_cols[1])
    
    # Can't find a good chart - that's ok!
    return None


def _make_line_chart(df, date_col, value_col):
    """Line chart for time series data."""
    try:
        fig = px.line(
            df, 
            x=date_col, 
            y=value_col,
            title=f"{value_col} over time"
        )
        fig.update_layout(height=400)
        return fig
    except:
        return None


def _make_bar_chart(df, category_col, value_col):
    """Bar chart for categorical comparisons."""
    try:
        # Group by category in case there are duplicates
        grouped = df.groupby(category_col)[value_col].sum().reset_index()
        
        fig = px.bar(
            grouped,
            x=category_col,
            y=value_col,
            title=f"{value_col} by {category_col}"
        )
        fig.update_layout(height=400)
        return fig
    except:
        return None


def _make_pie_chart(df, category_col, value_col):
    """Pie chart for showing proportions."""
    try:
        # Group and sum
        grouped = df.groupby(category_col)[value_col].sum().reset_index()
        
        fig = px.pie(
            grouped,
            names=category_col,
            values=value_col,
            title=f"{value_col} distribution"
        )
        fig.update_layout(height=400)
        return fig
    except:
        return None


def _make_scatter(df, x_col, y_col):
    """Scatter plot to show correlation between two numbers."""
    try:
        fig = px.scatter(
            df,
            x=x_col,
            y=y_col,
            title=f"{y_col} vs {x_col}"
        )
        fig.update_layout(height=400)
        return fig
    except:
        return None


def _looks_like_date(series: pd.Series) -> bool:
    """
    Quick check if a text column might be dates.
    
    Just looks for common date patterns in first few values.
    Not perfect but good enough.
    """
    
    # Sample first few non-null values
    sample = series.dropna().head(5)
    
    if len(sample) == 0:
        return False
    
    # Check if any look like dates
    date_patterns = ['-', '/', 'jan', 'feb', 'mar', 'apr', 'may', 'jun',
                    'jul', 'aug', 'sep', 'oct', 'nov', 'dec', '202']
    
    for val in sample:
        val_str = str(val).lower()
        if any(pattern in val_str for pattern in date_patterns):
            return True
    
    return False
