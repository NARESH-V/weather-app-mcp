# Weather MCP Application

A complete implementation of the **Model Context Protocol (MCP)** with Python 3, featuring separate server and client modules for weather data interaction, including interactive CLI and LLM-powered clients.

## 🌟 What is MCP?

The Model Context Protocol (MCP) is an open standard developed by Anthropic for connecting AI applications with external data sources and tools. Think of MCP like USB-C for AI - it provides a standardized way to:

- **Expose Resources**: Data that can be read by AI models
- **Provide Tools**: Functions that AI models can execute
- **Define Prompts**: Reusable templates for AI interactions

## 📁 Project Structure

```
weather-app-mcp/
├── server/                       # MCP Server Module
│   ├── __init__.py
│   └── mcp_server.py            # Weather server implementation
├── client/                       # MCP Client Module
│   ├── __init__.py
│   ├── mcp_client.py            # Core MCP client implementation
│   ├── interactive_client.py    # Simple interactive CLI
│   └── llm_interactive_client.py # LLM-powered interactive client
├── examples/                     # Example scripts
│   ├── run_server.py            # Run server standalone
│   ├── run_client.py            # Run client demo
│   └── custom_client.py         # Custom client examples
├── tests/                        # Test suite
│   ├── test_server.py
│   ├── test_client.py
│   └── test_integration.py
├── requirements.txt              # Python dependencies
├── pyproject.toml                # Package configuration
├── .gitignore
├── INTERACTIVE_GUIDE.md          # Interactive clients usage guide
├── INTERACTIVE_CLIENTS_SUMMARY.md # Technical details
└── README.md                     # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository** (or navigate to your project directory):
```bash
cd weather-app-mcp
```

2. **Create a virtual environment** (recommended):
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## 💻 Usage

### 🎯 Interactive Clients

The project includes **two interactive clients** that accept user queries and respond in real-time:

#### 1. Simple Interactive CLI Client

A command-line interface for querying weather data with simple commands:

```bash
python client/interactive_client.py
```

**Available commands:**
- `weather <city>` - Get current weather for a city
- `compare <city1> <city2>` - Compare weather between two cities
- `summary` - Get temperature summary for all cities
- `resource <city>` - Read raw weather resource data (JSON)
- `list` - Show all available cities
- `help` - Show help message
- `quit` or `exit` - Exit the client

**Available cities**: `new_york`, `london`, `tokyo`, `paris`

**Example session:**
```
weather> weather london
Current weather in London:
Temperature: 58°F
Conditions: Rainy
Humidity: 80%
Wind Speed: 15 mph

weather> compare new_york tokyo
Weather Comparison:

New York: 72°F, Partly Cloudy
Tokyo: 68°F, Clear

Temperature difference: 4°F (New York is warmer)

weather> summary
Temperature Summary Across All Cities:

Average Temperature: 65.0°F
Hottest: New York at 72°F
Coldest: London at 58°F
Range: 14°F

weather> quit
Goodbye! 👋
```

#### 2. LLM-Powered Interactive Client

Use natural language queries with AI (OpenAI GPT or Anthropic Claude). The LLM client automatically understands your questions, selects the right tools, and provides conversational responses.

**Prerequisites:**

1. **Install LLM dependencies:**

Edit `requirements.txt` and uncomment the LLM provider you want to use:
```python
# Uncomment one of these:
openai>=1.0.0              # For OpenAI GPT integration
# anthropic>=0.18.0        # For Anthropic Claude integration
```

Then install:
```bash
pip install -r requirements.txt
```

Or install directly:
```bash
pip install openai           # For OpenAI
# or
pip install anthropic        # For Claude
```

2. **Set up API credentials:**

**For OpenAI:**
```bash
export OPENAI_API_KEY='sk-your-key-here'
export LLM_PROVIDER=openai  # Optional, this is the default
```

**For Anthropic Claude:**
```bash
export ANTHROPIC_API_KEY='sk-ant-your-key-here'
export LLM_PROVIDER=anthropic
```

3. **Run the client:**
```bash
python client/llm_interactive_client.py
```

**Example natural language queries:**
```
You: What's the weather like in London?

🤔 Thinking...
🤖 Calling tool: get_current_weather with args: {'city': 'london'}