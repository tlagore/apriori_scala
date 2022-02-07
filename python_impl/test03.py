

# (set of 3 cake tins pantry design,recipe box pantry yellow design)

item_tuple = ("Clinkenbeard, Colleen", "Stoddard, Mark (I)")

count = 0
with open('../code/data/good-movies.csv', "r") as in_file:
    for line in in_file:
        unique_items = set([w.strip() for w in line.split(";")])
        if (item_tuple [1] in unique_items and item_tuple[0] in unique_items):
            count += 1


print(f"item tuple {item_tuple} was found {count} times")