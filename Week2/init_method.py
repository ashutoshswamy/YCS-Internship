class Item:
    pay_rate = 0.8
    def __init__(self, name: str, price: float, quantity: int):
        #validations
        assert price >= 0, f"Price {price} is not valid"
        assert quantity >= 0, f"Quantity {quantity} is not valid"

        self.name = name
        self.price = price
        self.quantity = quantity

    def calculate_total_price(self):
        return self.price * self.quantity
    
    def apply_discount(self):
        self.price = self.price * Item.pay_rate

item1 = Item("Phone", 1000, 5)

item2 = Item("Laptop", 5000, 3)
item2.has_numpad = False

print(item1.name)
print(item1.price)
print(item1.quantity)
print(item1.calculate_total_price())
item1.apply_discount()
print(item1.price)

print(item2.name)
print(item2.price)
print(item2.quantity)
print(item2.calculate_total_price())
item2.pay_rate = 0.7
item2.apply_discount()
print(item2.price)