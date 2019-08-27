#!/usr/bin/env python
import os, subprocess, time, signal
from microWebSrv import MicroWebSrv
import datetime

# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# Global Variables
# ----------------------------------------------------------------------------

record_command = 'parecord --rate=16000 --channels=1 /home/nherriot/test.wav'			# Used for recording voice from pluseaudio
record_process = None
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# Helper Functions
# ----------------------------------------------------------------------------


def record():
    print("*** Creating the record process ***")
    record_process = subprocess.Popen(record_command, shell=True)
    print("Record process PID is: {}".format(record_process.pid))
    #print("Sleeping for 10 seconds...")
    #time.sleep(10)
    #print("Stopping the record process.")


def record_stop():
    os.kill(record_process.pid, signal.SIGINT)
    os.kill((record_process.pid + 1), signal.SIGINT)

    if record_process.poll() is None:
        os.kill(record_process.pid, signal.SIGTERM)
        print("Process is not accepting SIGINT, now trying to Terminate the process")
        time.sleep(2)
    if record_process.poll() is None:  # Force kill if process is still alive
        print("Process is not accepting SIGTERM, now trying to Kill the process")
        os.kill(record_process.pid, signal.SIGKILL)

# ----------------------------------------------------------------------------


@MicroWebSrv.route('/r18')
def _httpHandlerTestGet(httpClient, httpResponse) :
    content = """\
    <!DOCTYPE html>
    <html lang=en>
        <head>
            <meta charset="UTF-8" />
            <title>R18 Test</title>
        </head>
        <body>
            <h1>R18 Test</h1>
            Client IP address = %s
            <br />
            <p> Hit the start button to record voice. The R18 will record 5 seconds of voice and decode</p>
            <form action="/r18" method="post" accept-charset="ISO-8859-1">
                <input type="submit" value="Submit">
            </form>
        </body>
    </html>
    """ % httpClient.GetIPAddr()
    httpResponse.WriteResponseOk( headers		 = None,
                                  contentType	 = "text/html",
                                  contentCharset = "UTF-8",
                                  content 		 = content )



@MicroWebSrv.route('/r18', 'POST')
def _httpHandlerTestPost(httpClient, httpResponse) :
    print("\NServer recieving HTTP: r18(POST)")
    formData  = httpClient.ReadRequestPostedFormData()

    content   = """\
    <!DOCTYPE html>
    <html lang=en>
        <head>
            <meta charset="UTF-8" />
            <title>R18 Test</title>
        </head>
        <body>
            <h1>R18 Test</h1>
            <p> Recording started...</p>
            <p> Please hit the stop button to stop recording and translate your speech to text.
            <form action="/r18-decode" method="post" accept-charset="ISO-8859-1">
                <input type="submit" value="Submit">
            </form>
            
        </body>
    </html>
    """
    httpResponse.WriteResponseOk( headers		 = None,
                                  contentType	 = "text/html",
                                  contentCharset = "UTF-8",
                                  content 		 = content )
    # Now record the audio
    record()


@MicroWebSrv.route('/test')
def _httpHandlerTestGet(httpClient, httpResponse) :
    content = """\
    <!DOCTYPE html>
    <html lang=en>
        <head>
            <meta charset="UTF-8" />
            <title>TEST GET</title>
        </head>
        <body>
            <h1>TEST GET</h1>
            Client IP address = %s
            <br />
            <form action="/test" method="post" accept-charset="ISO-8859-1">
                First name: <input type="text" name="firstname"><br />
                Last name: <input type="text" name="lastname"><br />
                <input type="submit" value="Submit">
            </form>
        </body>
    </html>
    """ % httpClient.GetIPAddr()
    httpResponse.WriteResponseOk( headers		 = None,
                                  contentType	 = "text/html",
                                  contentCharset = "UTF-8",
                                  content 		 = content )


@MicroWebSrv.route('/test', 'POST')
def _httpHandlerTestPost(httpClient, httpResponse) :
    formData  = httpClient.ReadRequestPostedFormData()
    firstname = formData["firstname"]
    lastname  = formData["lastname"]
    content   = """\
    <!DOCTYPE html>
    <html lang=en>
        <head>
            <meta charset="UTF-8" />
            <title>TEST POST</title>
        </head>
        <body>
            <h1>TEST POST</h1>
            Firstname = %s<br />
            Lastname = %s<br />
        </body>
    </html>
    """ % ( MicroWebSrv.HTMLEscape(firstname),
            MicroWebSrv.HTMLEscape(lastname) )
    httpResponse.WriteResponseOk( headers		 = None,
                                  contentType	 = "text/html",
                                  contentCharset = "UTF-8",
                                  content 		 = content )


@MicroWebSrv.route('/edit/<index>')             # <IP>/edit/123           ->   args['index']=123
@MicroWebSrv.route('/edit/<index>/abc/<foo>')   # <IP>/edit/123/abc/bar   ->   args['index']=123  args['foo']='bar'
@MicroWebSrv.route('/edit')                     # <IP>/edit               ->   args={}
def _httpHandlerEditWithArgs(httpClient, httpResponse, args={}) :
    content = """\
    <!DOCTYPE html>
    <html lang=en>
        <head>
            <meta charset="UTF-8" />
            <title>TEST EDIT</title>
        </head>
        <body>
    """
    content += "<h1>EDIT item with {} variable arguments</h1>"\
        .format(len(args))

    if 'index' in args :
        content += "<p>index = {}</p>".format(args['index'])

    if 'foo' in args :
        content += "<p>foo = {}</p>".format(args['foo'])

    content += """
        </body>
    </html>
    """
    httpResponse.WriteResponseOk( headers		 = None,
                                  contentType	 = "text/html",
                                  contentCharset = "UTF-8",
                                  content 		 = content )

# ----------------------------------------------------------------------------

def _acceptWebSocketCallback(webSocket, httpClient) :
    print("WS ACCEPT")
    webSocket.RecvTextCallback   = _recvTextCallback
    webSocket.RecvBinaryCallback = _recvBinaryCallback
    webSocket.ClosedCallback 	 = _closedCallback

def _recvTextCallback(webSocket, msg) :
    print("WS RECV TEXT : %s" % msg)
    webSocket.SendText("Reply for %s" % msg)

def _recvBinaryCallback(webSocket, data) :
    print("WS RECV DATA : %s" % data)

def _closedCallback(webSocket) :
    print("WS CLOSED")

# ----------------------------------------------------------------------------

#routeHandlers = [
#	( "/test",	"GET",	_httpHandlerTestGet ),
#	( "/test",	"POST",	_httpHandlerTestPost )
#]


srv = MicroWebSrv(webPath='www/')
srv.MaxWebSocketRecvLen     = 256
srv.WebSocketThreaded		= False
srv.AcceptWebSocketCallback = _acceptWebSocketCallback
print("*** Starting web server ***")
srv.Start(threaded=True)

raw_input("Press enter to stop the web server")
srv.Stop()

# ----------------------------------------------------------------------------
