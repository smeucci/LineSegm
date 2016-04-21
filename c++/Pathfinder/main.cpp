/*
 * main.cpp
 *
 *  Created on: Apr 18, 2016
 *      Author: saverio
 */

#include "opencv2/opencv.hpp"
#include <ctime>
#include "sauvola.cpp"
#include "linelocalization.cpp"
#include "astar.cpp"

using namespace std;
using namespace cv;

int main () {

	clock_t begin = clock();

	Mat im = imread("data/test6.jpg", 0);
	Mat imbw (im.rows, im.cols, CV_8U);
	cout << "Thresholding.." << endl;
	binarize(im, imbw, 20, 128, 0.3);
	imwrite("data/bw.jpg", imbw);
	cout << "Detecting lines location..";
	vector<int> lines = localize(imbw, 0.3);
	cout << "==> " << lines.size() << " lines found." << endl;

	if (true) {
		Map map;
		map.grid = imbw / 255;
		map.dmat = map.grid;

		for (int i = 0; i < map.grid.cols; i++) {

			Mat column = map.grid(Rect(i, 0, 1, map.grid.rows));
			Mat dcol;
			distanceTransform(column, dcol, CV_DIST_L2, 5);
			dcol.copyTo(map.dmat.col(i));
		}

		typedef Map::Node Node;
		vector<vector<Node>> paths;
		Mat p = map.grid.clone();
		for (vector<int>::iterator itr = lines.begin(); itr != lines.end(); itr++) {
			Node start{*itr, 0};
			Node goal{*itr, map.grid.cols - 1};

			cout << "From [" << get<0>(start) << ", " << get<1>(start) << "]";
			cout << " to [" << get<0>(goal) << ", " << get<1>(goal) << "]" << endl;

			unordered_map<Node, Node> parents;
			unordered_map<Node, double> gscore;

			astar(map, start, goal, parents, gscore);

			vector<Node> path = reconstruct_path(start, goal, parents);
			draw_path(p, path);
			paths.push_back(path);
		}


		vector<Mat> images;
		for (unsigned int i = 0; i < paths.size() - 1; i++) {
			Mat s = map.grid.clone() * 255;
			Mat im1 = s;
			Mat im2 = s;
			segment_line(s, im1, paths[i], i);
			segment_line(s, im2, paths[i+1], i+1);

			im2 = im2 - im1;

			imwrite("data/segmented/line_" + to_string(i) + ".jpg", im1);
			imwrite("data/segmented/line_" + to_string(i+1) + ".jpg", im2);

		}

	}



	clock_t end = clock();
	double elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;
	cout << "- Elapsed Time: " << elapsed_secs << endl;

}
