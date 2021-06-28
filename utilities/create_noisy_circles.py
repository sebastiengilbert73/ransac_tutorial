import logging
import argparse
import random
import math
import matplotlib.pyplot as plt
import ast

parser = argparse.ArgumentParser()
parser.add_argument('--number_of_inliers', help="The number of inliers. Default: 200", type=int, default=200)
parser.add_argument('--inliers_noise', help="The noise for the inliers. Default: 0.5", type=float, default=0.5)
parser.add_argument('--number_of_outliers', help="The number of outliers. Default: 200", type=int, default=200)
parser.add_argument('--outliers_range', help="For the outliers, the range of (x, y) values. Default: '[-10, 10]'", default='[-10, 10]')
parser.add_argument('--outputFilepath', help="The output filepath. Default: '../data/noisy_circles.csv'", default='../data/noisy_circles.csv')
args = parser.parse_args()

args.outliers_range = ast.literal_eval(args.outliers_range)
circle1_center = (1, 3.5)
circle2_center = (-7.5, -5.5)
circle1_radius = 4.0
circle2_radius = 2.0

logging.basicConfig(level=logging.INFO, format='%(asctime)-15s %(levelname)s \t%(message)s')

def main():
    logging.info("create_noisy_circles.py main()")

    xy_tuples = []
    # Principal circle
    for inlierNdx in range(args.number_of_inliers):
        theta = random.uniform(0, 2 * math.pi)
        pt = [circle1_center[0] + circle1_radius * math.cos(theta),
              circle1_center[1] + circle1_radius * math.sin(theta)]
        pt[0] += random.uniform(-args.inliers_noise, args.inliers_noise)
        pt[1] += random.uniform(-args.inliers_noise, args.inliers_noise)
        xy_tuples.append((pt, 0))
    # Secondary circle
    for inlierNdx in range(args.number_of_inliers//2):
        theta = random.uniform(0, 2 * math.pi)
        pt = [circle2_center[0] + circle2_radius * math.cos(theta),
              circle2_center[1] + circle2_radius * math.sin(theta)]
        pt[0] += random.uniform(-args.inliers_noise, args.inliers_noise)
        pt[1] += random.uniform(-args.inliers_noise, args.inliers_noise)
        xy_tuples.append((pt, 0))
    # Outliers
    for outlierNdx in range(args.number_of_outliers):
        pt = [random.uniform(args.outliers_range[0], args.outliers_range[1]),
              random.uniform(args.outliers_range[0], args.outliers_range[1])]
        xy_tuples.append((pt, 0))

    # Shuffle the data
    random.shuffle(xy_tuples)

    # Display the points
    fig, ax = plt.subplots()
    ax.scatter([xy[0][0] for xy in xy_tuples], [xy[0][1] for xy in xy_tuples],
               c='green', s=3)

    ax.grid(True)
    plt.show()

    # Write to file
    with open(args.outputFilepath, 'w') as output_file:
        output_file.write("x0,x1\n")
        for x_y in xy_tuples:
            output_file.write("{},{}\n".format(x_y[0][0], x_y[0][1]))


if __name__ == '__main__':
    main()
