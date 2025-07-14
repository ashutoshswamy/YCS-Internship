class Animal:
    def __init__(self, name, species):
        self.name = name
        self.species = species
    
    def make_sound(self):
        return f"{self.name} makes a sound"
    
    def info(self):
        return f"{self.name} is a {self.species}"

class Dog(Animal): 
    def __init__(self, name, breed):
        super().__init__(name, "Canine") 
        self.breed = breed
    
    def make_sound(self): 
        return f"{self.name} barks: Woof!"
    
    def fetch(self):  
        return f"{self.name} fetches the ball"

dog = Dog("Buddy", "Golden Retriever")
print(dog.info())        
print(dog.make_sound()) 
print(dog.fetch())