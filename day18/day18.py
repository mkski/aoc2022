inputs = [tuple(map(int, l.split(","))) for l in open("in").read().split("\n")]
test = [tuple(map(int, l.split(","))) for l in open("in-test").read().split("\n")]


def touching(c1, c2):
    return (
        (abs(c1[0] - c2[0]) == 1 and c1[1] == c2[1] and c1[2] == c2[2]) or
        (abs(c1[1] - c2[1]) == 1 and c1[0] == c2[0] and c1[2] == c2[2]) or
        (abs(c1[2] - c2[2]) == 1 and c1[0] == c2[0] and c1[1] == c2[1])
    )


def surface_area(inputs, air=[]):
    area = 0
    xmin, xmax = ymin, ymax = zmin, zmax = 999, 0
    for c1 in inputs:
        n_touching = 0
        xmin, xmax = min([xmin, c1[0]]), max([xmax, c1[0]])
        ymin, ymax = min([ymin, c1[1]]), max([ymax, c1[1]])
        zmin, zmax = min([zmin, c1[2]]), max([zmax, c1[2]])
        for c2 in inputs:
            if touching(c1, c2):
                n_touching += 1
        area += 6 - n_touching
    return area, xmin, xmax, ymin, ymax, zmin, zmax


def get_air_bubbles(inputs, xmin, xmax, ymin, ymax, zmin, zmax):
    bubbles = []
    for x in range(xmin, xmax+1):
        for y in range(ymin, ymax+1):
            for z in range(zmin, zmax+1):
                n_touching = 0
                if (x, y, z) in inputs:
                    continue

                for c in inputs:
                    if touching(c, (x, y, z)):
                        n_touching += 1

                if n_touching == 6:
                    bubbles.append((x, y, z))
    return bubbles


area, *minmax = surface_area(inputs)
print(area)
air_bubbles = get_air_bubbles(inputs, *minmax)
air_area, *_ = surface_area(air_bubbles)
print(area - air_area - len(air_bubbles))
