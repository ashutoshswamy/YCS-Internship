class Car:
    WHEELS = 4

    def __init__(self, make, model, year, mileage):
        self.make = make
        self.model = model
        self.year = year
        self.mileage = mileage

    def display_car_info(self):
        return f"{self.year} {self.make} {self.model} with {self.mileage} miles."

    @staticmethod
    def is_valid_year(year):
        current_year = 2025 
        return 1886 <= year <= current_year

    @staticmethod
    def convert_miles_to_km(miles):
        return miles * 1.60934

    @staticmethod
    def calculate_fuel_efficiency(distance_km, fuel_consumed_liters):
        if fuel_consumed_liters <= 0:
            return "Fuel consumed must be positive."
        return distance_km / fuel_consumed_liters


my_car = Car("Toyota", "Camry", 2020, 50000)
print(f"My car info: {my_car.display_car_info()}")


year_to_check_1 = 2023
print(f"Is {year_to_check_1} a valid car year? {Car.is_valid_year(year_to_check_1)}")

year_to_check_2 = 1800
print(f"Is {year_to_check_2} a valid car year? {Car.is_valid_year(year_to_check_2)}")

miles_distance = 100
km_distance = Car.convert_miles_to_km(miles_distance)
print(f"{miles_distance} miles is equal to {km_distance:.2f} kilometers.")

distance = 500 
fuel = 30   
efficiency = Car.calculate_fuel_efficiency(distance, fuel)
print(f"Fuel efficiency: {efficiency:.2f} km/liter.")

efficiency_invalid = Car.calculate_fuel_efficiency(100, 0)
print(f"Fuel efficiency (invalid fuel): {efficiency_invalid}")


print(f"\nUsing instance to call static method: Is 2025 valid? {my_car.is_valid_year(2025)}")
