import graphviz

def draw_nfa(nfa, final_frag, regex):
    dot = graphviz.Digraph(format='png')
    dot.graph_attr['rankdir'] = 'LR'
    dot.attr(label=f"NFA for: {regex}", labelloc='t', fontsize='14')

    dot.node('start_arrow', shape='none', label='')
    dot.edge('start_arrow', final_frag.start)

    states = set()
    for (s1, _, s2) in nfa.transitions:
        states.add(s1)
        states.add(s2)

    for state in states:
        shape = 'doublecircle' if state == final_frag.accept else 'circle'
        dot.node(state, shape=shape)

    for (s1, char, s2) in nfa.transitions:
        dot.edge(s1, s2, label=char)

    return dot