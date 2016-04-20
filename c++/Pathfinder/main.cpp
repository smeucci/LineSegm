/*
 * main.cpp
 *
 *  Created on: Apr 18, 2016
 *      Author: saverio
 */

#include "opencv2/opencv.hpp"
#include <ctime>
#include "sauvola.cpp"
#include "astar.cpp"

using namespace std;
using namespace cv;

int main () {

	clock_t begin = clock();

	Mat im = imread("data/test5.jpg", 0);
	Mat imbw (im.rows, im.cols, CV_8U);
	binarize(im, imbw, 20, 128, 0.3);
	imwrite("data/bw.jpg", imbw);

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
		Node start{470, 0};
		Node goal{470, map.grid.cols - 1};

		cout << "From [" << get<0>(start) << ", " << get<1>(start) << "]";
		cout << " To [" << get<0>(goal) << ", " << get<1>(goal) << "]" << endl;

		unordered_map<Node, Node> parents;
		unordered_map<Node, double> gscore;

		astar(map, start, goal, parents, gscore);

		vector<Node> path = reconstruct_path(start, goal, parents);
		draw_path(map.grid, path);
	}


	clock_t end = clock();
	double elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;
	cout << "- Elapsed Time: " << elapsed_secs << endl;

}
