from __future__ import print_function
import numpy as np
import tensorflow as tf
import sys
import urllib2

import argparse
import time
import os
from six.moves import cPickle

from utils import TextLoader
from model import Model

search = str(sys.argv[1])
print (search)
address = 'http://search.azlyrics.com/search.php?q='+search+'&p=0&w=songs'
response = urllib2.urlopen(address)
xData = response.read()
file = open("data/tinyshakespeare/input.txt","a+")

# Get list of songs that match word
lines = xData.splitlines()

# Go through webpage of 20 song lists and put them in a list
write = False
counter = 0
arr = []
for line in lines:
    line = line.strip()
    if line =='<div id="wordads-preview-parent" class="wpcnt">':
        write = False
    
    indx = line.find('<a href="')
    if indx > -1 and counter < 20:
        end = line.find('" target=')
        start = indx+9
        link = line[start:end]
        arr.append(link)
        counter = counter + 1

    if line =='<tr><td class="text-left visitedlyr">':
        write = True

# Go through the list of song links
# Visit each page, extract the lyrics & remove unwanted characters
# Add the lyrics to the database
if len(arr) > 0:
    # Process each song link
    for songAdd in arr:
        curResp = urllib2.urlopen(songAdd)
        curData = curResp.read()
        curLines = curData.splitlines()
    
        write = False
        # For each song web page get lyrics
        for lyricLine in curLines:
            chkStart = '<!-- Usage of azlyr'
            chkEnd = '<!-- MxM banner -->'
            curStart = lyricLine[0:19] # start of each line read in
            
            if curStart == chkEnd:
                write = False
    
            if write:
                # Make everything lowercase
                lyricLine = lyricLine.lower()
                # Remove HTML tags
                lyricLine = lyricLine.replace("<p>","")
                lyricLine = lyricLine.replace("</p>","")
                lyricLine = lyricLine.replace("<div>","")
                lyricLine = lyricLine.replace("</div>","")
                lyricLine = lyricLine.replace("<br>","")
                lyricLine = lyricLine.replace("<i>","")
                lyricLine = lyricLine.replace("</i>","")
                lyricLine = lyricLine.replace("<b>","")
                lyricLine = lyricLine.replace("</b>","")
                # Remove puncuation
                lyricLine = lyricLine.replace("verse","")
                lyricLine = lyricLine.replace("pre-chorus","")
                lyricLine = lyricLine.replace("chorus","")
                lyricLine = lyricLine.replace("breakdown","")
                lyricLine = lyricLine.replace("intro","")
                lyricLine = lyricLine.replace("outro","")
                lyricLine = lyricLine.replace("solo","")
                lyricLine = lyricLine.replace("instrumental","")
                lyricLine = lyricLine.replace("&quot","")
                # Remove puncuation
                lyricLine = lyricLine.replace("'","")
                lyricLine = lyricLine.replace("\"","")
                lyricLine = lyricLine.replace(",","")
                lyricLine = lyricLine.replace("!","")
                lyricLine = lyricLine.replace("(","")
                lyricLine = lyricLine.replace(")","")
                lyricLine = lyricLine.replace(".","")
                lyricLine = lyricLine.replace("/","")
                lyricLine = lyricLine.replace("\\","")
                lyricLine = lyricLine.replace("[","")
                lyricLine = lyricLine.replace("]","")
                lyricLine = lyricLine.replace(":","")
                lyricLine = lyricLine.replace(";","")
                lyricLine = lyricLine.replace("?","")
                lyricLine = lyricLine.replace("-","")
                lyricLine = lyricLine.replace("&","")
                # Write file
                file.write(lyricLine)
                file.write('\n')
    
            if curStart == chkStart:
                write = True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default='data/tinyshakespeare',
                        help='data directory containing input.txt')
    parser.add_argument('--save_dir', type=str, default='save',
                       help='directory to store checkpointed models')
    parser.add_argument('--rnn_size', type=int, default=256,
                       help='size of RNN hidden state')
    parser.add_argument('--num_layers', type=int, default=2,
                       help='number of layers in the RNN')
    parser.add_argument('--model', type=str, default='lstm',
                       help='rnn, gru, or lstm')
    parser.add_argument('--batch_size', type=int, default=50,
                       help='minibatch size')
    parser.add_argument('--seq_length', type=int, default=25,
                       help='RNN sequence length')
    parser.add_argument('--num_epochs', type=int, default=50,
                       help='number of epochs')
    parser.add_argument('--save_every', type=int, default=1000,
                       help='save frequency')
    parser.add_argument('--grad_clip', type=float, default=5.,
                       help='clip gradients at this value')
    parser.add_argument('--learning_rate', type=float, default=0.002,
                       help='learning rate')
    parser.add_argument('--decay_rate', type=float, default=0.97,
                       help='decay rate for rmsprop')
    parser.add_argument('--init_from', type=str, default=None,
                       help="""continue training from saved model at this path. Path must contain files saved by previous training process:
                            'config.pkl'        : configuration;
                            'words_vocab.pkl'   : vocabulary definitions;
                            'checkpoint'        : paths to model file(s) (created by tf).
                                                  Note: this file contains absolute paths, be careful when moving files around;
                            'model.ckpt-*'      : file(s) with model definition (created by tf)
                        """)
    args = parser.parse_args()

if __name__ == '__main__':
    main()
