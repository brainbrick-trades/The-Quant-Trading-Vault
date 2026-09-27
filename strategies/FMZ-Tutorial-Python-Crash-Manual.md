
> Name

FMZ-Tutorial-Python-Crash-Manual

> Author

作手君TradeMan





> Source (python)

``` python
# Single-line comment
""" Multiline strings can use
    wrapped in three quotation marks, but this can also be regarded as
    Multi-line comment
"""

####################################################
## 1. Primitive data types and operators
####################################################

# Numeric type
3  # => 3

# Simple arithmetic
1 + 1  # => 2
8 - 1  # => 7
10 * 2  # => 20
35 / 5  # => 7

# Division of integers will automatically round down
5 / 2  # => 2

# To perform precise division, we need to introduce floating-point numbers
2.0     # Floating-point number
11.0 / 4.0  # => 2.75 Much more precise

# Parentheses have the highest precedence
(1 + 3) * 2  # => 8

# Boolean values are also a basic data type
True
False

# Use 'not' for negation
not True  # => False
not False  # => True

# equal
1 == 1  # => True
2 == 1  # => False

# No wait
1 != 1  # => False
2 != 1  # => True

# More comparison operators
1 < 10  # => True
1 > 10  # => False
2 <= 2  # => True
2 >= 2  # => True

# Comparison operations can be chained!
1 < 2 < 3  # => True
2 < 3 < 2  # => False

# Strings are enclosed with " or '
"This is a string."
'This is also a string.'

# Strings are concatenated with plus
"Hello " + "world!"  # => "Hello world!"

# Strings can be considered as a list of characters
"This is a string"[0]  # => 'T'

# % Can be used to format strings
"%s can be %s" % ("strings", "interpolated")

# You can also use the format method to format strings
# It is recommended to use this method
"{0} can be {1}".format("strings", "formatted")
# You can also use variable names instead of numbers
"{name} wants to eat {food}".format(name="Bob", food="lasagna")

# None is the object
None  # => None

# Do not use the equality `==` symbol to compare with None
# to use `is`
"etc" is None  # => False
None is None  # => True

# 'is' Can be used to compare the equality of objects
# This operator is not very useful when comparing raw data, but it is essential when comparing objects

# None, 0, Are both considered empty strings False
# All others are True
0 == False  # => True
"" == False  # => True


####################################################
## 2. Variables and collections
####################################################

# Conveniently output
print "I'm Python. Nice to meet you!"


# There is no need to declare in advance before assigning a value to a variable.
some_var = 5    # It is generally recommended to use a combination of lowercase letters and underscores as variable names.
some_var  # => 5

# Accessing an unassigned variable will throw an exception
# You can check the control flow section to learn how to handle exceptions
some_other_var  # throw NameError

# if Statements can be used as expressions
"yahoo!" if 3 > 2 else 2  # => "yahoo!"

# Lists are used to store sequences
li = []
# Lists can be directly initialized
other_li = [4, 5, 6]

# Add elements to the end of a list
li.append(1)    # li It is now [1]
li.append(2)    # li It is now [1, 2]
li.append(4)    # li It is now [1, 2, 4]
li.append(3)    # li It is now [1, 2, 4, 3]
# Remove the last element of the list
li.pop()        # => 3 li It is now [1, 2, 4]
# Put back in
li.append(3)    # li is now [1, 2, 4, 3] again.

# Access lists like arrays in other languages
li[0]  # => 1
# Access the last element
li[-1]  # => 3

# Out-of-bounds will throw an exception
li[4]  # Throw an out-of-bounds exception

# Slicing syntax requires index access of the list
# can be regarded as a left-closed, right-open interval in mathematics
li[1:3]  # => [2, 4]
# Omitting the initial elements
li[2:]  # => [4, 3]
# Omit the last element
li[:3]  # => [1, 2, 4]

# Delete a specific element
del li[2]  # li It is now [1, 2, 3]

# Merge list
li + other_li  # => [1, 2, 3, 4, 5, 6] - will not change these two lists

# Merge lists by concatenation
li.extend(other_li)  # li Yes/Is [1, 2, 3, 4, 5, 6]

# Use in to return whether the element is in the list
1 in li  # => True

# Return the length of the list
len(li)  # => 6


# Tuple is similar to list, but it is immutable
tup = (1, 2, 3)
tup[0]  # => 1
tup[0] = 3  # Type error

# Most list operations also apply to tuples
len(tup)  # => 3
tup + (4, 5, 6)  # => (1, 2, 3, 4, 5, 6)
tup[:2]  # => (1, 2)
2 in tup  # => True

# You can unpack a tuple and assign it to multiple variables
a, b, c = (1, 2, 3)     # a is 1, b is 2, c is 3
# If parentheses are not included, it will automatically be treated as a tuple.
d, e, f = 4, 5, 6
# Now we can see how easy it is to swap two numbers
e, d = d, e     # d is 5, e is 4


# Dictionaries are used to store mapping relationships
empty_dict = {}
# Dictionary initialization
filled_dict = {"one": 1, "two": 2, "three": 3}

# Dictionaries also use square brackets to access elements
filled_dict["one"]  # => 1

# Save all keys in a list
filled_dict.keys()  # => ["three", "two", "one"]
# The order of keys is not unique, so the result may not be in this order.

# Save all values in a list
filled_dict.values()  # => [3, 2, 1]
# is in the same order as the keys

# Check if a key exists
"one" in filled_dict  # => True
1 in filled_dict  # => False

# Querying a non-existent key will throw KeyError
filled_dict["four"]  # KeyError

# Use get method to avoid KeyError
filled_dict.get("one")  # => 1
filled_dict.get("four")  # => None
# get Method supports returning a default value when not present
filled_dict.get("one", 4)  # => 1
filled_dict.get("four", 4)  # => 4

# setdefault is a safer way to add dictionary elements
filled_dict.setdefault("five", 5)  # filled_dict["five"] the value of 5
filled_dict.setdefault("five", 6)  # filled_dict["five"] The value is still 5


# Sets store unordered elements
empty_set = set()
# Initialize a collection
some_set = set([1, 2, 2, 3, 4])  # some_set It is now set([1, 2, 3, 4])

# Python 2.7 Afterwards, curly braces can be used to represent a set
filled_set = {1, 2, 2, 3, 4}  # => {1 2 3 4}

# Add elements to the collection
filled_set.add(5)  # filled_set It is now {1, 2, 3, 4, 5}

# Use & to calculate the intersection of sets
other_set = {3, 4, 5, 6}
filled_set & other_set  # => {3, 4, 5}

# Use | to calculate the union of sets
filled_set | other_set  # => {1, 2, 3, 4, 5, 6}

# Use - to calculate the difference between sets
{1, 2, 3, 4} - {2, 3, 5}  # => {1, 4}

# Use 'in' to check if an element exists in a collection
2 in filled_set  # => True
10 in filled_set  # => False


####################################################
## 3. Control flow
####################################################

# Create a new variable
some_var = 5

# This is an if statement, and indentation in Pi Zhan is very important.
# The following code snippet will output "some var is smaller than 10"
if some_var > 10:
    print "some_var is totally bigger than 10."
elif some_var < 10:    # this elif statement is not required
    print "some_var is smaller than 10."
else:           # This else is also not necessary
    print "some_var is indeed 10."


"""
Use a for loop to traverse a list
output:
    dog is a mammal
    cat is a mammal
    mouse is a mammal
"""
for animal in ["dog", "cat", "mouse"]:
    # You can use % to format strings
    print "%s is a mammal" % animal

"""
`range(number)` Returns a list from 0 to the given number
output:
    0
    1
    2
    3
"""
for i in range(4):
    print i

"""
while Loop
output:
    0
    1
    2
    3
"""
x = 0
while x < 4:
    print x
    x += 1  #  x = x + 1 abbreviation of

# Use try/except blocks to handle exceptions

# Python 2.6 And above applicable:
try:
    # Use raise to throw exceptions
    raise IndexError("This is an index error")
except IndexError as e:
    pass    # pass It does nothing, but usually some recovery work is done here.


####################################################
## 4. Function
####################################################

# Use def to create a new function
def add(x, y):
    print "x is %s and y is %s" % (x, y)
    return x + y    # pass return To return a value

# Call a function with arguments
add(5, 6)  # => output "x is 5 and y is 6" Return 11

# Call a function by assigning keywords
add(y=6, x=5)   # The order does not matter

# We can also define functions that accept multiple variables, arranged in order
def varargs(*args):
    return args

varargs(1, 2, 3)  # => (1,2,3)


# We can also define functions that accept multiple variables, which are arranged according to keywords
def keyword_args(**kwargs):
    return kwargs

# Actual effect:
keyword_args(big="foot", loch="ness")  # => {"big": "foot", "loch": "ness"}

# You can also define a function in two forms at the same time
def all_the_args(*args, **kwargs):
    print args
    print kwargs
"""
all_the_args(1, 2, a=3, b=4) prints:
    (1, 2)
    {"a": 3, "b": 4}
"""

# When calling a function, we can also perform the opposite operation and expand tuples and dictionaries as parameters
args = (1, 2, 3, 4)
kwargs = {"a": 3, "b": 4}
all_the_args(*args)  # Equivalent to foo(1, 2, 3, 4)
all_the_args(**kwargs)  # Equivalent to foo(a=3, b=4)
all_the_args(*args, **kwargs)  # Equivalent to foo(1, 2, 3, 4, a=3, b=4)

# Functions are first-class citizens in Python
def create_adder(x):
    def adder(y):
        return x + y
    return adder

add_10 = create_adder(10)
add_10(3)  # => 13

# Anonymous function
(lambda x: x > 2)(3)  # => True

# Built-in higher-order function
map(add_10, [1, 2, 3])  # => [11, 12, 13]
filter(lambda x: x > 5, [3, 4, 5, 6, 7])  # => [6, 7]

# You can use list methods to make more clever references to higher-order functions
[add_10(i) for i in [1, 2, 3]]  # => [11, 12, 13]
[x for x in [3, 4, 5, 6, 7] if x > 5]  # => [6, 7]

####################################################
## 5. Class
####################################################

# The new class we created inherits from the object class
class Human(object):

     # Class attributes, shared by all objects of the class
    species = "H. sapiens"

    # Basic constructor
    def __init__(self, name):
        # Assign parameters to object member properties
        self.name = name

    # Member methods, parameters are required self
    def say(self, msg):
        return "%s: %s" % (self.name, msg)

    # Class methods are shared by all objects of the class
    # This kind of method, when called, passes the class itself to the first parameter
    @classmethod
    def get_species(cls):
        return cls.species

    # Static methods are methods that can be called without referencing the class or object
    @staticmethod
    def grunt():
        return "*grunt*"


# Instantiate a class
i = Human(name="Ian")
print i.say("hi")     # output "Ian: hi"

j = Human("Joel")
print j.say("hello")  # output "Joel: hello"

# Access a class method
i.get_species()  # => "H. sapiens"

# Change shared attributes
Human.species = "H. neanderthalensis"
i.get_species()  # => "H. neanderthalensis"
j.get_species()  # => "H. neanderthalensis"

# Access static variables
Human.grunt()  # => "*grunt*"


####################################################
## 6. module
####################################################

# We can import other modules
import math
print math.sqrt(16)  # => 4

# We can also import specific functions from a module
from math import ceil, floor
print ceil(3.7)   # => 4.0
print floor(3.7)  # => 3.0

# Import all functions from the module
# Warning: not recommended
from math import *

# Abbreviated module name
import math as m
math.sqrt(16) == m.sqrt(16)  # => True

# PythonA module is really just an ordinary Python file
# You can also create your own modules and import them
# The module's name is the same as the file name

# You can also view what attributes and methods are in a module using the following method
import math
dir(math)
```

> Detail

https://www.fmz.com/strategy/395727

> Last Modified

2023-01-16 09:43:03
