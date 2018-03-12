#!/usr/bin/env python3
"""
Copyright 2018 Ryan Wick (rrwick@gmail.com)
https://github.com/rrwick/Dejumbler

This script uses FastANI output to generate a PHYLIP distance matrix suitable for quicktree.

This file is part of Dejumbler. Dejumbler is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later version. Dejumbler is
distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
Public License for more details. You should have received a copy of the GNU General Public
License along with Dejumbler. If not, see <http://www.gnu.org/licenses/>.
"""

import argparse
import sys


def get_arguments():
    parser = argparse.ArgumentParser(description='Distance matrix from FastANI identities')
    parser.add_argument('fastani_output', type=str, help='FastANI output file')
    args = parser.parse_args()
    return args


def main():
    args = get_arguments()

    clusters = set()
    distances = {}

    print()
    print('Convert FastANI distances to PHYLIP matrix', file=sys.stderr)
    print('------------------------------------------------', file=sys.stderr)

    fastani_output_filename = args.fastani_output

    with open(fastani_output_filename, 'rt') as fastani_output:
        for line in fastani_output:
            parts = line.strip().split(' ')
            cluster_1 = parts[0]
            cluster_2 = parts[1]
            ani = float(parts[2])
            if cluster_1 == cluster_2:
                distance = 0.0
            else:
                distance = 1.0 - (ani / 100.0)
            clusters.add(cluster_1)
            clusters.add(cluster_2)
            add_distance(distances, cluster_1, cluster_2, distance)
            add_distance(distances, cluster_2, cluster_1, distance)
    print('Found {} clusters and {} distances'.format(len(clusters), len(distances)), file=sys.stderr)

    print(len(clusters))
    clusters = sorted(clusters)
    for i in clusters:
        print(distance_matrix, end='')
        for j in clusters:
            print('\t', end='')
            try:
                distance = distances[(i, j)]
            except KeyError:
                distance = 0.2
            if distance > 0.2:
                distance = 0.2
            print('%.6f' % distance, end='')
        print()


def add_distance(distances, cluster_1, cluster_2, distance):
    # If this is the first time we've seen this pair, then we just add it to the dictionary.
    if (cluster_1, cluster_2) not in distances:
        distances[(cluster_1, cluster_2)] = distance
    # If we've seen this pair before (the other way around), then we make sure the distances are
    # close (sanity check) and then save the mean distance.
    else:
        assert abs(distance - distances[(cluster_1, cluster_2)]) < 0.1
        distances[(cluster_1, cluster_2)] = (distances[(cluster_1, cluster_2)] + distance) / 2.0


if __name__ == '__main__':
    main()
