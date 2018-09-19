import http.server
import cgi
import base64
import json
from urllib.parse import urlparse, parse_qs
import subprocess
import os

def run_bash_command(command):
    ## call date command ##
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    
    ## Talk with date command i.e. read data from stdout and stderr. Store this info in tuple ##
    ## Interact with process: Send data to stdin. Read data from stdout and stderr, until end-of-file is reached.  ##
    ## Wait for process to terminate. The optional input argument should be a string to be sent to the child process, ##
    ## or None, if no data should be sent to the child.
    (output, err) = p.communicate()
    
    ## Wait for date to terminate. Get return returncode ##
    p_status = p.wait()
    print ("Command output : ", output)
    print ("Command exit status/return code : ", p_status)
    return output

command="cd /data/test/ && git log --pretty=format:'%H' -n 1"
current_git_commit=run_bash_command(command)

command="cd /data/test/ && git log --pretty=format:'%h' -n 1"
current_git_commit_short=run_bash_command(command)

command="cat /data/test/mycron"
crontab_l=run_bash_command(command)

pid=(os.getppid())

print ("PID of this script is %d" % os.getpid())

#command="ps -p %d -o %cpu,%mem,cmd" % pid
command="ps -p %d -o %%cpu,%%mem,cmd" % os.getpid()
resource_usage_of_this_script=run_bash_command(command)




class CustomServerHandler(http.server.BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header(
            'WWW-Authenticate', 'Basic realm="Demo Realm"')
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        key = self.server.get_auth_key()

        ''' Present frontpage with user authentication. '''
        if self.headers.get('Authorization') == None:
            self.do_AUTHHEAD()

            response = {
                'success': False,
                'error': 'No auth header received'
            }

            self.wfile.write(bytes(json.dumps(response), 'utf-8'))

        elif self.headers.get('Authorization') == 'Basic ' + str(key):
            self.send_response(200)
            #self.send_header('Content-type', 'application/json')
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            
            self.wfile.write(b'Current git commit: ')
            self.wfile.write(current_git_commit)
            self.wfile.write(b'\n')
            self.wfile.write(b'Current git commit (short version): ')
            self.wfile.write(current_git_commit_short)            
            self.wfile.write(b'\n')
            self.wfile.write(b'\n')
            self.wfile.write(b'Resource usage of this script: ')
            self.wfile.write(b'\n')
            self.wfile.write(resource_usage_of_this_script)
            self.wfile.write(b'\n')
            self.wfile.write(b'\n')
            self.wfile.write(b'crontab -l:')
            self.wfile.write(b'\n')
            self.wfile.write(crontab_l)
            
            
            


            getvars = self._parse_GET()

            response = {
                'path': self.path,
                'get_vars': str(getvars)
            }

            base_path = urlparse(self.path).path
            if base_path == '/path1':
                # Do some work
                pass
            elif base_path == '/path2':
                # Do some work
                pass

            #self.wfile.write(bytes(json.dumps(response), 'utf-8'))
        else:
            self.do_AUTHHEAD()

            response = {
                'success': False,
                'error': 'Invalid credentials'
            }

            self.wfile.write(bytes(json.dumps(response), 'utf-8'))

    def do_POST(self):
        key = self.server.get_auth_key()

        ''' Present frontpage with user authentication. '''
        if self.headers.get('Authorization') == None:
            self.do_AUTHHEAD()

            response = {
                'success': False,
                'error': 'No auth header received'
            }

            self.wfile.write(bytes(json.dumps(response), 'utf-8'))

        elif self.headers.get('Authorization') == 'Basic ' + str(key):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            postvars = self._parse_POST()
            getvars = self._parse_GET()

            response = {
                'path': self.path,
                'get_vars': str(getvars),
                'get_vars': str(postvars)
            }

            base_path = urlparse(self.path).path
            if base_path == '/hello':
                # Do some work
                print('HELLO!')
                pass
            elif base_path == '/path2':
                # Do some work
                pass

            self.wfile.write(bytes(json.dumps(response), 'utf-8'))
        else:
            self.do_AUTHHEAD()

            response = {
                'success': False,
                'error': 'Invalid credentials'
            }

            self.wfile.write(bytes(json.dumps(response), 'utf-8'))

        response = {
            'path': self.path,
            'get_vars': str(getvars),
            'get_vars': str(postvars)
        }

        self.wfile.write(bytes(json.dumps(response), 'utf-8'))

    def _parse_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        if ctype == 'multipart/form-data':
            postvars = cgi.parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers.getheader('content-length'))
            postvars = cgi.parse_qs(
                self.rfile.read(length), keep_blank_values=1)
        else:
            postvars = {}

        return postvars

    def _parse_GET(self):
        getvars = parse_qs(urlparse(self.path).query)

        return getvars


class CustomHTTPServer(http.server.HTTPServer):
    key = ''

    def __init__(self, address, handlerClass=CustomServerHandler):
        super().__init__(address, handlerClass)

    def set_auth(self, username, password):
        self.key = base64.b64encode(
            bytes('%s:%s' % (username, password), 'utf-8')).decode('ascii')

    def get_auth_key(self):
        return self.key


if __name__ == '__main__':
    server = CustomHTTPServer(('', 80))
    server.set_auth('admin', '1234')
    server.serve_forever()
