import heapq

def find_safe_route(graph, start, end, blocked_nodes):
    """
    Finds the shortest path between two locations considering blocked nodes using Dijkstra's algorithm.
    Args:
        graph (list): N x N adjacency matrix where graph[i][j] is travel time (0 means no path).
        start (int): Index of the starting node.
        end (int): Index of the destination node.
        blocked_nodes (list): Indices of nodes that are closed for maintenance.
    Returns:
        tuple: (list of node indices for the shortest path, total travel time).
               Return ([], -1) if no path exists.
    """
    # Edge case: if the start or end node is blocked
    if start in blocked_nodes or end in blocked_nodes:
        return ([], -1)
    # Base case: if the start and end nodes are the same
    if start == end:
        return ([start], 0)

        
    n = len(graph)

    # time[i] will store the minimum time to reach node i from the start node
    time = {node: float('inf') for node in range(n)} # Initialize nodes with infinite time
    time[start] = 0 # time taken to reach the start node from itself is 0 !
    
    # predecessors[i] will store the node that precedes node i in the shortest path, mainly used to reconstruct the path
    predecessors = {node: None for node in range(n)} # Initialize predecessors to None
    
    # Priority queue stores (time, node)
    pq = []
    heapq.heappush(pq, (0, start)) # initialized with the start node and time 0
    
    while pq: # iterate while the priority queue is not empty
        current_time, current_node = heapq.heappop(pq) # take the top element (minimum time)
        
        # If we reached the end node, we can stop
        if current_node == end:
            break
            
        # If we found a longer path to reach the current node, ignore it, because all paths from here will be longer too
        if current_time > time[current_node]:
            continue
            
        # Explore neighbors
        for neighbor in range(n):
            weight = graph[current_node][neighbor]
            
            # 0 weight means no path and also skip the blocked nodes
            if weight > 0 and neighbor not in blocked_nodes:
                new_time = current_time + weight
                
                if new_time < time[neighbor]: # if we found a shorter path to the neighbor then update the time dict and predecessor dict
                    time[neighbor] = new_time
                    predecessors[neighbor] = current_node
                    heapq.heappush(pq, (new_time, neighbor)) # a valid (and shorter) path to the neighbor is found, push it to the priority queue to explore further
                    
    # Reconstruct path
    path = []
    curr = end
    if predecessors[curr] is None and curr != start: # if the end node is not reachable from the start node
        return ([], -1)
        
    while curr is not None: # trace back from the end node to the start node using the predecessors dict
        path.append(curr)
        curr = predecessors[curr]
    path.reverse() # path constructed will be end -> start, so we reverse it to get the path from start to end

    if time[end] != float('inf'): # if the end node is reachable from the start node
        return (path, int(time[end]))
    else: # if the end node is not reachable from the start node
        return ([], -1)

if __name__ == "__main__":
    graph = [
        [0, 5, 0, 8, 0],
        [5, 0, 3, 0, 0],
        [0, 3, 0, 2, 7],
        [8, 0, 2, 0, 4],
        [0, 0, 7, 4, 0]
    ]
    start_node = 0
    end_node = 4
    blocked = [3]  # Node 3 is closed
    
    result = find_safe_route(graph, start_node, end_node, blocked)
    print(f"Shortest path from {start_node} to {end_node} avoiding nodes {blocked}:")
    print(result)
    
    # Expected: ([0, 1, 2, 4], 15)
    # 0 -> 1 (5)
    # 1 -> 2 (3)
    # 2 -> 4 (7)
    # Total: 15
