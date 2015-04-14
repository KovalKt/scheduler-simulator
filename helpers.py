

def create_graph(node_list, line_list, mode_type):
    keys = set(node_list)
    graph = {key: set() for key in keys}
    for key in keys:
        for line in line_list:
            if line.from_node == key:
                graph[key].add(line.to_node)
            elif line.to_node == key and mode_type == 'system':
                graph[key].add(line.from_node)
    return graph

def check_system_graph(graph):
    visited_node = set()
    def dfs(graph, start, visited=None):
        if visited is None:
            visited = set()
        visited.add(start)
        for next in graph[start] - visited:
            dfs(graph, next, visited)
        return visited

    start_node = max(graph.iteritems(), key=lambda (k, v): len(v))
    visited_node = dfs(graph, start_node[0])
    if len(visited_node) < len(graph.keys()):
        return True  # it mean that error present
    return False

def check_task_graph(graph):
    pass

