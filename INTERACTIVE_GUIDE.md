# Interactive Client Quick Start Guide

This guide shows you how to use the interactive clients to query the weather MCP server.

## Simple Interactive Client

### Starting the Client

```bash
python interactive_client.py
```

### Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `weather <city>` | Get current weather for a city | `weather london` |
| `compare <city1> <city2>` | Compare weather between two cities | `compare new_york tokyo` |
| `summary` | Get temperature summary for all cities | `summary` |
| `resource <city>` | Read raw weather resource data (JSON) | `resource paris` |
| `list` | Show all available cities | `list` |
| `help` | Display help message | `help` |
| `quit` or `exit` | Exit the client | `quit` |

### Available Cities

- `new_york` (or New York)
- `london` (or London)
- `tokyo` (or Tokyo)
- `paris` (or Paris)

### Example Session

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

## LLM-Powered Interactive Client

### Prerequisites

1. Install the LLM library:
```bash
# For OpenAI
pip install openai

# For Anthropic Claude
pip install anthropic
```

2. Set up your API key:
```bash
# For OpenAI
export OPENAI_API_KEY='your-openai-api-key'

# For Anthropic Claude
export ANTHROPIC_API_KEY='your-anthropic-api-key'
```

3. (Optional) Set the provider:
```bash
export LLM_PROVIDER=openai  # or 'anthropic'
```

### Starting the Client

```bash
python llm_interactive_client.py
```

### How It Works

The LLM client:
1. **Understands natural language** - You can ask questions naturally
2. **Selects appropriate tools** - Automatically chooses the right MCP tool
3. **Executes operations** - Calls the MCP server
4. **Provides conversational responses** - Gives natural language answers

### Example Natural Language Queries

```
You: What's the weather like in London?
🤖 Calling tool: get_current_weather with args: {'city': 'london'}
Assistant: The current weather in London is rainy with a temperature of 58°F. 
The humidity is at 80% and there's a wind speed of 15 mph.

You: Which city is warmer, New York or Tokyo?
🤖 Calling tool: compare_weather with args: {'city1': 'new_york', 'city2': 'tokyo'}
Assistant: New York is warmer than Tokyo by 4°F. New York has a temperature 
of 72°F with partly cloudy conditions, while Tokyo is at 68°F with clear skies.

You: Can you give me a summary of all the temperatures?
🤖 Calling tool: get_temperature_summary with args: {}
Assistant: Here's the temperature summary across all cities:
- Average Temperature: 65.0°F
- Hottest city: New York at 72°F
- Coldest city: London at 58°F
- Temperature range: 14°F

You: What's the weather in Paris and London?
🤖 Calling tool: get_current_weather with args: {'city': 'paris'}
🤖 Calling tool: get_current_weather with args: {'city': 'london'}
Assistant: Here's the weather for both cities:

Paris: 62°F, Cloudy conditions, 70% humidity, 10 mph winds
London: 58°F, Rainy conditions, 80% humidity, 15 mph winds

London is a bit cooler and wetter than Paris today.

You: quit
Goodbye! 👋
```

### Tips for Best Results

1. **Be specific** - Mention city names clearly
2. **Ask one thing at a time** - For complex queries, break them down
3. **Use natural language** - No need for exact commands
4. **Context is maintained** - You can refer to previous queries

### Supported Providers

| Provider | Model | API Key Variable |
|----------|-------|------------------|
| OpenAI | gpt-4o-mini | `OPENAI_API_KEY` |
| Anthropic | claude-3-5-sonnet-20241022 | `ANTHROPIC_API_KEY` |

## Troubleshooting

### Common Issues

**Issue**: Client can't connect to server
```
Solution: Make sure the server module is accessible. The client automatically 
starts the server, but ensure server/mcp_server.py exists.
```

**Issue**: LLM client says "API key not set"
```
Solution: Export your API key:
export OPENAI_API_KEY='your-key-here'
```

**Issue**: City not found
```
Solution: Check available cities with the 'list' command. Use underscores 
for multi-word cities: 'new_york' not 'New York'
```

**Issue**: Import error for openai or anthropic
```
Solution: Install the required package:
pip install openai
# or
pip install anthropic
```

## Advanced Usage

### Programmatic Usage

You can also use the clients programmatically in your Python code:

```python
import asyncio
from client.mcp_client import WeatherMCPClient

async def get_weather_data():
    client = WeatherMCPClient()
    await client.connect_to_server("server/mcp_server.py")
    
    # Call a tool
    result = await client.call_tool("get_current_weather", {"city": "london"})
    print(result)
    
    # Read a resource
    data = await client.read_resource("weather://tokyo")
    print(data)
    
    await client.disconnect()

# Run it
asyncio.run(get_weather_data())
```

### Creating Custom Queries

Extend the `InteractiveClient` class to add your own commands:

```python
# In interactive_client.py

class CustomInteractiveClient(InteractiveClient):
    async def process_query(self, query: str) -> str:
        # Add your custom command handling
        if query.startswith("custom"):
            # Your custom logic here
            return "Custom response"
        
        # Fall back to parent implementation
        return await super().process_query(query)
```

## Next Steps

- **Explore the examples** - Check out `examples/` directory
- **Read the full README** - Learn about MCP architecture
- **Customize the server** - Add your own data sources
- **Build integrations** - Connect with LangChain, CrewAI, etc.

Happy exploring! 🌤️

