class Car:
    total_cars_produced = 0

    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
        Car.total_cars_produced += 1

    def display_info(self):
        return f"Car: {self.year} {self.make} {self.model}"

    @classmethod
    def get_total_cars(cls): 
        return cls.total_cars_produced

car1 = Car("Toyota", "Camry", 2020)
car2 = Car("Honda", "Civic", 2022)
car3 = Car("Porsche", "911", 2021)

print(car1.display_info())
print(car2.display_info())
print(car3.display_info())

print(f"\nTotal cars produced (via class): {Car.get_total_cars()}")
print(f"Total cars produced (via instance): {car1.get_total_cars()}")
