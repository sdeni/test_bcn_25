import networkx as nx
# 1. Generate small random graph
# 2. Plot the graph
# 3. Do BFS starting from node 0
# 4. Print the BFS path
# 5. Plot the edges which were used with red color
# 6. Do DFS starting from node 0
# 7. Print the DFS path
# 8. Plot the edges which were used with blue color

import re

pattern = r"\d+ a"
text = "There are 123 apples and 45 apricots."
numbers = re.findall(pattern, text)
print("Numbers found:", numbers)

pattern = r"\d+"
text = "I like 10 apple and 100 apple pie"
new_text = re.sub(pattern, "many", text)
print(new_text)

pattern = r"(\w+)@(\w+(?:\.\w+)+)"
text = "My email is test@example.best.of.sdsd.sds.com"
match = re.search(pattern, text)
if match:
    username, domain = match.groups()
    print("Username:", username)
    print("Domain:", domain)


pattern = r"\w+(?=\s+dog)"
text = "The quick brown fox jumps over the lazy dog"
matches = re.findall(pattern, text)
print("Word before 'dog':", matches)
