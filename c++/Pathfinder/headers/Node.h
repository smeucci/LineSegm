/*
 * Node.h
 *
 *  Created on: Apr 14, 2016
 *      Author: saverio
 */

#ifndef NODE_H_
#define NODE_H_

#include <math.h>
#include <stdlib.h>
#include <iostream>

using namespace std;

class Node {

	private:
		int r;
		int c;
		double g;
		double f;
		Node* p;

	public:
		Node ();
		Node (const int row, const int col, double gscore = INFINITY, double fscore = 0, Node* parent = NULL);
		~Node();
		// getter
		int row ();
		int col ();
		double gscore ();
		double fscore ();
		Node* parent ();

		// setter
		void gscore (double gscore);
		void fscore (double fscore);
		void parent (Node* parent);

		bool operator==(Node& node);
		friend ostream& operator<<(ostream& os, const Node& node);

};

#endif /* NODE_H_ */
