import sys
import os
from subprocess import Popen

class Audacity:

    def __init__(self, audacity_path=None):
        self.audacity_path = audacity_path
        self.TONAME = '/tmp/audacity_script_pipe.to.' + str(os.getuid())
        self.FROMNAME = '/tmp/audacity_script_pipe.from.' + str(os.getuid())
        self.EOL = '\n'
        self.audacity_path = '/usr/bin/audacity'

        if audacity_path:
            self.audacity_path = audacity_path
        else:
            if sys.platform == 'darwin':
                self.audacity_path = '/Applications/Audacity.app'
            if sys.platform == 'win32':
                self.audacity_path = 'C:\Program Files\Audacity\Audacity.exe'
                self.TONAME = '\\\\.\\pipe\\ToSrvPipe'
                self.FROMNAME = '\\\\.\\pipe\\FromSrvPipe'
                self.selfEOL = '\r\n\0'

        if not os.path.exists(self.TONAME):        
            raise Exception(f'No file {self.TONAME}, ensure audacity is running with mod-script-pipe')
        if not os.path.exists(self.FROMNAME):        
            raise Exception(f'No file {self.FROMNAME}, ensure audacity is running with mod-script-pipe')
        if not os.path.exists(self.audacity_path):
            raise Exception(f'No File {self.audacity_path}, ensure audacity is installed at the requested path.')

        self.TOFILE = open(self.TONAME, 'w')
        self.FROMFILE = open(self.FROMNAME, 'rt')
        return

    
    def open_audacity(self, audacity_path=None):
        if not audacity_path:
            audacity_path = self.audacity_path
        Popen(audacity_path)
        return

        
    def send_command(self, command):
        self.TOFILE.write(command + self.EOL)
        self.TOFILE.flush()
        return


    def get_response(self):
        result = ''
        line = ''
        while True:
            result += line
            line = self.FROMFILE.readline()
            if line == '\n' and len(result) > 0:
                break
        return result


    def do_command(self, command):
        self.send_command(command)
        response = self.get_response()
        return response


    def import_audio(self, audio_file_path):
        return


    def add_label_track(self, track_name):
        self.do_command('NewLabelTrack: ')
        self.do_command(f'SetTrackStatus" Name={track_name}')
        return


    def add_label(self, ts, txt):
        self.do_command('AddLabel: ')
        self.do_command(f'SetLabel: Label="0" Start="{ts}" End="{ts}" Text="{txt}"')
        return


    def save_project(self, path):
        return