# QoS Interpreter for KAIST FogOS Project

The main role of QoS Interpreter is to convert from service/user descriptions about a requesting service to a set of network QoS parameters.

## Prerequisites
* Python 3.x
* Flask (pip installation package: flask)
* Flask-RESTful (pip installation package: flask-restful)
* Flask-API (pip installation package: flask-api)

## Usage

### Running a REST API server for Edge Configuration/Utilization API
Run 'main.py' with a port number as an argument.
```
$ python main.py [PORT]
```
If you do not specify the port number, it will run as a port 9090 open.
Port number below 1024 would ask you a root permission. It would rather set the number more than 1024.

### Running the QoS Interpreter only
Run 'qos_interpreter.py'.
It includes a sample user/service description text for interpretation and show the result.
