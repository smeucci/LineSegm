/*
 * Astar.cpp
 *
 *  Created on: Apr 14, 2016
 *      Author: saverio
 */

#include "../headers/Astar.h"
#include <algorithm>
#include <set>
#include <unordered_set>

Astar :: Astar () {}

Astar :: Astar (Mat* grid) {
	this->grid = grid;
}

Astar :: ~Astar () {}

double Astar :: heuristic (Node* node1, Node* node2) {

	double a = pow((node1->row() - node2->row()), 2);
	double b = pow((node1->col() - node2->col()), 2);

	double dist = sqrt(a + b);

	return dist;

}

bool Astar :: in_bounds (Node* node) {

	if (node->row() >= 0 and node->row() < this->grid->rows and node->col() >= 0 and node->col() < this->grid->cols) {
		return true;
	} else {
		return false;
	}

}


bool Astar :: is_wall (Node* node) {

	if ((int) this->grid->at<uchar>(node->row(), node->col()) == 0) {
		return true;
	} else {
		return false;
	}
}


vector<Node*> Astar :: get_neighbors (Node* node) {

	vector<Node*> neighbors;
	int i, j;
	for (i = -1; i <= 1; i++) {
		for (j = -1; j <= 1; j++) {
			if (i != 0 or j != 0) {
				Node* neighbor = new Node (node->row() + i, node->col() + j);
				if (this->in_bounds(neighbor) and not this->is_wall(neighbor)) {
					neighbors.push_back(neighbor);
				}
			}

		}
	}

	return neighbors;

}

double Astar :: compute_cost (Node* current, Node* neighbor, Node* start) {

	double v = this->V (neighbor, start);
	double n = this->N (current, neighbor);
	double m = this->M (neighbor);
	double d = this->D (neighbor);
	double d2 = this->D2 (neighbor);

	return 3*v + 1*n + 50*m + 150*d + 50*d2;

}

double Astar :: V (Node* neighbor, Node* start) {

	return abs((neighbor->row () - start->row ()));

}

double Astar :: N (Node* current, Node* neighbor) {

	if (current->row () == neighbor->row () and current->col () == neighbor->col ()) {
		return (double) 10;
	} else {
		return (double) 14;
	}

}

double Astar :: M (Node* node) {

	if (this->is_wall(node)) {
		return (double) 0;
	} else {
		return (double) 1;
	}

}

double Astar :: D (Node* node) {

	return 1 / (1 + min(this->upward_obstacle(node), this->downward_obstacle(node)));

}

double Astar :: D2 (Node* node) {

	double m = min(this->upward_obstacle(node), this->downward_obstacle(node));
	return 1 / (1 + pow(m, 2));

}

double Astar :: upward_obstacle (Node* node) {

	int step = 1;
	while (step <= 50) {
		Node up = Node (node->row() - step, node->col());
		if (is_wall (&up)) {
			return (double) step;
		} else {
			step++;
		}
	}

	return INFINITY;

}

double Astar :: downward_obstacle (Node* node) {

	int step = 1;
	while (step <= 50) {
		Node down = Node (node->row() + step, node->col());
		if (is_wall (&down)) {
			return (double) step;
		} else {
			step++;
		}
	}

	return INFINITY;

}

vector<Node*> Astar :: reconstruct_path (vector<Node*> closedSet) {

	Node* current = closedSet.back();
	vector<Node*> total_path;
	total_path.push_back(current);
	while (current->parent() != NULL) {
		current = current->parent();
		total_path.push_back(current);
	}

	return total_path;

}

vector<Node*> Astar :: pathfind (Node* start, Node* goal) {

	vector<Node*> closedSet;
	priority_queue<Node*, vector<Node*>, CompareFscore> openSet;

	start->gscore(0);
	start->fscore(this->heuristic(start, goal));
	openSet.push(start);

	cout << "start" << endl;

	while (not openSet.empty()) {

		Node* current = openSet.top();
		//cout << *current << endl;
		openSet.pop();
		closedSet.push_back(current);

		if (*current == goal) {
			break;
		}

		vector<Node*> neighbors = this->get_neighbors(current);
		for (unsigned int i = 0; i < neighbors.size(); i++) {
			Node* neighbor = neighbors[i];

			if (find(closedSet.begin(), closedSet.end(), neighbor) != closedSet.end()){
				continue;
			}

			double new_gscore = current->gscore() + this->heuristic(current, neighbor); //this->compute_cost(current, neighbor, start);

			if (neighbor->parent() == NULL or new_gscore < neighbor->gscore()) {
				neighbor->gscore(new_gscore);
				double fscore = new_gscore + this->heuristic(neighbor, goal);
				neighbor->fscore(fscore);
				neighbor->parent(current);
				openSet.push(neighbor);
				//cout << "neighbor: " << *neighbor << " - fscore: " << neighbor->fscore() << " - parent: " << *neighbor->parent() << endl;

			}

		}

	}

	cout << "end" << endl;
	return this->reconstruct_path(closedSet);

}
