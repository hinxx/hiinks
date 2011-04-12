'''
Created on Apr 11, 2011

@author: hinko
'''
# VLC code from Qt example for VLC Python bindings
# Added some test LIRC control via pylirc

import sys
from PyQt4 import QtCore, QtGui, Qt
import vlc

class VLCPlayer(QtGui.QWidget):

    def __init__(self, parent = None, video_frame = None):
        QtGui.QWidget.__init__(self, parent)

        # Creating a basic VLC instance
        self.vlc_instance = vlc.Instance()
        self.vlc_instance.set_log_verbosity(3)
        self.vlc_log = self.vlc_instance.log_open()

        print "VLC verbosity : %d" % self.vlc_instance.get_log_verbosity()
        print "VLC msg count : %d" % self.vlc_log.count()

        # Creating an empty VLC media player
        self.media_player = self.vlc_instance.media_player_new()
        self.is_paused = False

        self.video_frame = video_frame

        # UI update timer
#        self.ui_timer = QtCore.QTimer(self)
#        self.ui_timer.setInterval(200)
#        QtCore.QObject.connect(self.ui_timer, QtCore.SIGNAL("timeout()"), self.update_UI)


    def open(self, mrl, stream = False):
        if not mrl:
            return

        print "opening MRL %s .." % mrl

        # Create the media
        if stream:
            self.media = self.vlc_instance.media_new_location(unicode(mrl))
        else:
            self.media = self.vlc_instance.media_new(unicode(mrl))

        print "MEdia: %s " % type(self.media)

        # Put the media in the media player
        self.media_player.set_media(self.media)

        print "MEdia2: %s " % type(self.media)
        print "Media MRL: %s" % self.media.get_mrl()
        print "media state %s" % self.media.get_state()

        # Parse the metadata of the file
        if not stream:
            self.media.parse()

        # the media player has to be 'connected' to the QFrame
        # (otherwise a video would be displayed in it's own window)
        # this is platform specific!
        # you have to give the id of the QFrame (or similar object) to
        # vlc, different platforms have different functions for this
        if self.video_frame:
            if sys.platform == "linux2": # for Linux using the X Server
                self.media_player.set_xwindow(self.video_frame.winId())
            elif sys.platform == "win32": # for Windows
                self.media_player.set_hwnd(self.video_frame.winId())
            elif sys.platform == "darwin": # for MacOS
                self.media_player.set_agl(self.video_frame.windId())


        self.play_pause()

    def play_pause(self):
        print "play_pause.."

        if self.media_player.is_playing():
            self.media_player.pause()
            #self.ui.pushButton_play.setText("Play")
            self.is_paused = True
        else:
#            if self.media_player.play() == -1:
#                return
            self.media_player.play()
            #self.ui.pushButton_play.setText("Pause")
            #self.ui_timer.start()
            self.is_paused = False
        print "VLC msg count : %d" % self.vlc_log.count()

    def stop(self):
        print "stop.."

        self.media_player.stop()
        #self.ui.pushButton_play.setText("Play")

    def set_position(self, pos):
        print "set_position pos = %d" % pos

        # setting the position to where the slider was dragged
        self.media_player.set_position(pos / 1000.0)
        # the vlc MediaPlayer needs a float value between 0 and 1, Qt
        # uses integer variables, so you need a factor; the higher the
        # factor, the more precise are the results
        # (1000 should be enough)

    def set_volume(self, pos):
        print "set_volume pos = %d" % pos

        self.media_player.audio_set_volume(pos)

    def set_fullscreen(self, root, mode = False):
        old_mode = self.media_player.get_fullscreen()
        new_mode = int(mode)
#        print "set_fullscreen: old mode %s, new mode %s" % (old_mode, new_mode)

        print "self.video_frame: %s" % self.video_frame.winId()
        self.media_player.set_fullscreen(new_mode)

        if new_mode:
            print "FULLSCREEN"
            # New frame for fullscreen
            full = QtGui.QFrame()
            self.media_player.set_xwindow(full.winId())
#            print "full: %s" % full
            print "full: %s" % full.winId()
        else:
            print "EMBEDD"
            self.media_player.set_xwindow(self.video_frame.winId())

