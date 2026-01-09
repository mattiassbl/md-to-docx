# Examples: Sorting Animals Alphabetically in Python

## Example 1: Using `sorted()`
```python
animals = ["dog", "cat", "elephant", "bear", "zebra", "lion"]

# Sort alphabetically
sorted_animals = sorted(animals)

print("Animals in alphabetical order:")
print(sorted_animals)
```

**Explanation:**
- `sorted()` returns a new list with elements sorted in ascending order (alphabetically for strings).

---

## Example 2: Using `list.sort()`
```python
animals = ["dog", "cat", "elephant", "bear", "zebra", "lion"]

# Sort the list in place
animals.sort()

print("Animals in alphabetical order:")
print(animals)
```

**Explanation:**
- `list.sort()` modifies the original list instead of creating a new one.
