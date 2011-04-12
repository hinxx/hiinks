'''
Created on Apr 10, 2011

@author: hinko
'''

# VLC code from Qt example for VLC Python bindings
# Added some test LIRC control via pylirc

import sys
from PyQt4 import QtCore, QtGui, Qt
from ui.pylirc_ui3 import Ui_MainWindow

from lircThread import LircThread
from media import Media
from vlcplayer import VLCPlayer

class Main(QtGui.QMainWindow):

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setWindowTitle("H&M Media Player")

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        QtCore.QObject.connect(self.ui.pushButton_exit, QtCore.SIGNAL("clicked()"), app, QtCore.SLOT("closeAllWindows()"))
        QtCore.QObject.connect(self.ui.pushButton_play, QtCore.SIGNAL("clicked()"), self.video_play_pause)
        QtCore.QObject.connect(self.ui.pushButton_stop, QtCore.SIGNAL("clicked()"), self.video_stop)
        QtCore.QObject.connect(self.ui.pushButton_open, QtCore.SIGNAL("clicked()"), self.video_open)

        QtCore.QObject.connect(self.ui.horizontalSlider_video, QtCore.SIGNAL("sliderMoved(int)"), self.video_set_position)
        QtCore.QObject.connect(self.ui.horizontalSlider_audio, QtCore.SIGNAL("valueChanged(int)"), self.audio_set_volume)

        self.lirc_thread = LircThread()
        QtCore.QObject.connect(self.lirc_thread, QtCore.SIGNAL("key(QString, int)"), self.lirc_handle)
        self.lirc_thread.doRun()

        # Init listboxes
        self.init_video()

    def init_video(self):
        print "init_video.."
        m = Media()
        files = m.scan_folders()
        for fil in files:
            i = QtGui.QListWidgetItem(fil)
            self.ui.listWidget_video.addItem(i)

        self.vlcplayer = VLCPlayer(self, self.ui.frame_video_wrap)
        self.fullscreen = False

    def video_open(self, mrl):
        print "video_open.."
        print "MRL: %s" % mrl

        self.vlcplayer.open(mrl, False)
        self.setWindowTitle("Playing " + mrl)

    def video_play_pause(self):
        print "video_play_pause.."
        self.vlcplayer.play_pause()

    def video_stop(self):
        print "video_stop.."
        self.vlcplayer.stop()

    def video_set_position(self, pos):
        print "video_set_position pos = %d" % pos

    def audio_set_volume(self, pos):
        print "audio_set_volume pos = %d" % pos

    def fullscreen_mode(self):
        self.fullscreen = not self.fullscreen
        self.vlcplayer.set_fullscreen(self, self.fullscreen)

    def lirc_handle(self, key, repeat):
        print "lirc_handle: event from LircThread: key = %s, repeat = %d" % (key, repeat)
        self.statusBar().showMessage("Last remote key: %s" % key)

        if key == 'video':
            self.ui.toolBox.setCurrentWidget(self.ui.video)
        elif key == 'tv':
            self.ui.toolBox.setCurrentWidget(self.ui.tv)
        elif key == 'music':
            self.ui.toolBox.setCurrentWidget(self.ui.music)
        elif key == 'photo':
            self.ui.toolBox.setCurrentWidget(self.ui.photo)
        elif key == 'arrow_up':
            i = self.ui.listWidget_video.currentRow() - 1
            if i < 0:
                i = 0
            self.ui.listWidget_video.setCurrentRow(i)
        elif key == 'arrow_down':
            i = self.ui.listWidget_video.currentRow() + 1
            if i >= self.ui.listWidget_video.count():
                i = self.ui.listWidget_video.count() - 1
            self.ui.listWidget_video.setCurrentRow(i)
        elif key == 'enter':
            self.video_open(self.ui.listWidget_video.currentItem().text())
        elif key == 'power':
            self.fullscreen_mode()


#        if key == 'play' or key == 'pause':
#            self.video_play_pause()
#        elif key == 'stop':
#            self.video_stop()
#        elif key == 'volume_up':
#            pos = self.ui.horizontalSlider_audio.value()
#            pos += 10
#            if pos > 100:
#                pos = 100
#            self.ui.horizontalSlider_audio.setValue(pos)
#            self.audio_set_volume(pos)
#        elif key == 'volume_down':
#            pos = self.ui.horizontalSlider_audio.value()
#            pos -= 10
#            if pos < 0:
#                pos = 0
#            self.ui.horizontalSlider_audio.setValue(pos)
#            self.audio_set_volume(pos)
#        elif key == 'arrow_right':
#            pos = self.ui.horizontalSlider_video.value()
#            pos += 100
#            if pos > 1000:
#                pos = 1000
#            self.ui.horizontalSlider_video.setValue(pos)
#            self.video_set_position(pos)
#        elif key == 'arrow_left':
#            pos = self.ui.horizontalSlider_video.value()
#            pos -= 100
#            if pos < 0:
#                pos = 0
#            self.ui.horizontalSlider_video.setValue(pos)
#            self.video_set_position(pos)
#
#        else:
#            print "Unhandled remote KEY: %s" % key

#    def __init__(self, parent = None):
#        QtGui.QWidget.__init__(self, parent)
#        self.setWindowTitle("H&M Media Player")
#
#        # Creating a basic VLC instance
#        self.vlc_instance = vlc.Instance()
#        self.vlc_instance.set_log_verbosity(3)
#        self.vlc_log = self.vlc_instance.log_open()
#
#        print "VLC verbosity : %d" % self.vlc_instance.get_log_verbosity()
#        print "VLC msg count : %d" % self.vlc_log.count()
#
#        # Creating an empty VLC media player
#        self.media_player = self.vlc_instance.media_player_new()
#        self.is_paused = False
#
#        self.ui = Ui_MainWindow()
#        self.ui.setupUi(self)
#
#        QtCore.QObject.connect(self.ui.pushButton_exit, QtCore.SIGNAL("clicked()"), app, QtCore.SLOT("closeAllWindows()"))
#        QtCore.QObject.connect(self.ui.pushButton_play, QtCore.SIGNAL("clicked()"), self.video_play_pause)
#        QtCore.QObject.connect(self.ui.pushButton_stop, QtCore.SIGNAL("clicked()"), self.video_stop)
#        QtCore.QObject.connect(self.ui.pushButton_open, QtCore.SIGNAL("clicked()"), self.video_open)
#
#        QtCore.QObject.connect(self.ui.horizontalSlider_video, QtCore.SIGNAL("sliderMoved(int)"), self.video_set_position)
#        QtCore.QObject.connect(self.ui.horizontalSlider_audio, QtCore.SIGNAL("valueChanged(int)"), self.audio_set_volume)
#
#        self.lirc_thread = LircThread()
#        QtCore.QObject.connect(self.lirc_thread, QtCore.SIGNAL("key(QString, int)"), self.lirc_handle)
#        self.lirc_thread.doRun()
#
#        # UI update timer
#        self.ui_timer = QtCore.QTimer(self)
#        self.ui_timer.setInterval(200)
#        QtCore.QObject.connect(self.ui_timer, QtCore.SIGNAL("timeout()"), self.update_UI)
#
#    def video_open(self):
#        #filename = QtGui.QFileDialog.getOpenFileName(self, "Open File", user.home)
#
#        filename = "http://localhost:8080"
#
#        if not filename:
#            return
#
#        print "opening %s .." % filename
#
#        # Create the media
#        #if filename.startswith('http'):
#        self.media = self.vlc_instance.media_new_location("http://localhost:8080")
#        #else:
#        #    self.media = self.vlc_instance.media_new(unicode(filename))
#
#        print "MEdia: %s " % type(self.media)
#
#        # Put the media in the media player
#        self.media_player.set_media(self.media)
#
#        print "MEdia2: %s " % type(self.media)
#        print "Media MRL: %s" % self.media.get_mrl()
#        print "media state %s" % self.media.get_state()
#
#        # Parse the metadata of the file
#        #self.media.parse()
#        #print "MEdia3: %s " % type(self.media)
#
#        # Set the title of the track as window title
#        #self.setWindowTitle(self.media.get_meta(0))
#
#        # the media player has to be 'connected' to the QFrame
#        # (otherwise a video would be displayed in it's own window)
#        # this is platform specific!
#        # you have to give the id of the QFrame (or similar object) to
#        # vlc, different platforms have different functions for this
#        if sys.platform == "linux2": # for Linux using the X Server
#            self.media_player.set_xwindow(self.ui.frame_video.winId())
#        elif sys.platform == "win32": # for Windows
#            self.media_player.set_hwnd(self.ui.frame_video.winId())
#        elif sys.platform == "darwin": # for MacOS
#            self.media_player.set_agl(self.ui.frame_video.windId())
#
#        # Set volume
#        #self.ui.horizontalSlider_audio.setValue(vlc.libvlc_audio_get_volume(self.vlc_instance))
#
#        self.video_play_pause()
#
#    def video_play_pause(self):
#        print "video_play_pause.."
#
#        if self.media_player.is_playing():
#            self.media_player.pause()
#            self.ui.pushButton_play.setText("Play")
#            self.is_paused = True
#        else:
#            if self.media_player.play() == -1:
#                self.video_open()
#                return
#            self.media_player.play()
#            self.ui.pushButton_play.setText("Pause")
#            self.ui_timer.start()
#            self.is_paused = False
#        print "VLC msg count : %d" % self.vlc_log.count()
#
#    def video_stop(self):
#        print "video_stop.."
#
#        self.media_player.stop()
#        self.ui.pushButton_play.setText("Play")
#
#    def video_set_position(self, pos):
#        print "video_set_position pos = %d" % pos
#
#        # setting the position to where the slider was dragged
#        self.media_player.set_position(pos / 1000.0)
#        # the vlc MediaPlayer needs a float value between 0 and 1, Qt
#        # uses integer variables, so you need a factor; the higher the
#        # factor, the more precise are the results
#        # (1000 should be enough)
#
#    def audio_set_volume(self, pos):
#        print "audio_set_volume pos = %d" % pos
#
#        self.media_player.audio_set_volume(pos)
#
#    def update_UI(self):
#        # setting the slider to the desired position
#        self.ui.horizontalSlider_video.setValue(self.media_player.get_position() * 1000)
#
#        if not self.media_player.is_playing():
#            # no need to call this function if nothing is played
#            self.ui_timer.stop()
#            if not self.is_paused:
#                # after the video finished, the play button stills shows
#                # "Pause", not the desired behavior of a media player
#                # this will fix it
#                self.video_stop()


###############################################################################
#
#
#        MAIN
#
#
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    myapp = Main()
    myapp.show()
    print "Executing!"
    ret = app.exec_()
    print "Ended!"
    sys.exit(ret)
