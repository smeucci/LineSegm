/*
 * utils.cpp
 *
 *  Created on: Apr 22, 2016
 *      Author: saverio
 */


#include "opencv2/opencv.hpp"
#include <dirent.h>

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

	imwrite("data/segmented/lines_" + to_string(1) + ".jpg", segmented_images[0]);
	for (unsigned int i = 1; i < segmented_images.size(); i++) {
		Mat output = abs(255 - segmented_images[i]) - abs(255 - segmented_images[i - 1]);
		imwrite("data/segmented/lines_" + to_string(i+1) + ".jpg", abs(255 - output));
	}

}


inline vector<Mat> read_folder (const char* folder) {
	DIR *pdir = NULL;
	pdir = opendir (folder);
	struct dirent *pent = NULL;
	vector<Mat> files;

	if (pdir == NULL) {
		cout << "\nERROR! pdir could not be initialised correctly";
		exit (3);
	}

	while ((pent = readdir (pdir))) {
		if (pent == NULL) {
			cout << "\nERROR! pent could not be initialised correctly";
			exit (3);
		}
		if (!strcmp(pent->d_name, ".") == 0 and !strcmp(pent->d_name, "..") == 0) {
			cout << folder + (string) pent->d_name << endl;
			Mat file = imread(folder + (string) pent->d_name, 0);
			files.push_back(file);
		}
	}
	closedir (pdir);

	return files;
}

inline int count_occurences (Mat& input, int num) {
	int count = 0;
	for (int i = 0; i < input.rows; i++) {
		for (int j = 0; j < input.cols; j++) {
			if (input.at<uchar>(i, j) == (uchar) num) {
				count++;
			}
		}
	}

	return count;
}

inline void compute_statistics () {

	const char* folder_lines = "data/segmented/";
	const char* folder_groundtruth = "data/groundtruth/";

	vector<Mat> lines = read_folder(folder_lines);
	vector<Mat> groundtruth = read_folder(folder_groundtruth);

	Mat line, ground, united, shared;
	for (unsigned int i = 0; i < lines.size(); i++) {
		for (unsigned int j = 0; j < groundtruth.size(); j++){

			line = lines[i] / 255;
			ground =  groundtruth[j] / 255;

			bitwise_or(line, ground, shared);
			bitwise_and(line, ground, united);

			int black_pixels_line = countNonZero(line == 0);
			int black_pixels_ground = countNonZero(ground == 0);
			int black_pixels_shared = countNonZero(shared == 0);
			int black_pixels_united = countNonZero(united == 0);
			float hitrate = (((float) black_pixels_shared) / ((float) black_pixels_united));

			cout << "segmented line: " << to_string(black_pixels_line);
			cout << " - groundtruth line: " << to_string(black_pixels_ground);
			cout << " - shared: " << to_string(black_pixels_shared);
			cout << " - united: " << to_string(black_pixels_united);
			cout << " - pixel level hit-rate: " << to_string((hitrate)) << endl;
		}
	}

}
