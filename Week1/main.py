#basic concepts of python

#this is a comment in python
#this is a multi-line comment
"""
this is also a multi-line comment
anything written here will not be executed
"""

#variables
name = "Ashutosh Swamy"
age = 17

print(name)

#data types
name = "Ashutosh Swamy" #string
age = 17 #integer
height = 5.9 #float
is_student = True #boolean
hobbies = ["coding", "gaming", "cycling", "cricket"] #list
hobbies_tuple = ("coding", "gaming", "cycling", "cricket") #tuple
numbers = {1, 2, 3, 4, 5} #set
profile = { #dictionary
    "name": "Ashutosh Swamy",
    "age": 17,
    "height": 5.9,
    "is_student": True,
    "hobbies": ["coding", "gaming", "cycling", "cricket"]
}

print(name, type(name))
print(age, type(age))
print(height, type(height)) 
print(is_student, type(is_student))
print(hobbies, type(hobbies))  
print(hobbies_tuple, type(hobbies_tuple))
print(numbers, type(numbers))
print(profile, type(profile))

#arithmetic operations
a = 10
b = 5
print(a + b) #addition
print(a - b) #subtraction
print(a * b) #multiplication
print(a / b) #division
print(a % b) #modulus
print(a ** b) #exponentiation
print(a // b) #floor division

#comparison operations
print(a == b)  # equal to
print(a != b)  # not equal to
print(a > b)   # greater than
print(a < b)   # less than
print(a >= b)  # greater than or equal to
print(a <= b)  # less than or equal to

#logical operations
print(a > 5 and b < 10)  # logical AND
print(a > 5 or b < 10)   # logical OR
print(not (a > 5))        # logical NOT

#conditional statements
age = 20

if age < 18:
    print("Minor")
elif age >= 18 and age < 65:
    print("Adult")
else:
    print("Senior")

#loops
for i in range(5): #for loop
    print(i)

count = 0 #while loop
while count < 5:
    print(count)
    count += 1

#functions
def greet(name):
    return f"Hello, {name}!"
print(greet("Ashutosh"))

def add(a, b):
    return a + b
print(add(10, 5))

#string manipulation
my_string = "Hello World!"
print(my_string.lower())  # lowercase
print(my_string.upper())  # uppercase
print(my_string.replace("World", "Ashutosh"))  # replace substring
print(my_string.split())  # split into list
print(my_string.find("World"))  # find substring index
print(my_string.startswith("Hello"))  # check if starts with substring
print(my_string.endswith("!"))  # check if ends with substring
print(len(my_string))  # length of string

#built-in functions
print(abs(-10))  # absolute value
print(round(3.14159, 2))  # round to 2 decimal places
print(max(1, 2, 3, 4, 5))  # maximum value
print(min(1, 2, 3, 4, 5))  # minimum value
print(sum([1, 2, 3, 4, 5]))  # sum of list
print(sorted([5, 3, 1, 4, 2]))  # sorted list

#list comprehension
squared_numbers = [x**2 for x in range(10)]
print(squared_numbers)

even_numbers = [x for x in range(20) if x % 2 == 0]  # even numbers
print(even_numbers)

#list functions
my_list = [1, 2, 3, 4, 5]
print(my_list)  # print list
print(my_list[0])  # access first element
print(my_list[-1])  # access last element
print(my_list[1:3])  # slice list
print(my_list + [6, 7, 8])  # concatenate lists
print(my_list * 2)  # repeat list
print(len(my_list))  # length of list
print(my_list.index(3))  # index of element
print(my_list.count(2))  # count occurrences of element
print(my_list.append(6))  # append element
print(my_list)  # print updated list
print(my_list.pop())  # remove and return last element
print(my_list)  # print updated list after pop
print(my_list.remove(2))  # remove first occurrence of element
print(my_list)  # print updated list after remove
print(my_list.sort())  # sort list in place
print(my_list)  # print sorted list
print(my_list.insert(1, 10))  # insert element at index
print(my_list)  # print updated list after insert
print(my_list.remove(10))  # remove element
print(my_list)  # print updated list after remove
print(my_list.reverse())  # reverse list in place
print(my_list)  # print reversed list
print(max(my_list))  # maximum value in list
print(min(my_list))  # minimum value in list    
print(sum(my_list))  # sum of elements in list
print(sorted(my_list))  # sorted list 

#lambda functions
add_numbers = lambda x, y: x + y
print(add_numbers(5, 10))  

#user input
user_name = str(input("Enter your name: "))
print(f"Hello, {user_name}!")
