from parser import parse_regex
from NFA import build_nfa
from visualizer import draw_nfa

def run_project():
    user_input = input("Enter Regex (e.g., a(b|c)*): ")
    try:
        postfix = parse_regex(user_input)
        nfa_obj, final_frag = build_nfa(postfix)
        
        if final_frag:
            dot = draw_nfa(nfa_obj, final_frag, user_input)
            dot.render("nfa_result", cleanup=True, view=True)
            print("Successfully generated nfa_result.png")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_project()