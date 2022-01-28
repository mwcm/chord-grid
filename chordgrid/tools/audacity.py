import sys
import os

class Audacity:

    def __init__(self, audio_file_path=None, audacity_path=None):
        self.audio_file_path = audio_file_path
        self.audacity_path = audacity_path
        self.TONAME = '/tmp/audacity_script_pipe.to.' + str(os.getuid())
        self.FROMNAME = '/tmp/audacity_script_pipe.from.' + str(os.getuid())
        self.EOL = '\n'

        if sys.platform == 'win32':
            self.TONAME = '\\\\.\\pipe\\ToSrvPipe'
            self.FROMNAME = '\\\\.\\pipe\\FromSrvPipe'
            self.selfEOL = '\r\n\0'

        if not os.path.exists(self.TONAME):        
            raise Exception(f'No file {self.TONAME}, ensure audacity is running with mod-script-pipe')
        if not os.path.exists(self.FROMNAME):        
            raise Exception(f'No file {self.FROMNAME}, ensure audacity is running with mod-script-pipe')

        self.TOFILE = open(self.TONAME, 'w')
        self.FROMFILE = open(self.FROMNAME, 'rt')
        return

    
    def open_audacity(self, audacity_path=None):
        # try self.audacity_path if none provided
        return


    def import_audio(self, audio_file_path=None):
        # try self.audio_file_path if none provided
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


    def add_label_track(self, track_name):
        self.do_command('')
        return


    def add_label(self, ts, txt):
        self.do_command('AddLabel: ')
        self.do_command(f'SetLabel: Label="0" Start="{ts}" End="{ts}" Text="{txt}"')
        return


    def save_project(self, path):
        return