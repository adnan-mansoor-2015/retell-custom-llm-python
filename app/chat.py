def chatbot(user_input):
    # Greet user
    if user_input.lower() in ["hi", "hello"]:
        return "Welcome to our restaurant! How can I help you today?"

    # Query menu database
    menu_item = query_menu(user_input)

    if menu_item:
        # If the user mentions a menu item
        if "price" in menu_item:
            return f"{menu_item['name']} is available for ${menu_item['price']}. Would you like to order it?"
    else:
        # Try extracting intent and details (basic example)
        if "order" in user_input.lower():
            return "Can you specify the dish you'd like to order?"
        elif "menu" in user_input.lower():
            return "Our menu includes Margherita Pizza, Pepperoni Pizza, and Coke. What would you like to order?"
    
    return "I'm sorry, I didn't quite catch that. Could you rephrase?"

# Example Usage
print(chatbot("Hi"))  # Greeting
print(chatbot("What's the price of Margherita Pizza?"))  # Query price
print(chatbot("I'd like to order a Margherita Pizza."))  # Order placement