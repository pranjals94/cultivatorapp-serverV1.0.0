Run a server manully

ASGI Servers

An ASGI (Asynchronous Server Gateway Interface) server is a standard interface in Python for web servers to communicate with asynchronous web applications and frameworks. It's built as a successor to WSGI (Web Server Gateway Interface) and is designed to handle multiple concurrent requests efficiently using asynchronous programming

FastAPI uses a standard for building Python web frameworks and servers called ASGI. FastAPI is an ASGI web framework.

The main thing you need to run a FastAPI application (or any other ASGI application) in a remote server machine is an ASGI server program like Uvicorn, this is the one that comes by default in the fastapi command.

There are several alternatives, including:

Uvicorn: a high performance ASGI server.
Hypercorn: an ASGI server compatible with HTTP/2 and Trio among other features.
Daphne: the ASGI server built for Django Channels.
Granian: A Rust HTTP server for Python applications.
NGINX Unit: NGINX Unit is a lightweight and versatile web application runtime.
Server Machine and Server Program¶
There's a small detail about names to keep in mind. 💡

The word "server" is commonly used to refer to both the remote/cloud computer (the physical or virtual machine) and also the program that is running on that machine (e.g. Uvicorn).

Just keep in mind that when you read "server" in general, it could refer to one of those two things.

When referring to the remote machine, it's common to call it server, but also machine, VM (virtual machine), node. Those all refer to some type of remote machine, normally running Linux, where you run programs.

Install the Server Program¶
When you install FastAPI, it comes with a production server, Uvicorn, and you can start it with the fastapi run command.

But you can also install an ASGI server manually.

Make sure you create a virtual environment, activate it, and then you can install the server application.

For example, to install Uvicorn:

pip install "uvicorn[standard]"

Run the server program:

uvicorn main:app --host 0.0.0.0 --port 80 //host can be localhost instead of the ip in case of development

INFO: Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)

Test the server by visiting
http://localhost:portnumber/docs //localhost or ip-address

a hashed password that can be used for the first time
(cost factor during hashing is 10) https://bcrypt.online/
pranjal = $2y$10$fIPWHLjIS6q.QtyTT.3ose7fZury9gQ6KgMpwtC/Y0LW2BuLIxRuW
