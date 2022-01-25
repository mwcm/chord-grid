
class Audacity:

    def __init__(self, audio_file_path=None, audacity_path=None, pipe_names=None):
        self.audio_file_path = audio_file_path
        self.audacity_path = audacity_path

            #if sys.platform == 'win32':
                #print("pipe-test.py, running on windows")
                #TONAME = '\\\\.\\pipe\\ToSrvPipe'
                #FROMNAME = '\\\\.\\pipe\\FromSrvPipe'
                #EOL = '\r\n\0'
            #else:
                #print("pipe-test.py, running on linux or mac")
                #TONAME = '/tmp/audacity_script_pipe.to.' + str(os.getuid())
                #FROMNAME = '/tmp/audacity_script_pipe.from.' + str(os.getuid())
                #EOL = '\n'

        self.open_audacity(self.audacity_path)

        return

    
    def open_audacity(self, audacity_path=None):
        # try self.audacity_path if none provided
        return


    def connect(self):
        ''' connect via mod-script-pipe '''
        return


    def import_audio(self, audio_file_path=None):
        # try self.audio_file_path if none provided
        return

        
    # note: this might be overkill
    # def do_command(self):
        # this need command, options args
        # return


    def add_label_track(self, track_name):
        return


    def add_label(self, label_ts, label_txt):
        return


    def save_project(self, project_name):
        return