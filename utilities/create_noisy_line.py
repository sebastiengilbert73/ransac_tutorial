import logging
import argparse
import random
import math
import matplotlib.pyplot as plt
import ast

parser = argparse.ArgumentParser()
parser.add_argument('--rho', help="The rho parameter for the line. Default: 4.2", type=float, default=4.2)
parser.add_argument('--theta', help="The theta parameter for the line. Default: 0.7", type=float, default=0.7)
parser.add_argument('--number_of_inliers', help="The number of inliers. Default: 100", type=int, default=100)
parser.add_argument('--inliers_noise', help="The noise for the inliers. Default: 0.5", type=float, default=0.5)
parser.add_argument('--number_of_outliers', help="The number of outliers. Default: 100", type=int, default=100)
parser.add_argument('--alpha_range', help="For the inliers, the range of distances from (rho*cos(theta), rho*sin(theta)). Default: '[-10, 10]'", default='[-10, 10]')
parser.add_argument('--outliers_range', help="For the outliers, the range of (x, y) values. Default: '[-10, 10]'", default='[-10, 10]')
parser.add_argument('--outputFilepath', help="The output filepath. Default: '../data/noisy_line.csv'", default='../data/noisy_line.csv')
args = parser.parse_args()

args.alpha_range = ast.literal_eval(args.alpha_range)
args.outliers_range = ast.literal_eval(args.outliers_range)

logging.basicConfig(level=logging.INFO, format='%(asctime)-15s %(levelname)s \t%(message)s')

def main():
    logging.info("create_noisy_line.py main()")
    xy_tuples = []
    for inlierNdx in range(args.number_of_inliers):
        alpha = random.uniform(args.alpha_range[0], args.alpha_range[1])
        pt = [args.rho * math.cos(args.theta) + alpha * math.sin(args.theta),
              args.rho * math.sin(args.theta) - alpha * math.cos(args.theta)]
        pt[0] += random.uniform(-args.inliers_noise, args.inliers_noise)
        pt[1] += random.uniform(-args.inliers_noise, args.inliers_noise)
        xy_tuples.append((pt, 0))
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
            output_file.write("{},{}\n".format(x_y[0][0],x_y[0][1]))


if __name__ == '__main__':
    main()