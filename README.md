# 💬 DataTalk SQL

**Talk to Your Data — Upload, Link, Ask & Analyze**

A production-ready natural language to SQL query system that lets non-technical users analyze CSV data through conversational questions, powered by AI with automatic visualizations and intelligent error correction.

---

### 🏢 Enterprise Hybrid Architecture
**Designed for Data Privacy and Scalability**

This application was officially engineered with a dual-mode deployment strategy to solve real-world SaaS requirements:
- ☁️ **Cloud Mode (Groq API):** Designed for fast, public-facing environments. This enables blazing-fast query resolution (1-2 seconds) using Llama 3.3 70B for standard data operations without local hardware constraints.
- 🔒 **On-Premise Local Mode (Ollama):** Architected deliberately for highly regulated environments (Healthcare, Finance, Government). Companies dealing with highly sensitive data (PII/PHI) are often legally prohibited from utilizing external APIs. The local architecture allows the exact same advanced RAG SQL analytics to run 100% offline on secure internal hardware.

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31-red)
![DuckDB](https://img.shields.io/badge/DuckDB-Latest-yellow)
![License](https://img.shields.io/badge/License-MIT-green)

**Live App:** [Live App (Hugging Face Spaces)](https://huggingface.co/spaces/pmistryds/DataTalkSQL)
---

## 🎯 Problem Statement

Business users often struggle to write SQL queries or understand relational data. They want to:

- ✅ Upload CSV files easily
- ✅ View data tables instantly  
- ✅ Define relationships between tables
- ✅ Ask questions in plain English
- ✅ Get instant visualizations
- ✅ Understand what SQL does

But no single open-source tool provides a conversational interface with automatic charts and error correction.

---

## 💡 Solution

**DataTalk SQL** is an intelligent NL → SQL engine that combines:

- **Streamlit** for beautiful, interactive UI
- **DuckDB** for blazing-fast analytics (10x faster than SQLite)
- **LangChain + LLM** for SQL generation with auto-repair
- **Plotly** for automatic visualizations
- **Smart relationship detection** with confidence scoring

### How It Works

```
1. Upload CSV files
   ↓
2. Auto-detects relationships (case-insensitive, smart pattern matching)
   ↓
3. Ask in plain English: "Show top customers by sales"
   ↓
4. AI generates DuckDB-optimized SQL
   ↓
5. If query fails → Auto-repairs and retries
   ↓
6. Shows results + automatic charts + SQL explanation
   ↓
7. Export as CSV or copy SQL
```

---

## 📊 Architecture & Diagrams

### System Architecture

![Architecture Diagram](docs/architecture_diagram.png)

*Complete system architecture showing all components, layers, and data flow*

### Folder Structure

![Folder Structure](docs/folder_structure.png)

*Project organization with file purposes and sizes*

### Project Flow & Logic

![Project Flow](docs/project_flow.png)

*Detailed flow diagram showing the complete user journey from upload to export, including auto-repair logic*

---

## 🚀 Features

### ✨ Core Features

- **📁 Multi-file CSV Upload** - Handle multiple files with auto-encoding detection
- **📊 Smart Data Summary** - Missing value analysis with recommendations
- **🔗 Advanced Relationship Detection** - Auto-detects FK relationships with confidence scoring
- **💬 Natural Language Queries** - Ask questions in plain English
- **🤖 Dual LLM Support** - Groq (recommended) or Ollama (local)
- **� Automatic SQL Repair** - Failed queries auto-fix themselves
- **📈 Smart Visualizations** - Auto-generates bar, line, pie, and scatter charts
- **💡 SQL Explanation** - Understand what queries do in plain English
- **📥 Export Results** - Download CSV, copy SQL
- **📜 Query History** - Revisit past questions (last 10)

### 🔒 Safety Features

- ✅ Read-only queries (SELECT only)
- ✅ SQL injection protection
- ✅ DuckDB-specific validation
- ✅ In-memory data (no persistence)
- ✅ Error recovery with LLM repair

### 🎨 Smart Features

- **Auto-Visualization** - Detects best chart type for your data
  - Time series → Line chart
  - Categories + values → Bar chart
  - Proportions → Pie chart
  - Number correlations → Scatter plot

- **SQL Explanation** - Click to understand any query
- **Auto-Repair** - Fixes common SQL errors automatically
- **Missing Data Insights** - Smart recommendations for null values

---

## 🛠️ Tech Stack

| Component | Technology | Why? |
|-----------|-----------|------|
| **Frontend** | Streamlit | Fast prototyping, interactive widgets |
| **Database** | DuckDB | 10x faster than SQLite, superior CSV handling |
| **LLM (Cloud)** | Groq API + Llama 3.3 70B | **RECOMMENDED** - Fast, accurate, free tier |
| **LLM (Local)** | Ollama + Llama 3 8B | Privacy-first, offline, but slower |
| **AI Framework** | LangChain | LLM integration, prompt management |
| **Visualizations** | Plotly | Interactive, professional charts |
| **Language** | Python 3.9+ | Data science ecosystem |

---

## 🤖 LLM Comparison: Groq vs Ollama

### ✅ **Groq (Recommended)**

**Model:** Llama 3.3 70B (70 billion parameters)

**Pros:**
- ⚡ **Lightning fast** - Responses in 1-2 seconds (custom LPU™ chips)
- 🎯 **More accurate** - 70B model understands complex SQL better
- 🔄 **Always available** - Cloud-hosted, no manual setup
- 📊 **Better for production** - Consistent, reliable performance
- 🆓 **Free tier** - 14,400 requests/day (plenty for development)

**Perfect for:** Production apps, real-time queries, professional use

---

### ⚠️ **Ollama (Local Alternative)**

**Model:** Llama 3 8B (8 billion parameters)

**Pros:**
- 🔒 **100% Private** - Data never leaves your machine
- 💰 **Completely free** - No API limits
- 📴 **Works offline** - No internet required

**Cons:**
- 🐌 **Slower** - 5-10+ seconds per query (CPU/GPU dependent)
- ⚙️ **Manual setup** - Requires installation and model download
- 💥 **Can crash** - Depends on system resources
- 📉 **Less accurate** - 8B model hallucinates more (see below)
- 🔄 **Inconsistent** - Performance varies with system load

**Best for:** Privacy-sensitive data, offline demos, learning purposes

---

### 🧠 Why Smaller LLMs Hallucinate in SQL

Even though we use Llama 3 (a great model), the **8B version struggles** with SQL generation compared to 70B. Here's why:

#### 1️⃣ **Limited Context Understanding**

**Problem:** 8B models have less "working memory"

- When you have 5+ tables with 50+ columns, smaller models get overwhelmed
- They can't keep track of all column names simultaneously
- Result: Hallucinate columns like `customer_name` when it's actually `first_name` + `last_name`

**Example:**
```sql
-- What user asked:
"Show customer names with their orders"

-- What 8B generates (WRONG):
SELECT customer_name, order_id FROM orders  -- customer_name doesn't exist!

-- What 70B generates (CORRECT):
SELECT c.first_name, c.last_name, o.order_id 
FROM orders o 
JOIN customers c ON o.customer_id = c.id
```

#### 2️⃣ **Weaker Instruction Following**

**Problem:** 8B models struggle with complex, multi-rule prompts

- Our SQL prompt has 50+ rules (DuckDB syntax, GROUP BY, dates, etc.)
- 70B models handle all rules simultaneously
- 8B models prioritize some rules and ignore others
- Result: Generates syntactically valid but logically wrong SQL

**Example:**
```sql
-- Rule: "Every non-aggregated column must be in GROUP BY"

-- What 8B generates (WRONG):
SELECT category, description, COUNT(*) 
FROM products 
GROUP BY category  -- Missing 'description' in GROUP BY!

-- What 70B generates (CORRECT):
SELECT category, ANY_VALUE(description), COUNT(*) 
FROM products 
GROUP BY category
```

---

### 💡 Our Recommendation

**Use Groq for production** - The speed and accuracy difference is **dramatic**:

| Metric | Groq (70B) | Ollama (8B) |
|--------|-----------|-------------|
| Response Time | 1-2 seconds | 5-15 seconds |
| SQL Accuracy | ~90% correct | ~60% correct |
| Complex Queries | ✅ Handles well | ❌ Often fails |
| User Experience | Professional | Frustrating |

**We keep Ollama as an option for:**
- Users with privacy requirements (healthcare, finance)
- Offline environments (demos, air-gapped systems)
- Learning and experimentation

---

## 📦 Installation

### Prerequisites

- Python 3.9 or higher
- (Optional) [Ollama](https://ollama.ai) for local LLM

### Quick Start

1. **Clone the repository**

```bash
git clone <your-repo-url>
cd DataTalk-SQL
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Configure environment (Recommended: Groq)**

```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your Groq API key
LLM_PROVIDER=groq
GROQ_API_KEY=your_api_key_here  # Get from https://console.groq.com/keys
GROQ_MODEL=llama-3.3-70b-versatile
```

**Alternative: Ollama (Local)**

```bash
# In .env file:
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3

# Then install and start Ollama:
# 1. Download from https://ollama.ai
# 2. Run: ollama pull llama3
# 3. Ollama runs automatically as background service
```

4. **Run the application**

```bash
streamlit run app.py
```

5. **Open your browser**

Navigate to `http://localhost:8501`

---

## 📖 Usage Guide

### Step 1: Upload CSV Files

- Click "Browse files" in **Upload Data** tab
- Select one or more CSV files
- System auto-detects encoding and shows summary

### Step 2: Review Data Summary

- Check **Data Summary** for missing values
- Review recommendations for data quality
- Use "NULL Help" for handling guidance

### Step 3: Define Relationships

- Go to **Define Relationships** tab
- **Auto-suggestions appear with confidence scores:**
  - 🟢 High confidence (>90% match)
  - 🟡 Medium confidence (70-90% match)
  - 🔵 Low confidence (<70% match)
- Click "Apply" to add suggested relationships
- Or manually define PK/FK relationships

### Step 4: Ask Questions

- Navigate to **Ask Questions** tab
- Type in plain English:
  - *"Show top 5 customers by total revenue"*
  - *"Compare sales between regions"*
  - *"Find customers with no orders"*
- Click **Ask**

### Step 5: Explore Results

- **See generated SQL** - Understand the query
- **Click "Explain SQL"** - Get plain English breakdown
- **View results table** - Your data
- **See automatic charts** - Visual insights (if applicable)
- **Export** - Download CSV or copy SQL

---

## 🎯 Example Queries

Try these with your data:

```
📊 "Show top 10 products by sales"

💰 "Compare revenue by category"

📈 "Show monthly trend for last 6 months"

� "Find customers who haven't ordered in 90 days"

⏰ "List all orders from last week"

� "Which products have declining sales?"
```

---

## 🗂️ Project Structure

```
DataTalk-SQL/
│
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .env.example                # Environment config template
├── .gitignore                  # Git ignore rules
│
├── core/                       # Business logic
│   ├── __init__.py
│   ├── database.py            # DuckDB manager
│   ├── sql_generator.py       # LLM → SQL + repair logic
│   ├── query_executor.py      # Safe query execution
│   └── schema_builder.py      # PK/FK + auto-detection
│
├── ui/                        # UI components
│   ├── __init__.py
│   ├── file_uploader.py       # CSV upload + data summary
│   ├── table_viewer.py        # Interactive data preview
│   ├── relationship_manager.py # PK/FK UI with confidence
│   ├── query_interface.py     # Query + results + history
│   └── visualizations.py      # Auto-chart generation
│
└── sample_data/               # Sample CSV files
    ├── customers.csv
    └── orders.csv
```

---

## 🔧 Configuration

### Groq API (Cloud - Recommended)

**Get API Key:** [console.groq.com/keys](https://console.groq.com/keys)

**Free Tier Limits:**
- 14,400 requests/day
- 30 requests/minute burst
- Perfect for development and small teams!

**Model:** `llama-3.3-70b-versatile` (70B parameters - best for SQL)

### Ollama (Local - Privacy Mode)

**Setup:**
```bash
# Install Ollama from https://ollama.ai

# Pull the model (one-time)
ollama pull llama3

# Ollama runs automatically
# No additional config needed!
```

**Requirements:** 8GB+ RAM recommended  
**Model:** `llama3` (8B parameters - good but slower and less accurate)

---

## 🧪 Testing

1. Use included sample data (`sample_data/`)
2. Upload `customers.csv` and `orders.csv`
3. System auto-detects: `orders.customer_id` → `customers.id`
4. Click "Apply" on the suggestion
5. Try: *"Show all customers with their order count"*
6. See results + automatic bar chart!

---

## 🚀 Roadmap

### ✅ Phase 1: MVP (Complete)
- ✅ CSV upload & smart preview
- ✅ DuckDB integration
- ✅ Auto relationship detection with confidence
- ✅ NL to SQL with DuckDB optimization
- ✅ Auto-repair for failed queries
- ✅ Smart visualizations
- ✅ SQL explanation feature

### 🔄 Phase 2: Enhancements (Documented)
- 📋 Data profiling dashboard
- 📋 Multi-step query refinement
- 📋 Query bookmarks
- 📋 Dark mode
- 📋 Excel export with formatting

See `future_enhancements.md` for complete roadmap

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Keep code simple and readable
4. Add natural docstrings
5. Submit a pull request

**Code Style:**
- Simple, clean, readable
- Natural comments (like a real engineer)
- Include TODO notes where appropriate
- Avoid overly formal AI-like text

---

## 📝 License

MIT License - feel free to use in your projects!

---

## 👨‍💻 Author

Built with ❤️ for making data accessible to everyone.

**Tech Stack Philosophy:**
- Keep it simple
- Make it fast
- Privacy-first
- Production-ready
- User experience matters

---

## 🆘 Troubleshooting

### "Groq API key not set"
- Check your `.env` file exists (copy from `.env.example`)
- Add your API key from [console.groq.com/keys](https://console.groq.com/keys)
- Restart Streamlit: `streamlit run app.py`

### "Ollama connection failed"
- Make sure Ollama is installed: [ollama.ai](https://ollama.ai)
- Pull model: `ollama pull llama3`
- Check service is running (it auto-starts on install)

### "SQL execution failed"
- System will *automatically try to repair* the query
- Check if relationships are defined correctly
- If auto-repair fails, try rephrasing your question
- Switch to Groq for better accuracy

### "Query is slow on Ollama"
- **Expected behavior** - Local 8B model is slower (5-10s)
- **Solution:** Switch to Groq for instant results (1-2s)
- Or upgrade to Llama 3.1 70B locally (requires powerful GPU)

### "Visualizations not showing"
- Charts only appear for suitable data (time series, categories, etc.)
- Check that results have numeric and categorical columns
- Large datasets (>1000 rows) skip visualization for performance

---

## 📞 Support

Found a bug? Have a feature request?

- Open an issue on GitHub
- Star ⭐ the repo if you find it useful!

---

## 🎥 Demo

Upload your CSVs, define relationships with confidence scores, and start asking questions in plain English. Watch as:

- ✨ SQL generates instantly
- 🔧 Errors auto-repair themselves
- 📊 Charts appear automatically
- 💡 Queries explain themselves

**Speed comparison:**
- Groq: 1-2 seconds ⚡
- Ollama: 5-15 seconds 🐌

---

**🎉 Happy Querying with DataTalk SQL!**
