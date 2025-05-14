from mcp.server.fastmcp import FastMCP, Context
from typing import Dict, List, Optional
from datetime import datetime

# Create an MCP server
mcp = FastMCP("Fruit & Vegetable Market")

# Simulated database of fruit and vegetable prices
PRICE_DATABASE = {
    "fruits": {
        "apple": {"price": 1.20, "unit": "kg", "organic": False},
        "banana": {"price": 0.90, "unit": "kg", "organic": False},
        "orange": {"price": 1.50, "unit": "kg", "organic": False},
        "strawberry": {"price": 3.50, "unit": "punnet", "organic": False},
        "blueberry": {"price": 4.20, "unit": "punnet", "organic": False},
        "organic_apple": {"price": 2.20, "unit": "kg", "organic": True},
        "organic_banana": {"price": 1.80, "unit": "kg", "organic": True},
    },
    "vegetables": {
        "carrot": {"price": 0.80, "unit": "kg", "organic": False},
        "potato": {"price": 1.00, "unit": "kg", "organic": False},
        "onion": {"price": 0.90, "unit": "kg", "organic": False},
        "broccoli": {"price": 2.50, "unit": "head", "organic": False},
        "spinach": {"price": 2.20, "unit": "bunch", "organic": False},
        "organic_carrot": {"price": 1.60, "unit": "kg", "organic": True},
        "organic_potato": {"price": 1.80, "unit": "kg", "organic": True},
    }
}

# Resource to get all available fruits
@mcp.resource("market://fruits")
def get_fruits() -> Dict:
    """Get a list of all available fruits with their prices"""
    return {"fruits": PRICE_DATABASE["fruits"]}

# Resource to get all available vegetables
@mcp.resource("market://vegetables")
def get_vegetables() -> Dict:
    """Get a list of all available vegetables with their prices"""
    return {"vegetables": PRICE_DATABASE["vegetables"]}

# Resource to get specific fruit price
@mcp.resource("market://fruits/{fruit_name}")
def get_fruit_price(fruit_name: str) -> Dict:
    """Get the price of a specific fruit"""
    fruits = PRICE_DATABASE["fruits"]
    if fruit_name in fruits:
        return {
            "name": fruit_name,
            "price": fruits[fruit_name]["price"],
            "unit": fruits[fruit_name]["unit"],
            "organic": fruits[fruit_name]["organic"]
        }
    return {"error": f"Fruit '{fruit_name}' not found"}

# Resource to get specific vegetable price
@mcp.resource("market://vegetables/{vegetable_name}")
def get_vegetable_price(vegetable_name: str) -> Dict:
    """Get the price of a specific vegetable"""
    vegetables = PRICE_DATABASE["vegetables"]
    if vegetable_name in vegetables:
        return {
            "name": vegetable_name,
            "price": vegetables[vegetable_name]["price"],
            "unit": vegetables[vegetable_name]["unit"],
            "organic": vegetables[vegetable_name]["organic"]
        }
    return {"error": f"Vegetable '{vegetable_name}' not found"}

# Tool to calculate the total cost of a shopping list
@mcp.tool()
def calculate_shopping_cost(items: List[Dict[str, str]]) -> Dict:
    """Calculate the total cost of a shopping list
    
    Args:
        items: List of dictionaries with keys 'type' (fruit/vegetable), 'name', and 'quantity'
              Example: [{"type": "fruit", "name": "apple", "quantity": 2}]
    
    Returns:
        Dictionary with total cost and itemized breakdown
    """
    total_cost = 0.0
    breakdown = []
    errors = []
    
    for item in items:
        item_type = item.get("type", "").lower()
        item_name = item.get("name", "").lower()
        quantity = float(item.get("quantity", 0))
        
        if item_type not in ["fruit", "vegetable"]:
            errors.append(f"Unknown item type: {item_type}")
            continue
            
        database = PRICE_DATABASE["fruits" if item_type == "fruit" else "vegetables"]
        
        if item_name not in database:
            errors.append(f"{item_type.capitalize()} '{item_name}' not found")
            continue
            
        item_price = database[item_name]["price"]
        item_unit = database[item_name]["unit"]
        item_cost = item_price * quantity
        total_cost += item_cost
        
        breakdown.append({
            "type": item_type,
            "name": item_name,
            "quantity": quantity,
            "unit": item_unit,
            "price_per_unit": item_price,
            "cost": item_cost
        })
    
    return {
        "total_cost": round(total_cost, 2),
        "items": breakdown,
        "errors": errors,
        "timestamp": datetime.now().isoformat()
    }

# Tool to search for fruits or vegetables by price range
@mcp.tool()
def search_by_price_range(min_price: float, max_price: float, category: Optional[str] = None) -> Dict:
    """Search for fruits or vegetables within a specific price range
    
    Args:
        min_price: Minimum price
        max_price: Maximum price
        category: Optional category filter ('fruit', 'vegetable', or None for both)
    
    Returns:
        Dictionary with matching items
    """
    results = {"fruits": [], "vegetables": []}
    
    if category is None or category.lower() == "fruit":
        for name, details in PRICE_DATABASE["fruits"].items():
            if min_price <= details["price"] <= max_price:
                results["fruits"].append({
                    "name": name,
                    "price": details["price"],
                    "unit": details["unit"],
                    "organic": details["organic"]
                })
    
    if category is None or category.lower() == "vegetable":
        for name, details in PRICE_DATABASE["vegetables"].items():
            if min_price <= details["price"] <= max_price:
                results["vegetables"].append({
                    "name": name,
                    "price": details["price"],
                    "unit": details["unit"],
                    "organic": details["organic"]
                })
    
    return results

# Tool to find organic products
@mcp.tool()
def find_organic_products() -> Dict:
    """Find all organic fruits and vegetables"""
    organic = {"fruits": [], "vegetables": []}
    
    for name, details in PRICE_DATABASE["fruits"].items():
        if details["organic"]:
            organic["fruits"].append({
                "name": name,
                "price": details["price"],
                "unit": details["unit"]
            })
    
    for name, details in PRICE_DATABASE["vegetables"].items():
        if details["organic"]:
            organic["vegetables"].append({
                "name": name,
                "price": details["price"],
                "unit": details["unit"]
            })
    
    return organic

# Tool to compare prices between regular and organic products
@mcp.tool()
def compare_regular_vs_organic() -> Dict:
    """Compare prices between regular and organic products"""
    comparisons = []
    
    # Extract base names from organic products
    for category in ["fruits", "vegetables"]:
        for name, details in PRICE_DATABASE[category].items():
            if details["organic"]:
                base_name = name.replace("organic_", "")
                if base_name in PRICE_DATABASE[category]:
                    regular_price = PRICE_DATABASE[category][base_name]["price"]
                    organic_price = details["price"]
                    price_difference = organic_price - regular_price
                    percentage_difference = (price_difference / regular_price) * 100
                    
                    comparisons.append({
                        "product": base_name,
                        "category": category[:-1],  # Remove 's' to get singular form
                        "regular_price": regular_price,
                        "organic_price": organic_price,
                        "price_difference": round(price_difference, 2),
                        "percentage_difference": round(percentage_difference, 2),
                        "unit": details["unit"]
                    })
    
    return {"comparisons": comparisons}

# Run the server when the script is executed directly
if __name__ == "__main__":
    mcp.run()
