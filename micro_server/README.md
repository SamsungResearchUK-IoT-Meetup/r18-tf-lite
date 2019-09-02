# Microweb Server Guide

This is a very simple micro web server used for the Samsung board demo. It will allow the user to select a record button which will cause the embedded system to record 5 seconds of speech.
The speech will then be displayed on the response to the post message.

To run the microweb server, from the /micro_server directory do:

```bash
   $/> ./start.py
   *** Starting web server ***
   Server process starting...
   Starting threaded process...
   Press enter to stop the web server
```   

The web server will be stopped cleanly by hitting enter in the terminal.

To view the web server go to your local IP address on port 8000 on page /r18 or if you are running it on the board, go to the local IP of the board. eg..

```bash
   http://192.168.1.43:8000/r18
```

You will be prested with a simple web interface to the board to record sound.

R18 Test
Client IP address = 192.168.110.138

Hit the 'record' button to record voice. The R18 will start recording

<html lang=en>
        <head>
            <meta charset="UTF-8" />
            <title>R18 Test</title>
        </head>
        <body>
            <h1>R18 Test</h1>
            Client IP address = 192.168.110.138
            <br />
            <p> Hit the 'record' button to record voice. The R18 will start recording</p>
            <form action="/r18" method="post" accept-charset="ISO-8859-1">
                <input type="submit" value="Record">
            </form>
        </body>
    </html>
