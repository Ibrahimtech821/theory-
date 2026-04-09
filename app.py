import streamlit as st
from parser import parse_regex
from NFA import build_nfa
from visualizer import draw_nfa

st.title("Regex → NFA Visualizer")

regex = st.text_input("Enter Regex:")

if st.button("Generate NFA"):

    try:
        postfix = parse_regex(regex)
        nfa_obj, final_frag = build_nfa(postfix)

        if not final_frag:
            st.error("Invalid regex")
        else:
            dot = draw_nfa(nfa_obj, final_frag, regex)

            path = "nfa_result.png"
            dot.render("nfa_result", cleanup=True, view=True)

            st.image(path, caption="Generated NFA")

            st.success("Done!")

    except Exception:
        st.error("Invalid regex")