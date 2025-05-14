# Fruit & Vegetable Market MCP Server

This is an MCP (Model Context Protocol) server implementation that simulates a fruit and vegetable price query system. It allows you to query prices, calculate shopping costs, search by price range, and find organic products.

## Features

### Resources
- Get all available fruits and their prices
- Get all available vegetables and their prices
- Get price information for a specific fruit
- Get price information for a specific vegetable

### Tools
- Calculate the total cost of a shopping list
- Search for products within a specific price range
- Find all organic products
- Compare prices between regular and organic products

## Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Server

### Development Mode with MCP Inspector

The fastest way to test and debug the server is with the MCP Inspector:

```bash
mcp dev fruit_veg_server.py
```

### Claude Desktop Integration

Once your server is ready, install it in Claude Desktop:

```bash
mcp install fruit_veg_server.py --name "Fruit & Vegetable Market"
```

### Direct Execution

You can also run the server directly:

```bash
python fruit_veg_server.py
# or
mcp run fruit_veg_server.py
```

## Example Usage

Once the server is running, you can interact with it using the MCP Inspector or Claude Desktop. Here are some example queries:

### Resource Queries
- "What fruits are available?"
- "What's the price of apples?"
- "Show me all vegetable prices."

### Tool Usage
- "Calculate the cost of 2kg of apples, 1kg of carrots, and 3 punnets of strawberries."
- "Find all products that cost between $1 and $2 per unit."
- "Show me all organic products."
- "Compare the prices of regular and organic products."

## Data Structure

The server uses a simulated database with the following structure:

```python
PRICE_DATABASE = {
    "fruits": {
        "apple": {"price": 1.20, "unit": "kg", "organic": False},
        # More fruits...
    },
    "vegetables": {
        "carrot": {"price": 0.80, "unit": "kg", "organic": False},
        # More vegetables...
    }
}
```
