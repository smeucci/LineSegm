import cv2
import os
from os import listdir
import xml.etree.ElementTree as parser
import numpy as np
import pprint
from time import time as timer


########################
#    DRAW FUNCTIONS    #
########################

def draw_line(image, points):
    
    for i in range(0, len(points) - 1):
        point = points[i]
        next_point = points[i+1]
        cv2.line(image, point, next_point, 150)
    

##############################
#      PARSING FUNCTIONS     #
##############################

def get_textline(root):
    lines = []
    for textregion in root.iter("TextRegion"):
        if textregion.attrib.get('type') == 'textline':
            for coords in textregion.iter("Coords"):
                lines.append(coords._children)
                
    return lines
    
def get_points(line):
    
    points = []
    for point in line:
        point = point.attrib
        row = int(point.get("y"))
        col = int(point.get("x"))
        point = (col, row)
        points.append(point)
    
    return points

    
###########################
#    SAVUOLA FUNCTIONS    #
###########################
    
def binarize(im, window, dr, k):
    # get the image dimensions
    rows, cols = im.shape
    # pad the image based on the window size
    impad = padding(im, window)
    # compute the mean and the squared mean
    mean, sqmean = integralMean(impad, rows, cols, window)
    # compute the variance and the standard deviation
    n = window[0] * window[1]
    variance = (sqmean - (mean**2) / n) / n
    # std = (sqmean - mean ** 2) ** 0.5
    std = variance ** 0.5
    # compute the threshold
    threshold = mean * (1 + k * (std / dr - 1))
    check_border = (mean >= 100)
    threshold = threshold * check_border
    # apply the threshold to the image
    output = np.array(255 * (im >= threshold), 'uint8')

    return output

def padding(im, window):
    pad = int(np.floor(window[0] / 2))
    im = cv2.copyMakeBorder(im, pad, pad, pad, pad, cv2.BORDER_CONSTANT)

    return im

def integralMean(im, rows, cols, window):
    # get the window size
    m, n = window
    # compute the integral images of im and im.^2
    sum, sqsum = cv2.integral2(im)
    # calculate the window area for each pixel
    isum = sum[m:rows + m, n:cols + n] + \
        sum[0:rows, 0:cols] - \
        sum[m:rows + m, 0:cols] - \
        sum[0:rows, n:cols + n]

    isqsum = sqsum[m:rows + m, n:cols + n] + \
        sqsum[0:rows, 0:cols] - \
        sqsum[m:rows + m, 0:cols] - \
        sqsum[0:rows, n:cols + n]
    # calculate the average values for each pixel
    mean = isum / (m * n)
    sqmean = isqsum / (m * n)

    return mean, sqmean


###################################
#     RESIZE DATASET FUNCTIONS    #
###################################

def resize_dataset(folder, new_folder):
    filenames = listdir(folder)
    print "Resizing " + str(len(filenames)) + " images."
    for filename in filenames:
        print "\t" + filename
        image = cv2.imread(folder + filename)
        image = cv2.resize(image, (0,0), fx=0.5, fy=0.5)
        cv2.imwrite(new_folder + filename, image)
        
def crop_dataset(folder, new_folder):
    filenames = listdir(folder)
    print "Cropping " + str(len(filenames)) + " images."
    for filename in filenames:
        print "\t- " + filename
        image = cv2.imread(folder + filename)
        image = image[250:2110, 100:1560]
        cv2.imwrite(new_folder + filename, image)       

#######################
#    MAIN FUNCTION    #
#######################

def parse_groundtruth(dataset_folder, xml_folder, lines_folder):
    
    print '######################################################'
    print '##    CREATING GROUNDTRUTH FOR SAINTGALL DATASET    ##'
    print '######################################################\n'
    
    xmls = listdir(xml_folder)
    print "Parsing " + str(len(xmls)) + " xml files.\n"
    
    for i in range(0, len(xmls)):
        
        xml = xmls[i]
        
        # parse xml
        root = parser.parse(xml_folder + xml).getroot()
        filename = root[1].attrib.get("imageFilename").replace("png", "jpg")
        
        print "## " + str(i + 1) + " ## " + xml + " ==> " + filename
        
        # load image
        image = cv2.imread(dataset_folder + filename, 0)
        image = binarize(image, [20, 20], 128, 0.3)
        
        # create folder
        directory = lines_folder + filename.replace(".jpg", "") + "/"
        if not os.path.isdir(directory):
            os.makedirs(directory)
               
        # get lines from xml
        lines = get_textline(root)
        
        for j in range(0, len(lines)):
            #print "\t- line: " + str(j + 1) + " / " + str(len(lines))
            
            line = lines[j]
            points = get_points(line)
            points = np.array(points)
            
            im = image.copy()
            cv2.fillPoly(im, [points], 255)
            
            output = abs(255 - (abs(255-image)-abs(255-im)))
            #output = output[250:2110, 100:1560]
            cv2.imwrite(directory + "ground_" + str(j + 1) +".jpg", output)


######################
#    SCRIPT START    #
######################

begin = timer()

parse_groundtruth("data/saintgall/images/", "data/saintgall/groundtruth/xml/", "data/saintgall/groundtruth/lines/")

#crop_dataset("data/saintgall/original_images/", "data/saintgall/images/") 
 
print '\n - Elapsed time: ' + str((timer() - begin)) + ' s\n'

