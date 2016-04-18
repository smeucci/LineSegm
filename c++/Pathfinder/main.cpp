/*
 * main.cpp
 *
 *  Created on: Apr 18, 2016
 *      Author: saverio
 */

#include "utils.cpp"
#include "opencv2/opencv.hpp"
#include <ctime>

using namespace std;
using namespace cv;

int main () {

	 clock_t begin = clock();

	Map map;
	map.grid = imread("data/test4.jpg", 0) / 255;

	//cout << map.grid << endl;

	typedef Map::Node Node;
	Node start{136, 0};
	Node goal{136, 1500};

	cout << "From [" << get<0>(start) << ", " << get<1>(start) << "]";
	cout << " To [" << get<0>(goal) << ", " << get<1>(goal) << "]" << endl;

	unordered_map<Node, Node> parents;
	unordered_map<Node, double> gscore;

	astar(map, start, goal, parents, gscore);

	vector<Node> path = reconstruct_path(start, goal, parents);
	draw_path(map.grid, path);

	clock_t end = clock();
	double elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;
	cout << "- Elapsed Time: " << elapsed_secs << endl;

}
