import pandas as pd
import random

# Set seed for reproducibility
random.seed(42)

# Define menu items by category
menu_data = []

# Main Dishes
main_dishes = [
    # Pasta dishes
    {"item_name": "Spaghetti Carbonara", "category": "pasta", "price": 16.99, "calories": 720},
    {"item_name": "Fettuccine Alfredo", "category": "pasta", "price": 15.99, "calories": 680},
    {"item_name": "Penne Arrabbiata", "category": "pasta", "price": 14.99, "calories": 620},
    {"item_name": "Lasagna Bolognese", "category": "pasta", "price": 18.99, "calories": 850},
    {"item_name": "Linguine with Clams", "category": "pasta", "price": 21.99, "calories": 580},
    
    # Steak dishes
    {"item_name": "Ribeye Steak", "category": "steak", "price": 34.99, "calories": 920},
    {"item_name": "Filet Mignon", "category": "steak", "price": 39.99, "calories": 780},
    {"item_name": "New York Strip", "category": "steak", "price": 32.99, "calories": 850},
    {"item_name": "Sirloin Steak", "category": "steak", "price": 28.99, "calories": 720},
    
    # Chicken dishes
    {"item_name": "Grilled Chicken Breast", "category": "chicken", "price": 17.99, "calories": 450},
    {"item_name": "Chicken Parmesan", "category": "chicken", "price": 19.99, "calories": 680},
    {"item_name": "Chicken Marsala", "category": "chicken", "price": 20.99, "calories": 620},
    {"item_name": "BBQ Chicken", "category": "chicken", "price": 18.99, "calories": 590},
    
    # Fish dishes
    {"item_name": "Grilled Salmon", "category": "fish", "price": 26.99, "calories": 520},
    {"item_name": "Pan-Seared Sea Bass", "category": "fish", "price": 29.99, "calories": 480},
    {"item_name": "Tuna Steak", "category": "fish", "price": 27.99, "calories": 460},
    {"item_name": "Fish and Chips", "category": "fish", "price": 16.99, "calories": 820},
    
    # Burgers
    {"item_name": "Classic Cheeseburger", "category": "burger", "price": 13.99, "calories": 720},
    {"item_name": "Bacon Burger", "category": "burger", "price": 15.99, "calories": 850},
    {"item_name": "Mushroom Swiss Burger", "category": "burger", "price": 14.99, "calories": 780},
    {"item_name": "Veggie Burger", "category": "burger", "price": 12.99, "calories": 520},
    
    # Pizza
    {"item_name": "Margherita Pizza", "category": "pizza", "price": 14.99, "calories": 680},
    {"item_name": "Pepperoni Pizza", "category": "pizza", "price": 16.99, "calories": 820},
    {"item_name": "BBQ Chicken Pizza", "category": "pizza", "price": 17.99, "calories": 780},
    {"item_name": "Vegetarian Pizza", "category": "pizza", "price": 15.99, "calories": 620},
    
    # Other main dishes
    {"item_name": "Lamb Chops", "category": "lamb", "price": 36.99, "calories": 880},
    {"item_name": "Pork Tenderloin", "category": "pork", "price": 24.99, "calories": 650},
    {"item_name": "Lobster Tail", "category": "seafood", "price": 44.99, "calories": 420},
    {"item_name": "Shrimp Scampi", "category": "seafood", "price": 23.99, "calories": 480},
    {"item_name": "Mushroom Risotto", "category": "risotto", "price": 18.99, "calories": 580},
]

# Beverages
beverages = [
    # Coffee
    {"item_name": "Espresso", "category": "coffee", "price": 3.99, "calories": 5},
    {"item_name": "Cappuccino", "category": "coffee", "price": 4.99, "calories": 120},
    {"item_name": "Latte", "category": "coffee", "price": 5.49, "calories": 180},
    {"item_name": "Americano", "category": "coffee", "price": 3.49, "calories": 10},
    {"item_name": "Mocha", "category": "coffee", "price": 5.99, "calories": 290},
    
    # Tea
    {"item_name": "Green Tea", "category": "tea", "price": 3.49, "calories": 0},
    {"item_name": "Black Tea", "category": "tea", "price": 3.49, "calories": 2},
    {"item_name": "Chamomile Tea", "category": "tea", "price": 3.99, "calories": 0},
    {"item_name": "Iced Tea", "category": "tea", "price": 3.99, "calories": 90},
    
    # Juice
    {"item_name": "Orange Juice", "category": "juice", "price": 4.99, "calories": 110},
    {"item_name": "Apple Juice", "category": "juice", "price": 4.99, "calories": 120},
    {"item_name": "Cranberry Juice", "category": "juice", "price": 4.99, "calories": 130},
    {"item_name": "Fresh Lemonade", "category": "juice", "price": 4.49, "calories": 150},
    
    # Soda
    {"item_name": "Coca-Cola", "category": "soda", "price": 2.99, "calories": 140},
    {"item_name": "Sprite", "category": "soda", "price": 2.99, "calories": 140},
    {"item_name": "Root Beer", "category": "soda", "price": 2.99, "calories": 150},
    {"item_name": "Ginger Ale", "category": "soda", "price": 2.99, "calories": 130},
    
    # Wine
    {"item_name": "Chardonnay", "category": "wine", "price": 9.99, "calories": 120},
    {"item_name": "Cabernet Sauvignon", "category": "wine", "price": 11.99, "calories": 125},
    {"item_name": "Pinot Grigio", "category": "wine", "price": 9.99, "calories": 120},
    {"item_name": "Merlot", "category": "wine", "price": 10.99, "calories": 125},
    
    # Beer
    {"item_name": "IPA", "category": "beer", "price": 6.99, "calories": 180},
    {"item_name": "Lager", "category": "beer", "price": 5.99, "calories": 150},
    {"item_name": "Wheat Beer", "category": "beer", "price": 6.49, "calories": 160},
    {"item_name": "Stout", "category": "beer", "price": 6.99, "calories": 210},
    
    # Cocktails
    {"item_name": "Margarita", "category": "cocktail", "price": 12.99, "calories": 280},
    {"item_name": "Mojito", "category": "cocktail", "price": 11.99, "calories": 240},
    {"item_name": "Old Fashioned", "category": "cocktail", "price": 13.99, "calories": 180},
    {"item_name": "Cosmopolitan", "category": "cocktail", "price": 12.99, "calories": 200},
    
    # Smoothies
    {"item_name": "Berry Smoothie", "category": "smoothie", "price": 7.99, "calories": 250},
    {"item_name": "Tropical Smoothie", "category": "smoothie", "price": 7.99, "calories": 280},
    {"item_name": "Green Smoothie", "category": "smoothie", "price": 8.49, "calories": 180},
    
    # Milkshakes
    {"item_name": "Chocolate Milkshake", "category": "milkshake", "price": 6.99, "calories": 520},
    {"item_name": "Vanilla Milkshake", "category": "milkshake", "price": 6.99, "calories": 480},
    {"item_name": "Strawberry Milkshake", "category": "milkshake", "price": 6.99, "calories": 500},
    
    # Water
    {"item_name": "Sparkling Water", "category": "water", "price": 2.49, "calories": 0},
    {"item_name": "Bottled Water", "category": "water", "price": 1.99, "calories": 0},
]

# Combine all items
all_items = main_dishes + beverages

# Add some random variation to simulate real data
for item in all_items:
    # Add slight price variations (±10%)
    variation = random.uniform(0.90, 1.10)
    item['price'] = round(item['price'] * variation, 2)
    
    # Add availability flag
    item['available'] = random.choice([True, True, True, True, False])  # 80% available
    
    # Add item_id
    item['item_id'] = f"MENU{random.randint(1000, 9999)}"

# Create DataFrame
df = pd.DataFrame(all_items)

# Reorder columns
df = df[['item_id', 'item_name', 'category', 'price', 'calories', 'available']]

# Save to CSV
df.to_csv('restaurant_menu.csv', index=False)

print("✅ restaurant_menu.csv created successfully!")
print(f"\n📊 Dataset Statistics:")
print(f"Total items: {len(df)}")
print(f"Main dishes: {len(main_dishes)}")
print(f"Beverages: {len(beverages)}")
print(f"\n🔍 Preview:")
print(df.head(10))
print(f"\n💰 Price range: ${df['price'].min():.2f} - ${df['price'].max():.2f}")
print(f"🔥 Calorie range: {df['calories'].min()} - {df['calories'].max()} cal")