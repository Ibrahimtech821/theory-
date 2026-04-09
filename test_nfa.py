from parser import parse_regex
from NFA import build_nfa

def test_regex(regex):
    print("\n==============================")
    print(f"Regex: {regex}")

    # Step 1: Parse regex → postfix
    postfix = parse_regex(regex)
    print("Postfix:", postfix)

    # Step 2: Build NFA
    nfa, final_frag = build_nfa(postfix)

    if not final_frag:
        print("Error: Could not build NFA")
        return

    # Step 3: Print results
    print("\n--- NFA ---")
    print("Start State:", final_frag.start)
    print("Accept State:", final_frag.accept)

    print("\nTransitions:")
    for (s1, sym, s2) in nfa.transitions:
        print(f"{s1} --({sym})--> {s2}")


if __name__ == "__main__":
    # You can change this anytime
    regex = input("Enter regex: ")

    test_regex(regex)