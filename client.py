#1/Users/ronaldodasiagan/Desktop/client.venv/bin/python

import sys
import requests

url = "http://127.0.0.1:8000"

def view():
    print("List of Orders")
    try:
        response = requests.get(f"{url}/orders")
        
        if response.status_code == 200:
            orders = response.json()
            
            if not orders:
                print("No orders found yet.")
                return
                
            for idx, order in enumerate(orders):
                items_str = ", ".join([f"{item['quantity']}x {item['name']}" for item in order['items']])
                print(f"ID: {order['id']} | Name: {order['customer_name']} | Items: {items_str} | Total Price: PHP {order['total']} | Time: {order['created_at'][:19].replace('T', ' ')}")
        else:
            print(f"Fetch Error: Server returned status {response.status_code}")
            
    except requests.exceptions.RequestException:
        print("Connection error: Is your FastAPI server running?")

def search(order_id):
    print(f"Search by ID: {order_id}")
    try:
        response = requests.get(f"{url}/orders/{order_id}")
        
        if response.status_code == 200:
            order = response.json()
            
            items_str = ", ".join([f"{item['quantity']}x {item['name']}" for item in order['items']])
            print(f"Name: {order['customer_name']} | Items: {items_str} | Total Price: PHP {order['total']} | Time: {order['created_at'][:19].replace('T', ' ')}") 
        
        elif response.status_code == 404:
            print("Error: Order not found! Check your ID.")
        else:
            print(f"Fetch Error: Server returned status {response.status_code}")
            
    except requests.exceptions.RequestException:
        print("Connection error: Is your FastAPI server running?")

def order():
    print("Place a New School Supply Order")
    
    # Interactively ask the user for details
    customer = input("Customer Name: ")
    item_name = input("Item Name (e.g., Bond Paper L): ")
    
    try:
        quantity = int(input("Quantity: "))
        unit_price = float(input("Unit Price (PHP): "))
    except ValueError:
        print("Error: Quantity must be a whole number, and Price must be a number.")
        return

    # Package the data exactly how your FastAPI OrderCreate model expects it
    new_order = {
        "customer_name": customer,
        "items": [
            {
                "name": item_name,
                "quantity": quantity,
                "unit_price": unit_price
            }
        ]
    }

    try:
        print("\nSending order to the shop...")
        # Send POST request to create the order
        response = requests.post(f"{url}/orders", json=new_order)
        
        if response.status_code == 201:
            saved_order = response.json()
            print(f"Success! Order placed with ID: {saved_order['id']}")
            print(f"Total Amount Due: PHP {saved_order['total']}")
        else:
            print(f"Failed to place order. Server said: {response.text}")
            
    except requests.exceptions.RequestException:
        print("Connection error: Is your FastAPI server running?")

def main():
    # Make sure the user typed a command!
    if len(sys.argv) < 2:
        print("Usage: python client.py [view | search | order]")
        return

    cmnd = sys.argv[1]

    if cmnd == "order":
        order() # No arguments passed here!

    elif cmnd == "search":
        # Make sure they actually provided an ID
        if len(sys.argv) < 3:
            print("Please provide an ID. Example: python client.py search 12345-abcde")
            return
        
        # Pass exactly the 3rd word (the ID) to the function
        search(sys.argv[2]) 

    elif cmnd == "view":
        view()
        
    else:
        print("Unknown command. Please use 'view', 'search', or 'order'.")

if __name__ == "__main__":
    main()
