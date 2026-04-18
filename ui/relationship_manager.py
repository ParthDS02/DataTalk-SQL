"""
Relationship manager UI - lets users define PK/FK relationships.

TODO: Add visual graph of relationships once defined.
"""

import streamlit as st
from core.schema_builder import SchemaBuilder
from typing import Dict, List


def render_relationship_manager(schema_builder: SchemaBuilder, db_manager):
    """
    UI for setting up primary keys and foreign keys.
    
    Args:
        schema_builder: SchemaBuilder instance
        db_manager: DatabaseManager instance
    """
    
    st.subheader("🔗 Define Relationships")
    
    table_names = db_manager.get_table_names()
    
    if not table_names:
        st.info("Upload some data first before defining relationships.")
        return
    
    # Show suggestions first (helps users)
    suggestions = schema_builder.suggest_relationships()
    
    if suggestions:
        st.write("**💡 Auto-Detected Relationships:**")
        st.caption("Based on column naming patterns and data analysis")
        
        for idx, suggestion in enumerate(suggestions):
            col1, col2, col3 = st.columns([4, 2, 1])
            
            with col1:
                st.write(
                    f"`{suggestion['from_table']}.{suggestion['from_column']}` "
                    f"→ `{suggestion['to_table']}.{suggestion['to_column']}`"
                )
                # Show reasoning
                st.caption(f"📊 {suggestion['reason']}")
            
            with col2:
                # Confidence badge
                conf = suggestion['confidence']
                if conf == 'high':
                    st.success(f"🟢 {conf.upper()}")
                elif conf == 'medium':
                    st.warning(f"🟡 {conf.upper()}")
                else:
                    st.info(f"🔵 {conf.upper()}")
            
            with col3:
                # Quick apply button
                if st.button("Apply", key=f"apply_suggestion_{idx}"):
                    success = schema_builder.add_foreign_key(
                        suggestion['from_table'],
                        suggestion['from_column'],
                        suggestion['to_table'],
                        suggestion['to_column']
                    )
                    if success:
                        st.success("✓ Added!")
                        st.rerun()
                    else:
                        st.error("Failed")
        
        st.divider()
    
    # Manual relationship definition
    st.write("**Manual Relationship Setup:**")
    
    tab1, tab2 = st.tabs(["Primary Keys", "Foreign Keys"])
    
    with tab1:
        # Set primary keys for each table
        st.caption("Define which column uniquely identifies each row")
        
        for table in table_names:
            df = db_manager.get_table_data(table)
            columns = list(df.columns)
            
            col1, col2 = st.columns([2, 3])
            
            with col1:
                st.write(f"**{table}**")
            
            with col2:
                current_pk = schema_builder.get_primary_key(table)
                default_idx = columns.index(current_pk) if current_pk in columns else 0
                
                pk = st.selectbox(
                    f"Primary key for {table}",
                    columns,
                    index=default_idx,
                    key=f"pk_{table}",
                    label_visibility="collapsed"
                )
                
                # Auto-save when changed
                if pk:
                    schema_builder.set_primary_key(table, pk)
    
    with tab2:
        # Define foreign keys
        st.caption("Link tables together by defining foreign keys")
        
        if len(table_names) < 2:
            st.info("Upload at least 2 tables to define relationships")
            return
        
        col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 2, 2])
        
        with col1:
            from_table = st.selectbox("From Table", table_names, key='fk_from_table')
        
        with col2:
            if from_table:
                from_df = db_manager.get_table_data(from_table)
                from_col = st.selectbox(
                    "Column", 
                    list(from_df.columns), 
                    key='fk_from_col'
                )
        
        with col3:
            st.write("→")
        
        with col4:
            ref_table = st.selectbox(
                "References Table", 
                [t for t in table_names if t != from_table],
                key='fk_ref_table'
            )
        
        with col5:
            if ref_table:
                ref_df = db_manager.get_table_data(ref_table)
                ref_col = st.selectbox(
                    "Column", 
                    list(ref_df.columns), 
                    key='fk_ref_col'
                )
        
        # Add button
        if st.button("➕ Add Relationship", use_container_width=True):
            success = schema_builder.add_foreign_key(
                from_table, from_col, ref_table, ref_col
            )
            if success:
                st.success(f"✓ Added: {from_table}.{from_col} → {ref_table}.{ref_col}")
                st.rerun()  # refresh to show in list
            else:
                st.error("Failed to add relationship")
    
    # Show current relationships
    relationships = schema_builder.get_all_relationships()
    
    if relationships:
        st.divider()
        st.write("**Current Relationships:**")
        
        for idx, rel in enumerate(relationships):
            st.write(f"{idx + 1}. `{rel['table']}.{rel['column']}` → `{rel['references']}`")
