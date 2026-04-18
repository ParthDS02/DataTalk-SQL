"""
DataTalk SQL - Natural Language to SQL Explorer

Main application entry point.
Run with: streamlit run app.py
"""

import streamlit as st
from core.database import DatabaseManager
from core.sql_generator import SQLGenerator
from core.query_executor import QueryExecutor
from core.schema_builder import SchemaBuilder
from ui.file_uploader import render_upload_section, show_data_summary
from ui.table_viewer import render_table_viewer
from ui.relationship_manager import render_relationship_manager
from ui.query_interface import render_query_interface


# Page config - must be first Streamlit command
st.set_page_config(
    page_title="DataTalk SQL",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)


def initialize_session_state():
    """
    Set up session state variables.
    
    Session state persists across reruns - perfect for storing
    database connection and loaded data.
    """
    
    if 'db_manager' not in st.session_state:
        st.session_state.db_manager = DatabaseManager()
    
    if 'schema_builder' not in st.session_state:
        st.session_state.schema_builder = SchemaBuilder(st.session_state.db_manager)
    
    if 'sql_generator' not in st.session_state:
        try:
            st.session_state.sql_generator = SQLGenerator()
        except Exception as e:
            st.error(f"Failed to initialize LLM: {str(e)}")
            st.info("Please check your .env configuration")
            st.stop()
    
    if 'query_executor' not in st.session_state:
        st.session_state.query_executor = QueryExecutor(st.session_state.db_manager)
    
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False


def main():
    """Main application flow."""
    
    # Initialize everything
    initialize_session_state()
    
    # Header
    st.title("💬 DataTalk SQL")
    st.caption("Talk to Your Data — Upload, Link, Ask & Analyze")
    
    # Sidebar - configuration and info
    with st.sidebar:
        # Creator attribution
        st.markdown("---")
        st.markdown("**Created by Parth B Mistry**")
        st.markdown("---")
        
        st.header("⚙️ Configuration")
        
        # Model selection - simplified to one model per provider
        provider_choice = st.selectbox(
            "LLM Provider:",
            ["groq", "ollama"],
            index=0 if st.session_state.sql_generator.provider == "groq" else 1,
            help="Choose between cloud (Groq) or local (Ollama)"
        )
        
        # Fixed models - no selection needed
        if provider_choice == "groq":
            selected_model = "llama-3.3-70b-versatile"
            st.info(f"🤖 Using: **GROQ** (Cloud)\n\nModel: Llama 3.3 70B\n\n✅ Best for SQL generation")
            
        else:  # ollama
            selected_model = "llama3"
            st.info(f"🤖 Using: **OLLAMA** (Local)\n\nModel: Llama 3\n\n✅ 100% free, runs offline")
            
            # Check Ollama connection (only show if not running)
            try:
                import requests
                response = requests.get("http://localhost:11434/api/tags", timeout=2)
                if response.status_code != 200:
                    st.warning("⚠️ Ollama connection issue")
            except:
                st.error("❌ Ollama not running!")
                st.caption("Start Ollama:\n1. Install from https://ollama.ai\n2. Run: `ollama pull llama3`")
        
        # Update generator if changed
        if provider_choice != st.session_state.sql_generator.provider:
            with st.spinner("🔄 Switching provider..."):
                try:
                    # Reinitialize with new settings
                    import os
                    os.environ['LLM_PROVIDER'] = provider_choice
                    os.environ['GROQ_MODEL'] = 'llama-3.3-70b-versatile'
                    os.environ['OLLAMA_MODEL'] = 'llama3'
                    
                    st.session_state.sql_generator = SQLGenerator()
                    st.success("✓ Provider switched!")
                except Exception as e:
                    st.error(f"Failed to switch: {str(e)}")
        
        # How to use section (moved below provider)
        with st.expander("❓ How to Use"):
            st.write("""
            1. **Upload** your CSV files
            2. **Preview** the data tables
            3. **Define** relationships (PK/FK)
            4. **Ask** questions in plain English
            5. **Export** your results
            """)
        
        st.divider()
        
        # Quick stats
        st.header("📊 Quick Stats")
        
        db = st.session_state.db_manager
        tables = db.get_table_names()
        relationships = db.get_relationships()
        
        st.metric("Tables Loaded", len(tables))
        st.metric("Relationships", len(relationships))
    
    # Main workflow tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📁 Upload Data",
        "📋 View Tables", 
        "🔗 Define Relationships",
        "💬 Ask Questions"
    ])
    
    with tab1:
        # Upload section
        uploaded_data = render_upload_section()
        
        # Load into database
        if uploaded_data:
            # Check if these files are already loaded
            current_tables = st.session_state.db_manager.get_table_names()
            new_files = [f for f in uploaded_data.keys() if f.replace('.csv', '').replace(' ', '_').lower() not in current_tables]
            
            if new_files:
                with st.spinner("Loading data into database..."):
                    for filename, df in uploaded_data.items():
                        st.session_state.db_manager.load_csv(filename, df)
                    
                    st.success(f"✓ Loaded {len(uploaded_data)} file(s) successfully!")
                    st.rerun()  # refresh to show in other tabs
        
        # Show data summary
        if uploaded_data:
            show_data_summary(uploaded_data)
    
    with tab2:
        # Table viewer
        tables_dict = {
            name: st.session_state.db_manager.get_table_data(name)
            for name in st.session_state.db_manager.get_table_names()
        }
        render_table_viewer(tables_dict)
    
    with tab3:
        # Relationship manager
        render_relationship_manager(
            st.session_state.schema_builder,
            st.session_state.db_manager
        )
    
    with tab4:
        # Query interface
        render_query_interface(
            st.session_state.sql_generator,
            st.session_state.query_executor,
            st.session_state.db_manager
        )
    
    # Footer
    st.divider()
    st.caption("Built with ❤️ using Streamlit, DuckDB, and LangChain")


if __name__ == "__main__":
    main()
