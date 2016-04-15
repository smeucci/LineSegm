/*
 * Astar.h
 *
 *  Created on: Apr 14, 2016
 *      Author: saverio
 */

#ifndef HEADERS_ASTAR_H_
#define HEADERS_ASTAR_H_

#include "Node.h"
#include <queue>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

using namespace std;
using namespace cv;


struct CompareFscore {
	bool operator() (Node* node1, Node* node2) {
		return node1->fscore() > node2->fscore();
	}
};


class Astar {

	private:
		const Mat* grid;

	public:
		Astar ();
		Astar (Mat* grid);
		~Astar ();

		vector<Node> pathfind (Node* start, Node* goal);
		double heuristic (Node* node1, Node* node2);
		vector<Node> get_neighbors (Node node);
		bool in_bounds (Node* node);
		bool is_wall (Node* node);
		double compute_cost (Node* current, Node* neighbor, Node* start);
		double V (Node* current, Node* start);
		double N (Node* current, Node* neighbor);
		double M (Node* node);
		double D (Node* node);
		double D2 (Node* node);
		double upward_obstacle (Node* node);
		double downward_obstacle (Node* node);
		vector<Node> reconstruct_path (vector<Node*> closedSet);

};

#endif /* HEADERS_ASTAR_H_ */
