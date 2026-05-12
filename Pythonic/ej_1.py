#1
"""
data = [3, 4, 7, 8, 10]
result = [ i * 10 for i in data if i % 2 == 0 ]

#2
names = ["Alice", "Bob", "Carol"]
scores = [7, 4, 9]

for index , (name, score) in enumerate(zip(names, scores)):
    status = "pass" if score >= 5 else "fail"
    print(f"{index} y {name} y {score} y {status}")
"""
#3
records = [
    ("Alice", "math"),
    ("Bob", "physics"),
    ("Alice", "programming"),
    ("Bob", "math"),
]
"""
result = {}
for name, subject in records:
    if name not in result:
        result[name] = []
    result[name].append(subject)
#{'Alice': ['math', 'programming'], 'Bob': ['physics', 'math']}

"""

data = (x for x in range(10))
filtered = (x for x in data if x % 2 == 0)
result = (x * 10 for x in filtered)

for x in result:
    print(x)