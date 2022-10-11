from graphviz import Digraph
from .consts import Consts
import tempfile

def draw_nfa(nfa, title=""):
    state_name = {}
    i = 0
    for state in nfa["states"]:
        state_name[state] = "q{}".format(i).translate(str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉"))
        i+=1

    g = Digraph()
    g.attr(rankdir='LR')

    if title == "":
        title = r'\n\nNFA'
    else:
        title = title.replace('╲', r'\\')
        title = title.replace('⁕', '*')
        title = title.replace('ʔ', '?')
        title = title.replace('⁾', ')')
        title = title.replace('⁽', '(')
        title = title.replace('⁺', '+')
        title = r'\n\nNFA : '+title
    g.attr(label=title, fontsize='30')

    # mark goal states
    g.attr('node', shape='doublecircle')
    for state in nfa['final_states']:
        g.node(state_name[state])

    # add an initial edge
    g.attr('node', shape='none')
    g.node("")
    
    g.attr('node', shape='circle')
    g.edge("", state_name[nfa["initial_state"]])

    for state in nfa["states"]:
        for character in nfa["transition_function"][state]:
            for transition_state in nfa["transition_function"][state][character]:
                if character not in [Consts.EPSILON, '╲', '⁕', 'ʔ', '⁾', '⁽', '⁺']:
                    lbl = character
                else:
                    lbl = replace_char(character)
                g.edge(state_name[state], state_name[transition_state], label=lbl)

    g.view(tempfile.mktemp('.gv'))

def draw_dfa(dfa, title=""):
    state_name = {}
    i = 0
    for state in dfa["reachable_states"]:
        if state == "phi":
            state_name[state] = "\u03A6"
        else:
            state_name[state] = "q{}".format(i).translate(str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉"))
            i+=1

    g = Digraph()
    g.attr(rankdir='LR')

    if title == "":
        title = r'\n\nDFA'
    else:
        title = title.replace('╲', r'\\')
        title = title.replace('⁕', '*')
        title = title.replace('ʔ', '?')
        title = title.replace('⁾', ')')
        title = title.replace('⁽', '(')
        title = title.replace('⁺', '+')
        title = r'\n\nDFA : '+title
    g.attr(label=title, fontsize='30')

    # mark goal states
    g.attr('node', shape='doublecircle')
    for state in dfa["final_reachable_states"]:
        g.node(state_name[state])

    # add an initial edge
    g.attr('node', shape='none')
    g.node("")
    
    g.attr('node', shape='circle')
    g.edge("", state_name[dfa["initial_state"]])

    for state in dfa["reachable_states"]:
        for character in dfa["transition_function"][state].keys():
            transition_state = dfa["transition_function"][state][character]
            if character not in ['╲', '⁕', 'ʔ', '⁾', '⁽', '⁺']:
                lbl = character
            else:
                lbl = replace_char(character)
            g.edge(state_name[state], state_name[transition_state], label=lbl)

    g.view(tempfile.mktemp('.gv'))

def replace_char(character):
    if character == Consts.EPSILON:
        lbl = "\u03B5"
    elif character == '╲':
        lbl = r'\\'
    elif character == '⁕':
        lbl = r'*'
    elif character == 'ʔ':
        lbl = r'?'
    elif character == '⁾':
        lbl = r')'
    elif character == '⁽':
        lbl = r'('
    elif character == '⁺':
        lbl = r'+'
    return lbl
