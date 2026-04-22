from matplotlib.axes import Axes
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from helper import is_debug_active


def rectangle_area(point_pair):
    (x1, y1), (x2, y2) = point_pair
    return (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)


def run(input_data: str):
    part1, part2 = 0, 0
    red_tiles = [tuple(map(int, line.split(","))) for line in input_data.splitlines()]

    largest_rectangle_pair = (red_tiles[0], red_tiles[1])
    for i1, (x1, y1) in enumerate(red_tiles[1:]):
        for x2, y2 in red_tiles[i1 + 2 :]:
            if rectangle_area(((x1, y1), (x2, y2))) > rectangle_area(
                largest_rectangle_pair
            ):
                largest_rectangle_pair = ((x1, y1), (x2, y2))
    part1 = rectangle_area(largest_rectangle_pair)

    edges = [[], []]
    for i in range(len(red_tiles)):
        (x1, y1), (x2, y2) = red_tiles[i - 1], red_tiles[i]
        if x1 == x2:
            edges[0].append((x1, (y1, y2), i))
        elif y1 == y2:
            edges[1].append((y1, (x1, x2), i))
        else:
            raise Exception
    edges[0].sort()
    edges[1].sort()

    # Some beams near the start and end of each axis are outside the polygon,
    # but still included since only 1 axis is iterated over at once.
    # This doesnt affect results for the provided input, and require intensive code overhaul, thus will not be fixed.
    # Beams also overlap a lot, but this doesnt affect results or complexity, thus will not be fixed either.
    beams = [{}, {}]
    for axis, step in ((0, 1), (0, -1), (1, 1), (1, -1)):
        current_beams = []
        for x_current, (y_start, y_end), index_edge in edges[axis][::step]:
            beams[axis].setdefault(x_current, []).extend((
                (y_start, y_end),
                (y_end, y_start),
            ))
            new_beams = []
            for index_start_edge, y_beam in current_beams:
                if y_start < y_beam < y_end or y_start > y_beam > y_end:
                    beams[1 - axis].setdefault(y_beam, []).extend((
                        (
                            red_tiles[index_start_edge][axis],
                            x_current,
                        ),
                        (
                            red_tiles[(index_start_edge + 1) % len(red_tiles)][axis],
                            x_current,
                        ),
                    ))
                else:
                    new_beams.append((index_start_edge, y_beam))
            new_beams.append((index_edge, y_start))
            new_beams.append((index_edge, y_end))
            current_beams = new_beams
    plot(red_tiles, beams, largest_rectangle_pair)

    largest_rectangle_pair = (red_tiles[0], red_tiles[1])
    for i1, point1 in enumerate(red_tiles[1:]):
        for point2 in red_tiles[i1 + 2 :]:
            points = point1, point2
            valid_pair = True
            for i_point, axis in ((0, 0), (0, 1), (1, 0), (1, 1)):
                try:
                    next(
                        (beam_start, beam_end)
                        for beam_start, beam_end in beams[1 - axis].get(
                            points[i_point][1 - axis], []
                        )
                        if points[i_point][axis] == beam_start
                        and (
                            beam_start <= points[1 - i_point][axis] <= beam_end
                            or beam_start >= points[1 - i_point][axis] >= beam_end
                        )
                    )
                except StopIteration:
                    valid_pair = False
                    break
            if valid_pair and rectangle_area(points) > rectangle_area(
                largest_rectangle_pair
            ):
                largest_rectangle_pair = points
    part2 = rectangle_area(largest_rectangle_pair)
    plot(red_tiles, beams, largest_rectangle_pair)
    return part1, part2


def plot(red_tiles, beams, largest_rectangle_pair=None):
    if not is_debug_active():
        return

    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1: Axes
    ax2: Axes
    tile_polygon = mpatches.Polygon(
        red_tiles, closed=True, facecolor="w", edgecolor="r"
    )
    ax1.add_patch(tile_polygon)
    for x, y_ends in beams[0].items():
        for i, (y1, y2) in enumerate(y_ends):
            ax1.plot([x, x], [y1, y2], ":g" if i % 2 else "--b")
    if largest_rectangle_pair:
        (rx1, ry1), (rx2, ry2) = largest_rectangle_pair
        ax1.plot([rx1, rx2], [ry1, ry1], "-.m")
        ax1.plot([rx1, rx2], [ry2, ry2], "-.m")

    tile_polygon = mpatches.Polygon(
        red_tiles, closed=True, facecolor="w", edgecolor="r"
    )
    ax2.add_patch(tile_polygon)
    for y, x_ends in beams[1].items():
        for i, (x1, x2) in enumerate(x_ends):
            ax2.plot([x1, x2], [y, y], ":g" if i % 2 else "--b")
    if largest_rectangle_pair:
        ax2.plot([rx1, rx1], [ry1, ry2], "-.m")
        ax2.plot([rx2, rx2], [ry1, ry2], "-.m")
    plt.show(block=False)
