

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
                paths = dfs_cycles(graph, begin, related, path, paths)
        path.pop()        
        return paths

    cycles = []
    for node in graph.iterkeys():
        cycles.append(dfs_cycles(graph, node, node))
    if any(map(lambda x: len(x) > 0, cycles)):
        return True  # Error when at lees one cycle present
    return False

def get_end_nodes(graph):
    return [node for node, childs in graph.iteritems() if not childs]

def get_start_nodes(graph):
    start_nodes = []
    all_childs = []
    for value in graph.itervalues():
        all_childs += value
    all_childs = set(all_childs)
    for node in graph.iterkeys():
        if node not in all_childs:
            start_nodes.append(node)
    return start_nodes

def build_queue3(graph):
    if not graph:
        return []

    def find_all_paths(graph, start, end, path=[]):
        path = path + [start]
        if start in end:
            return [path]
        if not graph.has_key(start):
            return []
        paths = []
        for node in graph[start]:
            if node not in path:
                newpaths = find_all_paths(graph, node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

    critical_time_map = {node: 0 for node in graph.iterkeys()}
    end_nodes = get_end_nodes(graph)
    for node in graph.iterkeys():
        all_paths = find_all_paths(graph, node, end_nodes)
        critical_time = sum(map(lambda n: int(n.weight), all_paths[0]))
        for path in all_paths[1:]:
            path_time = sum(map(lambda n: int(n.weight), path))
            if path_time < critical_time:
                critical_time = path_time
        critical_time_map[node] = critical_time
    queue3 = sorted(critical_time_map.iteritems(), key=lambda (k,v): v, reverse=True)
    # map(
    #     lambda (node, time): node, 
    #     sorted(critical_time_map.iteritems(), key=lambda (k,v): v, reverse=True)
    # )
    return queue3


