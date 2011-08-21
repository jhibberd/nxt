import math

class AStarSearchAlgorithm(object):
    """Implementation of the A* search algorithm used in pathfinding.
    
    http://en.wikipedia.org/wiki/A*_search_algorithm
    """

    def __init__(self, plane_width, plane_height):
        self.plane_width = plane_width
        self.plane_height = plane_height

    def _heuristic_cost_estimate(self, y, goal):
        return self._dist_between(y, goal)
     
    def _node_with_lowest_f_score(self, open_set, f_score):
        return min([(f_score[x], x) for x in open_set])[1]
     
    def _neighbor_nodes(self, p):
        px, py = p
        for x, y in [(px-1, py), (px+1, py), (px, py-1), (px, py+1)]:
            if x > -1 and y > -1 and\
               x < self.plane_width and y < self.plane_height:
                yield (x, y)
    
    def _dist_between(self, node_a, node_b):
        """Use the Pythagorean theorem to calculate the distance between two
        nodes.
        
        http://en.wikipedia.org/wiki/Pythagorean_theorem
        """
        node_a_x, node_a_y = node_a
        node_b_x, node_b_y = node_b
        edge_a = abs(node_a_x - node_b_x)
        edge_b = abs(node_a_y - node_b_y)
        return math.sqrt(math.pow(edge_a, 2.) + math.pow(edge_b, 2.))
    
    def reconstruct_path(self, came_from, current_node, path):
        if current_node in came_from:
            self.reconstruct_path(came_from, came_from[current_node], path)
        path.append(current_node)
     
    def search(self, start, goal, closed_set):
        closed_set = closed_set.copy()
        open_set = set()
        open_set.add(start)
        came_from = {}
         
        g_score = {start: 0}
        h_score = {start: self._heuristic_cost_estimate(start, goal)}
        f_score = {start: h_score[start]}
         
        while open_set:
            x = self._node_with_lowest_f_score(open_set, f_score)
            if x == goal:
                path = []
                self.reconstruct_path(came_from, came_from[goal], path)
                return path
            
            open_set.remove(x)
            closed_set.add(x)
            for y in self._neighbor_nodes(x):
                
                if y in closed_set:
                    continue
                tentative_g_score = g_score[x] + self._dist_between(x, y)
                
                if y not in open_set:
                    open_set.add(y)
                    tentative_is_better = True
                elif tentative_g_score < g_score[y]:
                    tentative_is_better = True
                else:
                    tentative_is_better = False
                    
                if tentative_is_better:
                    came_from[y] = x
                    g_score[y] = tentative_g_score
                    h_score[y] = self._heuristic_cost_estimate(y, goal)
                    f_score[y] = g_score[y] + h_score[y]
     
        return None
     

class DiscoveryManager(object):
    """Manages the movement of a robot through a plane so that it discovers
    all plane locations in the most efficient (fastest) way.
    """
    
    def __init__(self, plane_width, plane_height):
        
        self.plane_width = plane_width
        self.plane_height = plane_height
        self.search_algorithm = AStarSearchAlgorithm(plane_width, plane_height)
                
        # Define plane walls (closed set). In a real scenario this will be
        # detected in real-time as the robot moves within the plane.
        self.closed_set = set()
        self.closed_set.add((1, 0))
        self.closed_set.add((3, 0))
        self.closed_set.add((3, 1))        

        # Define starting point.
        self.current_pos = (0, 0)

        # Define undiscovered plane. Initially this will be the closed set. It 
        # is know that targets cannot exists at wall locations.
        self.discovered_set = set(self.closed_set)
        self.discovered_set.add(self.current_pos)
        
    def _get_next_goal(self):
        """Using the current discovered set, pick the next plane location to
        use as the robot's next goal.
        """
        for y in range(self.plane_height):
            for x in range(self.plane_width):
                p = (x, y)
                if p not in self.discovered_set:
                    return p
        return None     
    
    def next(self):  
        """Move the robot to the next goal.
        
        If there is no next goal then the plane has been completely discovered.
        If the search algorithm can find no path to the next goal then parts
        of the plane are undiscoverable.
        
        After a successful path has been identified, add all path locations
        to the discovered plane set and update the robot's current position.
        
        The last goal and path are preserved in state so aid rendering
        functions.
        """
         
        goal = self._get_next_goal()
        if not goal:
            return False
            
        path = self.search_algorithm.search(
            self.current_pos, goal, self.closed_set)        
        if not path:
            raise Exception('Undiscoverable plane locations.')        
        
        self.discovered_set.add(goal)
        self.discovered_set.update(path)    
        self.current_pos = goal
        
        self.last_goal = goal
        self.last_path = path
                
        return True

# Rendering --------------------------------------------------------------------

PLANE_WIDTH = 6
PLANE_HEIGHT = 4
        
def render_current_path(
    offset_x, offset_y, plane_width, plane_height, goal, path, closed_set):
    for y in range(plane_height):
        for x in range(plane_width):
            p = (x, y)
            if p in path:
                color = 1
            elif p == goal:
                color = 2
            elif p in closed_set:
                color = 3
            else:
                color = 4
            stdscr.addch(offset_y+y, offset_x+x, ord(' '), 
                         curses.color_pair(color))    

def render_discovered_plane(
    offset_x, offset_y, plane_width, plane_height, discovered_set):
    for y in range(plane_height):
        for x in range(plane_width):
            p = (x, y)
            if p in discovered_set:
                color = 1
            else:
                color = 4
            stdscr.addch(offset_y+y, offset_x+x, ord(' '), 
                         curses.color_pair(color))   

import curses
try:
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)
    curses.start_color()
    
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_MAGENTA)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_WHITE)
    
    win = curses.newwin(PLANE_HEIGHT, PLANE_WIDTH, 0, 0)
    curses.curs_set(0)

    discovery_manager = DiscoveryManager(PLANE_WIDTH, PLANE_HEIGHT)

    while True:     
            
        more = discovery_manager.next()
        
        render_current_path(0, 0, PLANE_WIDTH, PLANE_HEIGHT, 
                            discovery_manager.last_goal, 
                            discovery_manager.last_path, 
                            discovery_manager.closed_set)
        render_discovered_plane(0, 10, PLANE_WIDTH, PLANE_HEIGHT, 
                                discovery_manager.discovered_set)
        stdscr.refresh()
        if not more:
            break        
        c = stdscr.getch()    
    
finally:
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()