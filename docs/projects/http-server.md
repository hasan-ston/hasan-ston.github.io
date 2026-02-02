# HTTP Server in C++

An HTTP server built from scratch using C++ and POSIX sockets. Handles concurrent client connections through forking.

[GitHub](https://github.com/hasan-ston/HTTP-server-in-C-)

## How It Works

When a new HTTP request is made, the HTTP Server listens on Port 8000 and accepts the request. Once a Client sends a request, the HTTP Server creates a new process and returns the HTTP response as HTML. At this point, the new process is ready to accept additional requests.

The Server is built using POSIX Sockets through the use of the socket, bind, listen and accept calls of the POSIX Socket API to create a TCP Server. Because the listen TCP Port (Port 80) remains in a TIME_WAIT State as part of the TCP Protocol, the setsockopt() call using the SO_REUSEADDR option will allow multiple servers to exist on port 80, so when the server is restarted, you do not have to wait several minutes until you can re-bind to the port again.

## Concurrency via process forking

Whenever a Client connects to the HTTP Server, a new process is created using fork() to handle the individual Client Request. This allows multiple requests to be served at the same time by creating new processes to respond to each request, while the parent process continues to serve new connections. 

## SIGCHLD signal handler for zombie processes

In order to avoid "zombie" processes from accumulating, the HTTP Server has a handler for the SIGCHLD UNIX signal for terminated child processes via waitpid(). This prevents wastage of system resources.



