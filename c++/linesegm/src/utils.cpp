/*
 * utils.cpp
 *
 *  Created on: Apr 22, 2016
 *      Author: saverio
 */


#include "opencv2/opencv.hpp"
#include <dirent.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <iostream>
#include <fstream>

using namespace cv;
using namespace std;


inline void print_help () {

	fprintf(stderr,
	            "Usage: linesegm [FILES]... [OPTIONS]...\n"
	            "Line segmentation for handwritten documents.\n"
	            "\n"
	            "Options:\n"
	            "\t-s integer \t\tStep option.\n"
	            "             \t\tChange the step with which explore the map.\n"
	            "\t-mf integer   \t\tMultiplication factor.\n"
	            "             \t\tIncrease the multiplication factor to obtain a non-admissible heuristic.\n"
	            "\t--stats	\t\tCompute and show statistics about the line segmentation.\n"
	            "\t--help       \t\tShow this help information.\n"
	            "\n"
	            "Examples:\n"
	            "\tlinesegm image.jpg -s 2 -mf 5 --stats\n"
	            "\tlinesegm images/* -s 1 -mf 20 --stats\n"
			    "\tlinesegm data/saintgall/images/csg562-003.jpg --stats\n");

	    exit(0);

}


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
		if (col < graph.cols) {
			graph.at<uchar>(row, col + 1) = (uchar) 0;
		}
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
			if (col < output.cols) {
				output.at<uchar>(i, col + 1) = (uchar) 255;
			}
		}
	}

	return output;
}

inline bool strreplace (string& str, string& rem, string& repl) {
	size_t start_pos = str.find(rem);
	if (start_pos == string::npos)
		return false;
	str.replace(start_pos, rem.length(), repl);
	return true;
}

inline string infer_dataset (string filename) {
	size_t mls = filename.find("mls");
	size_t sg = filename.find("saintgall");
	if (mls != string::npos) {
		return "mls";
	} else if (sg != string::npos) {
		return "saintgall";
	} else {
		return "NULL";
	}
}

template<typename Node>
inline void line_segmentation (Mat& input, vector<vector<Node>> paths, string filename) {

	string dataset = infer_dataset(filename);

	string rem1 = "data/" + dataset + "/images/";
	string rem2 = ".jpg";
	string repl = "";
	strreplace(filename, rem1, repl);
	strreplace(filename, rem2, repl);


	string folder_segmented = "data/" + dataset + "/detected/";
	string folder_lines = folder_segmented + filename + "/";

	struct stat st = {0};

	if (stat(folder_lines.c_str(), &st) == -1) {
	    mkdir(folder_lines.c_str(), 0755);
	    cout << "- Created folder ";
	    cout << folder_lines.c_str() << endl;
	}

	vector<Mat> segmented_images;
	for (auto path : paths) {
		segmented_images.push_back(segment_line(input, path));
	}
	segmented_images.push_back(input);

	imwrite(folder_lines + "lines_" + to_string(1) + ".jpg", segmented_images[0]);
	for (unsigned int i = 1; i < segmented_images.size(); i++) {
		Mat output = abs(255 - segmented_images[i]) - abs(255 - segmented_images[i - 1]);
		imwrite(folder_lines + "lines_" + to_string(i+1) + ".jpg", abs(255 - output));
	}

}


inline vector<string> read_folder (const char* folder) {
	DIR *pdir = NULL;
	pdir = opendir (folder);
	struct dirent *pent = NULL;
	vector<string> files;

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
			files.push_back((string) pent->d_name);
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

inline vector<double> select_best_assignments (vector<double>& hitrate, vector<double>& line_detection_GT, vector<double>& line_detection_R,
									 vector<string> lines, string groudtruth) {

	auto max = max_element(hitrate.begin(), hitrate.end());
	int pos = distance(hitrate.begin(), max);

	double hit_rate = *max;
	double line_det_GT = line_detection_GT[pos];
	double line_det_R = line_detection_R[pos];

	vector<double> stats;
	stats.push_back(hit_rate);
	stats.push_back(line_det_GT);
	stats.push_back(line_det_R);

	cout << "\t## Groundtruth: " << groudtruth << " - Detected: " << lines[pos];
	cout << " - Hit rate: " << to_string(*max);
	cout << " - Line detection GT: " << to_string(line_det_GT);
	cout << " - Line detection R: " << to_string(line_det_R) << endl;

	return stats;

}

inline void compute_statistics (string filename) {

	string dataset = infer_dataset(filename);

	string rem1 = "data/" + dataset + "/images/";
	string rem2 = ".jpg";
	string repl = "";
	strreplace(filename, rem1, repl);
	strreplace(filename, rem2, repl);

	string folder_lines = "data/" + dataset + "/detected/" + filename + "/";
	string folder_groundtruth = "data/" + dataset + "/groundtruth/" + filename + "/";

	vector<string> lines = read_folder(folder_lines.c_str());
	vector<string> groundtruth = read_folder(folder_groundtruth.c_str());

	Mat line, ground, united, shared;

	int tot_correctly_detected = 0;
	double tot_hitrate, tot_line_detection_GT, tot_line_detection_R = 0;
	for (unsigned int i = 0; i < groundtruth.size(); i++) {

		vector<double> hitrate, line_detection_GT, line_detection_R;
		ground =  imread(folder_groundtruth + groundtruth[i], 0) / 255;

		for (unsigned int j = 0; j < lines.size(); j++){

			line = imread(folder_lines + lines[j], 0) / 255;

			bitwise_or(line, ground, shared);
			bitwise_and(line, ground, united);

			int black_pixels_line = countNonZero(line == 0);
			int black_pixels_ground = countNonZero(ground == 0);
			int black_pixels_shared = countNonZero(shared == 0);
			int black_pixels_united = countNonZero(united == 0);

			hitrate.push_back((((double) black_pixels_shared) / ((double) black_pixels_united)));
			line_detection_GT.push_back((((double) black_pixels_shared) / ((double) black_pixels_ground)));
			line_detection_R.push_back((((double) black_pixels_shared) / ((double) black_pixels_line)));
		}

		vector<double> stats = select_best_assignments(hitrate, line_detection_GT, line_detection_R, lines, groundtruth[i]);
		tot_hitrate = tot_hitrate + stats[0];
		tot_line_detection_GT = tot_line_detection_GT + stats[1];
		tot_line_detection_R = tot_line_detection_R + stats[2];

		if (stats[1] >= 0.9 && stats[2] >= 0.9) {
			tot_correctly_detected++;
		}

	}

	cout << "\n\t## Avg. stats ==> ";
	cout << " Hit rate: " << to_string(tot_hitrate / groundtruth.size());
	cout << " - Line detection GT: " << to_string(tot_line_detection_GT / groundtruth.size());
	cout << " - Line detection R: " << to_string(tot_line_detection_R / groundtruth.size());
	cout << " - Correctly detected: " << to_string(tot_correctly_detected) << "/" << to_string(groundtruth.size()) << endl;

	ofstream csvfile;
	csvfile.open("data/" + dataset + "/stats.csv", std::ios_base::app);
	csvfile << filename;
	csvfile << ",";
	csvfile << int(round((tot_hitrate / groundtruth.size()) * 100));
	csvfile << ",";
	csvfile << int(round((tot_line_detection_GT / groundtruth.size()) * 100));
	csvfile << ",";
	csvfile << int(round((tot_line_detection_R / groundtruth.size()) * 100));
	csvfile << ",";
	csvfile << tot_correctly_detected;
	csvfile << ",";
	csvfile << groundtruth.size();
	csvfile << "\n";

	csvfile.close();

}
