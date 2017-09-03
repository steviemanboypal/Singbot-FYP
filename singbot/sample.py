from __future__ import print_function
import numpy as np
import tensorflow as tf
import pygame
import pygame.midi
from pygame.locals import *
from pygame import midi
from pygame.midi import Input

import argparse
import time
import os
from six.moves import cPickle

from utils import TextLoader
from model import Model

wordcount = 1000

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--save_dir', type=str, default='save',
                       help='model directory to store checkpointed models')
    parser.add_argument('-n', type=int, default= wordcount,
                       help='number of words to sample')
    parser.add_argument('--prime', type=str, default=' ',
                       help='prime text')
    parser.add_argument('--sample', type=int, default=1,
                       help='0 to use max at each timestep, 1 to sample at each timestep, 2 to sample on spaces')

    args = parser.parse_args()
    sample(args)

def sample(args):
    with open(os.path.join(args.save_dir, 'config.pkl'), 'rb') as f:
        saved_args = cPickle.load(f)
    with open(os.path.join(args.save_dir, 'words_vocab.pkl'), 'rb') as f:
        words, vocab = cPickle.load(f)
    model = Model(saved_args, True)
    with tf.Session() as sess:
        tf.initialize_all_variables().run()
        saver = tf.train.Saver(tf.all_variables())
        ckpt = tf.train.get_checkpoint_state(args.save_dir)
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)
            lyrics = model.sample(sess, words, vocab, args.n, args.prime, args.sample)
            #print(lyrics)
            #os.system("say" + " " + lyrics)
            
            words = lyrics.split(' ')

            pygame.init()
            
            pygame.fastevent.init()
            event_get = pygame.fastevent.get
            event_post = pygame.fastevent.post

            pygame.midi.init()
            input_id = pygame.midi.get_default_input_id()
            inp = pygame.midi.Input( input_id )
            
    
            going = True
            i = 0

            while going:
                
                events = event_get()
                for e in events:
                    if e.type in [QUIT]:
                        going = False
                    if e.type in [KEYDOWN]:
                        going = False

                while inp.poll():
                    for e in events:
                        if e.type in [QUIT]:
                            going = False
                        if e.type in [KEYDOWN]:
                            going = False
                    midi_events = inp.read(128)
                    note = str(midi_events[0][0][1])
                    velocity = str(midi_events[0][0][2])
                    #for word in words:
                    if int(note) == 60 and int(velocity) > 80:
                        phrase1 = words[i] + " " + words[i+1] + " " + words[i+2] + " " + words[i+3]
                        os.system("say -r 140 -a 39" + " " + phrase1)
                        print(phrase1)
                        i += 4
                        if i >= wordcount-20:
                            i = 0
                        #time.sleep(0.2)
                
                    if int(note) == 61 and int(velocity) > 80:
                        phrase2 = words[i] + " " + words[i+1] + " " + words[i+2] + " " + words[i+3] + " " + words[i+4] + " " + words[i+5] + " " + words[i+6] + " " + words[i+7] + " " + words[i+8] + " " + words[i+9] + " " + words[i+10] + " " + words[i+11]
                        os.system("say -r 140 -a 39" + " " + phrase2)
                        print(phrase2)
                        i += 12
                        if i >= wordcount-20:
                            i = 0
                        #time.sleep(0.2)
                    
                    if int(note) == 62:
                        going = False
                

                    midi_evs = pygame.midi.midis2events(midi_events, inp.device_id)

                    for m_e in midi_evs:
                            event_post( m_e)

            print ("song ended")
            inp.close()
            pygame.midi.quit()
            pygame.quit()
            exit()


if __name__ == '__main__':
    main()
