# reading data of the complete dfa from the file
automata = open("input-files/test1.txt")
alphabet = [x for x in automata.readline().split()]
nrStates = int(automata.readline())
initialState = automata.readline().strip('\n')
finalStates = [x for x in automata.readline().split()]
# building delta function = transition table
delta = {}
line = automata.readline()
while line:
    aux = line.split()
    state1 = aux[0]
    state2 = aux[1]
    transition = aux[2]

    if state1 not in delta:
        delta[state1] = {transition: state2}
    else:
        delta[state1][transition] = state2
    line = automata.readline()
# print(delta)
# removing unreachable states (states that are not reachable from the initial state, for any input string => they can be removed from the automata without changhing the accepted language)
# r -> set of reachable states
r = set(initialState)
ok = True
while ok:
    ok = False
    new_states = set()
    for s in r.copy():
        for letter in alphabet:
            new_states.add(delta[s][letter])
    if new_states - r:
        r.update(new_states)
        ok = True

# update nr of states and delta function if any unreachable states were found
if len(r) != nrStates:
    nrStates = len(r)
    new_delta = {}
    for state in delta:
        if state in r:
            new_delta[state] = delta[state]
    delta = new_delta

# now we finally have our dfa with no unreachable states
# assigning an index for each state in order to complete the table correspondingly
find_state_from_index = {i: state for i, state in enumerate(delta)}
find_index_of_state = {state: i for i, state in enumerate(delta)}

# Myhill Nerode Theorem - Table filling method

# Step 1
# Creating half of table
table = [[0 for j in range(i)] for i in range(nrStates)]
# Step 2
# If one state is final and the other is nonfinal => they are not equivalent for sure, so we mark them with 1 in the table.
for i in range(1, nrStates):
    for j in range(i):
        if (find_state_from_index[i] in finalStates and find_state_from_index[j] not in finalStates) or (
                find_state_from_index[i] not in finalStates and find_state_from_index[j] in finalStates):
            table[i][j] = 1
        else:
            table[i][j] = 0

# Step 3
# Check if unmarked pairs (p,q) compose a pair (delta[p][letter], delta[q][letter]) marked, if so => mark pair (p,q) too
# Repeating the process until no more markings can be done
marked = True
while marked:
    marked = False
    for i in range(1, nrStates):
        for j in range(i):
            if table[i][j] == 0:
                for letter in alphabet:
                    # composed pair
                    state1 = delta[find_state_from_index[i]][letter]
                    state2 = delta[find_state_from_index[j]][letter]
                    # find their indexes
                    x = find_index_of_state[state1]
                    y = find_index_of_state[state2]
                    try:
                        check = table[x][y] if x > y else table[y][x]
                        if check == 1:
                            table[i][j] = 1
                            marked = True
                            break
                    except:
                        pass
# In the end, the unmarked pairs give me the equivalent states

# print filled table
# for i in range(1, nrStates):
#     print(*table[i])

# Step 4
# Combine all unmarked pairs and make them a single state

# components -> list of sets representing the remaining components in the minimized dfa
components = []
for i in range(1, nrStates):
    for j in range(i):
        if table[i][j] == 0:
            # append the equivalent pair of states
            components.append(set([find_state_from_index[i], find_state_from_index[j]]))
# form the components
for i in range(len(components)):
    try:
        current_pair = components[i]
        j = i + 1
        while j < len(components):
            if current_pair.intersection(components[j]):
                current_pair = current_pair.union(components[j])
                components.pop(j)
            else:
                j += 1
        components[i] = current_pair
    except IndexError:
        # index out of range because I remove the sets which were merged into another set, so components[i] might not exist anymore
        pass

# adding the states which are not equivalent to any other state because they form a component on their own in the minimized dfa
components_flat = []
nr = 0
for comp in components:
    for state in comp:
        nr += 1
        components_flat.append(state)

if nr != nrStates:
    for i in range(nrStates):
        if find_state_from_index[i] not in components_flat:
            new_comp = find_state_from_index[i]
            components.append(new_comp)

components = [''.join(comp) for comp in components]
# print(components)

found = False
for comp in components:
    for state in comp:
        if state == initialState:
            initialComponent = comp
            found = True
            break
    if found:
        break

finalComponents = []
for comp in components:
    for state in comp:
        if state in finalStates:
            finalComponents.append(comp)
            break

def build_minimized_delta(components):
    global alphabet, delta
    minimized_delta = {}
    for i, comp in enumerate(components):
        for letter in alphabet:
            for state in comp:
                if delta[state][letter] in comp:
                    if comp not in minimized_delta:
                        minimized_delta[comp] = {letter: comp}
                    else:
                        minimized_delta[comp][letter] = comp
                else:
                    for j in range(len(components)):
                        if delta[state][letter] in components[j]:
                            if comp not in minimized_delta:
                                minimized_delta[comp] = {letter: components[j]}
                            else:
                                minimized_delta[comp][letter] = components[j]
    return minimized_delta

minimized_delta = build_minimized_delta(components)
# Printing the minimized dfa
def print_minimized_dfa(components):
    global alphabet, initialComponent, finalComponents, minimized_delta
    print("The minimized DFA is: \n")
    print("States:", *components)
    print("Alphabet:", *alphabet)
    print("Initial state:", initialComponent)
    print("Final states:", *finalComponents)
    print("Transition table:")
    for comp in minimized_delta:
        for letter in minimized_delta[comp]:
            print(f"\t{comp} -> {letter} -> {minimized_delta[comp][letter]}")


print("Do you want the minimized DFA to be complete? [0/1]: ")
choice = int(input())

if choice == 0:
    # removing dead states -> states from which you can never reach a final state
    componentsUpdated = []
    for state in components:
        deadState = True
        reachableStates = [state]
        #the while loop continues until newStates is equal to reachableStates, which means that no new states were added in the last iteration, so we found all the reachable states starting from the current state
        while True:
            next = []
            for s in reachableStates:
                for letter in alphabet:
                    next.append(minimized_delta[s][letter])
            newStates = list(set(next))
            if newStates == reachableStates:
                break
            reachableStates = newStates
        for rs in reachableStates:
            if rs in finalComponents:
                deadState = False
        if not deadState:
            componentsUpdated.append(state)

    componentsUpdated = list(set(componentsUpdated))

    minimized_delta = build_minimized_delta(componentsUpdated)
    print_minimized_dfa(componentsUpdated)
elif choice == 1:
    print_minimized_dfa(components)
else:
    print("Invalid command")
