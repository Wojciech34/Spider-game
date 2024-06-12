from collections import deque

def get_avaible_moves(start_pos, moves, is_spider=False):
    avaible_places = set()

    def reku(v, i):
        i -= 1
        for w in v.conns_map.values():
            # any figure blocks a move
            if not w.figure:
                avaible_places.add(w)
                if i > 0:
                    reku(w, i)
            # there is a figure but we are a spider so we can eat them ^^
            elif is_spider:
                avaible_places.add(w)
    
    reku(start_pos, moves)

    return avaible_places


def get_distance(places, pos1, pos2):


    def dijkstra_algorithm(places, start_place, stop_place):
        visited = [False for place in places]
        queue = deque()

        visited[start_place.c] = True
        for v in start_place.conns_map.values():
            queue.append((v, 1))

        while len(queue) > 0:
            v, distance = queue.popleft()
            if v.c == stop_place.c:
                return distance
            visited[v.c] = True
            for w in v.conns_map.values():
                if not visited[w.c]:
                    queue.append((w, distance+1))
        return -1
    
    distance = dijkstra_algorithm(places, pos1, pos2)
    if distance != -1:
        return distance
    raise ValueError('did not manage to find path')