def linear_distance(p1, p2):
    p1x, p1y = p1.get_coord()
    p2x, p2y = p2.get_coord()
    
    return max([abs(p2x - p1x), abs(p2y - p1y)])
