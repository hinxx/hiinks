'''
Created on Apr 11, 2011

@author: hinko
'''

import os
import sys
import user
import magic

class Media():

    def __init__(self):

        self.folders = [user.home + '/Videos']
        self.video_type = ['avi', 'wmv', 'mp4']
        self.videos = []
        self.magic = magic.open(magic.MAGIC_MIME)
        self.magic.load()
        #self.mime = magic.Magic(mime = True)

    def scan_folders(self):
        print "Scanning folders for media .."
        for fol in self.folders:
            print "Folder: %s" % fol
            files = os.listdir(fol)
            print "Files: %s" % files
            for fil in files:
                fil_path = fol + '/' + fil
                (mime, charset) = self.magic.file(fil_path).split(';')
                #mime = self.magic.from_file(fil_path)
                print "File: %s, MIME: %s" % (fil_path, mime)
                if mime.startswith('video'):
                    self.videos.append(fil_path)

        print "Found video files:"
        print self.videos

        return self.videos
