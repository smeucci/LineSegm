/*
 * main.cpp
 *
 *  Created on: Apr 14, 2016
 *      Author: saverio
 */

#include <iostream>
#include <string>
#include <opencv2/opencv.hpp>
#include "headers/Node.h"
#include "headers/Astar.h"

using namespace std;
using namespace cv;

int main () {

	string filename = "test.jpg";
	Mat image = imread(filename, 0) / 255;
	cout << image << endl;

	Node start = Node(5, 0);
	Node goal = Node(5, 9);

	Astar astar = Astar(&image);

	vector<Node> path = astar.pathfind(&start, &goal);

	for (Node node : path) {
		cout << node << endl;
	}



}
