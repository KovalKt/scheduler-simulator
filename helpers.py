from math import ceil
from random import randint
from Objects import Line, Node, Gant_diagram

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

def build_queue3(graph):
    if not graph:
        return []

    critical_time_map = {node: 0 for node in graph.iterkeys()}
    end_nodes = get_end_nodes(graph)
    for node in graph.iterkeys():
        all_paths = find_all_paths(graph, node, end_nodes)
        critical_time = sum(map(lambda n: int(n.weight), all_paths[0]))
        for path in all_paths[1:]:
            path_time = sum(map(lambda n: int(n.weight), path))
            if path_time > critical_time:
                critical_time = path_time
        critical_time_map[node] = critical_time
    queue3 = sorted(critical_time_map.iteritems(), key=lambda (k,v): v, reverse=True)
    # map(
    #     lambda (node, time): node, 
    #     sorted(critical_time_map.iteritems(), key=lambda (k,v): v, reverse=True)
    # )
    return queue3

def invert_graph(graph):
    new_graph = {node: set() for node in graph.iterkeys()}
    # for k,v in graph.iteritems():
    #     print k, v
    for node, childs in graph.iteritems():
        for child in childs:
            new_graph[child].add(node)
    # for k,v in new_graph.iteritems():
    #     print k, v
    return new_graph


def build_queue8(graph):
    if not graph:
        return

    graph = invert_graph(graph)
    critical_count_map = {node: 0 for node in graph.iterkeys()}
    end_nodes = get_end_nodes(graph)
    for node in graph.iterkeys():
        all_paths = find_all_paths(graph, node, end_nodes)
        critical_count = max(map(lambda p: len(p)-1, all_paths))
        critical_count_map[node] = critical_count
        # print 'crit count --- ', node, critical_count
    queue8 = sorted(critical_count_map.iteritems(), key=lambda (k,v): int(k.weight), reverse=True)
    return map(lambda (n, c): (n, c, int(n.weight)), sorted(queue8, key=lambda (n,c): c))

def find_connections_and_invert_graph(graph):
    inverted_graph = invert_graph(graph)
    connections_map = {node: len(graph[node]) + len(inverted_graph[node]) for node in graph.iterkeys()}
    return inverted_graph, connections_map


def build_queue11(graph):
    if not graph:
        return

    graph, connections_map = find_connections_and_invert_graph(graph)
    critical_count_map = {node: 0 for node in graph.iterkeys()}
    end_nodes = get_end_nodes(graph)
    for node in graph.iterkeys():
        all_paths = find_all_paths(graph, node, end_nodes)
        critical_count = max(map(lambda p: len(p)-1, all_paths))
        critical_count_map[node] = critical_count
    queue11 = sorted(critical_count_map.iteritems(), key=lambda (n,c): c)
    return map(lambda (k,v): (k,connections_map[k],v), sorted(queue11, key=lambda (n,c): connections_map[n], reverse=True))

def generate_graph_hendler():
    try:
        min_node_weight = int(raw_input('Input MIN Node weight: '))
    except ValueError:
        print "Not a number"
    try:
        max_node_weight = int(raw_input('Input MAX Node weight: '))
    except ValueError:
        print "Not a number"
    try:
        n_count = int(raw_input('Input Node number: '))
    except ValueError:
        print "Not a number"
    try:
        correlation = float(raw_input('Input correlation: '))
    except ValueError:
        print "Not a number"
    try:
        min_line_weight = int(raw_input('Input MIN Line weight: '))
    except ValueError:
        print "Not a number"
    try:
        max_line_weight = int(raw_input('Input MAX Line weight: '))
    except ValueError:
        print "Not a number"

    # print min_node_weight, max_node_weight, n_count, correlation, min_line_weight, max_line_weight
    node_weight = [randint(min_node_weight, max_node_weight) for x in range(n_count)]
    node_list = []
    for indx, weight in enumerate(node_weight):
        new_node = Node(indx+1, 50+20*indx, 50+10*indx)
        new_node.weight = weight
        node_list.append(new_node)
    sum_node_weight = sum(node_weight)
    sum_line_weight = int(round(sum_node_weight/correlation - sum_node_weight))
    # max_line_count = sum([n_count - i for i in range(1, n_count)])

    l_count = 0
    l_list = []
    current_sum_weight = 0
    line_ends, max_line_count = get_lines_ends(n_count)
    while l_count < max_line_count:
        new_weight = randint(min_line_weight, max_line_weight)
        current_sum_weight += new_weight
        l_count += 1
        new_line = Line(l_count, 0, 0)
        new_line.weight = new_weight
        l_list.append(new_line)
        if current_sum_weight == sum_line_weight:
            break
        if (sum_line_weight - current_sum_weight) <= 0:
            new_line.weight = sum_line_weight
            break
        if 0 < (sum_line_weight - current_sum_weight) <= max_line_weight:
            l_count += 1
            new_line = Line(l_count, 0, 0)
            new_line.weight = sum_line_weight - current_sum_weight
            l_list.append(new_line)
            current_sum_weight += new_line.weight
            break

    if l_count == max_line_count and current_sum_weight != sum_line_weight:
        diff = sum_line_weight - current_sum_weight
        while diff > 0:
            add_weight = randint(1, int(ceil(diff/2.0)))
            line = min(l_list, key=lambda l: l.weight)
            line.weight += add_weight
            diff -= add_weight

    for line in l_list:
        end_number = randint(0, len(line_ends)-1)
        from_id, to_id = line_ends[end_number]
        line.from_node = node_list[from_id-1]
        line.to_node = node_list[to_id-1]
        line_ends.remove((from_id, to_id))

    # node_list = organize_graph_location(node_list, l_list)
    return node_list, l_list


def organize_graph_location(node_list, line_list):
    pass

def generate_gant_hendler(proc_list, tasks_queue, task_graph):
    diagram = Gant_diagram(tasks_queue)
    diagram.prepare_data(proc_list)
    diagram.first_assign_algorithm(task_graph)




def get_lines_ends(node_count):
    max_line_count = sum([node_count - i for i in range(1, node_count)])
    line_ends = []
    for i in range(1, node_count):
        for j in range(i+1, node_count+1):
            line_ends.append((i, j))
    return line_ends, max_line_count 