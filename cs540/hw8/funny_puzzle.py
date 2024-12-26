import heapq

def state_check(state):
    """check the format of state, and return corresponding goal state.
       Do NOT edit this function."""
    non_zero_numbers = [n for n in state if n != 0]
    num_tiles = len(non_zero_numbers)
    if num_tiles == 0:
        raise ValueError('At least one number is not zero.')
    elif num_tiles > 9:
        raise ValueError('At most nine numbers in the state.')
    matched_seq = list(range(1, num_tiles + 1))
    if len(state) != 9 or not all(isinstance(n, int) for n in state):
        raise ValueError('State must be a list contain 9 integers.')
    elif not all(0 <= n <= 9 for n in state):
        raise ValueError('The number in state must be within [0,9].')
    elif len(set(non_zero_numbers)) != len(non_zero_numbers):
        raise ValueError('State can not have repeated numbers, except 0.')
    elif sorted(non_zero_numbers) != matched_seq:
        raise ValueError('For puzzles with X tiles, the non-zero numbers must be within [1,X], '
                          'and there will be 9-X grids labeled as 0.')
    goal_state = matched_seq
    for _ in range(9 - num_tiles):
        goal_state.append(0)
    return tuple(goal_state)

def get_manhattan_distance(from_state, to_state):
    """
    TODO: implement this function. This function will not be tested directly by the grader. 

    INPUT: 
        Two states (The first one is current state, and the second one is goal state)

    RETURNS:
        A scalar that is the sum of Manhattan distances for all tiles.
    """
    distance = 0
    for i in range(9):
        if from_state[i] != 0:
            from_pos = (i // 3, i % 3)
            goal_index = to_state.index(from_state[i])
            goal_pos = (goal_index // 3, goal_index % 3)
            distance += abs(from_pos[0] - goal_pos[0]) + abs(from_pos[1] - goal_pos[1])
    return distance

def print_succ(state):
    """
    TODO: This is based on get_succ function below, so should implement that function.

    INPUT: 
        A state (list of length 9)

    WHAT IT DOES:
        Prints the list of all the valid successors in the puzzle. 
    """

    # given state, check state format and get goal_state.
    goal_state = state_check(state)
    # please remove debugging prints when you submit your code.
    # print('initial state: ', state)
    # print('goal state: ', goal_state)

    succ_states = get_succ(state)

    for succ_state in succ_states:
        print(succ_state, "h={}".format(get_manhattan_distance(succ_state,goal_state)))


def get_succ(state):
    """
    INPUT: 
        A state (list of length 9)

    RETURNS:
        A list of all the valid successors in the puzzle (sorted in lexicographical order).
    """
    succ_states = []
    zero_index = state.index(0)  # Find the index of the blank space (0)
    row, col = zero_index // 3, zero_index % 3  # Calculate the row and column of the blank space
    
    # Possible moves: up, down, left, right (row offset, column offset)
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for dr, dc in moves:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:  # Check if the new position is within bounds
            new_index = new_row * 3 + new_col  # Calculate the index in the 1D list
            new_state = state[:]  # Create a copy of the current state
            # Swap the blank space with the tile at the new index
            new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
            succ_states.append(new_state)
    
    return sorted(succ_states)  # Return the sorted list of successor states



# +
import heapq

def solve(state, goal_state=[1, 2, 3, 4, 5, 6, 7, 0, 0]):
    """
    Implement the A* algorithm to find the path from the initial state to the goal state.

    INPUT: 
        An initial state (list of length 9)

    WHAT IT SHOULD DO:
        Prints a path of configurations from initial state to goal state along with h values, number of moves, and max queue length.
    """
    # Count inversions to determine if the puzzle is solvable
    inversions = 0
    non_zero = [x for x in state if x != 0]
    for i in range(len(non_zero)):
        for j in range(i + 1, len(non_zero)):
            if non_zero[i] > non_zero[j]:
                inversions += 1
    is_solvable = inversions % 2 == 0

    # Initial state check
    goal_state = state_check(state)
    
    print(is_solvable)
    if not is_solvable:
        print(False)
        
    else:
        print(True)

    # Priority queue for A* (min-heap)
    queue = []
    # Push the initial state with f(n) = h(n) + g(n), g(n)=0 initially
    heapq.heappush(queue, (get_manhattan_distance(state, goal_state), 0, state, []))
    visited = set()
    max_queue_length = 0

    while queue:
        # Update max queue length
        max_queue_length = max(max_queue_length, len(queue))
        # Pop the state with the lowest f(n) from the priority queue
        f, g, current_state, path = heapq.heappop(queue)

        # Check if we've reached the goal
        if current_state == goal_state:
            path.append((current_state, get_manhattan_distance(current_state, goal_state), g))
            for state_info in path:
                current, h, moves = state_info
                print(current, "h={}".format(h), "moves: {}".format(moves))
            print("Max queue length: {}".format(max_queue_length))
            return

        # Mark current state as visited
        visited.add(tuple(current_state))
        
        # Get successors of the current state
        for succ in get_succ(current_state):
            if tuple(succ) not in visited:
                new_path = path + [(current_state, get_manhattan_distance(current_state, goal_state), g)]
                heapq.heappush(queue, (g + 1 + get_manhattan_distance(succ, goal_state), g + 1, succ, new_path))
                visited.add(tuple(succ))

    # If no solution is found
    print("No solution found")



# -

if __name__ == "__main__":
    """
    Feel free to write your own test code here to exaime the correctness of your functions. 
    Note that this part will not be graded.
    """
    # print_succ([2,5,1,4,0,6,7,0,3])
    # print()
    #
    # print(get_manhattan_distance([2,5,1,4,0,6,7,0,3], [1, 2, 3, 4, 5, 6, 7, 0, 0]))
    # print()

    solve([2,5,1,4,0,6,7,0,3])
    print()

solve([1,3,2,4,5,6,7,8,0])


