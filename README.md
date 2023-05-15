# DFA Minimization Algorithm
This is an algorithm that transforms a given complete DFA (Deterministic Finite Automaton) into an equivalent DFA that has a minimum number of states.

The algorithm consists of the following steps:
1) Remove the unreachable states if they exist (the states that are not reachable from the initial state of the DFA, for any input string)
2) Find the equivalent states using Myhill Nerode Theorem
3) Remove dead states if they exist (the states from which no final state is reachable) !! These states can be removed unless the minimized automaton is required to be complete.

For a better understanding of the code, watch this yt video: [Myhill Nerode Theorem - Table Filling Method](https://www.youtube.com/watch?v=UiXkJUTkp44&ab_channel=NesoAcademy)
## Input
![complete-dfa](https://github.com/ana-rosu/minimization-of-dfa/assets/108434901/b9cd4432-262c-459d-9fd2-cfd370a2507f)

For the above complete dfa, the algorithm takes in as an input a file.txt containing the dfa in the following format (without comments):
```python
0 1     #representing the sigma of the dfa
6       #representing the number of states of the dfa
a       #representing the initial state of the dfa
c d e   #representing the final states of the dfa
a b 0   #representing a transition where a is the present state and b is the next state for input 0
a c 1
b a 0
b d 1
c e 0
c f 1
d e 0
d f 1
e e 0
e f 1
f f 0
f f 1
```

## Usage
The algorithm can be used to reduce the size and complexity of a DFA, while preserving its language. This can be useful in various applications, such as pattern matching and parsing.
