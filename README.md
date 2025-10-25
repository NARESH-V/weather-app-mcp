# Weather MCP Application

A complete implementation of the **Model Context Protocol (MCP)** with Python 3, featuring separate server and client modules for weather data interaction.

## 🌟 What is MCP?

The Model Context Protocol (MCP) is an open standard developed by Anthropic for connecting AI applications with external data sources and tools. Think of MCP like USB-C for AI - it provides a standardized way to:

- **Expose Resources**: Data that can be read by AI models
- **Provide Tools**: Functions that AI models can execute
- **Define Prompts**: Reusable templates for AI interactions

## 📁 Project Structure

```
weather-app-mcp/
├── server/                  # MCP Server Module
│   ├── __init__.py
│   └── mcp_server.py       # Weather server implementation
├── client/                  # MCP Client Module
│   ├── __init__.py
│   └── mcp_client.py       # Weather client implementation
├── examples/                # Example scripts
│   ├── run_server.py       # Run server standalone
│   ├── run_client.py       # Run client demo
│   └── custom_client.py    # Custom client examples
├── tests/                   # Test suite
│   ├── test_server.py
│   ├── test_client.py
│   └── test_integration.py
├── requirements.txt         # Python dependencies
├── .gitignore
└── README.md               # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**:
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

### Running the Server

The MCP server exposes weather data through resources, tools, and prompts.

```bash
# Run the server directly
python server/mcp_server.py

# Or use the example script
python examples/run_server.py
```

The server provides:
- **4 Resources**: Weather data for New York, London, Tokyo, and Paris
- **3 Tools**: 
  - `get_current_weather` - Get weather for a specific city
  - `compare_weather` - Compare weather between two cities
  - `get_temperature_summary` - Get temperature statistics across all cities
- **2 Prompts**:
  - `weather_report` - Generate a weather report
  - `travel_weather_advice` - Get travel advice based on weather

### Running the Client

The MCP client connects to the server and demonstrates all available operations.

```bash
# Run the full demo
python client/mcp_client.py

# Or use the example script
python examples/run_client.py

# Or run custom examples
python examples/custom_client.py
```

The client demonstration shows:
1. Listing all available resources
2. Reading specific resource data
3. Listing available tools
4. Calling tools with various arguments
5. Listing available prompts
6. Using prompt templates

## 🏗️ Architecture

### Server Module (`server/`)

The server implements the MCP specification using the official MCP SDK:

- **Resources**: Exposes weather data via URIs like `weather://new_york`
- **Tools**: Provides callable functions for weather operations
- **Prompts**: Defines reusable templates for weather queries
- **Transport**: Uses stdio for communication (JSON-RPC over stdin/stdout)

Key features:
- Async/await architecture for efficient I/O
- Comprehensive logging
- Clean separation of concerns
- Easily extensible for new cities or features

### Client Module (`client/`)

The client connects to MCP servers and provides a clean API:

- **Session Management**: Handles connection lifecycle
- **Resource Operations**: List and read resources
- **Tool Invocation**: Call tools with type-safe arguments
- **Prompt Handling**: Retrieve and use prompt templates
- **Error Handling**: Graceful error management

## 🔧 Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_server.py -v

# Run with coverage
pytest tests/ --cov=server --cov=client
```

### Adding New Weather Cities

Edit `server/mcp_server.py` and add to the `weather_data` dictionary:

```python
self.weather_data["berlin"] = {
    "city": "Berlin",
    "temperature": 55,
    "conditions": "Cloudy",
    "humidity": 75,
    "wind_speed": 14
}
```

### Creating New Tools

Add a new tool in the `handle_list_tools` function:

```python
Tool(
    name="your_tool_name",
    description="What your tool does",
    inputSchema={
        "type": "object",
        "properties": {
            "param1": {"type": "string", "description": "Parameter description"}
        },
        "required": ["param1"]
    }
)
```

Then implement it in the `handle_call_tool` function.

## 📚 MCP Concepts

### Resources
Resources are data sources that clients can read. In this example:
- `weather://new_york` - Weather data for New York
- `weather://london` - Weather data for London
- etc.

### Tools
Tools are executable functions. Our server provides:
- **get_current_weather**: Fetch current weather for a city
- **compare_weather**: Compare conditions between two cities
- **get_temperature_summary**: Get aggregate temperature statistics

### Prompts
Prompts are reusable templates for AI interactions:
- **weather_report**: Template for generating weather reports
- **travel_weather_advice**: Template for travel planning

## 🌐 Real-World Applications

This example can be extended for:
- **Real Weather APIs**: Connect to OpenWeather, WeatherAPI, etc.
- **Database Integration**: Store historical weather data
- **AI Assistant Integration**: Use with Claude, GPT, or other LLMs
- **Business Intelligence**: Weather analytics for decision-making
- **IoT Integration**: Connect with weather stations

## 🔒 Security Considerations

When deploying to production:
- Use authentication for MCP connections
- Validate all inputs thoroughly
- Implement rate limiting
- Use secure transport (HTTPS/TLS)
- Don't expose sensitive data through resources
- Implement proper error handling without leaking information

## 📖 Additional Resources

- [MCP Official Documentation](https://docs.anthropic.com/en/docs/agents-and-tools/mcp)
- [MCP GitHub Repository](https://github.com/modelcontextprotocol)
- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [Anthropic Blog Post](https://www.anthropic.com/news/model-context-protocol)

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add new weather data sources
- Implement additional tools
- Create more prompt templates
- Improve documentation
- Add tests
- Fix bugs

## 📝 License

This project is open source and available under the MIT License.

## 🙋 Support

If you have questions or run into issues:
1. Check the examples in the `examples/` directory
2. Review the test files in `tests/` for usage patterns
3. Read the inline documentation in the code
4. Refer to the official MCP documentation

## 🎯 Next Steps

To learn more about MCP:
1. Run the examples and observe the output
2. Modify the server to add your own data
3. Create custom tools for your use case
4. Experiment with different prompt templates
5. Integrate with an AI model like Claude

---

**Happy coding! 🌤️**
