"""
##############################
###### THE CAM2 PROJECT ######
##############################
Authors: Caleb Tung,
Created: 6/13/2017
Python 3.x

Brief:
   This module uses Streamlink to find a livestream src URL on a webpage.

Usage:
   python fetchstreamsrc.py [WEBPAGE]

Notes and Warnings:
   This is currently a test script and IS NOT ROBUST. Do not use for production.
"""

from __future__ import print_function # Force the use of Python3.x print()

import re
import sys
import streamlink


def get_stream_src_from_url(page_url):
    """
    Fetches the source URL of a livestream on a given webpage

    @param page_url the URL of the webpage with a livestream on it

    @return the URL of the livestream source
    """

    src_url = None # The source URL to return

    try:
        page_streams = streamlink.streams(page_url) # Get a dictionary of all streams

        # TODO: Figure out how to handle multiple different streams (not just one stream
        #       with multiple resolutions

        # TODO: Find a way to collect the frame width and height, along with FPS, if
        #       possible.  Might need to use FFmpeg?

        if len(page_streams) >= 1:
            if 'best' in page_streams: # Default choose the stream with best resolution
                src_url = page_streams['best'].url
            else: # No 'best' resolution was determined
                unused_key, stream_val = page_streams.popitem() # Just get the first one
                src_url = stream_val.url

    except streamlink.exceptions.PluginError as perr:
        # If no suitable URL can be confirmed, Streamlink may suggest a potential one
        # e.g. //bla.com/stream.m3u8 which is perfectly legit once 'http:' is prepended
        # Extract it from the error message with regex
        src_url_match = re.search(r"Invalid URL '(.*?)'", str(perr), re.M|re.I)
        if src_url_match != None:
            src_url = 'http:' + str(src_url_match.group(1))

            # TODO: Implement check to see if http:// needs to be prepended

    return src_url


if __name__ == '__main__':
    EXPECTED_NUM_ARGS = 1 + 1

    if len(sys.argv) < EXPECTED_NUM_ARGS:
        print('Expected ' + str(+ EXPECTED_NUM_ARGS-1) + ' cmd line args.')
    else:
        print(get_stream_src_from_url(sys.argv[1]))