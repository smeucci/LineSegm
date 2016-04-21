/*
 * sauvola.cpp
 *
 *  Created on: Apr 20, 2016
 *      Author: saverio
 */


#include "opencv2/opencv.hpp"

using namespace cv;
using namespace std;


inline void padding (Mat& im, Mat&out, int window) {
	int pad = (int) round((double) window / 2);
	copyMakeBorder(im, out, pad, pad, pad, pad, BORDER_CONSTANT);
}

inline void compute_integrals (Mat& im, Mat& im_mean, Mat& im_std, int window) {


	int window_height, window_width, window_area, m;
	double mean, std, sum, sqsum;

	window_height = window_width = window;
	window_area = window_height * window_width;
	m = window_height / 2;

	Mat im_sum, im_sqsum;
	cv::integral(im, im_sum, im_sqsum, CV_64F);

	for	(int i = m; i <= im.rows - m - 1; i++){
		sum = sqsum = 0;

		sum = im_sum.at<double>(i - m + window_width, window_height) - im_sum.at<double>(i - m, window_height) -
			  im_sum.at<double>(i - m + window_width, 0) + im_sum.at<double>(i - m, 0);

		sqsum = im_sqsum.at<double>(i - m + window_width, window_height) - im_sqsum.at<double>(i - m, window_height) -
				im_sqsum.at<double>(i - m + window_width, 0) + im_sqsum.at<double>(i - m, 0);

		mean  = sum / window_area;
		std  = sqrt((sqsum - mean * sum) / window_area);

		im_mean.at<double>(i, m) = mean;
		im_std.at<double>(i, m) = std;

		// Shift the window, add and remove	new/old values to the histogram
		for	(int j = 1; j <= im.cols - window_height; j++) {

			// Remove the left old column and add the right new column
			sum -= im_sum.at<double>(i - m + window_width, j) - im_sum.at<double>(i - m, j) -
				   im_sum.at<double>(i - m + window_width, j - 1) + im_sum.at<double>(i - m, j - 1);

			sum += im_sum.at<double>(i - m + window_width, j + window_height) - im_sum.at<double>(i - m, j + window_height) -
				   im_sum.at<double>(i - m + window_width, j + window_height-1) + im_sum.at<double>(i - m, j + window_height - 1);

			sqsum -= im_sqsum.at<double>(i - m + window_width,j) - im_sqsum.at<double>(i - m, j) -
					 im_sqsum.at<double>(i - m + window_width,j-1) + im_sqsum.at<double>(i - m, j - 1);

			sqsum += im_sqsum.at<double>(i - m + window_width, j + window_height) - im_sqsum.at<double>(i - m, j + window_height) -
					 im_sqsum.at<double>(i - m + window_width, j + window_height - 1) + im_sqsum.at<double>(i - m, j + window_height - 1);

			mean  = sum / window_area;
			std  = sqrt((sqsum - mean * sum)/window_area);

			im_mean.at<double>(i, j + m) = mean;
			im_std.at<double>(i, j + m) = std;

		}
	}

}

inline void binarize (Mat& im, Mat& output, int window, double dr, double k) {


	Mat im_mean = Mat::zeros (im.rows, im.cols, CV_64F);
	Mat im_std = Mat::zeros (im.rows, im.cols, CV_64F);
	compute_integrals(im, im_mean, im_std, window);

	double mean, std, th;
	int window_height, window_width, m;

	window_height = window_width = window;
	m = window_height / 2;

	Mat threshold (im.rows, im.cols, CV_64F);

	for	(int i = m; i <= im.rows - m - 1; i++) {

		for	(int j = 0; j <= im.cols - window_width; j++) {

			mean = im_mean.at<double>(i, j + m);
			std = im_std.at<double>(i, j + m);

			th = mean * (1 + k * (std / dr - 1));

			threshold.at<double>(i, j + m) = th;

			if (j == 0) {
				for (int j = 0; j <= m; ++j) {
					threshold.at<double>(i, j) = th;
				}

				if (i == m)
					for (int k = 0; k  <m; ++k) {
						for (int h = 0; h <= m; ++h) {
							threshold.at<double>(k, h) = th;
						}
					}

				if (i == im.cols - m - 1) {
					for (int k = im.cols - m; k < im.rows; ++k) {
						for (int h = 0; h <= m; ++h) {
							threshold.at<double>(k, h) = th;
						}
					}
				}
			}

			if (i == m) {
				for (int k = 0; k < m; ++k) {
					threshold.at<double>(k, j + m) = th;
				}
			}

			if (i == im.cols - m - 1) {
				for (int k = im.cols - m; k < im.rows; ++k) {
					threshold.at<double>(k, j + m) = th;
				}
			}
		}

		for (int j = im.cols - m - 1; j < im.cols; ++j) {
			threshold.at<double>(i, j) = th;
		}

		if (i == m) {
			for (int k = 0; k < m; ++k) {
				for (int h = im.cols - m - 1; h < im.cols; ++h) {
					threshold.at<double>(k, h) = th;
				}
			}
		}

		if (i == im.cols - m - 1) {
			for (int k = im.cols - m; k < im.rows; ++k) {
				for (int h = im.cols - m - 1; h < im.cols; ++h) {
					threshold.at<double>(k, h) = th;
				}
			}
		}
	}

	for	(int i = 0; i < im.rows; ++i) {
		for	(int j = 0; j < im.cols; ++j) {
			if ((double) im.at<uchar>(i, j) >= threshold.at<double>(i, j)) {
				output.at<uchar>(i, j) = (uchar) 255;
			} else {
				output.at<uchar>(i, j) = (uchar) 0;
			}
		}
	}


}


