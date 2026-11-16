"""
The coding problem bank. Every problem is Python-only (per training focus).

Each problem is a dict:
  id                 unique slug
  title              display title
  category           one of meta.PROBLEM_TYPES
  difficulty         one of meta.DIFFICULTIES
  time_limit_min     suggested time box, used to seed the timer
  prompt             full problem statement shown to the competitor
  starter_code       skeleton dropped into the editor
  reference_solution shown only when the user clicks "Reveal Solution"
  test_cases         list of {"stdin": "...", "expect": "..."}; a test passes
                      when `expect` appears verbatim (after trimming each
                      line's trailing whitespace) inside the program's stdout.
                      This is intentionally a "contains" check, not exact
                      match, so extra menu text/prompts don't break grading.
  hints              optional list of nudges, revealed one at a time
"""

PROBLEMS = [
    {
        "id": "menu_contacts",
        "title": "Contact Book Menu",
        "category": "Menu-driven console app",
        "difficulty": "Easy",
        "time_limit_min": 25,
        "prompt": """Build a console contact book.

Print this exact menu every time you ask for a choice, then read the choice with input():

1. Add Contact
2. View Contacts
3. Delete Contact
4. Quit

- Add Contact: prompt "Name: " then "Phone: ", store the contact.
- View Contacts: print each stored contact as "Name - Phone" (one per line).
  If there are none, print exactly: No contacts yet.
- Delete Contact: prompt "Name to delete: ". If found, remove it (no output
  required beyond removal). If not found, print exactly: Contact not found.
- Quit: print exactly: Goodbye! and end the program.

Loop back to the menu after every action except Quit.""",
        "starter_code": '''def main():
    contacts = {}
    while True:
        print("1. Add Contact")
        print("2. View Contacts")
        print("3. Delete Contact")
        print("4. Quit")
        choice = input()

        if choice == "1":
            pass  # TODO
        elif choice == "2":
            pass  # TODO
        elif choice == "3":
            pass  # TODO
        elif choice == "4":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
''',
        "reference_solution": '''def main():
    contacts = {}
    while True:
        print("1. Add Contact")
        print("2. View Contacts")
        print("3. Delete Contact")
        print("4. Quit")
        choice = input()

        if choice == "1":
            name = input("Name: ")
            phone = input("Phone: ")
            contacts[name] = phone
        elif choice == "2":
            if not contacts:
                print("No contacts yet.")
            else:
                for name, phone in contacts.items():
                    print(f"{name} - {phone}")
        elif choice == "3":
            name = input("Name to delete: ")
            if name in contacts:
                del contacts[name]
            else:
                print("Contact not found.")
        elif choice == "4":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
''',
        "test_cases": [
            {"stdin": "2\n4\n", "expect": "No contacts yet."},
            {"stdin": "1\nAlice\n555-1234\n2\n4\n", "expect": "Alice - 555-1234"},
            {"stdin": "3\nCharlie\n4\n", "expect": "Contact not found."},
            {"stdin": "1\nBob\n555-0000\n3\nBob\n2\n4\n", "expect": "No contacts yet."},
        ],
        "hints": [
            "Use a dict keyed by name so add/delete/lookup are all simple.",
            "The menu text must print every loop iteration, exactly as shown.",
        ],
    },
    {
        "id": "menu_inventory",
        "title": "Inventory Manager",
        "category": "Menu-driven console app",
        "difficulty": "Medium",
        "time_limit_min": 30,
        "prompt": """Build a console inventory manager.

Print this exact menu every time you ask for a choice:

1. Add Item
2. Update Quantity
3. View Inventory
4. Total Value
5. Quit

- Add Item: prompt "Item name: ", "Price: ", "Quantity: " and store them.
- Update Quantity: prompt "Item name: " then "New quantity: ". If the item
  doesn't exist, print exactly: Item not found.
- View Inventory: print each item as "name: qty @ $price" (price with 2
  decimals, e.g. "Widget: 4 @ $2.50"). If empty, print exactly:
  Inventory is empty.
- Total Value: print exactly: Total Value: $X.XX (sum of price * qty over
  all items, 2 decimal places).
- Quit: print exactly: Goodbye! and stop.""",
        "starter_code": '''def main():
    items = {}
    while True:
        print("1. Add Item")
        print("2. Update Quantity")
        print("3. View Inventory")
        print("4. Total Value")
        print("5. Quit")
        choice = input()
        # TODO: implement each branch
        if choice == "5":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
''',
        "reference_solution": '''def main():
    items = {}
    while True:
        print("1. Add Item")
        print("2. Update Quantity")
        print("3. View Inventory")
        print("4. Total Value")
        print("5. Quit")
        choice = input()

        if choice == "1":
            name = input("Item name: ")
            price = float(input("Price: "))
            qty = int(input("Quantity: "))
            items[name] = {"price": price, "qty": qty}
        elif choice == "2":
            name = input("Item name: ")
            if name not in items:
                print("Item not found.")
            else:
                items[name]["qty"] = int(input("New quantity: "))
        elif choice == "3":
            if not items:
                print("Inventory is empty.")
            else:
                for name, info in items.items():
                    print(f"{name}: {info['qty']} @ ${info['price']:.2f}")
        elif choice == "4":
            total = sum(i["price"] * i["qty"] for i in items.values())
            print(f"Total Value: ${total:.2f}")
        elif choice == "5":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
''',
        "test_cases": [
            {"stdin": "3\n5\n", "expect": "Inventory is empty."},
            {"stdin": "1\nWidget\n2.50\n4\n4\n5\n", "expect": "Total Value: $10.00"},
            {"stdin": "2\nGadget\n5\n5\n", "expect": "Item not found."},
            {"stdin": "1\nWidget\n2.50\n4\n3\n5\n", "expect": "Widget: 4 @ $2.50"},
        ],
        "hints": ["Store each item as a dict with 'price' and 'qty' keys."],
    },
    {
        "id": "file_grades",
        "title": "Grade Report Parser",
        "category": "File I/O & data parsing",
        "difficulty": "Medium",
        "time_limit_min": 25,
        "prompt": """Parse student records and compute grades (this simulates reading a
data file: the "file contents" arrive over stdin instead, so you can still
grade it automatically).

Input format:
  Line 1: an integer N
  Next N lines: "Name,Score" (score is an integer 0-100)

For each student print: Name: Score (Letter)
using the standard scale: 90+ A, 80-89 B, 70-79 C, 60-69 D, below 60 F.

After all students, print exactly: Class Average: XX.XX
(the mean score, rounded to 2 decimal places).""",
        "starter_code": '''def letter_grade(score):
    # TODO: return "A", "B", "C", "D", or "F"
    pass


def main():
    n = int(input())
    total = 0
    for _ in range(n):
        line = input()
        name, score = line.split(",")
        score = int(score)
        total += score
        print(f"{name}: {score} ({letter_grade(score)})")
    print(f"Class Average: {total / n:.2f}")


if __name__ == "__main__":
    main()
''',
        "reference_solution": '''def letter_grade(score):
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"


def main():
    n = int(input())
    total = 0
    for _ in range(n):
        line = input()
        name, score = line.split(",")
        score = int(score)
        total += score
        print(f"{name}: {score} ({letter_grade(score)})")
    print(f"Class Average: {total / n:.2f}")


if __name__ == "__main__":
    main()
''',
        "test_cases": [
            {"stdin": "3\nAlice,95\nBob,82\nCarl,58\n", "expect": "Alice: 95 (A)"},
            {"stdin": "3\nAlice,95\nBob,82\nCarl,58\n", "expect": "Carl: 58 (F)"},
            {"stdin": "3\nAlice,95\nBob,82\nCarl,58\n", "expect": "Class Average: 78.33"},
        ],
        "hints": ["Split each line on the comma; the score arrives as a string."],
    },
    {
        "id": "file_log_analyzer",
        "title": "Server Log Level Counter",
        "category": "File I/O & data parsing",
        "difficulty": "Medium",
        "time_limit_min": 25,
        "prompt": """Read simulated log file contents from stdin and summarize them.

Input format:
  Line 1: an integer N
  Next N lines: "LEVEL: message" where LEVEL is INFO, WARNING, or ERROR

Print, in this exact order:
  INFO: <count>
  WARNING: <count>
  ERROR: <count>
  Most Common: <LEVEL with the highest count>

(You can assume the test data never produces a tie for most common.)""",
        "starter_code": '''def main():
    n = int(input())
    counts = {"INFO": 0, "WARNING": 0, "ERROR": 0}
    for _ in range(n):
        line = input()
        level = line.split(":")[0]
        # TODO: increment counts[level]

    # TODO: print the three counts, then the most common level


if __name__ == "__main__":
    main()
''',
        "reference_solution": '''def main():
    n = int(input())
    counts = {"INFO": 0, "WARNING": 0, "ERROR": 0}
    for _ in range(n):
        line = input()
        level = line.split(":")[0]
        counts[level] += 1

    for level in ("INFO", "WARNING", "ERROR"):
        print(f"{level}: {counts[level]}")
    most_common = max(counts, key=counts.get)
    print(f"Most Common: {most_common}")


if __name__ == "__main__":
    main()
''',
        "test_cases": [
            {
                "stdin": "6\nINFO: start\nERROR: fail\nINFO: ok\nWARNING: low disk\nERROR: crash\nINFO: done\n",
                "expect": "INFO: 3\nWARNING: 1\nERROR: 2\nMost Common: INFO",
            },
            {
                "stdin": "3\nERROR: a\nERROR: b\nERROR: c\n",
                "expect": "INFO: 0\nWARNING: 0\nERROR: 3\nMost Common: ERROR",
            },
        ],
        "hints": ["`line.split(':')[0]` pulls the level off the front of each log line."],
    },
    {
        "id": "validate_signup",
        "title": "Signup Form Validator",
        "category": "Input validation focus",
        "difficulty": "Easy",
        "time_limit_min": 20,
        "prompt": """Build a signup prompt that never crashes on bad input.

Ask "Enter age: " (no trailing newline required) and re-ask until the input
is a whole number between 1 and 120 inclusive:
  - not a whole number -> print exactly: Invalid input. Enter a whole number.
  - out of range        -> print exactly: Age must be between 1 and 120.

Then ask "Enter email: " and re-ask until the value contains "@" and a "."
after the "@":
  - invalid -> print exactly: Please enter a valid email address.

Once both are valid, print exactly: Registration complete for age X.
(where X is the validated age, as an integer, no leading zeros)""",
        "starter_code": '''def main():
    age = None
    while age is None:
        raw = input("Enter age: ")
        # TODO: validate raw, set age when valid

    email = None
    while email is None:
        raw = input("Enter email: ")
        # TODO: validate raw, set email when valid

    print(f"Registration complete for age {age}.")


if __name__ == "__main__":
    main()
''',
        "reference_solution": '''def main():
    age = None
    while age is None:
        raw = input("Enter age: ")
        if not raw.lstrip("-").isdigit():
            print("Invalid input. Enter a whole number.")
            continue
        value = int(raw)
        if value < 1 or value > 120:
            print("Age must be between 1 and 120.")
            continue
        age = value

    email = None
    while email is None:
        raw = input("Enter email: ")
        if "@" not in raw or "." not in raw.split("@")[-1]:
            print("Please enter a valid email address.")
            continue
        email = raw

    print(f"Registration complete for age {age}.")


if __name__ == "__main__":
    main()
''',
        "test_cases": [
            {
                "stdin": "abc\n-5\n200\n30\nnotanemail\nuser@site\nuser@site.com\n",
                "expect": "Invalid input. Enter a whole number.",
            },
            {
                "stdin": "abc\n-5\n200\n30\nnotanemail\nuser@site\nuser@site.com\n",
                "expect": "Age must be between 1 and 120.",
            },
            {
                "stdin": "abc\n-5\n200\n30\nnotanemail\nuser@site\nuser@site.com\n",
                "expect": "Please enter a valid email address.",
            },
            {
                "stdin": "abc\n-5\n200\n30\nnotanemail\nuser@site\nuser@site.com\n",
                "expect": "Registration complete for age 30.",
            },
        ],
        "hints": ["`str.isdigit()` rejects a leading '-', so strip it before checking."],
    },
    {
        "id": "validate_division",
        "title": "Safe Divider",
        "category": "Input validation focus",
        "difficulty": "Easy",
        "time_limit_min": 15,
        "prompt": """Ask "Enter numerator: " and "Enter denominator: " and keep re-asking
BOTH values as a pair until the division succeeds:

  - denominator is not a valid number -> print exactly: Invalid number, try again.
  - denominator is a valid number but equals 0 -> print exactly:
    Cannot divide by zero, try again.

Once you get a valid, non-zero denominator, print exactly: Result: X
(the numerator divided by the denominator, using normal Python float
division/formatting), then stop.""",
        "starter_code": '''def main():
    while True:
        num = input("Enter numerator: ")
        den = input("Enter denominator: ")
        # TODO: validate den, retry the pair on failure, else compute and break
        break


if __name__ == "__main__":
    main()
''',
        "reference_solution": '''def main():
    while True:
        num = input("Enter numerator: ")
        den = input("Enter denominator: ")
        try:
            num_v = float(num)
            den_v = float(den)
        except ValueError:
            print("Invalid number, try again.")
            continue
        if den_v == 0:
            print("Cannot divide by zero, try again.")
            continue
        print(f"Result: {num_v / den_v}")
        break


if __name__ == "__main__":
    main()
''',
        "test_cases": [
            {"stdin": "10\n0\n10\nabc\n10\n2\n", "expect": "Cannot divide by zero, try again."},
            {"stdin": "10\n0\n10\nabc\n10\n2\n", "expect": "Invalid number, try again."},
            {"stdin": "10\n0\n10\nabc\n10\n2\n", "expect": "Result: 5.0"},
        ],
        "hints": ["Validate the denominator with try/except float(), not .isdigit() (it must accept decimals)."],
    },
    {
        "id": "oop_bank",
        "title": "Bank Account Class",
        "category": "OOP / class-based model",
        "difficulty": "Medium",
        "time_limit_min": 30,
        "prompt": """Define a BankAccount class with an owner and a balance (starts at 0),
plus methods deposit(amount) and withdraw(amount). withdraw() must refuse
to overdraw: if the amount exceeds the balance, print exactly:
Insufficient funds. and leave the balance unchanged.

Then build this console program around it:
  Read the owner's name with input() (no prompt text required).
  Loop printing this menu:
    1. Deposit
    2. Withdraw
    3. Check Balance
    4. Quit
  - Deposit: prompt "Amount: ", add it.
  - Withdraw: prompt "Amount: ", subtract it (or refuse per above).
  - Check Balance: print exactly: Balance: $X.XX
  - Quit: print exactly: Goodbye! and stop.""",
        "starter_code": '''class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        pass  # TODO

    def withdraw(self, amount):
        pass  # TODO


def main():
    owner = input()
    account = BankAccount(owner)
    while True:
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Check Balance")
        print("4. Quit")
        choice = input()
        # TODO: dispatch on choice
        if choice == "4":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
''',
        "reference_solution": '''class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds.")
        else:
            self.balance -= amount


def main():
    owner = input()
    account = BankAccount(owner)
    while True:
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Check Balance")
        print("4. Quit")
        choice = input()
        if choice == "1":
            account.deposit(float(input("Amount: ")))
        elif choice == "2":
            account.withdraw(float(input("Amount: ")))
        elif choice == "3":
            print(f"Balance: ${account.balance:.2f}")
        elif choice == "4":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
''',
        "test_cases": [
            {"stdin": "Alice\n1\n100\n2\n30\n3\n4\n", "expect": "Balance: $70.00"},
            {"stdin": "Alice\n2\n500\n4\n", "expect": "Insufficient funds."},
        ],
        "hints": ["Keep the validation logic inside withdraw(), not in main() -- that's the point of the class."],
    },
    {
        "id": "oop_shapes",
        "title": "Shape Hierarchy",
        "category": "OOP / class-based model",
        "difficulty": "Medium",
        "time_limit_min": 30,
        "prompt": """Build a small class hierarchy: a base Shape class and Rectangle,
Circle, and Triangle subclasses, each implementing area().
  Rectangle(width, height): area = width * height
  Circle(radius): area = pi * radius^2  (use math.pi)
  Triangle(base, height): area = 0.5 * base * height

Program:
  Read an integer N, then N lines of "TYPE,dim1[,dim2]", e.g.
  "Rectangle,4,5", "Circle,3", "Triangle,6,2".
  For each, print exactly: Area: X.XX (2 decimal places).""",
        "starter_code": '''import math


class Shape:
    def area(self):
        raise NotImplementedError


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        pass  # TODO


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        pass  # TODO


class Triangle(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height

    def area(self):
        pass  # TODO


def main():
    n = int(input())
    for _ in range(n):
        parts = input().split(",")
        kind = parts[0]
        nums = [float(p) for p in parts[1:]]
        # TODO: build the right shape and print its area


if __name__ == "__main__":
    main()
''',
        "reference_solution": '''import math


class Shape:
    def area(self):
        raise NotImplementedError


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2


class Triangle(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height

    def area(self):
        return 0.5 * self.base * self.height


def main():
    n = int(input())
    for _ in range(n):
        parts = input().split(",")
        kind = parts[0]
        nums = [float(p) for p in parts[1:]]
        if kind == "Rectangle":
            shape = Rectangle(*nums)
        elif kind == "Circle":
            shape = Circle(*nums)
        else:
            shape = Triangle(*nums)
        print(f"Area: {shape.area():.2f}")


if __name__ == "__main__":
    main()
''',
        "test_cases": [
            {"stdin": "3\nRectangle,4,5\nCircle,3\nTriangle,6,2\n", "expect": "Area: 20.00"},
            {"stdin": "3\nRectangle,4,5\nCircle,3\nTriangle,6,2\n", "expect": "Area: 28.27"},
            {"stdin": "3\nRectangle,4,5\nCircle,3\nTriangle,6,2\n", "expect": "Area: 6.00"},
        ],
        "hints": ["`Rectangle(*nums)` unpacks the parsed dimensions straight into the constructor."],
    },
    {
        "id": "search_binary",
        "title": "Binary Search",
        "category": "Search & sort algorithm",
        "difficulty": "Medium",
        "time_limit_min": 20,
        "prompt": """Implement binary search (not a linear scan -- it should stay O(log n)).

Input:
  Line 1: an integer N
  Line 2: N integers, already sorted ascending, space separated
  Line 3: a target integer

If found, print exactly: Found at index X (0-based index).
Otherwise print exactly: Not found""",
        "starter_code": '''def binary_search(values, target):
    lo, hi = 0, len(values) - 1
    # TODO: implement, return the index or -1
    return -1


def main():
    n = int(input())
    values = [int(x) for x in input().split()]
    target = int(input())
    idx = binary_search(values, target)
    if idx == -1:
        print("Not found")
    else:
        print(f"Found at index {idx}")


if __name__ == "__main__":
    main()
''',
        "reference_solution": '''def binary_search(values, target):
    lo, hi = 0, len(values) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if values[mid] == target:
            return mid
        if values[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def main():
    n = int(input())
    values = [int(x) for x in input().split()]
    target = int(input())
    idx = binary_search(values, target)
    if idx == -1:
        print("Not found")
    else:
        print(f"Found at index {idx}")


if __name__ == "__main__":
    main()
''',
        "test_cases": [
            {"stdin": "5\n1 3 5 7 9\n7\n", "expect": "Found at index 3"},
            {"stdin": "5\n1 3 5 7 9\n4\n", "expect": "Not found"},
            {"stdin": "5\n1 3 5 7 9\n1\n", "expect": "Found at index 0"},
        ],
        "hints": ["Track lo/hi indices and compare against the midpoint each time."],
    },
    {
        "id": "sort_selection",
        "title": "Selection Sort",
        "category": "Search & sort algorithm",
        "difficulty": "Easy",
        "time_limit_min": 20,
        "prompt": """Implement selection sort yourself (don't call sorted()/.sort()).

Input:
  Line 1: an integer N
  Line 2: N integers, space separated

Print exactly one line: Sorted: v1 v2 v3 ... (ascending, space separated).""",
        "starter_code": '''def selection_sort(values):
    # TODO: sort `values` in place using selection sort
    return values


def main():
    n = int(input())
    values = [int(x) for x in input().split()]
    result = selection_sort(values)
    print("Sorted: " + " ".join(str(v) for v in result))


if __name__ == "__main__":
    main()
''',
        "reference_solution": '''def selection_sort(values):
    for i in range(len(values)):
        min_idx = i
        for j in range(i + 1, len(values)):
            if values[j] < values[min_idx]:
                min_idx = j
        values[i], values[min_idx] = values[min_idx], values[i]
    return values


def main():
    n = int(input())
    values = [int(x) for x in input().split()]
    result = selection_sort(values)
    print("Sorted: " + " ".join(str(v) for v in result))


if __name__ == "__main__":
    main()
''',
        "test_cases": [
            {"stdin": "6\n5 3 8 1 9 2\n", "expect": "Sorted: 1 2 3 5 8 9"},
            {"stdin": "1\n7\n", "expect": "Sorted: 7"},
        ],
        "hints": ["Each pass: find the minimum of the unsorted remainder, swap it to the front."],
    },
    {
        "id": "string_palindrome",
        "title": "Palindrome & Anagram Checker",
        "category": "String manipulation",
        "difficulty": "Easy",
        "time_limit_min": 15,
        "prompt": """Read two lines of text, word1 then word2.

Ignoring case and spaces:
  Print exactly: Palindrome: Yes   or   Palindrome: No
  (whether word1 reads the same forwards and backwards)

  Print exactly: Anagram: Yes   or   Anagram: No
  (whether word1 and word2 use exactly the same letters, same counts)""",
        "starter_code": '''def normalize(s):
    return s.replace(" ", "").lower()


def main():
    word1 = input()
    word2 = input()
    n1 = normalize(word1)
    n2 = normalize(word2)
    # TODO: check palindrome and anagram, print results


if __name__ == "__main__":
    main()
''',
        "reference_solution": '''def normalize(s):
    return s.replace(" ", "").lower()


def main():
    word1 = input()
    word2 = input()
    n1 = normalize(word1)
    n2 = normalize(word2)

    is_pal = n1 == n1[::-1]
    print(f"Palindrome: {'Yes' if is_pal else 'No'}")

    is_ana = sorted(n1) == sorted(n2)
    print(f"Anagram: {'Yes' if is_ana else 'No'}")


if __name__ == "__main__":
    main()
''',
        "test_cases": [
            {"stdin": "Race Car\nListen\n", "expect": "Palindrome: Yes"},
            {"stdin": "Race Car\nListen\n", "expect": "Anagram: No"},
            {"stdin": "listen\nsilent\n", "expect": "Palindrome: No"},
            {"stdin": "listen\nsilent\n", "expect": "Anagram: Yes"},
        ],
        "hints": ["`s[::-1]` reverses a string; `sorted(s)` gives a comparable letter fingerprint."],
    },
    {
        "id": "string_caesar",
        "title": "Caesar Cipher",
        "category": "String manipulation",
        "difficulty": "Medium",
        "time_limit_min": 25,
        "prompt": """Read a line of text, then an integer shift on the next line.

Shift every letter forward by `shift` positions in the alphabet (wrapping
z -> a), preserving uppercase/lowercase. Leave non-letters (spaces,
punctuation) unchanged.

Print exactly: Encrypted: <result>""",
        "starter_code": '''def caesar(text, shift):
    result = []
    for ch in text:
        # TODO: shift letters, leave everything else alone
        result.append(ch)
    return "".join(result)


def main():
    text = input()
    shift = int(input())
    print(f"Encrypted: {caesar(text, shift)}")


if __name__ == "__main__":
    main()
''',
        "reference_solution": '''def caesar(text, shift):
    result = []
    for ch in text:
        if ch.isupper():
            result.append(chr((ord(ch) - ord("A") + shift) % 26 + ord("A")))
        elif ch.islower():
            result.append(chr((ord(ch) - ord("a") + shift) % 26 + ord("a")))
        else:
            result.append(ch)
    return "".join(result)


def main():
    text = input()
    shift = int(input())
    print(f"Encrypted: {caesar(text, shift)}")


if __name__ == "__main__":
    main()
''',
        "test_cases": [
            {"stdin": "Hello, World!\n3\n", "expect": "Encrypted: Khoor, Zruog!"},
            {"stdin": "abcXYZ\n2\n", "expect": "Encrypted: cdeZAB"},
        ],
        "hints": ["`(ord(ch) - ord('a') + shift) % 26 + ord('a')` handles the wraparound in one line."],
    },
    {
        "id": "recursion_fib_fact",
        "title": "Recursive Factorial & Fibonacci",
        "category": "Recursion",
        "difficulty": "Easy",
        "time_limit_min": 20,
        "prompt": """Read an integer n. Using RECURSIVE functions (no loops for the math
itself), compute and print:
  Factorial: X   (n!, with 0! = 1)
  Fibonacci: X   (nth Fibonacci number, 0-indexed: fib(0)=0, fib(1)=1)""",
        "starter_code": '''def factorial(n):
    # TODO: recursive base case + recursive call
    pass


def fibonacci(n):
    # TODO: recursive base case + recursive call
    pass


def main():
    n = int(input())
    print(f"Factorial: {factorial(n)}")
    print(f"Fibonacci: {fibonacci(n)}")


if __name__ == "__main__":
    main()
''',
        "reference_solution": '''def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)


def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def main():
    n = int(input())
    print(f"Factorial: {factorial(n)}")
    print(f"Fibonacci: {fibonacci(n)}")


if __name__ == "__main__":
    main()
''',
        "test_cases": [
            {"stdin": "6\n", "expect": "Factorial: 720"},
            {"stdin": "6\n", "expect": "Fibonacci: 8"},
            {"stdin": "0\n", "expect": "Factorial: 1"},
        ],
        "hints": ["Every recursive function needs a base case that returns without recursing."],
    },
    {
        "id": "recursion_nested_sum",
        "title": "Recursive Nested List Sum",
        "category": "Recursion",
        "difficulty": "Medium",
        "time_limit_min": 25,
        "prompt": """Read one line containing a Python-style nested list literal, e.g.
[1, [2, 3], [4, [5, 6]]]

Parse it with ast.literal_eval, then use a RECURSIVE function to sum every
integer at any depth. Print exactly: Sum: X""",
        "starter_code": '''import ast


def nested_sum(data):
    total = 0
    # TODO: if data is a list, recurse into each item; otherwise add it
    return total


def main():
    data = ast.literal_eval(input())
    print(f"Sum: {nested_sum(data)}")


if __name__ == "__main__":
    main()
''',
        "reference_solution": '''import ast


def nested_sum(data):
    if isinstance(data, list):
        return sum(nested_sum(item) for item in data)
    return data


def main():
    data = ast.literal_eval(input())
    print(f"Sum: {nested_sum(data)}")


if __name__ == "__main__":
    main()
''',
        "test_cases": [
            {"stdin": "[1, [2, 3], [4, [5, 6]]]\n", "expect": "Sum: 21"},
            {"stdin": "[10, 20, 30]\n", "expect": "Sum: 60"},
        ],
        "hints": ["`isinstance(data, list)` tells you whether to recurse or add."],
    },
    {
        "id": "mock_grades_system",
        "title": "Student Grade Management System",
        "category": "Full mock project (3-part)",
        "difficulty": "Hard",
        "time_limit_min": 45,
        "prompt": """A 3-part mock project: data entry, computation, and reporting, all in
one program.

Menu (print exactly, every loop):
1. Add Student
2. View Report
3. Quit

- Add Student: prompt "Name: ", then "Score 1: ", "Score 2: ", "Score 3: "
  (each an integer). Store the student and their three scores.
- View Report: for each student, in the order added, print:
    Name: avg (Letter)
  where avg is the mean of their 3 scores to 2 decimal places, and Letter
  uses the standard scale (90+ A, 80-89 B, 70-79 C, 60-69 D, below 60 F).
  After listing every student, print:
    Class Average: XX.XX   (mean of all students' averages, 2 decimals)
    Top Student: Name      (highest average; assume no ties in test data)
    Lowest Student: Name   (lowest average; assume no ties in test data)
- Quit: print exactly: Goodbye! and stop.""",
        "starter_code": '''def letter_grade(avg):
    # TODO
    pass


def main():
    students = []  # list of (name, avg)
    while True:
        print("1. Add Student")
        print("2. View Report")
        print("3. Quit")
        choice = input()

        if choice == "1":
            name = input("Name: ")
            s1 = int(input("Score 1: "))
            s2 = int(input("Score 2: "))
            s3 = int(input("Score 3: "))
            avg = (s1 + s2 + s3) / 3
            students.append((name, avg))
        elif choice == "2":
            pass  # TODO: print each student, then class stats
        elif choice == "3":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
''',
        "reference_solution": '''def letter_grade(avg):
    if avg >= 90:
        return "A"
    if avg >= 80:
        return "B"
    if avg >= 70:
        return "C"
    if avg >= 60:
        return "D"
    return "F"


def main():
    students = []
    while True:
        print("1. Add Student")
        print("2. View Report")
        print("3. Quit")
        choice = input()

        if choice == "1":
            name = input("Name: ")
            s1 = int(input("Score 1: "))
            s2 = int(input("Score 2: "))
            s3 = int(input("Score 3: "))
            avg = (s1 + s2 + s3) / 3
            students.append((name, avg))
        elif choice == "2":
            for name, avg in students:
                print(f"{name}: {avg:.2f} ({letter_grade(avg)})")
            class_avg = sum(a for _, a in students) / len(students)
            print(f"Class Average: {class_avg:.2f}")
            top = max(students, key=lambda s: s[1])
            low = min(students, key=lambda s: s[1])
            print(f"Top Student: {top[0]}")
            print(f"Lowest Student: {low[0]}")
        elif choice == "3":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
''',
        "test_cases": [
            {
                "stdin": "1\nAlice\n90\n85\n95\n1\nBob\n60\n65\n70\n2\n3\n",
                "expect": "Alice: 90.00 (A)",
            },
            {
                "stdin": "1\nAlice\n90\n85\n95\n1\nBob\n60\n65\n70\n2\n3\n",
                "expect": "Bob: 65.00 (D)",
            },
            {
                "stdin": "1\nAlice\n90\n85\n95\n1\nBob\n60\n65\n70\n2\n3\n",
                "expect": "Class Average: 77.50",
            },
            {
                "stdin": "1\nAlice\n90\n85\n95\n1\nBob\n60\n65\n70\n2\n3\n",
                "expect": "Top Student: Alice",
            },
            {
                "stdin": "1\nAlice\n90\n85\n95\n1\nBob\n60\n65\n70\n2\n3\n",
                "expect": "Lowest Student: Bob",
            },
        ],
        "hints": ["Store (name, avg) tuples so max()/min() with key= can find the top/bottom directly."],
    },
    {
        "id": "mock_ticket_booking",
        "title": "Movie Ticket Booking System",
        "category": "Full mock project (3-part)",
        "difficulty": "Hard",
        "time_limit_min": 45,
        "prompt": """A theater has 10 seats, numbered 1-10, all free at start.

Menu (print exactly, every loop):
1. View Available Seats
2. Book Seat
3. Cancel Booking
4. Quit

- View: print exactly: Available: n1 n2 n3 ... (free seat numbers, space
  separated, ascending). If none are free, print exactly: No seats available.
- Book: prompt "Seat number: ".
    out of range (not 1-10)        -> print exactly: Invalid seat number.
    already booked                 -> print exactly: Seat X is already booked.
    otherwise                      -> book it, print exactly: Seat X booked.
- Cancel: prompt "Seat number: ".
    not currently booked           -> print exactly: Seat X was not booked.
    otherwise                      -> free it, print exactly: Seat X canceled.
- Quit: print exactly: Goodbye! and stop.""",
        "starter_code": '''def main():
    booked = set()
    while True:
        print("1. View Available Seats")
        print("2. Book Seat")
        print("3. Cancel Booking")
        print("4. Quit")
        choice = input()
        # TODO: implement each branch
        if choice == "4":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
''',
        "reference_solution": '''def main():
    booked = set()
    while True:
        print("1. View Available Seats")
        print("2. Book Seat")
        print("3. Cancel Booking")
        print("4. Quit")
        choice = input()

        if choice == "1":
            free = [s for s in range(1, 11) if s not in booked]
            if free:
                print("Available: " + " ".join(str(s) for s in free))
            else:
                print("No seats available.")
        elif choice == "2":
            seat = int(input("Seat number: "))
            if seat < 1 or seat > 10:
                print("Invalid seat number.")
            elif seat in booked:
                print(f"Seat {seat} is already booked.")
            else:
                booked.add(seat)
                print(f"Seat {seat} booked.")
        elif choice == "3":
            seat = int(input("Seat number: "))
            if seat in booked:
                booked.discard(seat)
                print(f"Seat {seat} canceled.")
            else:
                print(f"Seat {seat} was not booked.")
        elif choice == "4":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
''',
        "test_cases": [
            {
                "stdin": "1\n2\n3\n3\n3\n4\n",
                "expect": "Available: 1 2 3 4 5 6 7 8 9 10",
            },
            {
                "stdin": "1\n2\n3\n3\n3\n4\n",
                "expect": "Seat 3 booked.",
            },
            {
                "stdin": "1\n2\n3\n3\n3\n4\n",
                "expect": "Seat 3 canceled.",
            },
            {
                "stdin": "2\n99\n4\n",
                "expect": "Invalid seat number.",
            },
        ],
        "hints": ["A `set()` of booked seat numbers keeps booking/canceling/checking all O(1)."],
    },
    {
        "id": "speed_fizzbuzz",
        "title": "FizzBuzz Plus",
        "category": "Speed drill (30 min)",
        "difficulty": "Easy",
        "time_limit_min": 15,
        "prompt": """Read an integer n. Print the numbers 1..n, one per line, except:
  multiple of 3       -> print Fizz
  multiple of 5       -> print Buzz
  multiple of 3 and 5 -> print FizzBuzz
  multiple of 7       -> append Bang to whatever you'd already print
                          (so 7 alone -> Bang, 21 -> FizzBang, 35 -> BuzzBang,
                          105 -> FizzBuzzBang)
  none of the above    -> print the number itself""",
        "starter_code": '''def main():
    n = int(input())
    for i in range(1, n + 1):
        out = ""
        # TODO: build up out with the Fizz (3) / Buzz (5) / Bang (7) checks,
        # then fall back to the number itself if out is still empty
        print(out if out else i)


if __name__ == "__main__":
    main()
''',
        "reference_solution": '''def main():
    n = int(input())
    for i in range(1, n + 1):
        out = ""
        if i % 3 == 0:
            out += "Fizz"
        if i % 5 == 0:
            out += "Buzz"
        if i % 7 == 0:
            out += "Bang"
        print(out if out else i)


if __name__ == "__main__":
    main()
''',
        "test_cases": [
            {
                "stdin": "15\n",
                "expect": "1\n2\nFizz\n4\nBuzz\nFizz\nBang\n8\nFizz\nBuzz\n11\nFizz\n13\nBang\nFizzBuzz",
            },
            {
                "stdin": "35\n",
                "expect": "FizzBang",
            },
            {
                "stdin": "35\n",
                "expect": "BuzzBang",
            },
        ],
        "hints": ["Build up a string with the Fizz/Buzz/Bang checks, then fall back to the number if it's still empty."],
    },
    {
        "id": "speed_temp_convert",
        "title": "Temperature Converter Suite",
        "category": "Speed drill (30 min)",
        "difficulty": "Easy",
        "time_limit_min": 15,
        "prompt": """Read an integer N, then N pairs of lines: a numeric value, then a unit
letter ('C', 'F', or 'K').

For each, convert to all three scales and print exactly:
  C: a.aa  F: b.bb  K: c.cc
(each value to 2 decimal places, two spaces between fields)

Conversions: F = C * 9/5 + 32, K = C + 273.15 (convert everything via
Celsius as the common unit).""",
        "starter_code": '''def to_celsius(value, unit):
    # TODO: convert value (given in `unit`, which is "C", "F", or "K") to Celsius
    pass


def main():
    n = int(input())
    for _ in range(n):
        value = float(input())
        unit = input().strip()
        c = to_celsius(value, unit)
        # TODO: derive f and k from c, then print all three
        f = c
        k = c
        print(f"C: {c:.2f}  F: {f:.2f}  K: {k:.2f}")


if __name__ == "__main__":
    main()
''',
        "reference_solution": '''def to_celsius(value, unit):
    if unit == "C":
        return value
    if unit == "F":
        return (value - 32) * 5 / 9
    return value - 273.15  # K


def main():
    n = int(input())
    for _ in range(n):
        value = float(input())
        unit = input().strip()
        c = to_celsius(value, unit)
        f = c * 9 / 5 + 32
        k = c + 273.15
        print(f"C: {c:.2f}  F: {f:.2f}  K: {k:.2f}")


if __name__ == "__main__":
    main()
''',
        "test_cases": [
            {"stdin": "2\n0\nC\n100\nC\n", "expect": "C: 0.00  F: 32.00  K: 273.15"},
            {"stdin": "2\n0\nC\n100\nC\n", "expect": "C: 100.00  F: 212.00  K: 373.15"},
            {"stdin": "1\n32\nF\n", "expect": "C: 0.00  F: 32.00  K: 273.15"},
            {"stdin": "1\n273.15\nK\n", "expect": "C: 0.00  F: 32.00  K: 273.15"},
        ],
        "hints": ["Convert the input to Celsius first, then derive F and K from that single value."],
    },

    # The five problems below are modeled directly on real national SkillsUSA
    # Computer Programming contest packets (2014 Kansas City nationals; 2021
    # virtual nationals) -- rate-table lookups, mandatory rounding rules,
    # variable-length input, and running totals across a session are all
    # patterns that show up repeatedly in the actual contest.
    {
        "id": "menu_currency",
        "title": "Currency Converter",
        "category": "Menu-driven console app",
        "difficulty": "Medium",
        "time_limit_min": 25,
        "prompt": """Build a currency converter using this fixed rate table (units per 1 USD):
  British pound (GBP): 0.64
  Euro (EUR): 0.91
  Japanese yen (JPY): 149.50
  Canadian dollar (CAD): 1.36

Print this exact menu every loop:

1. Calculate
2. Clear
3. Exit

- Calculate: prompt "USD amount: ", then print each conversion on its own
  line, in this exact order and format (2 decimal places):
    GBP: X.XX
    EUR: X.XX
    JPY: X.XX
    CAD: X.XX
- Clear: print exactly: Cleared. (no calculation needed -- it just
  acknowledges and returns to the menu, ready for a new amount)
- Exit: print exactly: Goodbye! and stop.""",
        "starter_code": '''RATES = {"GBP": 0.64, "EUR": 0.91, "JPY": 149.50, "CAD": 1.36}


def main():
    while True:
        print("1. Calculate")
        print("2. Clear")
        print("3. Exit")
        choice = input()

        if choice == "1":
            usd = float(input("USD amount: "))
            # TODO: print each converted amount
        elif choice == "2":
            print("Cleared.")
        elif choice == "3":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
''',
        "reference_solution": '''RATES = {"GBP": 0.64, "EUR": 0.91, "JPY": 149.50, "CAD": 1.36}


def main():
    while True:
        print("1. Calculate")
        print("2. Clear")
        print("3. Exit")
        choice = input()

        if choice == "1":
            usd = float(input("USD amount: "))
            for code in ("GBP", "EUR", "JPY", "CAD"):
                print(f"{code}: {usd * RATES[code]:.2f}")
        elif choice == "2":
            print("Cleared.")
        elif choice == "3":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
''',
        "test_cases": [
            {
                "stdin": "1\n100\n3\n",
                "expect": "GBP: 64.00\nEUR: 91.00\nJPY: 14950.00\nCAD: 136.00",
            },
            {"stdin": "2\n3\n", "expect": "Cleared."},
        ],
        "hints": ["Store the rate table as a dict so Calculate is just one loop over it."],
    },
    {
        "id": "validate_payroll",
        "title": "Payroll Calculator",
        "category": "Input validation focus",
        "difficulty": "Medium",
        "time_limit_min": 30,
        "prompt": """Write a payroll calculator. Prompt "Pay rate code (1-5): " and keep
re-asking until a valid code is entered:
  invalid (not 1-5)  -> print exactly: Invalid code. Enter 1-5.

Pay rate table:
  1 = $10.00/hr   2 = $12.50/hr   3 = $15.00/hr
  4 = $17.50/hr   5 = $20.00/hr

Then prompt "Hours worked: " and keep re-asking until a valid, non-negative
number is entered:
  invalid (not a number, or negative) -> print exactly: Invalid hours.

Overtime is anything over 40 hours, paid at time-and-a-half. Tax is 10% of
gross pay (before tax/insurance are subtracted). Insurance is 5% of gross
pay. Gross pay = (up to 40 regular hours * rate) + (overtime hours * rate
* 1.5).

Print, in this exact order, each formatted to 2 decimal places:
  Gross Pay: $X.XX
  Tax: $X.XX
  Insurance: $X.XX
  Take Home Pay: $X.XX
(Take Home Pay = Gross Pay - Tax - Insurance)""",
        "starter_code": '''RATES = {1: 10.00, 2: 12.50, 3: 15.00, 4: 17.50, 5: 20.00}


def main():
    code = None
    while code is None:
        raw = input("Pay rate code (1-5): ")
        # TODO: validate raw is one of "1".."5", set code

    hours = None
    while hours is None:
        raw = input("Hours worked: ")
        # TODO: validate raw is a non-negative number, set hours

    rate = RATES[code]
    # TODO: compute gross pay (with overtime), tax, insurance, take-home pay
    # and print all four lines


if __name__ == "__main__":
    main()
''',
        "reference_solution": '''RATES = {1: 10.00, 2: 12.50, 3: 15.00, 4: 17.50, 5: 20.00}


def main():
    code = None
    while code is None:
        raw = input("Pay rate code (1-5): ")
        if raw not in ("1", "2", "3", "4", "5"):
            print("Invalid code. Enter 1-5.")
            continue
        code = int(raw)

    hours = None
    while hours is None:
        raw = input("Hours worked: ")
        try:
            value = float(raw)
        except ValueError:
            print("Invalid hours.")
            continue
        if value < 0:
            print("Invalid hours.")
            continue
        hours = value

    rate = RATES[code]
    regular = min(hours, 40)
    overtime = max(hours - 40, 0)
    gross = regular * rate + overtime * rate * 1.5
    tax = gross * 0.10
    insurance = gross * 0.05
    take_home = gross - tax - insurance

    print(f"Gross Pay: ${gross:.2f}")
    print(f"Tax: ${tax:.2f}")
    print(f"Insurance: ${insurance:.2f}")
    print(f"Take Home Pay: ${take_home:.2f}")


if __name__ == "__main__":
    main()
''',
        "test_cases": [
            {
                "stdin": "1\n40\n",
                "expect": "Gross Pay: $400.00\nTax: $40.00\nInsurance: $20.00\nTake Home Pay: $340.00",
            },
            {
                "stdin": "9\n3\n45\n",
                "expect": "Invalid code. Enter 1-5.",
            },
            {
                "stdin": "3\nabc\n-5\n45\n",
                "expect": "Invalid hours.",
            },
            {
                "stdin": "3\nabc\n-5\n45\n",
                "expect": "Gross Pay: $712.50",
            },
        ],
        "hints": ["Overtime hours = max(hours - 40, 0); regular hours = min(hours, 40)."],
    },
    {
        "id": "speed_calorie",
        "title": "Calorie Calculator",
        "category": "Speed drill (30 min)",
        "difficulty": "Easy",
        "time_limit_min": 20,
        "prompt": """A person burns 398 calories/hour jogging and 557 calories/hour running.

Food calorie chart:
  Big Mac: 563
  Medium Fries: 378
  Small Shake: 530

Read three integers on three separate lines: number of Big Macs, number of
Medium Fries, and number of Small Shakes consumed.

Print exactly: Total Calories: X

Then print, each rounded to the nearest hundredth (2 decimal places):
  Hours to Jog: X.XX
  Hours to Run: X.XX""",
        "starter_code": '''def main():
    big_macs = int(input())
    fries = int(input())
    shakes = int(input())

    # TODO: compute total calories, then hours to burn it off jogging/running


if __name__ == "__main__":
    main()
''',
        "reference_solution": '''def main():
    big_macs = int(input())
    fries = int(input())
    shakes = int(input())

    total = big_macs * 563 + fries * 378 + shakes * 530
    print(f"Total Calories: {total}")
    print(f"Hours to Jog: {total / 398:.2f}")
    print(f"Hours to Run: {total / 557:.2f}")


if __name__ == "__main__":
    main()
''',
        "test_cases": [
            {"stdin": "1\n1\n1\n", "expect": "Total Calories: 1471"},
            {"stdin": "1\n1\n1\n", "expect": "Hours to Jog: 3.70"},
            {"stdin": "1\n1\n1\n", "expect": "Hours to Run: 2.64"},
            {"stdin": "0\n0\n0\n", "expect": "Total Calories: 0"},
        ],
        "hints": ["This is pure arithmetic + formatting -- no loops or branches needed."],
    },
    {
        "id": "search_grade_positions",
        "title": "Grade Tracker with Test Positions",
        "category": "Search & sort algorithm",
        "difficulty": "Medium",
        "time_limit_min": 25,
        "prompt": """Read a student's name, then a class name, then an unlimited number of
test scores (one per line) until the input line is exactly "done"
(case-insensitive). There is always at least one score before "done".

After "done", print exactly:
  Name: <name>
  Class: <class name>
  Average: X (Letter)
  Highest: X (Test #N)
  Lowest: X (Test #N)

Average is the mean of all scores, rounded to the nearest whole number,
graded on the standard scale (90+ A, 80-89 B, 70-79 C, 60-69 D, below 60
F). Test numbers are 1-indexed in entry order (the first score entered is
Test #1). If there's a tie for highest or lowest, report whichever one was
entered first.""",
        "starter_code": '''def letter_grade(avg):
    # TODO
    pass


def main():
    name = input()
    class_name = input()
    scores = []
    while True:
        line = input()
        if line.strip().lower() == "done":
            break
        scores.append(int(line))

    # TODO: compute average (rounded), letter grade, and the position
    # (1-indexed) of the highest and lowest score, then print all 5 lines


if __name__ == "__main__":
    main()
''',
        "reference_solution": '''def letter_grade(avg):
    if avg >= 90:
        return "A"
    if avg >= 80:
        return "B"
    if avg >= 70:
        return "C"
    if avg >= 60:
        return "D"
    return "F"


def main():
    name = input()
    class_name = input()
    scores = []
    while True:
        line = input()
        if line.strip().lower() == "done":
            break
        scores.append(int(line))

    avg = round(sum(scores) / len(scores))
    high_idx = scores.index(max(scores))
    low_idx = scores.index(min(scores))

    print(f"Name: {name}")
    print(f"Class: {class_name}")
    print(f"Average: {avg} ({letter_grade(avg)})")
    print(f"Highest: {scores[high_idx]} (Test #{high_idx + 1})")
    print(f"Lowest: {scores[low_idx]} (Test #{low_idx + 1})")


if __name__ == "__main__":
    main()
''',
        "test_cases": [
            {
                "stdin": "Alice\nMath\n70\n95\n82\ndone\n",
                "expect": "Average: 82 (B)",
            },
            {
                "stdin": "Alice\nMath\n70\n95\n82\ndone\n",
                "expect": "Highest: 95 (Test #2)",
            },
            {
                "stdin": "Alice\nMath\n70\n95\n82\ndone\n",
                "expect": "Lowest: 70 (Test #1)",
            },
        ],
        "hints": ["`list.index(value)` finds the position of the first matching value -- exactly what you need for ties."],
    },
    {
        "id": "mock_concessions",
        "title": "Movie Concessions Stand",
        "category": "Full mock project (3-part)",
        "difficulty": "Hard",
        "time_limit_min": 45,
        "prompt": """Simulate a concessions stand for one shift.

Menu (print exactly, every loop):
1. Concessions
2. Checkout
3. Manager
4. Quit

Prices:
  Small Popcorn: $3.00   Medium Popcorn: $4.00   Large Popcorn: $5.00
  Soda: $2.00             Candy: $1.50

- Concessions: prompt for a quantity of each item, in this exact order and
  wording, storing them as the current order (overwriting any previous
  uncommitted order):
    "Small Popcorn qty: "
    "Medium Popcorn qty: "
    "Large Popcorn qty: "
    "Soda qty: "
    "Candy qty: "
- Checkout: print each item's line cost as "Name: $X.XX" for all 5 items
  (using the current order's quantities), then print exactly:
    Total: $X.XX
  Then prompt "Payment: ", read the amount tendered, and print exactly:
    Change: $X.XX
  Add this order's quantities and dollars into the running daily totals,
  then clear the current order back to zero for the next customer.
- Manager: prompt "Access Code: ". If it isn't exactly 7777, print exactly:
    Access denied.
  and return to the menu. If correct, print each item as "Name: N sold"
  for all 5 items (cumulative across every checkout so far this session),
  then print exactly:
    Total Gross Sales: $X.XX
- Quit: print exactly: Goodbye! and stop.""",
        "starter_code": '''PRICES = {
    "Small Popcorn": 3.00, "Medium Popcorn": 4.00, "Large Popcorn": 5.00,
    "Soda": 2.00, "Candy": 1.50,
}
ITEMS = list(PRICES.keys())


def main():
    order = {item: 0 for item in ITEMS}
    daily = {item: 0 for item in ITEMS}
    daily_gross = 0.0

    while True:
        print("1. Concessions")
        print("2. Checkout")
        print("3. Manager")
        print("4. Quit")
        choice = input()

        if choice == "1":
            pass  # TODO: prompt for each item's quantity into `order`
        elif choice == "2":
            pass  # TODO: print breakdown, total, take payment, print change,
                  # fold `order` into `daily`/`daily_gross`, reset `order`
        elif choice == "3":
            pass  # TODO: check access code, print daily report
        elif choice == "4":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
''',
        "reference_solution": '''PRICES = {
    "Small Popcorn": 3.00, "Medium Popcorn": 4.00, "Large Popcorn": 5.00,
    "Soda": 2.00, "Candy": 1.50,
}
ITEMS = list(PRICES.keys())


def main():
    order = {item: 0 for item in ITEMS}
    daily = {item: 0 for item in ITEMS}
    daily_gross = 0.0

    while True:
        print("1. Concessions")
        print("2. Checkout")
        print("3. Manager")
        print("4. Quit")
        choice = input()

        if choice == "1":
            for item in ITEMS:
                order[item] = int(input(f"{item} qty: "))
        elif choice == "2":
            total = 0.0
            for item in ITEMS:
                cost = order[item] * PRICES[item]
                total += cost
                print(f"{item}: ${cost:.2f}")
            print(f"Total: ${total:.2f}")
            payment = float(input("Payment: "))
            print(f"Change: ${payment - total:.2f}")
            for item in ITEMS:
                daily[item] += order[item]
            daily_gross += total
            order = {item: 0 for item in ITEMS}
        elif choice == "3":
            code = input("Access Code: ")
            if code != "7777":
                print("Access denied.")
            else:
                for item in ITEMS:
                    print(f"{item}: {daily[item]} sold")
                print(f"Total Gross Sales: ${daily_gross:.2f}")
        elif choice == "4":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
''',
        "test_cases": [
            {
                "stdin": "1\n2\n0\n0\n2\n1\n2\n20\n3\n7777\n4\n",
                "expect": "Total: $11.50",
            },
            {
                "stdin": "1\n2\n0\n0\n2\n1\n2\n20\n3\n7777\n4\n",
                "expect": "Change: $8.50",
            },
            {
                "stdin": "1\n2\n0\n0\n2\n1\n2\n20\n3\n7777\n4\n",
                "expect": "Small Popcorn: 2 sold",
            },
            {
                "stdin": "1\n2\n0\n0\n2\n1\n2\n20\n3\n7777\n4\n",
                "expect": "Total Gross Sales: $11.50",
            },
            {
                "stdin": "3\nwrong\n4\n",
                "expect": "Access denied.",
            },
        ],
        "hints": [
            "Keep two dicts: `order` (this customer, reset after checkout) and `daily` (cumulative, never reset).",
            "Fold `order` into `daily` BEFORE resetting `order` back to zero.",
        ],
    },
    {
        "id": "recursion_hanoi",
        "title": "Tower of Hanoi",
        "category": "Recursion",
        "difficulty": "Hard",
        "time_limit_min": 30,
        "prompt": """Read an integer N (number of disks). Solve the classic Tower of Hanoi puzzle:
move all N disks from peg A to peg C, using peg B as auxiliary, one disk at
a time, never placing a larger disk on a smaller one.

Print each move, one per line, in exactly this format:
  Move disk X from A to C
(X is the disk number; the two letters are whichever pegs that move uses)

After every move has been printed, print exactly:
  Total moves: <count>

Solve this recursively -- move N-1 disks out of the way, move the biggest
disk, then move the N-1 disks back on top of it.""",
        "starter_code": '''def hanoi(n, source, target, aux, moves):
    if n == 0:
        return
    # TODO: move the top n-1 disks from source to aux (using target as the
    # spare), record moving disk n from source to target, then move the
    # n-1 disks from aux to target (using source as the spare)


def main():
    n = int(input())
    moves = []
    hanoi(n, "A", "C", "B", moves)
    for m in moves:
        print(m)
    print(f"Total moves: {len(moves)}")


if __name__ == "__main__":
    main()
''',
        "reference_solution": '''def hanoi(n, source, target, aux, moves):
    if n == 0:
        return
    hanoi(n - 1, source, aux, target, moves)
    moves.append(f"Move disk {n} from {source} to {target}")
    hanoi(n - 1, aux, target, source, moves)


def main():
    n = int(input())
    moves = []
    hanoi(n, "A", "C", "B", moves)
    for m in moves:
        print(m)
    print(f"Total moves: {len(moves)}")


if __name__ == "__main__":
    main()
''',
        "test_cases": [
            {"stdin": "1\n", "expect": "Move disk 1 from A to C\nTotal moves: 1"},
            {"stdin": "2\n", "expect": "Move disk 1 from A to B\nMove disk 2 from A to C\nMove disk 1 from B to C\nTotal moves: 3"},
            {
                "stdin": "3\n",
                "expect": "Move disk 1 from A to C\nMove disk 2 from A to B\nMove disk 1 from C to B\n"
                          "Move disk 3 from A to C\nMove disk 1 from B to A\nMove disk 2 from B to C\n"
                          "Move disk 1 from A to C\nTotal moves: 7",
            },
            {"stdin": "4\n", "expect": "Total moves: 15"},
        ],
        "hints": [
            "To move n disks source->target: recursively move n-1 disks source->aux, move disk n source->target, then recursively move n-1 disks aux->target.",
            "Total moves for n disks is always 2^n - 1 -- a good sanity check on your output.",
        ],
    },
    {
        "id": "oop_payroll_hierarchy",
        "title": "Employee Payroll Hierarchy",
        "category": "OOP / class-based model",
        "difficulty": "Hard",
        "time_limit_min": 35,
        "prompt": """Model two kinds of employees with a shared base class, then run payroll.

Build an `Employee` base class and two subclasses:
  - HourlyEmployee(name, hours, rate): pay() = hours * rate
  - SalariedEmployee(name, annual_salary): pay() = annual_salary / 12

Input:
  Line 1: an integer N
  Next N lines, each one employee, comma-separated with no spaces:
    "H,<name>,<hours>,<rate>"        for an hourly employee
    "S,<name>,<annual_salary>"       for a salaried employee

For each employee (in input order) print:
  <name>: $<pay, 2 decimal places>
Then print the total of everyone's pay as:
  Total Payroll: $<total, 2 decimal places>""",
        "starter_code": '''class Employee:
    def __init__(self, name):
        self.name = name

    def pay(self):
        raise NotImplementedError


class HourlyEmployee(Employee):
    def __init__(self, name, hours, rate):
        super().__init__(name)
        self.hours = hours
        self.rate = rate

    def pay(self):
        # TODO: hours * rate
        pass


class SalariedEmployee(Employee):
    def __init__(self, name, annual_salary):
        super().__init__(name)
        self.annual_salary = annual_salary

    def pay(self):
        # TODO: annual_salary / 12
        pass


def main():
    n = int(input())
    employees = []
    for _ in range(n):
        parts = input().split(",")
        if parts[0] == "H":
            employees.append(HourlyEmployee(parts[1], float(parts[2]), float(parts[3])))
        else:
            employees.append(SalariedEmployee(parts[1], float(parts[2])))

    total = 0
    for e in employees:
        p = e.pay()
        total += p
        print(f"{e.name}: ${p:.2f}")
    print(f"Total Payroll: ${total:.2f}")


if __name__ == "__main__":
    main()
''',
        "reference_solution": '''class Employee:
    def __init__(self, name):
        self.name = name

    def pay(self):
        raise NotImplementedError


class HourlyEmployee(Employee):
    def __init__(self, name, hours, rate):
        super().__init__(name)
        self.hours = hours
        self.rate = rate

    def pay(self):
        return self.hours * self.rate


class SalariedEmployee(Employee):
    def __init__(self, name, annual_salary):
        super().__init__(name)
        self.annual_salary = annual_salary

    def pay(self):
        return self.annual_salary / 12


def main():
    n = int(input())
    employees = []
    for _ in range(n):
        parts = input().split(",")
        if parts[0] == "H":
            employees.append(HourlyEmployee(parts[1], float(parts[2]), float(parts[3])))
        else:
            employees.append(SalariedEmployee(parts[1], float(parts[2])))

    total = 0
    for e in employees:
        p = e.pay()
        total += p
        print(f"{e.name}: ${p:.2f}")
    print(f"Total Payroll: ${total:.2f}")


if __name__ == "__main__":
    main()
''',
        "test_cases": [
            {"stdin": "3\nH,Alice,40,15.50\nS,Bob,60000\nH,Carl,35,20\n", "expect": "Alice: $620.00"},
            {"stdin": "3\nH,Alice,40,15.50\nS,Bob,60000\nH,Carl,35,20\n", "expect": "Bob: $5000.00"},
            {"stdin": "3\nH,Alice,40,15.50\nS,Bob,60000\nH,Carl,35,20\n", "expect": "Total Payroll: $6320.00"},
            {"stdin": "1\nS,Solo,36000\n", "expect": "Solo: $3000.00"},
        ],
        "hints": [
            "`Employee` holds the shared `name`; each subclass's `__init__` calls `super().__init__(name)` then stores its own fields.",
            "Polymorphism does the work in the payroll loop: `e.pay()` calls the right subclass's version without an if/elif chain.",
        ],
    },
    {
        "id": "string_word_frequency",
        "title": "Word Frequency Counter",
        "category": "String manipulation",
        "difficulty": "Hard",
        "time_limit_min": 25,
        "prompt": """Read a block of text and report its 3 most frequent words.

Input:
  Line 1: an integer N
  Next N lines: text (words separated by whitespace)

Treat words case-insensitively and strip any leading/trailing punctuation
from each word before counting (so "fox." and "Fox" both count as "fox").
Ignore anything that strips down to nothing.

Print the top 3 most frequent words, one per line, as:
  <word>: <count>
Ordered by count descending; break ties alphabetically (ascending). If
there are fewer than 3 distinct words, print however many there are.""",
        "starter_code": '''import string


def main():
    n = int(input())
    counts = {}
    for _ in range(n):
        line = input()
        for raw in line.split():
            word = raw.strip(string.punctuation).lower()
            # TODO: if word isn't empty, increment counts[word]

    # TODO: sort counts by (-count, word) and print the top 3 as "word: count"


if __name__ == "__main__":
    main()
''',
        "reference_solution": '''import string


def main():
    n = int(input())
    counts = {}
    for _ in range(n):
        line = input()
        for raw in line.split():
            word = raw.strip(string.punctuation).lower()
            if word:
                counts[word] = counts.get(word, 0) + 1

    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    for word, count in ranked[:3]:
        print(f"{word}: {count}")


if __name__ == "__main__":
    main()
''',
        "test_cases": [
            {
                "stdin": "3\nThe quick brown fox jumps over the lazy dog.\n"
                         "The dog barks. The fox runs away quickly!\n"
                         "Quick thinking helps the fox escape the dog again.\n",
                "expect": "the: 6\ndog: 3\nfox: 3",
            },
            {
                "stdin": "1\napple banana apple banana cherry\n",
                "expect": "apple: 2\nbanana: 2\ncherry: 1",
            },
        ],
        "hints": [
            "`raw.strip(string.punctuation)` peels punctuation off both ends of a token without touching apostrophes/hyphens in the middle.",
            "Sort with `key=lambda kv: (-kv[1], kv[0])` to get count-descending, then alphabetical for ties, in one pass.",
        ],
    },
    {
        "id": "file_word_count",
        "title": "File Word Counter",
        "category": "File I/O & data parsing",
        "difficulty": "Easy",
        "time_limit_min": 15,
        "prompt": """Read simulated file contents from stdin and summarize them.

Input:
  Line 1: an integer N
  Next N lines: the file's contents, one line each

Print, in this exact order:
  Lines: <N>
  Words: <total number of whitespace-separated words across all lines>
  Characters: <total number of characters across all lines (excluding the newlines themselves)>""",
        "starter_code": '''def main():
    n = int(input())
    lines = [input() for _ in range(n)]
    # TODO: compute total_words (sum of len(line.split()) per line)
    # TODO: compute total_chars (sum of len(line) per line)
    print(f"Lines: {n}")
    print(f"Words: {total_words}")
    print(f"Characters: {total_chars}")


if __name__ == "__main__":
    main()
''',
        "reference_solution": '''def main():
    n = int(input())
    lines = [input() for _ in range(n)]
    total_words = sum(len(line.split()) for line in lines)
    total_chars = sum(len(line) for line in lines)
    print(f"Lines: {n}")
    print(f"Words: {total_words}")
    print(f"Characters: {total_chars}")


if __name__ == "__main__":
    main()
''',
        "test_cases": [
            {
                "stdin": "3\nHello world\nThis is a test file\nGoodbye\n",
                "expect": "Lines: 3\nWords: 8\nCharacters: 37",
            },
            {
                "stdin": "1\nOnlyOneWord\n",
                "expect": "Lines: 1\nWords: 1\nCharacters: 11",
            },
        ],
        "hints": [
            "`line.split()` with no arguments splits on any whitespace and drops empty strings -- exactly what you want for a word count.",
        ],
    },
    {
        "id": "pcap_generator_fibonacci",
        "title": "Generator: Fibonacci Stream",
        "category": "PCAP Skill Builder",
        "difficulty": "Medium",
        "time_limit_min": 20,
        "prompt": """PCAP focus: generator functions (`yield`) and the iterator protocol.

Write a generator function `fib_stream()` that yields the Fibonacci
sequence forever, starting 0, 1, 1, 2, 3, 5, 8, ... (each value after the
first two is the sum of the previous two).

Read an integer N, then pull N values from your generator with `next()`
and print each one on its own line.

Your generator must actually use `yield` -- it should be able to produce
values forever without ever building the whole sequence as a list.""",
        "starter_code": '''def fib_stream():
    a, b = 0, 1
    while True:
        # TODO: yield a, then advance (a, b) to the next Fibonacci pair
        pass


def main():
    n = int(input())
    gen = fib_stream()
    for _ in range(n):
        print(next(gen))


if __name__ == "__main__":
    main()
''',
        "reference_solution": '''def fib_stream():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def main():
    n = int(input())
    gen = fib_stream()
    for _ in range(n):
        print(next(gen))


if __name__ == "__main__":
    main()
''',
        "test_cases": [
            {"stdin": "1\n", "expect": "0"},
            {"stdin": "8\n", "expect": "0\n1\n1\n2\n3\n5\n8\n13"},
            {"stdin": "10\n", "expect": "0\n1\n1\n2\n3\n5\n8\n13\n21\n34"},
        ],
        "hints": [
            "Inside the `while True:` loop: `yield a` first, then `a, b = b, a + b` to advance -- the loop body never needs to return or break.",
            "Each call to `next(gen)` resumes right after the last `yield`, picking up with whatever `a` and `b` were at that point.",
        ],
    },
    {
        "id": "pcap_comprehension_report",
        "title": "List/Dict Comprehension Report",
        "category": "PCAP Skill Builder",
        "difficulty": "Easy",
        "time_limit_min": 20,
        "prompt": """PCAP focus: list and dict comprehensions.

Read an integer N, then N lines of "name,score" (score is an integer).

Using a single dict comprehension, build a dict mapping name -> score.
Using a single list comprehension over that dict, build a sorted
(alphabetically) list of names with a passing score (score >= 60).

Print each passing name on its own line (alphabetical order), then print:
  Pass Rate: XX.XX%
(the percentage of ALL students who passed, 2 decimal places)""",
        "starter_code": '''def main():
    n = int(input())
    entries = [input().split(",") for _ in range(n)]
    # TODO: build `scores` as a dict comprehension: {name: int(score), ...}
    scores = {}
    # TODO: build `passing` as a sorted list comprehension of names with scores[name] >= 60
    passing = []
    for name in passing:
        print(name)
    rate = 100 * len(passing) / len(scores) if scores else 0
    print(f"Pass Rate: {rate:.2f}%")


if __name__ == "__main__":
    main()
''',
        "reference_solution": '''def main():
    n = int(input())
    entries = [input().split(",") for _ in range(n)]
    scores = {name: int(score) for name, score in entries}
    passing = sorted(name for name, score in scores.items() if score >= 60)
    for name in passing:
        print(name)
    rate = 100 * len(passing) / len(scores) if scores else 0
    print(f"Pass Rate: {rate:.2f}%")


if __name__ == "__main__":
    main()
''',
        "test_cases": [
            {
                "stdin": "5\nAlice,72\nBob,55\nCarl,60\nDee,90\nEd,40\n",
                "expect": "Alice\nCarl\nDee\nPass Rate: 60.00%",
            },
            {"stdin": "2\nX,30\nY,20\n", "expect": "Pass Rate: 0.00%"},
        ],
        "hints": [
            "Dict comprehension: `{name: int(score) for name, score in entries}` -- entries is already a list of [name, score_str] pairs.",
            "A generator expression works fine inside `sorted(...)`: `sorted(name for name, score in scores.items() if score >= 60)`.",
        ],
    },
    {
        "id": "pcap_custom_exception",
        "title": "Custom Exception: Inventory Guard",
        "category": "PCAP Skill Builder",
        "difficulty": "Medium",
        "time_limit_min": 25,
        "prompt": """PCAP focus: defining and raising your own exception class.

Define a custom exception class `OutOfStockError(Exception)`.

Read commands, one per line, until "Quit":
  STOCK <name> <qty>   add qty units of name to stock; print "Stocked: <name> <qty>"
  SELL <name> <qty>    if enough stock exists, remove qty units and print
                        "Sold: <name> <qty>"; otherwise RAISE OutOfStockError
                        with a message, CATCH it, and print "Error: <message>"
  Quit                 print exactly "Goodbye!" and stop

A name with no prior STOCK has 0 units on hand.""",
        "starter_code": '''class OutOfStockError(Exception):
    pass


def main():
    stock = {}
    while True:
        line = input().split()
        cmd = line[0]
        if cmd == "Quit":
            print("Goodbye!")
            break
        elif cmd == "STOCK":
            name, qty = line[1], int(line[2])
            stock[name] = stock.get(name, 0) + qty
            print(f"Stocked: {name} {qty}")
        elif cmd == "SELL":
            name, qty = line[1], int(line[2])
            # TODO: try to sell `qty` of `name`. If qty is more than what's on
            # hand, raise OutOfStockError(f"only {have} {name} in stock"),
            # catch it, and print f"Error: {e}". Otherwise subtract the stock
            # and print f"Sold: {name} {qty}".


if __name__ == "__main__":
    main()
''',
        "reference_solution": '''class OutOfStockError(Exception):
    pass


def main():
    stock = {}
    while True:
        line = input().split()
        cmd = line[0]
        if cmd == "Quit":
            print("Goodbye!")
            break
        elif cmd == "STOCK":
            name, qty = line[1], int(line[2])
            stock[name] = stock.get(name, 0) + qty
            print(f"Stocked: {name} {qty}")
        elif cmd == "SELL":
            name, qty = line[1], int(line[2])
            try:
                have = stock.get(name, 0)
                if qty > have:
                    raise OutOfStockError(f"only {have} {name} in stock")
                stock[name] = have - qty
                print(f"Sold: {name} {qty}")
            except OutOfStockError as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    main()
''',
        "test_cases": [
            {
                "stdin": "STOCK widget 5\nSELL widget 3\nSELL widget 10\nSELL widget 2\nQuit\n",
                "expect": "Stocked: widget 5\nSold: widget 3\nError: only 2 widget in stock\nSold: widget 2\nGoodbye!",
            },
            {"stdin": "SELL ghost 1\nQuit\n", "expect": "Error: only 0 ghost in stock"},
        ],
        "hints": [
            "`raise OutOfStockError(\"message\")` inside the same function's `try` block that catches it is perfectly normal -- raise and except don't need to be in different functions.",
            "`except OutOfStockError as e:` binds the exception object to `e`; `str(e)` (or an f-string with `{e}`) gives you back the message you raised it with.",
        ],
    },
    {
        "id": "pcap_closure_average",
        "title": "Closures: Running Average Tracker",
        "category": "PCAP Skill Builder",
        "difficulty": "Medium",
        "time_limit_min": 20,
        "prompt": """PCAP focus: closures and the `nonlocal` keyword.

Write a function `make_average_tracker()` that returns a NEW function.
Each time that returned function is called with a number, it should:
  - remember every number it's been given so far (via closure state --
    no globals, no classes)
  - return the running average of all numbers seen so far, including this one

Read an integer N, then N numbers (one per line). Create one tracker with
`make_average_tracker()`, feed it each number in order, and print the
running average after each one, to 2 decimal places.""",
        "starter_code": '''def make_average_tracker():
    total = 0.0
    count = 0

    def add(value):
        # TODO: update `total` and `count` from the enclosing scope (you'll
        # need `nonlocal`), then return the new running average
        pass

    return add


def main():
    n = int(input())
    tracker = make_average_tracker()
    for _ in range(n):
        value = float(input())
        avg = tracker(value)
        print(f"{avg:.2f}")


if __name__ == "__main__":
    main()
''',
        "reference_solution": '''def make_average_tracker():
    total = 0.0
    count = 0

    def add(value):
        nonlocal total, count
        total += value
        count += 1
        return total / count

    return add


def main():
    n = int(input())
    tracker = make_average_tracker()
    for _ in range(n):
        value = float(input())
        avg = tracker(value)
        print(f"{avg:.2f}")


if __name__ == "__main__":
    main()
''',
        "test_cases": [
            {"stdin": "4\n10\n20\n30\n0\n", "expect": "10.00\n15.00\n20.00\n15.00"},
            {"stdin": "1\n5\n", "expect": "5.00"},
        ],
        "hints": [
            "Without `nonlocal total, count`, assigning to `total`/`count` inside `add` would create new LOCAL variables instead of updating the enclosing ones -- and Python would actually raise an UnboundLocalError.",
            "`make_average_tracker()` is called once (creating one closure with its own private total/count); `add`/`tracker` is called once per number.",
        ],
    },
    {
        "id": "pcap_slicing_windows",
        "title": "Slice & Dice: Data Windowing",
        "category": "PCAP Skill Builder",
        "difficulty": "Medium",
        "time_limit_min": 20,
        "prompt": """PCAP focus: sequence slicing syntax.

Read a line of space-separated integers, then read an integer K.

Using ONLY slicing (no loops, no manual index math) to extract each
result, print exactly:
  First K: <the first K elements, as a Python list>
  Last K: <the last K elements, as a Python list>
  Reversed: <every element, reversed, as a Python list>
  Every 2nd: <every other element starting from the first, as a Python list>

(printing a Python list directly, e.g. `print(f"First K: {values[:k]}")`,
already produces the `[1, 2, 3]`-style format expected here)""",
        "starter_code": '''def main():
    values = [int(x) for x in input().split()]
    k = int(input())

    # TODO: first_k    = the first k elements, via slicing
    # TODO: last_k     = the last k elements, via slicing
    # TODO: reversed_all = all elements reversed, via slicing
    # TODO: every_2nd  = every other element starting from index 0, via slicing

    print(f"First {k}: {first_k}")
    print(f"Last {k}: {last_k}")
    print(f"Reversed: {reversed_all}")
    print(f"Every 2nd: {every_2nd}")


if __name__ == "__main__":
    main()
''',
        "reference_solution": '''def main():
    values = [int(x) for x in input().split()]
    k = int(input())

    first_k = values[:k]
    last_k = values[-k:]
    reversed_all = values[::-1]
    every_2nd = values[::2]

    print(f"First {k}: {first_k}")
    print(f"Last {k}: {last_k}")
    print(f"Reversed: {reversed_all}")
    print(f"Every 2nd: {every_2nd}")


if __name__ == "__main__":
    main()
''',
        "test_cases": [
            {
                "stdin": "1 2 3 4 5 6 7 8\n3\n",
                "expect": "First 3: [1, 2, 3]\nLast 3: [6, 7, 8]\nReversed: [8, 7, 6, 5, 4, 3, 2, 1]\nEvery 2nd: [1, 3, 5, 7]",
            },
            {
                "stdin": "10 20 30 40 50\n2\n",
                "expect": "First 2: [10, 20]\nLast 2: [40, 50]\nReversed: [50, 40, 30, 20, 10]\nEvery 2nd: [10, 30, 50]",
            },
        ],
        "hints": [
            "`values[:k]` and `values[-k:]` are the first/last k elements; `values[::-1]` reverses; `values[::2]` steps by 2.",
            "All four are one-liners -- if you're writing a loop for any of them, you're missing the slice syntax that does it in one step.",
        ],
    },
    {
        "id": "pcap_context_manager",
        "title": "Custom Context Manager: Transaction Log",
        "category": "PCAP Skill Builder",
        "difficulty": "Hard",
        "time_limit_min": 30,
        "prompt": """PCAP/PCPP focus: writing your own context manager (`__enter__`/`__exit__`).

Define a class `Transaction` usable in a `with Transaction():` block:
  - `__enter__`: print exactly "BEGIN", return self
  - `__exit__(self, exc_type, exc, tb)`:
      - if an exception occurred inside the block, print
        "ROLLBACK: <exception message>" and SUPPRESS the exception
        (the program must keep running afterward, not crash)
      - if no exception occurred, print exactly "COMMIT"

Read an integer N, then N lines each formatted "OK <text>" or
"FAIL <text>". For each one, open a `with Transaction():` block:
  - "OK <text>": inside the block, print "Doing: <text>"
  - "FAIL <text>": inside the block, raise RuntimeError(text)
Process all N lines this way, continuing after every rollback.""",
        "starter_code": '''class Transaction:
    def __enter__(self):
        # TODO: print "BEGIN", return self
        pass

    def __exit__(self, exc_type, exc, tb):
        # TODO: if exc_type is not None, print f"ROLLBACK: {exc}" and
        # return True to suppress it. Otherwise print "COMMIT" and return False.
        pass


def main():
    n = int(input())
    for _ in range(n):
        line = input()
        cmd, text = line.split(" ", 1)
        with Transaction():
            if cmd == "OK":
                print(f"Doing: {text}")
            else:
                raise RuntimeError(text)


if __name__ == "__main__":
    main()
''',
        "reference_solution": '''class Transaction:
    def __enter__(self):
        print("BEGIN")
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type is not None:
            print(f"ROLLBACK: {exc}")
            return True
        print("COMMIT")
        return False


def main():
    n = int(input())
    for _ in range(n):
        line = input()
        cmd, text = line.split(" ", 1)
        with Transaction():
            if cmd == "OK":
                print(f"Doing: {text}")
            else:
                raise RuntimeError(text)


if __name__ == "__main__":
    main()
''',
        "test_cases": [
            {
                "stdin": "3\nOK write file\nFAIL disk full\nOK cleanup\n",
                "expect": "BEGIN\nDoing: write file\nCOMMIT\nBEGIN\nROLLBACK: disk full\nBEGIN\nDoing: cleanup\nCOMMIT",
            },
            {"stdin": "1\nFAIL boom\n", "expect": "BEGIN\nROLLBACK: boom"},
        ],
        "hints": [
            "`__exit__` returning `True` is what suppresses the exception -- returning `False` (or None) lets it propagate and crash the program.",
            "`exc` in `__exit__(self, exc_type, exc, tb)` IS the exception instance -- an f-string `f\"ROLLBACK: {exc}\"` stringifies it to its message automatically.",
        ],
    },
    {
        "id": "pcep_temp_classifier",
        "title": "Temperature Classifier",
        "category": "PCEP Skill Builder",
        "difficulty": "Easy",
        "time_limit_min": 15,
        "prompt": """PCEP focus: functions, parameters/return, and if/elif/else chains.

Write a function `classify(temp)` that returns a category string for a
Fahrenheit temperature (an int):
  temp <= 32          -> "Freezing"
  33 <= temp <= 50     -> "Cold"
  51 <= temp <= 70     -> "Mild"
  71 <= temp <= 85     -> "Warm"
  temp > 85            -> "Hot"

Read an integer N, then N temperatures (one per line). For each one, call
classify() and print its result.""",
        "starter_code": '''def classify(temp):
    # TODO: return the right category string for temp using if/elif/else
    pass


def main():
    n = int(input())
    for _ in range(n):
        temp = int(input())
        print(classify(temp))


if __name__ == "__main__":
    main()
''',
        "reference_solution": '''def classify(temp):
    if temp <= 32:
        return "Freezing"
    elif temp <= 50:
        return "Cold"
    elif temp <= 70:
        return "Mild"
    elif temp <= 85:
        return "Warm"
    else:
        return "Hot"


def main():
    n = int(input())
    for _ in range(n):
        temp = int(input())
        print(classify(temp))


if __name__ == "__main__":
    main()
''',
        "test_cases": [
            {"stdin": "6\n20\n45\n65\n80\n95\n32\n", "expect": "Freezing\nCold\nMild\nWarm\nHot\nFreezing"},
        ],
        "hints": [
            "Each `elif` only needs an upper-bound check, since anything that reached it already failed the checks above -- you don't need a lower-bound check too.",
        ],
    },
    {
        "id": "pcep_mult_table",
        "title": "Multiplication Table Printer",
        "category": "PCEP Skill Builder",
        "difficulty": "Easy",
        "time_limit_min": 15,
        "prompt": """PCEP focus: nested for loops and range().

Read an integer N. Print an N-by-N multiplication table: N rows, each with
N space-separated values, where the value in row i, column j (both
1-indexed) is i * j.""",
        "starter_code": '''def main():
    n = int(input())
    for i in range(1, n + 1):
        # TODO: build one row as a list of str(i * j) for j in 1..n,
        # then print it space-separated
        pass


if __name__ == "__main__":
    main()
''',
        "reference_solution": '''def main():
    n = int(input())
    for i in range(1, n + 1):
        row = [str(i * j) for j in range(1, n + 1)]
        print(" ".join(row))


if __name__ == "__main__":
    main()
''',
        "test_cases": [
            {"stdin": "3\n", "expect": "1 2 3\n2 4 6\n3 6 9"},
            {"stdin": "1\n", "expect": "1"},
            {"stdin": "4\n", "expect": "1 2 3 4\n2 4 6 8\n3 6 9 12\n4 8 12 16"},
        ],
        "hints": [
            "A nested loop works fine too: outer `for i`, inner `for j`, building up a row string or list before printing it.",
        ],
    },
    {
        "id": "pcep_min_max_three",
        "title": "Min/Max of Three (Function Practice)",
        "category": "PCEP Skill Builder",
        "difficulty": "Easy",
        "time_limit_min": 15,
        "prompt": """PCEP focus: defining functions with multiple parameters and returning values.

Write two functions:
  min_of_three(a, b, c) -- returns the smallest of the three
  max_of_three(a, b, c) -- returns the largest of the three

Read three integers (one per line), call both functions, and print:
  Smallest: <value>
  Largest: <value>""",
        "starter_code": '''def min_of_three(a, b, c):
    # TODO: return the smallest of a, b, c
    pass


def max_of_three(a, b, c):
    # TODO: return the largest of a, b, c
    pass


def main():
    a = int(input())
    b = int(input())
    c = int(input())
    smallest = min_of_three(a, b, c)
    largest = max_of_three(a, b, c)
    print(f"Smallest: {smallest}")
    print(f"Largest: {largest}")


if __name__ == "__main__":
    main()
''',
        "reference_solution": '''def min_of_three(a, b, c):
    return min(a, min(b, c))


def max_of_three(a, b, c):
    return max(a, max(b, c))


def main():
    a = int(input())
    b = int(input())
    c = int(input())
    smallest = min_of_three(a, b, c)
    largest = max_of_three(a, b, c)
    print(f"Smallest: {smallest}")
    print(f"Largest: {largest}")


if __name__ == "__main__":
    main()
''',
        "test_cases": [
            {"stdin": "5\n2\n8\n", "expect": "Smallest: 2\nLargest: 8"},
            {"stdin": "-3\n-3\n0\n", "expect": "Smallest: -3\nLargest: 0"},
        ],
        "hints": [
            "Python's built-in `min()`/`max()` already accept multiple arguments directly -- `min(a, b, c)` works without nesting calls, if you'd rather use that.",
        ],
    },
    {
        "id": "pcpp1_abstract_shapes",
        "title": "Abstract Shape Enforcement",
        "category": "PCPP1 Skill Builder",
        "difficulty": "Medium",
        "time_limit_min": 25,
        "prompt": """PCPP1 focus: abstract base classes (the `abc` module) and polymorphism.

Define an abstract base class `Shape` (using `ABC` and `@abstractmethod`)
with an abstract method `area()`. Define two concrete subclasses:
  Circle(radius): area() = pi * radius**2  (use math.pi)
  Rectangle(width, height): area() = width * height

Read an integer N, then N lines, each either:
  circle <radius>
  rectangle <width> <height>

For each shape (in order), print:
  <Kind> area: <area, 2 decimal places>
(Kind is "Circle" or "Rectangle", capitalized)
Then print the running total of every shape's area:
  Total area: <total, 2 decimal places>""",
        "starter_code": '''from abc import ABC, abstractmethod
import math


class Shape(ABC):
    @abstractmethod
    def area(self):
        pass


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        # TODO: pi * radius ** 2
        pass


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        # TODO: width * height
        pass


def main():
    n = int(input())
    total = 0.0
    for _ in range(n):
        parts = input().split()
        kind = parts[0]
        if kind == "circle":
            shape = Circle(float(parts[1]))
        else:
            shape = Rectangle(float(parts[1]), float(parts[2]))
        a = shape.area()
        total += a
        print(f"{kind.capitalize()} area: {a:.2f}")
    print(f"Total area: {total:.2f}")


if __name__ == "__main__":
    main()
''',
        "reference_solution": '''from abc import ABC, abstractmethod
import math


class Shape(ABC):
    @abstractmethod
    def area(self):
        pass


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


def main():
    n = int(input())
    total = 0.0
    for _ in range(n):
        parts = input().split()
        kind = parts[0]
        if kind == "circle":
            shape = Circle(float(parts[1]))
        else:
            shape = Rectangle(float(parts[1]), float(parts[2]))
        a = shape.area()
        total += a
        print(f"{kind.capitalize()} area: {a:.2f}")
    print(f"Total area: {total:.2f}")


if __name__ == "__main__":
    main()
''',
        "test_cases": [
            {"stdin": "2\ncircle 2\nrectangle 3 4\n", "expect": "Circle area: 12.57"},
            {"stdin": "2\ncircle 2\nrectangle 3 4\n", "expect": "Rectangle area: 12.00"},
            {"stdin": "2\ncircle 2\nrectangle 3 4\n", "expect": "Total area: 24.57"},
        ],
        "hints": [
            "`Shape` never gets instantiated directly -- only Circle and Rectangle are. Because Shape inherits from ABC and has an @abstractmethod, Python would refuse `Shape()` outright if you tried.",
            "The `main()` loop calls `shape.area()` the same way regardless of which subclass it is -- that's polymorphism doing the work instead of an if/elif chain on type.",
        ],
    },
    {
        "id": "pcpp1_csv_roster",
        "title": "CSV Round-Trip: Student Roster",
        "category": "PCPP1 Skill Builder",
        "difficulty": "Medium",
        "time_limit_min": 25,
        "prompt": """PCPP1 focus: the `csv` module for real CSV parsing (not manual `.split(",")`).

Read an integer N, then N lines of CSV-formatted "name,score" data (a name
may be double-quoted and contain a comma, e.g. `"Smith, Jane",90` -- a
plain `.split(",")` would break on that, which is exactly why this uses
the `csv` module instead).

Use `csv.reader` to parse the N lines (it accepts any iterable of
strings -- you don't need a real file). For each row, in order, print:
  <name>: <score>
Then print:
  Average: <mean score, 2 decimal places>
  Top: <name of the highest scorer>
(assume no ties for the top score in the test data)""",
        "starter_code": '''import csv


def main():
    n = int(input())
    lines = [input() for _ in range(n)]
    # TODO: parse `lines` with csv.reader into a list of [name, score_str] rows
    rows = []

    total = 0
    top_name = None
    top_score = -1
    for name, score_str in rows:
        score = int(score_str)
        total += score
        if score > top_score:
            top_score = score
            top_name = name
        print(f"{name}: {score}")

    avg = total / len(rows) if rows else 0
    print(f"Average: {avg:.2f}")
    print(f"Top: {top_name}")


if __name__ == "__main__":
    main()
''',
        "reference_solution": '''import csv


def main():
    n = int(input())
    lines = [input() for _ in range(n)]
    reader = csv.reader(lines)
    rows = list(reader)

    total = 0
    top_name = None
    top_score = -1
    for name, score_str in rows:
        score = int(score_str)
        total += score
        if score > top_score:
            top_score = score
            top_name = name
        print(f"{name}: {score}")

    avg = total / len(rows) if rows else 0
    print(f"Average: {avg:.2f}")
    print(f"Top: {top_name}")


if __name__ == "__main__":
    main()
''',
        "test_cases": [
            {
                "stdin": "3\nAlice,88\nBob,95\nCarl,72\n",
                "expect": "Alice: 88\nBob: 95\nCarl: 72\nAverage: 85.00\nTop: Bob",
            },
            {
                "stdin": '2\n"Smith, Jane",90\nBob,80\n',
                "expect": "Smith, Jane: 90\nBob: 80\nAverage: 85.00\nTop: Smith, Jane",
            },
        ],
        "hints": [
            "`csv.reader(lines)` works on a plain list of strings just like it would on an open file object -- both are just iterables of lines.",
            "The whole point of this exercise is the quoted-comma case: `.split(\",\")` would wrongly break \"Smith, Jane\" into two fields, but csv.reader handles the quoting correctly.",
        ],
    },
    {
        "id": "pcpp1_json_merge",
        "title": "JSON Config Merger",
        "category": "PCPP1 Skill Builder",
        "difficulty": "Medium",
        "time_limit_min": 20,
        "prompt": """PCPP1 focus: the `json` module (`loads`/`dumps`).

Read two lines, each a JSON object as text: a base config, then an
override config. Parse both with `json.loads`, merge them so that any key
in the override replaces the same key in the base (keys only in the base
are kept as-is), and print the merged result as a single line of JSON
using `json.dumps(merged, sort_keys=True)` (sort_keys keeps the output
order deterministic).""",
        "starter_code": '''import json


def main():
    base_json = input()
    override_json = input()

    # TODO: parse both lines with json.loads()
    base = {}
    override = {}

    # TODO: merge -- start from a copy of base, then apply override on top
    merged = {}

    print(json.dumps(merged, sort_keys=True))


if __name__ == "__main__":
    main()
''',
        "reference_solution": '''import json


def main():
    base_json = input()
    override_json = input()

    base = json.loads(base_json)
    override = json.loads(override_json)

    merged = dict(base)
    merged.update(override)

    print(json.dumps(merged, sort_keys=True))


if __name__ == "__main__":
    main()
''',
        "test_cases": [
            {
                "stdin": '{"host": "localhost", "port": 8080, "debug": false}\n{"port": 9090, "debug": true}\n',
                "expect": '{"debug": true, "host": "localhost", "port": 9090}',
            },
            {"stdin": '{"a": 1}\n{"b": 2}\n', "expect": '{"a": 1, "b": 2}'},
        ],
        "hints": [
            "`dict(base)` makes a shallow copy so you don't mutate the original `base` dict; `merged.update(override)` then overwrites/adds keys from override on top of it.",
            "`sort_keys=True` is required here -- without it, dict key order in the printed JSON wouldn't be guaranteed to match the expected output exactly.",
        ],
    },
    {
        "id": "pcpp2_singleton_logger",
        "title": "Singleton Logger",
        "category": "PCPP2 Skill Builder",
        "difficulty": "Medium",
        "time_limit_min": 25,
        "prompt": """PCPP2 focus: the Singleton design pattern.

Implement a `Logger` class where EVERY call to `Logger()` returns the
SAME instance (a classic Singleton), by overriding `__new__`. The single
shared instance keeps a `messages` list.

Read an integer N, then N commands, one per line:
  LOG <text>   append <text> to the shared logger's messages; print "Logged: <text>"
  COUNT        print "Count: <number of messages logged so far>"
  SAME         create a second Logger() and print "Same instance: <True/False>"
               comparing it to a fresh Logger() with `is`""",
        "starter_code": '''class Logger:
    _instance = None

    def __new__(cls):
        # TODO: if cls._instance is None, create it with super().__new__(cls)
        # and give it an empty `messages` list. Either way, return cls._instance.
        pass

    def log(self, message):
        self.messages.append(message)


def main():
    n = int(input())
    for _ in range(n):
        parts = input().split(" ", 1)
        cmd = parts[0]
        logger = Logger()
        if cmd == "LOG":
            logger.log(parts[1])
            print(f"Logged: {parts[1]}")
        elif cmd == "COUNT":
            print(f"Count: {len(logger.messages)}")
        elif cmd == "SAME":
            other = Logger()
            print(f"Same instance: {logger is other}")


if __name__ == "__main__":
    main()
''',
        "reference_solution": '''class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.messages = []
        return cls._instance

    def log(self, message):
        self.messages.append(message)


def main():
    n = int(input())
    for _ in range(n):
        parts = input().split(" ", 1)
        cmd = parts[0]
        logger = Logger()
        if cmd == "LOG":
            logger.log(parts[1])
            print(f"Logged: {parts[1]}")
        elif cmd == "COUNT":
            print(f"Count: {len(logger.messages)}")
        elif cmd == "SAME":
            other = Logger()
            print(f"Same instance: {logger is other}")


if __name__ == "__main__":
    main()
''',
        "test_cases": [
            {
                "stdin": "5\nLOG first entry\nLOG second entry\nCOUNT\nSAME\nCOUNT\n",
                "expect": "Logged: first entry\nLogged: second entry\nCount: 2\nSame instance: True\nCount: 2",
            },
        ],
        "hints": [
            "`__new__` runs BEFORE `__init__` and is what actually creates (or, here, reuses) the object -- overriding it is the classic way to implement Singleton in Python.",
            "The class attribute `_instance` is shared by the class itself, not by any one object -- that's exactly why it persists across separate `Logger()` calls.",
        ],
    },
    {
        "id": "pcpp2_sqlite_roster",
        "title": "Mini SQLite Roster",
        "category": "PCPP2 Skill Builder",
        "difficulty": "Hard",
        "time_limit_min": 30,
        "prompt": """PCPP2 focus: the `sqlite3` module -- real SQL from Python.

Use `sqlite3.connect(":memory:")` for a scratch in-memory database. Create
a table `students(name TEXT, score INTEGER)`.

Read an integer N, then N lines of "name,score". INSERT each one using a
PARAMETERIZED query (`?` placeholders -- never format the SQL string by
hand). Then:
  1. SELECT name, score ordered by score descending; print each as
     "<name>: <score>"
  2. Print "Average: <AVG(score), 2 decimal places>"
  3. Print "Passing: <COUNT of students with score >= 60>"
""",
        "starter_code": '''import sqlite3


def main():
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE students (name TEXT, score INTEGER)")

    n = int(input())
    for _ in range(n):
        name, score = input().split(",")
        # TODO: INSERT this student using a parameterized query (? placeholders)
    conn.commit()

    # TODO: SELECT name, score ordered by score DESC, and print each "name: score"

    # TODO: SELECT AVG(score), print "Average: <2 decimals>"

    # TODO: SELECT COUNT(*) WHERE score >= 60, print "Passing: <count>"

    conn.close()


if __name__ == "__main__":
    main()
''',
        "reference_solution": '''import sqlite3


def main():
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE students (name TEXT, score INTEGER)")

    n = int(input())
    for _ in range(n):
        name, score = input().split(",")
        cur.execute("INSERT INTO students (name, score) VALUES (?, ?)", (name, int(score)))
    conn.commit()

    cur.execute("SELECT name, score FROM students ORDER BY score DESC")
    for name, score in cur.fetchall():
        print(f"{name}: {score}")

    cur.execute("SELECT AVG(score) FROM students")
    avg = cur.fetchone()[0]
    print(f"Average: {avg:.2f}")

    cur.execute("SELECT COUNT(*) FROM students WHERE score >= 60")
    passing = cur.fetchone()[0]
    print(f"Passing: {passing}")

    conn.close()


if __name__ == "__main__":
    main()
''',
        "test_cases": [
            {
                "stdin": "4\nAlice,88\nBob,95\nCarl,55\nDee,72\n",
                "expect": "Bob: 95\nAlice: 88\nDee: 72\nCarl: 55\nAverage: 77.50\nPassing: 3",
            },
            {
                "stdin": "2\nX,45\nY,65\n",
                "expect": "Y: 65\nX: 45\nAverage: 55.00\nPassing: 1",
            },
        ],
        "hints": [
            "`cur.execute(\"INSERT ... VALUES (?, ?)\", (name, int(score)))` -- the `?` placeholders and the tuple of values keep this injection-safe, unlike building the SQL string with f-strings.",
            "`cur.fetchone()` on an aggregate query like `SELECT AVG(score) FROM students` returns a one-element tuple; `[0]` pulls out the actual number.",
        ],
    },
]

PROBLEMS_BY_ID = {p["id"]: p for p in PROBLEMS}
