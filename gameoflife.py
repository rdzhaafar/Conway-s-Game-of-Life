'''
John Conway's Game of Life implementation using pygame.
This implementation tries to emulate an infinite screen by wrapping edges of the window around like they would be in a sphere.
This means that the left-most top cells' neighbor to the top left is actually the bottom right-most cell.
The reason for this is that it avoids having a dead space near the edges of the window and more efficient than emulating a 500x500 game
while displaying only the 450x450 cells at the center.
'''

import random
import pygame

def update(cell, n1, n2, n3, n4, n5, n6, n7, n8):
    nsum = n1 + n2 + n3 + n4 + n5 + n6 + n7 + n8
    if cell:
        if nsum < 2:
            return 0
        elif nsum < 4:
            return 1
        else:
            return 0
    else:
        if nsum == 3:
            return 1
        else:
            return 0
    
def step(cells):
    '''
    Calculate the next generation of cells based on the current cells.
    '''
    new = []
    lh = len(cells)-1
    lw = len(cells[0])-1
    for h in range(lh+1):
        row = []
        for w in range(lw+1):
            cur = cells[h][w]
            if h == 0:
                if w == 0:
                    # h = 0 and w = 0
                    row.append(update(
                        cur,
                        cells[lh][lw], # top left
                        cells[lh][0],   # top center
                        cells[lh][1], # top right
                        cells[0][lw],   # center left
                        cells[h][w+1],   # center right
                        cells[1][lw], # bottom left
                        cells[h+1][w],   # bottom center
                        cells[h+1][w+1]  # bottom right
                    ))
                elif w != 0 and w != lw:
                    # h = 0 and w in middle
                    row.append(update(
                        cur,
                        cells[lh][w-1], # top left
                        cells[lh][w],   # top center
                        cells[lh][w+1], # top right
                        cells[h][w-1],   # center left
                        cells[h][w+1],   # center right
                        cells[h+1][w-1], # bottom left
                        cells[h+1][w],   # bottom center
                        cells[h+1][w+1]  # bottom right
                    ))
                else:
                    # h = 0 and w = lw
                    row.append(update(
                        cur,
                        cells[lh][lw-1], # top left
                        cells[lh][lw],   # top center
                        cells[lh][0], # top right
                        cells[h][w-1],   # center left
                        cells[0][0],   # center right
                        cells[h+1][w-1], # bottom left
                        cells[h+1][w],   # bottom center
                        cells[1][lw]  # bottom right
                    ))
            elif h != 0 and h != lh:
                if w == 0:
                    # h in middle and w = 0
                    row.append(update(
                        cur,
                        cells[h-1][lw], # top left
                        cells[h-1][w],   # top center
                        cells[h-1][w+1], # top right
                        cells[h][lw],   # center left
                        cells[h][w+1],   # center right
                        cells[h+1][lw], # bottom left
                        cells[h+1][w],   # bottom center
                        cells[h+1][w+1]  # bottom right
                    ))
                elif w != 0 and w != lw:
                    # i in middle and j in middle
                    row.append(update(cur,
                        cells[h-1][w-1], # top left
                        cells[h-1][w],   # top center
                        cells[h-1][w+1], # top right
                        cells[h][w-1],   # center left
                        cells[h][w+1],   # center right
                        cells[h+1][w-1], # bottom left
                        cells[h+1][w],   # bottom center
                        cells[h+1][w+1]  # bottom right
                    ))
                else:
                    # h in middle and w = lj
                    row.append(update(cur,
                        cells[h-1][w-1], # top left
                        cells[h-1][w],   # top center
                        cells[h-1][0], # top right
                        cells[h][w-1],   # center left
                        cells[h][0],   # center right
                        cells[h+1][w-1], # bottom left
                        cells[h+1][w],   # bottom center
                        cells[h+1][0]  # bottom right
                    ))
            else:
                if w == 0:
                    # h = li and w = 0
                    row.append(update(cur,
                        cells[lh-1][lw], # top left
                        cells[h-1][w],   # top center
                        cells[h-1][w+1], # top right
                        cells[lh][lw],   # center left
                        cells[h][w+1],   # center right
                        cells[0][lw], # bottom left
                        cells[0][0],   # bottom center
                        cells[0][1]  # bottom right
                    ))
                elif w != 0 and w != lw:
                    # h = li and w in middle
                    row.append(update(cur,
                        cells[h-1][w-1], # top left
                        cells[h-1][w],   # top center
                        cells[h-1][w+1], # top right
                        cells[h][w-1],   # center left
                        cells[h][w+1],   # center right
                        cells[0][w-1], # bottom left
                        cells[0][w],   # bottom center
                        cells[0][w+1]  # bottom right
                    ))
                else:
                    # h = li and w = lj
                    row.append(update(cur,
                        cells[h-1][w-1], # top left
                        cells[h-1][w],   # top center
                        cells[lh-1][0], # top right
                        cells[h][w-1],   # center left
                        cells[lh][0],   # center right
                        cells[0][lw-1], # bottom left
                        cells[0][lw],   # bottom center
                        cells[0][0]  # bottom right
                    ))
        new.append(row)
    return new

def generate(h, w):
    '''
    Generate cells.
    '''
    cells = []
    for _ in range(h):
        row = []
        for _ in range(w):
            row.append(random.choice([0, 1]))
        cells.append(row)
    return cells

def draw(screen, cells, scalef):
    '''
    Draw the cells onto the screen.
    Args:
        screen (pygame.display): surface to draw onto
        cells  (int[][]): cells to draw
        scalef (int): scale factor.
    '''
    screen.fill((255, 255, 255))
    for i in range(len(cells)-1):
        for j in range(len(cells[i])-1):
            if cells[i][j]:
                startx, starty = i * scalef, j * scalef
                for ii in range(scalef):
                    for jj in range(scalef):
                        screen.set_at((startx+ii, starty+jj), (0,0,0))
    pygame.display.flip()

def main():
    pygame.init()
    screen = pygame.display.set_mode([600, 600])
    pygame.display.set_caption("Conway's Game of Life")
    running = True
    cells = generate(100, 100)
    draw(screen, cells, 6)

    #Main loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        cells = step(cells)
        draw(screen, cells, 6)

    pygame.quit()


if __name__=="__main__":
    main()