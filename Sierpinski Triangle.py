import pygame as game

game.init()

window = game.display.set_mode((600, 600))

depth = 2
BACKGROUND = (0, 0, 0)
colour = (255, 255, 255)


class Triangle:
    def __init__(self, vertices):
        # order of vertices is clockwise starting at the top
        self.vertices = vertices
        self.children = []

    def new_triangles(self):
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


        self.children.append(Triangle(tri1))
        self.children.append(Triangle(tri2))
        self.children.append(Triangle(tri3))

    def draw(self):
        game.draw.line(window, colour, self.vertices[0], self.vertices[1])
        game.draw.line(window, colour, self.vertices[1], self.vertices[2])
        game.draw.line(window, colour, self.vertices[2], self.vertices[0])


main_triangle = Triangle([[300, 50], [550, 483], [50, 483]])
to_draw = [main_triangle]

count_depth = depth
curr_tris = [main_triangle]

while count_depth:
    count_depth -= 1
    replic_curr = curr_tris[:]
    curr_tris = []
    for tri in replic_curr:
        tri.new_triangles()
        for child in tri.children:
            to_draw.append(child)
            curr_tris.append(child)

count = 0
running = True
while running:
    for event in game.event.get():
        if event.type == game.QUIT:
            running = False
        elif event.type == game.KEYDOWN:
            if event.key == game.K_SPACE:
                depth += 1
                replic_curr = curr_tris[:]
                curr_tris = []
                for tri in replic_curr:
                    tri.new_triangles()
                    for child in tri.children:
                        to_draw.append(child)
                        curr_tris.append(child)


    window.fill(BACKGROUND)

    for tri in to_draw:
        tri.draw()

    count += 1

    game.display.update()
