"""
Inventory Management System
A comprehensive system for managing product inventory, suppliers, and orders.

The system uses file-based storage with the following file structure:
- products.txt: Stores product information
- suppliers.txt: Stores supplier information
- orders.txt: Stores customer order history
- supplier_orders.txt: Stores supplier order history

Each entity is stored in a pipe-delimited format with a header row.
"""
import os
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass

class Product:
    """
    Represents a product in the inventory system.
    
    Attributes:
        product_id (str): Unique identifier for the product
        name (str): Name of the product
        description (str): Product description
        price (float): Product price
        stock (int): Current quantity in stock
        supplier_id (Optional[str]): ID of the supplier, if any
    """
    product_id: str
    name: str
    description: str
    price: float
    stock: int = 0
    supplier_id: Optional[str] = None

    def to_string(self) -> str:
        """Converts product data to pipe-delimited string format for file storage."""
        return f"{self.product_id}|{self.name}|{self.description}|{self.price}|{self.stock}|{self.supplier_id or ''}"

    @classmethod
    def from_string(cls, line: str) -> Optional['Product']:
        """Creates a Product instance from a pipe-delimited string.
        Returns None if the input string is invalid or incomplete.
        """
        try:
            data = line.strip().split("|")
            if len(data) >= 5:
                price = float(data[3])
                stock = int(data[4])
                supplier_id = data[5] if len(data) > 5 else None
                return cls(data[0], data[1], data[2], price, stock, supplier_id)
        except (ValueError, IndexError):
            return None

@dataclass
class Supplier:
    """
    Represents a supplier in the inventory system.
    Attributes:
        supplier_id (str): Unique identifier for the supplier
        name (str): Name of the supplier
        contact (str): Contact information for the supplier
    """
    supplier_id: str
    name: str
    contact: str

    def to_string(self) -> str:
        """Converts supplier data to pipe-delimited string format for file storage."""
        return f"{self.supplier_id}|{self.name}|{self.contact}"

    @classmethod
    def from_string(cls, line: str) -> Optional['Supplier']:
        """Creates a Supplier instance from a pipe-delimited string."""
        try:
            data = line.strip().split("|")
            if len(data) == 3:
                return cls(data[0], data[1], data[2])
        except (ValueError, IndexError):
            return None

@dataclass
class Order:
    """
    Represents a customer order in the inventory system.
    Attributes:
        order_id (str): Unique identifier for the order
        product_id (str): ID of the product ordered
        quantity (int): Quantity of the product ordered
        order_date (str): Date of the order (YYYY-MM-DD format)
    """
    order_id: str
    product_id: str
    quantity: int
    order_date: str

    def to_string(self) -> str:
        """Converts an Order instance to a pipe-delimited string format for file storage."""
        return f"{self.order_id}|{self.product_id}|{self.quantity}|{self.order_date}"

    @classmethod
    def from_string(cls, line: str) -> Optional['Order']:
        """Creates an Order instance from a pipe-delimited string."""
        try:
            data = line.strip().split("|")
            if len(data) == 4:
                quantity = int(data[2])
                return cls(data[0], data[1], quantity, data[3])
        except (ValueError, IndexError):
            return None

@dataclass
class SupplierOrder:
    """
    Represents a supplier order in the inventory system.
    Attributes:
        order_id (str): Unique identifier for the order
        supplier_id (str): ID of the supplier
        product_id (str): ID of the product ordered
        quantity (int): Quantity of the product ordered
        order_date (str): Date of the order (YYYY-MM-DD format)
    """
    order_id: str
    supplier_id: str
    product_id: str
    quantity: int
    order_date: str

    def to_string(self) -> str:
        """Converts a SupplierOrder instance to a pipe-delimited string format for file storage."""
        return f"{self.order_id}|{self.supplier_id}|{self.product_id}|{self.quantity}|{self.order_date}"

    @classmethod
    def from_string(cls, line: str) -> Optional['SupplierOrder']:
        """Creates a SupplierOrder instance from a pipe-delimited string."""
        try:
            data = line.strip().split("|")
            if len(data) == 5:
                quantity = int(data[3])
                return cls(data[0], data[1], data[2], quantity, data[4])
        except (ValueError, IndexError):
            return None

class FileManager:
    """
    Utility class for reading and writing data to files.
    Provides methods to load and save data from/to files.
    """
    @staticmethod
    def load_data_from_file(filename: str, parser_func) -> List:
        items = []
        if os.path.exists(filename):
            with open(filename, "r") as f:
                next(f, None)  # Skip header
                for line in f:
                    item = parser_func(line)
                    if item:
                        items.append(item)
        return items

    @staticmethod
    def save_data_to_file(filename: str, header: str, items: List):
        with open(filename, "w") as f:
            f.write(header + "\n")
            for item in items:
                f.write(item.to_string() + "\n")

class InventoryManagementSystem:
    """
    Main class for the Inventory Management System.
    Manages products, suppliers, orders, and provides functionality to add, update, and view data.
    
    Attributes:
        products (Dict[str, Product]): A dictionary of products with product ID as key
        suppliers (Dict[str, Supplier]): A dictionary of suppliers with supplier ID as key
        orders (List[Order]): A list of customer orders
        supplier_orders (List[SupplierOrder]): A list of supplier orders
        file_manager (FileManager): Utility class for file I/O operations
    """
    def __init__(self):
        """Initializes the InventoryManagementSystem with data from files.
        The system loads product, supplier, order, and supplier order data from files.
        """
        
        self.products: Dict[str, Product] = {}
        self.suppliers: Dict[str, Supplier] = {}
        self.orders: List[Order] = []
        self.supplier_orders: List[SupplierOrder] = []
        self.file_manager = FileManager()
        self.load_data()

    def load_data(self):
        """
        Loads product, supplier, order, and supplier order data from files.
        The data is loaded into the respective attributes of the InventoryManagementSystem.   
        """
        self.products = {
            p.product_id: p for p in self.file_manager.load_data_from_file("products.txt", Product.from_string) if p
        }
        self.suppliers = {
            s.supplier_id: s for s in self.file_manager.load_data_from_file("suppliers.txt", Supplier.from_string) if s
        }
        self.orders = [
            o for o in self.file_manager.load_data_from_file("orders.txt", Order.from_string) if o
        ]
        self.supplier_orders = [
            so for so in self.file_manager.load_data_from_file("supplier_orders.txt", SupplierOrder.from_string) if so
        ]

    def save_data(self):
        """
        Saves product, supplier, order, and supplier order data to files.
        The data is saved from the respective attributes of the InventoryManagementSystem.
        """
        self.file_manager.save_data_to_file(
            "products.txt", "product_id|name|description|price|stock|supplier_id", list(self.products.values())
        )
        self.file_manager.save_data_to_file(
            "suppliers.txt", "supplier_id|name|contact", list(self.suppliers.values())
        )
        self.file_manager.save_data_to_file(
            "orders.txt", "order_id|product_id|quantity|order_date", self.orders
        )
        self.file_manager.save_data_to_file(
            "supplier_orders.txt", "order_id|supplier_id|product_id|quantity|order_date", self.supplier_orders
        )

    def validate_numeric_input(self, prompt: str, convert_func, min_value: float = 0) -> Optional[float]:
        """
        Prompts the user for numeric input and validates the input.
        Args:
            prompt (str): The prompt message to display
            convert_func (Callable): The function to convert the input to a numeric value
            min_value (float): The minimum valid value for the input
            Returns:
            Optional[float]: The validated numeric input, or None if the input is invalid
        """
        try:
            value = convert_func(input(prompt))
            if value < min_value:
                print(f"Value must be greater than or equal to {min_value}")
                return None
            return value
        except ValueError:
            print("Invalid numeric input")
            return None

    def add_product(self):
        """
        Adds a new product to the inventory system.
        The user is prompted to enter product details, and the product is added to the product dictionary.
        """
        product_id = input("Enter product ID: ").strip()
        if not product_id or product_id in self.products:
            print("Invalid or duplicate Product ID!")
            return

        name = input("Enter product name: ").strip()
        description = input("Enter product description: ").strip()
        price = self.validate_numeric_input("Enter product price: ", float)
        stock = self.validate_numeric_input("Enter initial stock: ", int)

        print("\nAvailable suppliers:")
        for supplier_id, supplier in self.suppliers.items():
            print(f"{supplier_id}: {supplier.name}")

        supplier_id = input("Enter supplier ID (press Enter to skip): ").strip()
        if supplier_id and supplier_id not in self.suppliers:
            print("Supplier not found!")
            return
        product = Product(product_id, name, description, price, stock, supplier_id or None)
        self.products[product_id] = product
        self.save_data()
        print("Product added successfully!")

    def update_product(self):
        """
        Updates an existing product in the inventory system.
        The user is prompted to enter the product ID to update, and then the new product details.
        The product details are updated in the product dictionary.
        """
        old_product_id = input("Enter product ID to update: ")
        if old_product_id not in self.products:
            print("Product not found!")
            return

        product = self.products[old_product_id]
        print("\nCurrent Product Details:")
        print(f"ID: {product.product_id}")
        print(f"Name: {product.name}")
        print(f"Description: {product.description}")
        print(f"Price: {product.price}")
        print(f"Stock: {product.stock}")
        print(f"Supplier ID: {product.supplier_id or 'None'}")

        # Handle product ID update
        new_product_id = input("Enter new product ID (press Enter to keep current): ").strip()
        if new_product_id and new_product_id != old_product_id:
            if new_product_id in self.products:
                print("New product ID already exists!")
                return
            del self.products[old_product_id]
            product.product_id = new_product_id
            self.products[new_product_id] = product
            # Update product ID in orders
            for order in self.orders:
                if order.product_id == old_product_id:
                    order.product_id = new_product_id

        # Update other fields
        name = input("Enter new name (press Enter to keep current): ").strip()
        if name:
            product.name = name

        description = input("Enter new description (press Enter to keep current): ")
        if description:
            product.description = description

        new_price = input("Enter new price (press Enter to keep current): ")
        if new_price:
            price = self.validate_numeric_input("Enter new price: ", float)
            if price is not None:
                product.price = price

        new_stock = input("Enter new stock (press Enter to keep current): ")
        if new_stock:
            stock = self.validate_numeric_input("Enter new stock: ", int)
            if stock is not None:
                product.stock = stock

        supplier_id = input("Enter new supplier ID (press Enter to keep current, 'none' to remove): ").strip().lower()
        if supplier_id:
            if supplier_id == 'none':
                product.supplier_id = None
            elif supplier_id not in self.suppliers:
                print("Supplier not found!")
                return
            else:
                product.supplier_id = supplier_id

        self.save_data()
        print("Product updated successfully!")

    def add_supplier(self):
        """"
        Adds a new supplier to the inventory system.
        The user is prompted to enter supplier details, and the supplier is added to the supplier dictionary.
        """
        supplier_id = input("Enter supplier ID: ").strip()
        if not supplier_id:
            print("Supplier ID cannot be empty!")
            return
        if supplier_id in self.suppliers:
            print("Supplier ID already exists!")
            return

        name = input("Enter supplier name: ").strip()
        if not name:
            print("Supplier name cannot be empty!")
            return

        contact = input("Enter supplier contact details: ")
        
        supplier = Supplier(supplier_id, name, contact)
        self.suppliers[supplier_id] = supplier
        self.save_data()
        print("Supplier added successfully!")
        
    def place_customer_order(self):
        """
        Places a new customer order in the inventory system.
        The user is prompted to enter the product ID and quantity for the order.
        If the product is available in stock, the order is placed and the product stock is updated.
        """
        print("\nAvailable products:")
        for product_id, product in self.products.items():
            print(f"{product_id}: {product.name} (Stock: {product.stock})")

        product_id = input("Enter product ID: ").strip()
        if product_id not in self.products:
            print("Product not found!")
            return

        quantity = self.validate_numeric_input("Enter quantity: ", int, 1)
        if quantity is None or self.products[product_id].stock < quantity:
            print("Insufficient stock or invalid quantity!")
            return

        order_id = f"O{len(self.orders) + 1:03d}"
        order_date = datetime.now().strftime("%Y-%m-%d")

        order = Order(order_id, product_id, quantity, order_date)
        self.orders.append(order)
        self.products[product_id].stock -= quantity
        self.save_data()
        print("Customer order placed successfully!")

    def place_supplier_order(self):
        """
        Places a new supplier order in the inventory system.
        The user is prompted to enter the supplier ID, product ID, and quantity for the order.
        The order is placed and the product stock is updated based on the supplier order.
        """
        print("\nAvailable suppliers:")
        for supplier_id, supplier in self.suppliers.items():
            print(f"{supplier_id}: {supplier.name}")

        supplier_id = input("Enter supplier ID: ").strip()
        if supplier_id not in self.suppliers:
            print("Supplier not found!")
            return

        print("\nAvailable products:")
        for product_id, product in self.products.items():
            print(f"{product_id}: {product.name} (Stock: {product.stock})")

        product_id = input("Enter product ID: ").strip()
        if product_id not in self.products:
            print("Product not found!")
            return

        quantity = self.validate_numeric_input("Enter quantity: ", int, 1)
        if quantity is None:
            return

        order_id = f"SO{len(self.supplier_orders) + 1:03d}"
        order_date = datetime.now().strftime("%Y-%m-%d")

        supplier_order = SupplierOrder(order_id, supplier_id, product_id, quantity, order_date)
        self.supplier_orders.append(supplier_order)

        self.products[product_id].stock += quantity
        self.save_data()
        print("Supplier order placed successfully and inventory updated!")

    def view_inventory(self):
        """
        Displays the current inventory of products in the system.
        The product ID, name, stock, description, price, and supplier are displayed for each product.
        """  
        print("\nCurrent Inventory:")
        print("ID | Name | Stock | Description | Price | Supplier")
        for product in self.products.values():
        # Fix: Handle the supplier lookup properly
            supplier_name = self.suppliers[product.supplier_id].name if product.supplier_id and product.supplier_id in self.suppliers else 'N/A'
            print(f"{product.product_id} | {product.name} | {product.stock} | {product.description} | ${product.price:.2f} | {supplier_name}")

    def generate_reports(self):
        """
        Displays a menu to generate different reports from the inventory system.
        The user can choose to generate reports for low stock items, product sales, and supplier order history.
        """
        while True:
            print("\nReports Menu:")
            print("1. Low Stock Items (< 5 units)")
            print("2. Product Sales Report")
            print("3. Supplier Order History:")
            print("4. Back to Main Menu")
            
            choice = input("Enter your choice (1-4): ")
            
            if choice == "1":
                self._generate_low_stock_report()
            elif choice == "2":
                self._generate_sales_report()
            elif choice == "3":
                self._generate_supplier_report()
            elif choice == "4":
                break
            else:
                print("Invalid choice!")

    def _generate_low_stock_report(self):
        """
        Generates a report of low stock items (stock < 5) in the inventory system.
        The product ID, name, and current stock are displayed for each low stock item.
        """
        low_stock_items = [(p.product_id, p.name, p.stock) 
                          for p in self.products.values() if p.stock < 5]
        if not low_stock_items:
            print("\nNo low stock items found.")
            return

        print("\nLow Stock Items:")
        print("ID | Name | Stock")
        print("-" * 30)
        for pid, name, stock in low_stock_items:
            print(f"{pid} | {name} | {stock}")

    def _generate_sales_report(self):
        """
        Generates a product sales report based on the customer orders in the inventory system.
        The total quantity sold and revenue generated for each product are displayed in the report.
        """
        if not self.orders:
            print("\nNo orders found.")
            return

        sales_data = {}
        for order in self.orders:
            if order.product_id not in sales_data:
                sales_data[order.product_id] = 0
            sales_data[order.product_id] += order.quantity

        print("\nProduct Sales Report:")
        print("Product ID | Product Name | Total Quantity Sold | Total Revenue")
        print("-" * 65)
        for product_id, quantity in sales_data.items():
            product = self.products.get(product_id)
            if product:
                revenue = quantity * product.price
                print(f"{product_id} | {product.name} | {quantity} | ${revenue:.2f}")

    def _generate_supplier_report(self):
        """
        Generates a report showing the order history for all suppliers.
        Handles cases where supplier IDs in orders might not exist in the suppliers dictionary.
        """
        if not self.supplier_orders:
            print("\nNo supplier orders found.")
            return

        print("\nSupplier Order History:")
        print("Order ID | Supplier | Product | Quantity | Order Date")
        print("-" * 80)
    
        for order in self.supplier_orders:
            try:
                # Safely get supplier and product information
                supplier_name = self.suppliers.get(order.supplier_id, Supplier(order.supplier_id, "Unknown Supplier", "")).name
                product_name = self.products.get(order.product_id, Product(order.product_id, "Unknown Product", "", 0.0)).name
            
                print(f"{order.order_id} | {supplier_name} | {product_name} | {order.quantity} | {order.order_date}")
            except Exception as e:
                print(f"Error processing order {order.order_id}: {str(e)}")
                continue
    
    def main_menu(self):
        """
        Displays the main menu of the Inventory Management System.
        The user can choose to add products, update products, add suppliers, place orders, view inventory, generate reports, or exit the system.
        """
        while True:
            print("\n1. Add Product\n2. Update Product\n3. Add Supplier\n4. Place Customer Order\n5. Place Supplier Order\n6. View Inventory\n7. Generate Reports\n8. Exit")
            choice = input("Enter your choice (1-8): ").strip()

            if choice == "1":
                self.add_product()
            elif choice == "2":
                self.update_product()
            elif choice == "3":
                self.add_supplier()
            elif choice == "4":
                self.place_customer_order()
            elif choice == "5":
                self.place_supplier_order()
            elif choice == "6":
                self.view_inventory()
            elif choice == "7":
                self.generate_reports()
            elif choice == "8":
                print("Exiting system. Goodbye!")
                break
            else:
                print("Invalid choice, please try again.")

if __name__ == "__main__":
    """
    Main function to run the 3.
    Creates an instance of the InventoryManagementSystem and displays the main menu.
    """
    ims = InventoryManagementSystem()
    ims.main_menu()
