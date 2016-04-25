/*
 * main.cpp
 *
 *  Created on: Apr 18, 2016
 *      Author: saverio
 */


#include "opencv2/opencv.hpp"
#include <ctime>
#include <iostream>
#include "src/utils.cpp"
#include "src/sauvola.cpp"
#include "src/linelocalization.cpp"
#include "src/astar.cpp"

using namespace std;
using namespace cv;


int main (int argc, char* argv[]) {

	clock_t begin = clock();
	cout << "\n########################################" << endl;
	cout << "##          LINE SEGMENTATION         ##" << endl;
	cout << "########################################\n" << endl;

	string filename = "data/test5.jpg";
	cout << "\nReading image '" << filename << "'" << endl;;
	Mat im = imread(filename, 0);
	Mat imbw (im.rows, im.cols, CV_8U);

	cout << "- Thresholding.." << endl;
	binarize(im, imbw, 20, 128, 0.3);
	imwrite("data/bw.jpg", imbw);

	cout << "- Detecting lines location..";
	vector<int> lines = localize(imbw);
	cout << " ==> " << lines.size() + 1 << " lines found." << endl;


	cout << "- A* path planning algorithm.." << endl;
	Map map;
	map.grid = imbw / 255;
	map.dmat = distance_transform(map.grid);


	typedef Map::Node Node;
	vector<vector<Node>> paths;
	Mat image_path = map.grid.clone();
	int num = 1;
	for (vector<int>::iterator itr = lines.begin(); itr != lines.end(); itr++) {

		clock_t _start = clock();

		Node start{*itr, 0};
		Node goal{*itr, map.grid.cols - 1};

		cout << "\t" << to_string(num) + "# from [" << get<0>(start) << ", " << get<1>(start) << "]";
		cout << " to [" << get<0>(goal) << ", " << get<1>(goal) << "]";

		unordered_map<Node, Node> parents;

		astar(map, start, goal, parents);

		vector<Node> path = reconstruct_path(start, goal, parents);
		draw_path(image_path, path);
		paths.push_back(path);

		clock_t _finish = clock();

		cout << " ==> path found in " + to_string(double(_finish - _start) / CLOCKS_PER_SEC) << " s" << endl;
		num++;
	}

	cout << "\n- Segmenting lines and saving images.." << endl;
	line_segmentation(imbw, paths);

	compute_statistics();

	clock_t end = clock();
	double elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;
	cout << "\n## Elapsed Time: " << elapsed_secs << " s ##\n" << endl;

	return 0;
}
