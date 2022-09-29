import math as m
import pygame as game

game.init()

WIDTH = 800
HEIGHT = 800
window = game.display.set_mode((WIDTH, HEIGHT))

depth = 8
BACKGROUND = (0, 0, 0)
colour = (255, 255, 255)


class Triangle:
    def __init__(self, vertices, _depth):
        # order of vertices is clockwise starting at the top
        self.vertices = vertices
        self.children = []
        self.depth = _depth

    def new_triangles(self):
        self.children = []

        tri1 = [
            self.vertices[0],
            [self.vertices[0][0] + (self.vertices[1][0]-self.vertices[0][0])/2, self.vertices[0][1] + (self.vertices[1][1]-self.vertices[0][1])/2],
            [self.vertices[2][0] + (self.vertices[0][0]-self.vertices[2][0])/2, self.vertices[0][1] + (self.vertices[1][1]-self.vertices[0][1])/2]
        ]

        tri2 = [
            [self.vertices[0][0] + (self.vertices[1][0]-self.vertices[0][0])/2, self.vertices[0][1] + (self.vertices[1][1]-self.vertices[0][1])/2],
            self.vertices[1],
            [self.vertices[0][0], self.vertices[1][1]]
        ]

        tri3 = [
            [self.vertices[2][0] + (self.vertices[0][0]-self.vertices[2][0])/2, self.vertices[0][1] + (self.vertices[1][1]-self.vertices[0][1])/2],
            [self.vertices[0][0], self.vertices[1][1]],
            self.vertices[2]
        ]


        self.children.append(Triangle(tri1, self.depth+1))
        self.children.append(Triangle(tri2, self.depth+1))
        self.children.append(Triangle(tri3, self.depth+1))

    def draw(self):
        game.draw.line(window, colour, self.vertices[0], self.vertices[1])
        game.draw.line(window, colour, self.vertices[1], self.vertices[2])
        game.draw.line(window, colour, self.vertices[2], self.vertices[0])


s_length = 700
to_draw = []
curr_tris = []

def generate_tris():
    global to_draw, curr_tris

    left_coord = [50, HEIGHT - 50]
    right_coord = [left_coord[0] + s_length, HEIGHT - 50]
    top_coord = [left_coord[0] + (s_length/2), left_coord[1] - m.sqrt((3/4) * s_length**2)]

    main_triangle = Triangle([top_coord, right_coord, left_coord], 1)
    # 3c^2 / 4 = h^2
    to_draw = [main_triangle]

    curr_tris = [main_triangle]
    count_depth = depth

    while count_depth:
        if main_triangle.vertices[1][0] < WIDTH * 2.5:
            replic_curr = curr_tris[:]
            curr_tris = []
            for tri in replic_curr:
                tri.new_triangles()
                for child in tri.children:
                    if child.vertices[1][0] < WIDTH * 2.5:
                        to_draw.append(child)
                        curr_tris.append(child)
                    else:
                        del child
            count_depth -= 1
        else:
            main_triangle.new_triangles()
            main_triangle = main_triangle.children[2]
            to_draw = [main_triangle]
            curr_tris = [main_triangle]



def calculate_tris_by_depth(depth):
    total = 0
    for x in range(0, depth+1):
        total += 3**x
    return total

scroll = False
scroll_speed = 0.1

generate_tris()

count = 0
running = True
while running:
    for event in game.event.get():
        if event.type == game.QUIT:
            running = False
        elif event.type == game.KEYDOWN:
            if event.key == game.K_SPACE:
                depth += 1
                generate_tris()
            elif event.key == game.K_s:
                scroll = 1 - scroll

    window.fill(BACKGROUND)
        
    changed = False
    for tri in to_draw:
        tri.draw()
        if tri.vertices[1][0] > WIDTH * 2.5:
            del to_draw[to_draw.index(tri)]
            
    if scroll:
        s_length *= 1.01
        generate_tris()

    count += 1

    game.display.update()
