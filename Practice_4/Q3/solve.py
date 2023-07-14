# coding: utf-8
def solve(a, b, centers, radiuses):
    import numpy as np
    grid_size = 1000
    cell_area = (a * b) / (grid_size ** 2)
    total_covered_area = 0

    for i in range(grid_size):
        for j in range(grid_size):
            cell_x = a * (i + 0.5) / grid_size
            cell_y = b * (j + 0.5) / grid_size
            cell_covered = False

            for k in range(len(centers)):
                antenna_x, antenna_y = centers[k]
                radius = radiuses[k]
                distance = np.sqrt((cell_x - antenna_x) ** 2 + (cell_y - antenna_y) ** 2)

                if distance <= radius:
                    cell_covered = True
                    break

            if cell_covered:
                total_covered_area += cell_area

    return total_covered_area
