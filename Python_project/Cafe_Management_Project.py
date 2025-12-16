# Advanced Python Mini Project - Café Management System
# Features: Discount, GST, Bill Number, File Saving

from datetime import datetime
import os

CAFE_NAME = "Chill & Fill Café"

# Menu: item -> price
menu = {
    "pizza": 120,
    "burger": 80,
    "salad": 60,
    "pop corn": 90,
    "coffee": 40,
    "tea": 20,
    "fries": 50
}

GST_PERCENT = 5
DISCOUNT_PERCENT = 10
DISCOUNT_THRESHOLD = 500

# Create folder for bills
if not os.path.exists("Bills"):
    os.mkdir("Bills")


def get_next_bill_number():
    """
    Reads/updates bill_counter.txt to generate the next bill number.
    """
    counter_file = "bill_counter.txt"

    # If file doesn't exist, start with bill no. 1
    if not os.path.exists(counter_file):
        with open(counter_file, "w") as f:
            f.write("1")
        return 1

    # Read last bill number
    with open(counter_file, "r") as f:
        content = f.read().strip()
        bill_no = int(content) if content.isdigit() else 1

    # Save next bill number
    with open(counter_file, "w") as f:
        f.write(str(bill_no + 1))

    return bill_no


def display_menu():
    print(f"\n------ {CAFE_NAME} MENU ------")
    for item, price in menu.items():
        print(f"{item.title():<12} : ₹{price}")
    print("-" * 30)


def get_valid_item():
    while True:
        item = input("Enter item (or 'done' to finish): ").strip().lower()
        if item == "done":
            return None
        if item in menu:
            return item
        print("❌ Item not in menu. Try again.")


def get_valid_quantity():
    while True:
        qty = input("Enter quantity: ").strip()
        if qty.isdigit() and int(qty) > 0:
            return int(qty)
        print("❌ Invalid quantity. Try again.")


def save_bill_to_file(content, customer_name, bill_no):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_name = customer_name.replace(" ", "_") if customer_name else "Customer"
    filename = f"Bills/Bill_{bill_no}_{safe_name}_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\n📄 Bill saved successfully as: {filename}")


def print_bill(order_items, customer_name):
    bill_no = get_next_bill_number()  # Get unique bill number

    bill_content = "\n========== BILL RECEIPT ==========\n"
    bill_content += f"{CAFE_NAME}\n"
    bill_content += f"Bill No: {bill_no}\n"
    bill_content += f"Customer: {customer_name}\n"
    bill_content += f"Date/Time: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n"
    bill_content += "----------------------------------\n"
    bill_content += f"{'Item':<15}{'Qty':<5}{'Price':<8}{'Total'}\n"
    bill_content += "-" * 35 + "\n"

    subtotal = 0
    for item, qty in order_items.items():
        price = menu[item]
        total = price * qty
        subtotal += total
        bill_content += f"{item.title():<15}{qty:<5}{price:<8}₹{total}\n"

    bill_content += "-" * 35 + "\n"
    bill_content += f"Subtotal:{'':<18}₹{subtotal}\n"

    # Discount logic
    discount = 0
    if subtotal >= DISCOUNT_THRESHOLD:
        discount = round(subtotal * DISCOUNT_PERCENT / 100, 2)
        bill_content += f"Discount @ {DISCOUNT_PERCENT}%:{'':<8}-₹{discount}\n"
    else:
        bill_content += "Discount:{'':<19}₹0.00\n"

    after_discount = subtotal - discount

    # GST on discounted amount
    gst = round(after_discount * GST_PERCENT / 100, 2)
    grand_total = round(after_discount + gst, 2)

    bill_content += f"GST @ {GST_PERCENT}%:{'':<14}₹{gst}\n"
    bill_content += f"Grand Total:{'':<14}₹{grand_total}\n"
    bill_content += "==================================\n"
    bill_content += "Thank you for visiting! 😊\n"

    # Show bill on screen
    print(bill_content)

    # Save bill to file
    save_bill_to_file(bill_content, customer_name, bill_no)


def main():
    print(f"Welcome to {CAFE_NAME}! ☕🍕🍔")
    customer_name = input("Enter customer name: ").strip()
    if not customer_name:
        customer_name = "Guest"

    display_menu()

    order_items = {}

    while True:
        item = get_valid_item()
        if item is None:  # user typed 'done'
            break

        qty = get_valid_quantity()
        order_items[item] = order_items.get(item, 0) + qty
        print(f"✔ Added {qty} x {item.title()}")

    if order_items:
        print_bill(order_items, customer_name)
    else:
        print("\nNo items ordered. Thank you!")


if __name__ == "__main__":
    main()


