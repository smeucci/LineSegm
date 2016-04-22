/*
 * utils.cpp
 *
 *  Created on: Apr 22, 2016
 *      Author: saverio
 */


#include "opencv2/opencv.hpp"

using namespace cv;
using namespace std;


inline Mat distance_transform (Mat input) {

	Mat dmat = input.clone();
	for (int i = 0; i < input.cols; i++) {
		Mat column = input(Rect(i, 0, 1, input.rows));
		Mat dcol;
		distanceTransform(column, dcol, CV_DIST_L2, 5);
		dcol.copyTo(dmat.col(i));
	}

	return dmat;
}

template<typename Node>
inline void draw_path (Mat& graph, vector<Node>& path) {

	for (auto node : path) {
		int row, col;
		tie (row, col) = node;
		graph.at<uchar>(row, col) = (uchar) 0;
	}
	imwrite("data/map.jpg", graph*255);
}

template<typename Node>
inline Mat segment_line (Mat& input, vector<Node> path){

	Mat output = input.clone();
	for (auto node: path) {
		int row, col;
		tie(row, col) = node;
		for (int i = row; i < input.rows; i++) {
			output.at<uchar>(i, col) = (uchar) 255;
		}
	}

	return output;
}

template<typename Node>
inline void line_segmentation (Mat& input, vector<vector<Node>> paths) {

	vector<Mat> segmented_images;
	for (auto path : paths) {
		segmented_images.push_back(segment_line(input, path));
	}
	segmented_images.push_back(input);

	imwrite("data/segmented/lines_" + to_string(0) + ".jpg", segmented_images[0]);
	for (unsigned int i = 1; i < segmented_images.size(); i++) {
		Mat output = abs(255 - segmented_images[i]) - abs(255 - segmented_images[i - 1]);
		imwrite("data/segmented/lines_" + to_string(i) + ".jpg", abs(255 - output));
	}

}
