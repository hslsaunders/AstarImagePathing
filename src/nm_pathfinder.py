from math import sqrtfrom heapq import heappush, heappopno_path_str = "No path!"def old_find_path(source_point, destination_point, mesh):    """    Searches for a path from source_point to destination_point through the mesh    Args:        source_point: starting point of the pathfinder        destination_point: the ultimate goal the pathfinder must reach        mesh: pathway constraints the path adheres to    Returns:        A path (list of points) from source_point to destination_point if exists        A list of boxes explored by the algorithm    """    detail_points = {}    predecessors = {}    cost = {}    source_box = None    dest_box = None    for box in mesh["boxes"]:        if pos_inside_box(source_point, box):            source_box = box            detail_points[source_box] = source_point        if pos_inside_box(destination_point, box):            dest_box = box            detail_points[dest_box] = destination_point    if source_box is None or dest_box is None:        print(no_path_str)        return [], []    if source_box == dest_box:        return [source_point, destination_point], [source_box]    open_boxes = []    heappush(open_boxes, (0, source_box))    predecessors[source_box] = None    cost[source_box] = 0    while open_boxes:        priority, current_box = heappop(open_boxes)        curr_detail_point = detail_points[current_box]        if current_box == dest_box:            path = trace_path(predecessors, detail_points, current_box, destination_point)            print(path)            return path, detail_points.keys()        curr_cost = cost[current_box]        for neighbor in mesh["adj"][current_box]:            edge_point = clamp_pos_in_box(curr_detail_point, neighbor)            path_cost = curr_cost + dist(curr_detail_point, edge_point)            if neighbor not in cost or path_cost < cost[neighbor]:                cost[neighbor] = path_cost                new_priority = path_cost + heuristic(edge_point, destination_point)                heappush(open_boxes, (new_priority, neighbor))                predecessors[neighbor] = current_box                detail_points[neighbor] = edge_point    print(no_path_str)    return [], detail_points.keys()def find_path(source_point, destination_point, mesh):    old_find_path(source_point, destination_point, mesh)    """    Searches for a path from source_point to destination_point through the mesh    Args:        source_point: starting point of the pathfinder        destination_point: the ultimate goal the pathfinder must reach        mesh: pathway constraints the path adheres to    Returns:        A path (list of points) from source_point to destination_point if exists        A list of boxes explored by the algorithm    """    detail_points = {}    forward_predecessors = {}    back_predecessors = {}    forward_cost = {}    back_cost = {}    source_box = None    dest_box = None    for box in mesh["boxes"]:        if pos_inside_box(source_point, box):            source_box = box            detail_points[source_box] = source_point        if pos_inside_box(destination_point, box):            dest_box = box            detail_points[dest_box] = destination_point    if source_box is None or dest_box is None:        print(no_path_str)        return [], []    if source_box == dest_box:        return [source_point, destination_point], [source_box]    open_boxes = []    heappush(open_boxes, (0, source_box, True))    heappush(open_boxes, (0, dest_box, False))    forward_predecessors[source_box] = None    forward_cost[source_box] = 0.0    back_predecessors[dest_box] = None    back_cost[dest_box] = 0.0    while open_boxes:        priority, current_box, isForward = heappop(open_boxes)        curr_detail_point = detail_points[current_box]        if isForward and current_box in back_cost or not isForward and current_box in forward_cost:            path = trace_path(forward_predecessors, detail_points, current_box, destination_point)            path.pop()            secondHalf = trace_path(back_predecessors, detail_points, current_box, source_point)            secondHalf.pop()            secondHalf.reverse()            path += secondHalf            return path, detail_points.keys()        if isForward:            curr_cost = forward_cost[current_box]        else:            curr_cost = back_cost[current_box]        dest = destination_point if isForward else source_point        costDict = forward_cost if isForward else back_cost        predecessors = forward_predecessors if isForward else back_predecessors        for neighbor in mesh["adj"][current_box]:            edge_point = clamp_pos_in_box(curr_detail_point, neighbor)            path_cost = curr_cost + dist(curr_detail_point, edge_point)            if neighbor not in costDict or path_cost < costDict[neighbor]:                costDict[neighbor] = path_cost                new_priority = path_cost + heuristic(edge_point, dest)                heappush(open_boxes, (new_priority, neighbor, isForward))                predecessors[neighbor] = current_box                detail_points[neighbor] = edge_point    print(no_path_str)    return [], detail_points.keys()def trace_path(predecessors, detail_points, node_box, destination):    path = [destination]    while node_box is not None:        path.insert(0, detail_points[node_box])        node_box = predecessors[node_box]    return pathdef pos_inside_box(pos, box):    return box[0] <= pos[0] <= box[1] and box[2] <= pos[1] <= box[3]def clamp(num, min_value, max_value):    return max(min(num, max_value), min_value)def clamp_pos_in_box(pos, box_corners):    xPos = pos[0]    yPos = pos[1]    boxMinX = box_corners[0]    boxMaxX = box_corners[1]    boxMinY = box_corners[2]    boxMaxY = box_corners[3]    return clamp(xPos, boxMinX, boxMaxX), clamp(yPos, boxMinY, boxMaxY)def dist(pos1, pos2):    x1 = pos1[0]    y1 = pos1[1]    x2 = pos2[0]    y2 = pos2[1]    x = x2 - x1    y = y2 - y1    return sqrt(x * x + y * y)def heuristic(pos1, pos2):    return abs(pos2[0] - pos1[0]) + abs(pos2[1] - pos1[1])