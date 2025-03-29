from dataclasses import dataclass
from collections import deque


def rotate_left(point, center):
    x, y = point
    c1, c2 = center
    return int((y-c2)+c1), int(-(x-c1)+c2)


def rotate_right(point, center):
    x, y = point
    c1, c2 = center
    return int(-(y-c2)+c1), int((x-c1)+c2)


@dataclass
class Face:
    nbs: deque
    walls: set
    dim: int
    offset: tuple
    rot: int = 0

    def rotate_left(self):
        walls_r = set()
        c = (self.dim-1)/2  # center of rotation
        for p in self.walls:
            walls_r.add(rotate_left(p, (c, c)))
        self.walls = walls_r
        self.nbs.rotate(-1)
        self.rot = (self.rot-1) % 4

    def rotate_right(self):
        walls_r = set()
        c = (self.dim-1)/2  # center of rotation
        for p in self.walls:
            walls_r.add(rotate_right(p, (c, c)))
        self.walls = walls_r
        self.nbs.rotate(1)
        self.rot = (self.rot+1) % 4

    def print(self):
        for y in range(self.dim):
            row = ''
            for x in range(self.dim):
                row += '#' if (x, y) in self.walls else '.'
            print(row)
        print()

    @property
    def right(self):
        return self.nbs[0]

    @property
    def left(self):
        return self.nbs[2]


class Cube:
    def __init__(self, data, dim):
        data = data.splitlines()
        bad = [[1, 2, 3, 5], [4, 2, 0, 5], [1, 4, 3, 0], [4, 5, 0, 2], [1, 5, 3, 2], [4, 1, 0, 3]]

        self.faces = []
        for cy in range(0, len(data), dim):  # per face
            for cx in range(0, len(data[cy]), dim):
                if data[cy][cx] == ' ':  # no face
                    continue

                walls = set()
                for y in range(dim):
                    for x in range(dim):
                        if data[cy+y][cx+x] == '#':
                            walls.add((x, y))

                self.faces.append(Face(walls=walls, nbs=deque(bad[len(self.faces)]), dim=dim, offset=(cx, cy)))

        for f in self.faces:  # chance idx to reference
            f.nbs = deque([self.faces[i] for i in f.nbs])


def print_passwd(x, y, r, face):
    r = (r-face.rot) % 4

    for _ in range(face.rot):
        x, y = rotate_left((x, y), (face.dim/2, face.dim/2))

    x = x + face.offset[0]
    y = y + face.offset[1]

    print(x, y, r, 1000*y + 4*x + r)


def gen_passwd(data):
    data, commands = data.split('\n\n')

    # parse commands
    movements = list(map(int, commands.replace('R', ' ').replace('L', ' ').split()))
    rotations = [x for x in commands if x in 'RL']
    inputs = [x for t in zip(movements, rotations) for x in t] + [movements[-1]]

    dim = 50  # dim of faces
    cube = Cube(data, dim)

    face = cube.faces[0]  # top-left

    x = y = r = 0

    for ipt in inputs:
        match ipt:
            case int():
                for _ in range(ipt):
                    if x < dim-1:  # if next tile on same face
                        if (x, y) not in face.walls:
                            x += 1
                        else:  # hit wall
                            break
                    else:
                        # orient next face to line up
                        while face is not face.right.left:
                            face.right.rotate_right()
                        if (x, y) not in face.right.walls:
                            # move to next face
                            face = face.right
                            x = 0
                        else:  # hit wall
                            break

            case 'R':
                r = (r+1) % 4
                # counter rotate
                x, y = rotate_left((x, y), (dim/2, dim/2))
                face.rotate_left()
            case 'L':
                r = (r-1) % 4
                # counter rotate
                x, y = rotate_right((x, y), (dim/2, dim/2))
                face.rotate_right()

        print_passwd(x, y, r, face)

    # "rotate face" back to 0
    r = (r-face.rot) % 4

    # rotate player with face
    for _ in range(face.rot):
        x, y = rotate_left((x, y), (face.dim/2, face.dim/2))

    x = x + face.offset[0]
    y = y + face.offset[1]

    return 1000*y + 4*x + r


with open('input.txt') as f:
    pzl = f.read()

print(gen_passwd(pzl))