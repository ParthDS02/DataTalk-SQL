"""
Query interface - the main user interaction point.

User types questions, sees SQL + results, and can export data.
Now with smart features: charts and explanations!
"""

import streamlit as st
import pandas as pd
import pyperclip
from core.sql_generator import SQLGenerator
from core.query_executor import QueryExecutor
from ui.visualizations import try_visualize
from typing import Optional


def render_query_interface(
    sql_generator: SQLGenerator,
    query_executor: QueryExecutor,
    db_manager
):
    """
    Main query interface where users ask questions.
    
    Shows:
    - Question input box
    - Generated SQL query + explanation
    - Results table + auto visualization
    - Export options
    """
    
    st.subheader("💬 Ask Your Data")
    
    # Check if we have any tables loaded
    if not db_manager.get_table_names():
        st.warning("Upload and configure your data first!")
        return
    
    # Initialize query history in session state
    if 'query_history' not in st.session_state:
        st.session_state.query_history = []
    
    # Query input
    question = st.text_area(
        "What would you like to know?",
        placeholder="Example: Show me all customers who made orders above $1000",
        height=100,
        key='query_input'
    )
    
    # Example queries to help users
    with st.expander("💡 Example Questions"):
        st.write("Try asking:")
        st.code("Show top 10 customers by total order value")
        st.code("List all orders from the last 30 days")
        st.code("Find customers who haven't placed any orders")
        st.code("What's the average order amount per customer?")
    
    col1, col2 = st.columns([1, 5])
    
    with col1:
        ask_button = st.button("🔍 Ask", type="primary", use_container_width=True)
    
    with col2:
        # Show query history dropdown
        if st.session_state.query_history:
            selected_history = st.selectbox(
                "Or select from history:",
                [''] + [q['question'] for q in st.session_state.query_history],
                key='history_select'
            )
            if selected_history:
                question = selected_history
    
    # Process the query
    if ask_button and question:
        with st.spinner("🤔 Thinking..."):
            try:
                # Get schema and relationships
                schema = db_manager.get_schema_info()
                relationships = db_manager.get_relationships()
                
                # Generate SQL from natural language
                sql_query = sql_generator.generate_sql(
                    question, 
                    schema, 
                    relationships
                )
                
                st.divider()
                
                # Show the generated SQL
                st.write("**Generated SQL Query:**")
                st.code(sql_query, language='sql')
                
                # NEW: SQL Explanation in expander (doesn't cause page refresh)
                with st.expander("📊 Click to Explain this SQL"):
                    with st.spinner("Explaining..."):
                        explanation = sql_generator.explain_sql(sql_query)
                        st.info(f"**What this query does:**\n\n{explanation}")
                
                # Execute the query
                success, result_df, error_msg = query_executor.execute_safe(sql_query)
                
                # If query failed, try to auto-repair it once
                if not success and "Binder Error" in error_msg or "Catalog Error" in error_msg or "Parser Error" in error_msg:
                    st.warning("⚠️ Query failed. Attempting auto-repair...")
                    
                    with st.spinner("🔧 Fixing SQL..."):
                        try:
                            # Ask LLM to fix the query based on error
                            fixed_sql = sql_generator.repair_sql(sql_query, error_msg, schema)
                            
                            if fixed_sql != sql_query:  # only if it actually changed
                                st.info("**Auto-Corrected SQL:**")
                                st.code(fixed_sql, language='sql')
                                
                                # Try executing the fixed query
                                success, result_df, error_msg = query_executor.execute_safe(fixed_sql)
                                
                                if success:
                                    sql_query = fixed_sql  # use fixed version for display
                                    st.success("✅ Auto-repair successful!")
                        except:
                            pass  # if repair fails, continue with original error
                
                if success:
                    # Show results
                    st.write("**Results:**")
                    
                    if not result_df.empty:
                        st.dataframe(result_df, use_container_width=True)
                        
                        # NEW: Try to show a visualization
                        try_visualize(result_df)
                        
                        # Export options
                        _render_export_options(result_df, sql_query, question)
                        
                        # Save to history
                        st.session_state.query_history.append({
                            'question': question,
                            'sql': sql_query,
                            'result_count': len(result_df)
                        })
                        
                        # Keep only last 10 queries
                        if len(st.session_state.query_history) > 10:
                            st.session_state.query_history = st.session_state.query_history[-10:]
                    
                    else:
                        st.info("Query executed successfully but returned no results.")
                
                else:
                    # Show error
                    st.error(f"❌ {error_msg}")
            
            except Exception as e:
                error_msg = str(e)
                st.error("❌ Query Failed")
                
                # Show error with formatting preserved
                st.code(error_msg, language=None)
                
                # Show helpful hint
                if "Ollama" in error_msg:
                    st.info("💡 **Quick Fix:** Switch to Groq in the sidebar (cloud, free tier)")
                elif "Groq" in error_msg:
                    st.info("💡 **Quick Fix:** Switch to Ollama in the sidebar (local, 100% free)")


def _render_export_options(df: pd.DataFrame, sql: str, question: str):
    """
    Show export options for query results.
    
    Includes:
    - Download as CSV
    - Copy SQL to clipboard
    - Download chart (if visualization was shown)
    """
    
    st.divider()
    st.write("**Export Options:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # CSV download
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Data (CSV)",
            data=csv,
            file_name="query_results.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        # Copy SQL to clipboard
        if st.button("📋 Copy SQL", use_container_width=True):
            try:
                pyperclip.copy(sql)
                st.success("✓ SQL copied to clipboard!")
            except Exception:
                # Fallback if clipboard doesn't work
                st.code(sql, language='sql')
                st.caption("Copy the SQL above manually")
