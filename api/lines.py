import random
import string
import math
import time

# Section 1: String Manipulations

def random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def is_palindrome(s):
    return s == s[::-1]

def longest_palindrome(s):
    n = len(s)
    if n == 0:
        return ""
    result = ""
    for i in range(n):
        for j in range(i + 1, n + 1):
            substring = s[i:j]
            if is_palindrome(substring) and len(substring) > len(result):
                result = substring
    return result

# Section 2: Sorting and Searching

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# Section 3: Math Utilities

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def prime_factors(n):
    factors = []
    while n % 2 == 0:
        factors.append(2)
        n = n // 2
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        while n % i == 0:
            factors.append(i)
            n = n // i
    if n > 2:
        factors.append(n)
    return factors

# Section 4: Classes and Objects

class Animal:
    def __init__(self, name, species):
        self.name = name
        self.species = species

    def speak(self):
        return f"{self.name} makes a sound."

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name, "Dog")
        self.breed = breed

    def speak(self):
        return f"{self.name} barks!"

class Cat(Animal):
    def __init__(self, name, color):
        super().__init__(name, "Cat")
        self.color = color

    def speak(self):
        return f"{self.name} meows!"

# Section 5: Fibonacci and Factorial

def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)

# Section 6: File Handling

def write_to_file(filename, content):
    with open(filename, "w") as file:
        file.write(content)

def read_from_file(filename):
    with open(filename, "r") as file:
        return file.read()

# Section 7: Performance Testing

def time_function(func, *args):
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")
    return result

# Section 8: Miscellaneous Utilities

def generate_random_list(size, lower_bound=0, upper_bound=100):
    return [random.randint(lower_bound, upper_bound) for _ in range(size)]

def unique_elements(arr):
    return list(set(arr))

def find_max_min(arr):
    return max(arr), min(arr)

# Section 9: Data Structures

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def insert(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def display(self):
        elements = []
        current = self.head
        while current:
            elements.append(current.data)
            current = current.next
        print(elements)

# Section 10: Graph Algorithms

class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, u, v):
        if u not in self.graph:
            self.graph[u] = []
        self.graph[u].append(v)

    def dfs(self, start, visited=None):
        if visited is None:
            visited = set()
        visited.add(start)
        print(start, end=" ")
        for neighbor in self.graph.get(start, []):
            if neighbor not in visited:
                self.dfs(neighbor, visited)

# Section 11: Recursive Algorithms

def power(x, y):
    if y == 0:
        return 1
    half = power(x, y // 2)
    if y % 2 == 0:
        return half * half
    else:
        return x * half * half

# Section 12: Random Walk Simulation

def random_walk(steps):
    x, y = 0, 0
    for _ in range(steps):
        dx, dy = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
        x += dx
        y += dy
    return x, y

# Section 13: Matrix Operations

def create_matrix(rows, cols):
    return [[random.randint(0, 10) for _ in range(cols)] for _ in range(rows)]

def matrix_addition(mat1, mat2):
    result = [[mat1[i][j] + mat2[i][j] for j in range(len(mat1[0]))] for i in range(len(mat1))]
    return result

# Section 14: Simple Encryption (Caesar Cipher)

def caesar_cipher(text, shift):
    result = ""
    for i in text:
        if i.isalpha():
            shift_amount = shift % 26
            new_char = chr(((ord(i) - 97 + shift_amount) % 26) + 97) if i.islower() else chr(((ord(i) - 65 + shift_amount) % 26) + 65)
            result += new_char
        else:
            result += i
    return result

# Section 15: Data Parsing

def parse_csv(filename):
    with open(filename, "r") as file:
        rows = [line.strip().split(",") for line in file]
    return rows

def parse_json(json_string):
    import json
    return json.loads(json_string)

# Section 16: Prime Number Generator

def generate_primes(limit):
    primes = []
    sieve = [True] * (limit + 1)
    sieve[0], sieve[1] = False, False
    for num in range(2, limit + 1):
        if sieve[num]:
            primes.append(num)
            for multiple in range(num * num, limit + 1, num):
                sieve[multiple] = False
    return primes

# Section 17: Web Scraping Example

def scrape_website(url):
    import requests
    from bs4 import BeautifulSoup
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup.title.string

# Section 18: API Requests

def get_weather(city):
    api_key = "your_api_key_here"
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(base_url)
    return response.json()

# Section 19: Text Analysis

def word_frequency(text):
    words = text.lower().split()
    frequency = {}
    for word in words:
        frequency[word] = frequency.get(word, 0) + 1
    return frequency

# Section 20: Main Execution

def main():
    print("Random String:", random_string())
    print("Is Palindrome:", is_palindrome("racecar"))
    print("Longest Palindrome:", longest_palindrome("babad"))

    arr = generate_random_list(10)
    print("Original List:", arr)
    bubble_sort(arr)
    print("Sorted List:", arr)

    primes = generate_primes(100)
    print("Primes up to 100:", primes)

    llist = LinkedList()
    for i in range(5):
        llist.insert(i)
    llist.display()

if __name__ == "__main__":
    main()
import random
import string
import math
import time

# Section 1: String Manipulations

def random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def is_palindrome(s):
    return s == s[::-1]

def longest_palindrome(s):
    n = len(s)
    if n == 0:
        return ""
    result = ""
    for i in range(n):
        for j in range(i + 1, n + 1):
            substring = s[i:j]
            if is_palindrome(substring) and len(substring) > len(result):
                result = substring
    return result

# Section 2: Sorting and Searching

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# Section 3: Math Utilities

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def prime_factors(n):
    factors = []
    while n % 2 == 0:
        factors.append(2)
        n = n // 2
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        while n % i == 0:
            factors.append(i)
            n = n // i
    if n > 2:
        factors.append(n)
    return factors

# Section 4: Classes and Objects

class Animal:
    def __init__(self, name, species):
        self.name = name
        self.species = species

    def speak(self):
        return f"{self.name} makes a sound."

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name, "Dog")
        self.breed = breed

    def speak(self):
        return f"{self.name} barks!"

class Cat(Animal):
    def __init__(self, name, color):
        super().__init__(name, "Cat")
        self.color = color

    def speak(self):
        return f"{self.name} meows!"

# Section 5: Fibonacci and Factorial

def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)

# Section 6: File Handling

def write_to_file(filename, content):
    with open(filename, "w") as file:
        file.write(content)

def read_from_file(filename):
    with open(filename, "r") as file:
        return file.read()

# Section 7: Performance Testing

def time_function(func, *args):
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")
    return result

# Section 8: Miscellaneous Utilities

def generate_random_list(size, lower_bound=0, upper_bound=100):
    return [random.randint(lower_bound, upper_bound) for _ in range(size)]

def unique_elements(arr):
    return list(set(arr))

def find_max_min(arr):
    return max(arr), min(arr)

# Section 9: Data Structures

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def insert(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def display(self):
        elements = []
        current = self.head
        while current:
            elements.append(current.data)
            current = current.next
        print(elements)

# Section 10: Graph Algorithms

class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, u, v):
        if u not in self.graph:
            self.graph[u] = []
        self.graph[u].append(v)

    def dfs(self, start, visited=None):
        if visited is None:
            visited = set()
        visited.add(start)
        print(start, end=" ")
        for neighbor in self.graph.get(start, []):
            if neighbor not in visited:
                self.dfs(neighbor, visited)

# Section 11: Recursive Algorithms

def power(x, y):
    if y == 0:
        return 1
    half = power(x, y // 2)
    if y % 2 == 0:
        return half * half
    else:
        return x * half * half

# Section 12: Random Walk Simulation

def random_walk(steps):
    x, y = 0, 0
    for _ in range(steps):
        dx, dy = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
        x += dx
        y += dy
    return x, y

# Section 13: Matrix Operations

def create_matrix(rows, cols):
    return [[random.randint(0, 10) for _ in range(cols)] for _ in range(rows)]

def matrix_addition(mat1, mat2):
    result = [[mat1[i][j] + mat2[i][j] for j in range(len(mat1[0]))] for i in range(len(mat1))]
    return result

# Section 14: Simple Encryption (Caesar Cipher)

def caesar_cipher(text, shift):
    result = ""
    for i in text:
        if i.isalpha():
            shift_amount = shift % 26
            new_char = chr(((ord(i) - 97 + shift_amount) % 26) + 97) if i.islower() else chr(((ord(i) - 65 + shift_amount) % 26) + 65)
            result += new_char
        else:
            result += i
    return result

# Section 15: Data Parsing

def parse_csv(filename):
    with open(filename, "r") as file:
        rows = [line.strip().split(",") for line in file]
    return rows

def parse_json(json_string):
    import json
    return json.loads(json_string)

# Section 16: Prime Number Generator

def generate_primes(limit):
    primes = []
    sieve = [True] * (limit + 1)
    sieve[0], sieve[1] = False, False
    for num in range(2, limit + 1):
        if sieve[num]:
            primes.append(num)
            for multiple in range(num * num, limit + 1, num):
                sieve[multiple] = False
    return primes

# Section 17: Web Scraping Example

def scrape_website(url):
    import requests
    from bs4 import BeautifulSoup
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup.title.string

# Section 18: API Requests

def get_weather(city):
    api_key = "your_api_key_here"
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(base_url)
    return response.json()

# Section 19: Text Analysis

def word_frequency(text):
    words = text.lower().split()
    frequency = {}
    for word in words:
        frequency[word] = frequency.get(word, 0) + 1
    return frequency

# Section 20: Main Execution

def main():
    print("Random String:", random_string())
    print("Is Palindrome:", is_palindrome("racecar"))
    print("Longest Palindrome:", longest_palindrome("babad"))

    arr = generate_random_list(10)
    print("Original List:", arr)
    bubble_sort(arr)
    print("Sorted List:", arr)

    primes = generate_primes(100)
    print("Primes up to 100:", primes)

    llist = LinkedList()
    for i in range(5):
        llist.insert(i)
    llist.display()

if __name__ == "__main__":
    main()
import random
import string
import math
import time

# Section 1: String Manipulations

def random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def is_palindrome(s):
    return s == s[::-1]

def longest_palindrome(s):
    n = len(s)
    if n == 0:
        return ""
    result = ""
    for i in range(n):
        for j in range(i + 1, n + 1):
            substring = s[i:j]
            if is_palindrome(substring) and len(substring) > len(result):
                result = substring
    return result

# Section 2: Sorting and Searching

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# Section 3: Math Utilities

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def prime_factors(n):
    factors = []
    while n % 2 == 0:
        factors.append(2)
        n = n // 2
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        while n % i == 0:
            factors.append(i)
            n = n // i
    if n > 2:
        factors.append(n)
    return factors

# Section 4: Classes and Objects

class Animal:
    def __init__(self, name, species):
        self.name = name
        self.species = species

    def speak(self):
        return f"{self.name} makes a sound."

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name, "Dog")
        self.breed = breed

    def speak(self):
        return f"{self.name} barks!"

class Cat(Animal):
    def __init__(self, name, color):
        super().__init__(name, "Cat")
        self.color = color

    def speak(self):
        return f"{self.name} meows!"

# Section 5: Fibonacci and Factorial

def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)

# Section 6: File Handling

def write_to_file(filename, content):
    with open(filename, "w") as file:
        file.write(content)

def read_from_file(filename):
    with open(filename, "r") as file:
        return file.read()

# Section 7: Performance Testing

def time_function(func, *args):
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")
    return result

# Section 8: Miscellaneous Utilities

def generate_random_list(size, lower_bound=0, upper_bound=100):
    return [random.randint(lower_bound, upper_bound) for _ in range(size)]

def unique_elements(arr):
    return list(set(arr))

def find_max_min(arr):
    return max(arr), min(arr)

# Section 9: Data Structures

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def insert(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def display(self):
        elements = []
        current = self.head
        while current:
            elements.append(current.data)
            current = current.next
        print(elements)

# Section 10: Graph Algorithms

class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, u, v):
        if u not in self.graph:
            self.graph[u] = []
        self.graph[u].append(v)

    def dfs(self, start, visited=None):
        if visited is None:
            visited = set()
        visited.add(start)
        print(start, end=" ")
        for neighbor in self.graph.get(start, []):
            if neighbor not in visited:
                self.dfs(neighbor, visited)

# Section 11: Recursive Algorithms

def power(x, y):
    if y == 0:
        return 1
    half = power(x, y // 2)
    if y % 2 == 0:
        return half * half
    else:
        return x * half * half

# Section 12: Random Walk Simulation

def random_walk(steps):
    x, y = 0, 0
    for _ in range(steps):
        dx, dy = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
        x += dx
        y += dy
    return x, y

# Section 13: Matrix Operations

def create_matrix(rows, cols):
    return [[random.randint(0, 10) for _ in range(cols)] for _ in range(rows)]

def matrix_addition(mat1, mat2):
    result = [[mat1[i][j] + mat2[i][j] for j in range(len(mat1[0]))] for i in range(len(mat1))]
    return result

# Section 14: Simple Encryption (Caesar Cipher)

def caesar_cipher(text, shift):
    result = ""
    for i in text:
        if i.isalpha():
            shift_amount = shift % 26
            new_char = chr(((ord(i) - 97 + shift_amount) % 26) + 97) if i.islower() else chr(((ord(i) - 65 + shift_amount) % 26) + 65)
            result += new_char
        else:
            result += i
    return result

# Section 15: Data Parsing

def parse_csv(filename):
    with open(filename, "r") as file:
        rows = [line.strip().split(",") for line in file]
    return rows

def parse_json(json_string):
    import json
    return json.loads(json_string)

# Section 16: Prime Number Generator

def generate_primes(limit):
    primes = []
    sieve = [True] * (limit + 1)
    sieve[0], sieve[1] = False, False
    for num in range(2, limit + 1):
        if sieve[num]:
            primes.append(num)
            for multiple in range(num * num, limit + 1, num):
                sieve[multiple] = False
    return primes

# Section 17: Web Scraping Example

def scrape_website(url):
    import requests
    from bs4 import BeautifulSoup
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup.title.string

# Section 18: API Requests

def get_weather(city):
    api_key = "your_api_key_here"
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(base_url)
    return response.json()

# Section 19: Text Analysis

def word_frequency(text):
    words = text.lower().split()
    frequency = {}
    for word in words:
        frequency[word] = frequency.get(word, 0) + 1
    return frequency

# Section 20: Main Execution

def main():
    print("Random String:", random_string())
    print("Is Palindrome:", is_palindrome("racecar"))
    print("Longest Palindrome:", longest_palindrome("babad"))

    arr = generate_random_list(10)
    print("Original List:", arr)
    bubble_sort(arr)
    print("Sorted List:", arr)

    primes = generate_primes(100)
    print("Primes up to 100:", primes)

    llist = LinkedList()
    for i in range(5):
        llist.insert(i)
    llist.display()

if __name__ == "__main__":
    main()
import random
import string
import math
import time

# Section 1: String Manipulations

def random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def is_palindrome(s):
    return s == s[::-1]

def longest_palindrome(s):
    n = len(s)
    if n == 0:
        return ""
    result = ""
    for i in range(n):
        for j in range(i + 1, n + 1):
            substring = s[i:j]
            if is_palindrome(substring) and len(substring) > len(result):
                result = substring
    return result

# Section 2: Sorting and Searching

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# Section 3: Math Utilities

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def prime_factors(n):
    factors = []
    while n % 2 == 0:
        factors.append(2)
        n = n // 2
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        while n % i == 0:
            factors.append(i)
            n = n // i
    if n > 2:
        factors.append(n)
    return factors

# Section 4: Classes and Objects

class Animal:
    def __init__(self, name, species):
        self.name = name
        self.species = species

    def speak(self):
        return f"{self.name} makes a sound."

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name, "Dog")
        self.breed = breed

    def speak(self):
        return f"{self.name} barks!"

class Cat(Animal):
    def __init__(self, name, color):
        super().__init__(name, "Cat")
        self.color = color

    def speak(self):
        return f"{self.name} meows!"

# Section 5: Fibonacci and Factorial

def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)

# Section 6: File Handling

def write_to_file(filename, content):
    with open(filename, "w") as file:
        file.write(content)

def read_from_file(filename):
    with open(filename, "r") as file:
        return file.read()

# Section 7: Performance Testing

def time_function(func, *args):
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")
    return result

# Section 8: Miscellaneous Utilities

def generate_random_list(size, lower_bound=0, upper_bound=100):
    return [random.randint(lower_bound, upper_bound) for _ in range(size)]

def unique_elements(arr):
    return list(set(arr))

def find_max_min(arr):
    return max(arr), min(arr)

# Section 9: Data Structures

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def insert(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def display(self):
        elements = []
        current = self.head
        while current:
            elements.append(current.data)
            current = current.next
        print(elements)

# Section 10: Graph Algorithms

class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, u, v):
        if u not in self.graph:
            self.graph[u] = []
        self.graph[u].append(v)

    def dfs(self, start, visited=None):
        if visited is None:
            visited = set()
        visited.add(start)
        print(start, end=" ")
        for neighbor in self.graph.get(start, []):
            if neighbor not in visited:
                self.dfs(neighbor, visited)

# Section 11: Recursive Algorithms

def power(x, y):
    if y == 0:
        return 1
    half = power(x, y // 2)
    if y % 2 == 0:
        return half * half
    else:
        return x * half * half

# Section 12: Random Walk Simulation

def random_walk(steps):
    x, y = 0, 0
    for _ in range(steps):
        dx, dy = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
        x += dx
        y += dy
    return x, y

# Section 13: Matrix Operations

def create_matrix(rows, cols):
    return [[random.randint(0, 10) for _ in range(cols)] for _ in range(rows)]

def matrix_addition(mat1, mat2):
    result = [[mat1[i][j] + mat2[i][j] for j in range(len(mat1[0]))] for i in range(len(mat1))]
    return result

# Section 14: Simple Encryption (Caesar Cipher)

def caesar_cipher(text, shift):
    result = ""
    for i in text:
        if i.isalpha():
            shift_amount = shift % 26
            new_char = chr(((ord(i) - 97 + shift_amount) % 26) + 97) if i.islower() else chr(((ord(i) - 65 + shift_amount) % 26) + 65)
            result += new_char
        else:
            result += i
    return result

# Section 15: Data Parsing

def parse_csv(filename):
    with open(filename, "r") as file:
        rows = [line.strip().split(",") for line in file]
    return rows

def parse_json(json_string):
    import json
    return json.loads(json_string)

# Section 16: Prime Number Generator

def generate_primes(limit):
    primes = []
    sieve = [True] * (limit + 1)
    sieve[0], sieve[1] = False, False
    for num in range(2, limit + 1):
        if sieve[num]:
            primes.append(num)
            for multiple in range(num * num, limit + 1, num):
                sieve[multiple] = False
    return primes

# Section 17: Web Scraping Example

def scrape_website(url):
    import requests
    from bs4 import BeautifulSoup
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup.title.string

# Section 18: API Requests

def get_weather(city):
    api_key = "your_api_key_here"
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(base_url)
    return response.json()

# Section 19: Text Analysis

def word_frequency(text):
    words = text.lower().split()
    frequency = {}
    for word in words:
        frequency[word] = frequency.get(word, 0) + 1
    return frequency

# Section 20: Main Execution

def main():
    print("Random String:", random_string())
    print("Is Palindrome:", is_palindrome("racecar"))
    print("Longest Palindrome:", longest_palindrome("babad"))

    arr = generate_random_list(10)
    print("Original List:", arr)
    bubble_sort(arr)
    print("Sorted List:", arr)

    primes = generate_primes(100)
    print("Primes up to 100:", primes)
    llist = LinkedList()
    for i in range(5):
        llist.insert(i)
    llist.display()
    
if __name__ == "__main__":
    main()
