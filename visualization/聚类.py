import numpy as np
import random
def get_distance(p1, p2):
    diff = [x-y for x, y in zip(p1, p2)]
    distance = np.sqrt(sum(map(lambda x: x**2, diff)))
    return distance
def calc_center_point(cluster):
    N = len(cluster)
    m = np.matrix(cluster).transpose().tolist()
    center_point = [sum(x)/N for x in m]
    return center_point
def check_center_diff(center, new_center):
    n = len(center)
    for c, nc in zip(center, new_center):
        if c != nc:
            return False
    return True
def K_means(points, center_points):
    N = len(points)
    n = len(points[0][1:])
    k = len(center_points)
    tot = 0
    while True:             
        temp_center_points = []
        clusters = []
        for c in range(0, k):
            clusters.append([])
        for i, data in enumerate(points):
            distances = []
            for center_point in center_points:
                distances.append(get_distance(data[1:], center_point))
            index = distances.index(min(distances))
            clusters[index].append(data)
        tot += 1
        k = len(clusters)
        for cluster in clusters:
            temp_center_points.append(calc_center_point([i[1:] for i in cluster]))
        for j in range(0, k):
            if len(clusters[j]) == 0:
                temp_center_points[j] = center_points[j]
        for c, nc in zip(center_points, temp_center_points):
            if not check_center_diff(c, nc):
                center_points = temp_center_points[:]
                break
        else:
            break
    return clusters