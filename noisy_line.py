import logging
import ransac.core as ransac
import ransac.models.line as ransac_line
import random
import math
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

logging.basicConfig(level=logging.INFO, format='%(asctime)-15s %(levelname)s \t%(message)s')
alpha_range = [-10, 10]  # When creating the data from a line model, this is the range of distances from (rho*cos(theta), rho*sin(theta))

def main():
    logging.info("noisy_line.py main()")

    noisy_line_filepath = './data/noisy_line.csv'
    # Read the points from the file
    points_df = pd.read_csv(noisy_line_filepath)
    x0x1_list = list(zip(list(points_df.loc[:, 'x0']), list(points_df.loc[:, 'x1'])))
    x0x1_y_tuples = [(x0x1, 0) for x0x1 in x0x1_list]  # Since we are dealing with a cloud point, there is no output: we fill the 2nd member of the tuple with 0

    # Display the point cloud
    fig, ax = plt.subplots()
    ax.scatter([x0x1_y[0][0] for x0x1_y in x0x1_y_tuples], [x0x1_y[0][1] for x0x1_y in x0x1_y_tuples],
               c='green', s=3)
    ax.grid(True)
    plt.show()

    # *** Fit a line with all the data ***
    line_with_all_data = ransac_line.Line()
    line_with_all_data.Create(x0x1_y_tuples)
    logging.info("line_with_all_data.rho = {}; line_with_all_data.theta = {}".format(line_with_all_data.rho, line_with_all_data.theta))
    # Display the found line
    line_with_all_data_list = SamplePointsFromModel(line_with_all_data.rho, line_with_all_data.theta, alpha_range)
    # Display the point cloud and the found line
    fig, ax = plt.subplots()
    ax.scatter([x0x1_y[0][0] for x0x1_y in x0x1_y_tuples], [x0x1_y[0][1] for x0x1_y in x0x1_y_tuples],
               c='green', s=3, label='raw data')
    ax.scatter([x0x1[0] for x0x1 in line_with_all_data_list],
               [x0x1[1] for x0x1 in line_with_all_data_list], c='blue', s=3, label='line found with all the points')
    ax.legend()
    ax.grid(True)
    plt.show()

    # *** Apply RANSAC to fit a line ***
    number_of_trials = 100
    acceptable_error = 1.0
    line_modeler = ransac.Modeler(ransac_line.Line, number_of_trials, acceptable_error)
    consensus_model, inliers_list, outliers_list = line_modeler.ConsensusModel(x0x1_y_tuples)
    logging.info("consensus_model.rho = {}; consensus_model.theta = {}".format(consensus_model.rho, consensus_model.theta))
    # Display the inliers, the outliers and the found line
    consensus_line_data_list = SamplePointsFromModel(consensus_model.rho, consensus_model.theta, alpha_range)
    fig, ax = plt.subplots()
    ax.scatter([inlier[0][0] for inlier in inliers_list], [inlier[0][1] for inlier in inliers_list],
               c='green', s=3, label='inliers')
    ax.scatter([outlier[0][0] for outlier in outliers_list], [outlier[0][1] for outlier in outliers_list],
               c='red', s=3, label='outliers')
    ax.scatter([x0x1[0] for x0x1 in consensus_line_data_list],
               [x0x1[1] for x0x1 in consensus_line_data_list], c='blue', s=3,
               label='line found with RANSAC')
    ax.legend()
    ax.grid(True)
    plt.show()



def SamplePointsFromModel(rho, theta, alpha_range):
    return [(rho * math.cos(theta) + alpha * math.sin(theta),
                                rho * math.sin(theta) - alpha * math.cos(theta))
                       for alpha in np.arange(alpha_range[0], alpha_range[1], 0.01)]

if __name__ == '__main__':
    main()