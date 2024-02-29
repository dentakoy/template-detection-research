# Calculate the centroid of a polygon

# Original idea: https://stackoverflow.com/a/75699257
# Thanks to harriet! https://stackoverflow.com/users/17433572/harriet

class NotEnoughtVertices(Exception):
    pass


def centroid(vertices, n = None) -> tuple[int, int]:
    x, y    = 0, 0
    n       = len(vertices) if n is None else n
    
    if (n < 3):
        raise NotEnoughtVertices('More than 2 vertices are expected.')
    
    signed_area = 0
    for i in range(n):
        x0, y0 = vertices[i]
        x1, y1 = vertices[(i + 1) % n]
        # shoelace formula
        area = (x0 * y1) - (x1 * y0)
        signed_area += area
        x += (x0 + x1) * area
        y += (y0 + y1) * area
    signed_area *= 0.5
    x /= 6 * signed_area
    y /= 6 * signed_area
    return int(x), int(y)
