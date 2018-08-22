#!/usr/bin/env python2
"""
Logpuzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Google's Python Class
http://code.google.com/edu/languages/google-python-class/

Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"

"""

import os
import re
import sys
import urllib
import argparse


def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""

    urls = []
    # file = open(filename, 'r')
    # content = file.readlines()
    with open(filename, 'r') as f:
        for line in f:
            if 'puzzle' in line:
                match = re.search(r'GET\s(.*)HTTP', line)
                url = match.group(1)
                urls.append(url.strip())

    urls = sorted(set(urls))
    for url in urls:
        print url[-8:-4]
    return urls


read_urls('./animal_code.google.com')


def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """
    # Creating the directory if the directory does not already exist
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    os.chdir(dest_dir)
    path = os.getcwd()

    # Creating and Writing file
    file = open('index.html', 'w')
    file.write('<html>\n<main>\n<body>\n')

    # Run through the urls and if the does not exist already download the file
    # into the dirctory
    for index, url in enumerate(img_urls):
        img_name = 'img' + str(index + 1)

        if img_name not in os.listdir(os.getcwd()):
            urllib.urlretrieve('http://code.google.com' + url, img_name)
            print 'Downloaded ' + img_name + " " + \
                str(index + 1) + " images downloaded"
            file.write('<img src="' + os.path.join(path, img_name) + '">')
    file.write('</body>\n</html>')
    file.close()
    print 'Download Complete!'


def create_parser():
    """Create an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--todir',  help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parse args, scan for urls, get images from urls"""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
