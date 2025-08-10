import re

def dsa_suggestions(code):
    """
    Look for patterns that indicate inefficient DSA usage and give tips.
    """
    suggestions = []

    # Linear search detection (naive pattern)
    if re.search(r'for\s*\(.*<.*\.length|for\s*\(.*<.*size', code) and re.search(r'if\s*\(.*==.*\)', code):
        suggestions.append("[SUGGESTION] Detected possible linear search. If data is sorted, consider binary search for O(log n) performance.")

    # Bubble sort detection
    if "for" in code and re.search(r'for\s*\(.*i.*\)\s*{[^}]*for\s*\(.*j.*\)', code, re.DOTALL):
        if "swap" in code or re.search(r'\btemp\b', code):
            suggestions.append("[SUGGESTION] Nested loops with swapping detected. Consider using merge sort or quicksort for faster sorting.")

    # Large nested loops
    loop_count = len(re.findall(r'for\s*\(', code))
    if loop_count >= 2:
        suggestions.append("[SUGGESTION] Multiple nested loops detected. Consider using hashing or better data structures to reduce complexity.")

    # Recursion detection
    func_names = re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', code)
    for name in func_names:
        if re.search(rf'\b{name}\s*\(.*\)', code) and re.search(rf'{name}\s*\(.*\)', code):
            suggestions.append(f"[SUGGESTION] Recursion detected in function '{name}'. If performance is an issue, consider an iterative approach.")

    return suggestions
