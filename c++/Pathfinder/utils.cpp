/*
 * utils.cpp
 *
 *  Created on: Apr 18, 2016
 *      Author: saverio
 */

#include "opencv2/opencv.hpp"
#include <queue>
#include <algorithm>
#include <unordered_map>

using namespace cv;
using namespace std;

struct Map {

	typedef tuple<int, int> Node;

	Mat grid;

	Node DIRS[8] = {Node{-1, -1}, Node{-1, 0}, Node{-1, 1},
					Node{0, -1}, Node{0, 1},
					Node{1, -1}, Node{1, 0}, Node{1, 1}};

	inline bool in_bounds (Node node) const {

		int row, col;
		tie (row, col) = node;
		return 0 <= row and row < grid.rows and 0 <= col and col < grid.cols;

	}

	inline bool is_wall (Node node) const {
		int row, col;
		tie (row, col) = node;
		return (int) grid.at<uchar>(row, col) == 0;

	}

	vector<Node> neighbors(Node node) const {

		int row, col, dr, dc;
		tie (row, col) = node;
		vector<Node> neighbors;

		for (auto dir : DIRS) {
			tie (dr, dc) = dir;
			Node neighbor(row + dr, col + dc);
			if (in_bounds(neighbor) and not is_wall(neighbor)) {
				neighbors.push_back(neighbor);
			}
		}

		return neighbors;

	}

};

template<typename T, typename Priority = double>
struct PriorityQueue {

	typedef pair<Priority, T> Element;
	priority_queue<Element, vector<Element>, greater<Element>> elements;

	inline bool empty () {
		return elements.empty();
	}

	inline void put (T element, Priority priority) {
		elements.emplace(priority, element);
	}

	inline T get () {

		T element = elements.top().second;
		elements.pop();
		return element;

	}

};

inline double heuristic (Map::Node start, Map::Node end) {

	int r1, r2, c1, c2;
	tie (r1, c1) = start;
	tie (r2, c2) = end;

	double a = pow((r1 - r2), 2);
	double b = pow((c1 - c2), 2);

	return sqrt(a + b);

}

namespace std {
  template <>
  struct hash<tuple<int,int> > {
    inline size_t operator() (const tuple<int,int>& node) const {
      int x, y;
      tie (x, y) = node;
      return x * 1812433253 + y;
    }
  };
}

template<typename Node>
vector<Node> reconstruct_path (Node start, Node goal, unordered_map<Node, Node>& parents) {

	vector<Node> path;
	Node current = goal;
	path.push_back(current);
	while (current != start) {
		current = parents[current];
		path.push_back(current);
	}

	reverse(path.begin(), path.end());
	return path;

}

template<typename Graph>
void astar (const Graph& graph, typename Graph::Node start, typename Graph::Node goal,
			unordered_map<typename Graph::Node, typename Graph::Node>& parents,
			unordered_map<typename Graph::Node, double>& gscore) {

	cout << "start" << endl;

	typedef typename Graph::Node Node;
	PriorityQueue<Node> openSet;
	openSet.put(start, 0);

	gscore[start] = 0;

	while (not openSet.empty()) {

		auto current = openSet.get();

		if (current == goal) {
			break;
		}

		for (auto neighbor : graph.neighbors(current)) {

			double new_gscore = gscore[current] + heuristic(current, neighbor);

			if (!gscore.count(neighbor) or new_gscore < gscore[neighbor]) {
				gscore[neighbor] = new_gscore;
				parents[neighbor] = current;
				double fscore = new_gscore + heuristic(neighbor, goal);
				openSet.put(neighbor, fscore);
			}

		}

	}

	cout << "end" << endl;

}

template<typename Node>
void draw_path (Mat& graph, vector<Node>& path) {

	Mat map = graph;
	for (auto node : path) {
		int row, col;
		tie (row, col) = node;
		map.at<uchar>(row, col) = (uchar) 0;
	}

	imwrite("data/map.jpg", map*255);

}


