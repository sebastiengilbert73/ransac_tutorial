import logging
import ransac.core as ransac
import ransac.models.circle as ransac_circle
import random
import math
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

logging.basicConfig(level=logging.INFO, format='%(asctime)-15s %(levelname)s \t%(message)s')


def main():
    logging.info("noisy_circle.py main()")

    noisy_line_filepath = './data/noisy_circles.csv'
    # Read the points from the file
    points_df = pd.read_csv(noisy_line_filepath)
    x0x1_list = list(zip(list(points_df.loc[:, 'x0']), list(points_df.loc[:, 'x1'])))
    x0x1_y_tuples = [(x0x1, 0) for x0x1 in
                     x0x1_list]  # Since we are dealing with a point cloud, there is no output: we fill the 2nd member of the tuple with 0

    # Display the point cloud
    fig, ax = plt.subplots()
    ax.scatter([x0x1_y[0][0] for x0x1_y in x0x1_y_tuples], [x0x1_y[0][1] for x0x1_y in x0x1_y_tuples],
               c='green', s=3)
    ax.grid(True)
    plt.show()

    # *** Apply RANSAC to fit a circle ***
    number_of_trials = 100
    acceptable_error = 1.0
    line_modeler = ransac.Modeler(ransac_circle.Circle, number_of_trials, acceptable_error)
    consensus_model, inliers_list, outliers_list = line_modeler.ConsensusModel(x0x1_y_tuples)
    logging.info(
        "consensus_model.center = {}; consensus_model.radius = {}".format(consensus_model.center, consensus_model.radius))

    # Display the inliers, the outliers and the found circle
    consensus_circle_data_list = SamplePointsFromModel(consensus_model.center, consensus_model.radius, 200)
    fig, ax = plt.subplots()
    ax.scatter([inlier[0][0] for inlier in inliers_list], [inlier[0][1] for inlier in inliers_list],
               c='green', s=3, label='inliers')
    ax.scatter([outlier[0][0] for outlier in outliers_list], [outlier[0][1] for outlier in outliers_list],
               c='red', s=3, label='outliers')
    ax.scatter([x0x1[0] for x0x1 in consensus_circle_data_list],
               [x0x1[1] for x0x1 in consensus_circle_data_list], c='blue', s=3,
               label='circle found with RANSAC')
    ax.legend()
    ax.grid(True)
    plt.show()


def SamplePointsFromModel(center, radius, number_of_samples):
    samples_list = []
    for sampleNdx in range(number_of_samples):
        theta = sampleNdx * 2 * math.pi/number_of_samples
        samples_list.append((center[0] + radius * math.cos(theta), center[1] + radius * math.sin(theta)))
    return samples_list


if __name__ == '__main__':
    main()
