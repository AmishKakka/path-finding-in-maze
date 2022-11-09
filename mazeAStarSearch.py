import maze
from queue import PriorityQueue

class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node


class AStar():
    def __init__(self, file):
        # Initialize an empty explored set
        self.explored = set()

        self.m = maze.Maze(file)
        print("Solving using A* Search.")
        """Finds a solution to maze, if one exists."""

        # Keep track of number of states explored
        self.num_explored = 0

        # Initialize frontier to just the starting position
        self.start = Node(state=self.m.start, parent=None, action=None)
        self.frontier = QueueFrontier()
        self.frontier.add(self.start)

    def heuristic(self, d1, d2, d3):
        d1_d2 = (abs(d1[0]-d2[0]) + abs(d1[1]-d2[1]))
        d2_d3 = (abs(d3[0]-d2[0]) + abs(d3[1]-d2[1]))
        return d1_d2+d2_d3

    def solve(self):
        # Keep looping until solution found
        while True:
            # If nothing left in frontier, then no path
            if self.frontier.empty():
                raise Exception("no solution")

            # Choose a node from the frontier
            node = self.frontier.remove()
            self.num_explored += 1

            # If node is the goal, then we have a solution
            if node.state == self.m.goal:
                print("Reached goal state...\n")
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.m.solution = (actions, cells)
                self.m.explored = self.explored

                #print("\nStates explored: ", self.num_explored)
                #print("Found Solution.")
                self.sol = self.m.output_image(filename='..\mazeSolution.png', 
                                                show_solution=True,
                                                show_explored=True)
                #print("\nCreated Solution image.")
                return

            # Mark node as explored
            self.explored.add(node.state)
            # Creating a list which will hold the distances along with (action, state)
            distances = []
        
            # Add neighbors to frontier
            for action, state in self.m.neighbors(node.state):
                if not self.frontier.contains_state(state) and state not in self.explored:
                    distances.append((self.heuristic(self.start.state, state, self.m.goal), (action, state)))
            
            if distances is None:
                print(state, "\n")
                # Doing this we go to the next-best state with the same parent node but different heuristic value.
                continue
            else:
                distances = sorted(distances)
                for d in distances:
                    child = Node(state=d[1][1], parent=node, action=d[1][0])
                    self.frontier.add(child)
            del distances
