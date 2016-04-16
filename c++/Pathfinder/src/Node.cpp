/*
 * Node.cpp
 *
 *  Created on: Apr 14, 2016
 *      Author: saverio
 */

#include "../headers/Node.h"

Node :: Node () {}

Node :: Node (const int row, const int col, double gscore, double fscore, Node* parent) {
	this->r = row;
	this->c = col;
	this->g = gscore;
	this->f = fscore;
	this->p = parent;
}

Node :: ~Node () {}

int Node :: row () {
	return this->r;
}

int Node :: col () {
	return this->c;
}

double Node :: gscore () {
	return this->g;
}

double Node :: fscore () {
	return this->f;
}

Node* Node :: parent () {
	return this->p;
}

void Node :: gscore (double gscore) {
	this->g = gscore;
}

void Node :: fscore (double fscore) {
	this->f = fscore;
}

void Node :: parent (Node* parent) {
	this->p = parent;
}

bool Node :: operator==(Node* node) {

	if (this->r == node->row() and this->c == node->col()) {
		return true;
	} else {
		return false;
	}

}

ostream& operator<<(ostream& os, const Node &node) {
	os << "(" << node.r << ", " << node.c << ")";
	return os;
}
