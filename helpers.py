

def create_graph(node_list, line_list, mode_type):
    if len(node_list) == 0:
        return
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
    if not graph:
        return False
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
        return True  # it's mean that error present
    return False

def check_task_graph(graph):
    if not graph:
        return False

    def dfs_cycles(graph, begin, current, path = [], paths = []):
        path.append(current)
        for related in graph[current]:
            if related == begin and len(path) > 2:
                paths.append(list(path))
            if related not in path:
                paths = algo(graph, begin, related, path, paths)
        path.pop()        
        return paths

    cycles = []
    for node in graph.iterkeys():
        cycles.append(algo(graph, node, node))
    if any(map(lambda x: len(x) > 0, cycles)):
        return True  # Error when at lees one cycle present
    return False
