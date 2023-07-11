# Python & C++ Metrics App

## Overview
Python & C++ Metrics App is a Flask web application that demonstrates how to expose and combine Python and C++ application metrics to a Prometheus monitoring system.

## Features
* A test endpoint at "/" that responds with a "Hello World!" message.
* An endpoint at "/metrics" that returns combined Python and C++ application metrics.

## Technologies
This project uses the following technologies:
* CMake
* Bash
* C++20
* Python 3
* Cython
* Flask
* Prometheus Client for Python
* Prometheus Client for C++

## Installation
Clone this repository and navigate into the project directory. Make sure you have Python 3 and pip installed.

## Usage
Build:
```bash
./run_cyprometheus.sh --build
```
Run:
```bash
./run_cyprometheus.sh --run
```
Clean:
```bash
./run_cyprometheus.sh --clean
```

The application will be available at `http://localhost:5050`.


To test the application, send a GET request to `http://localhost:5050/metrics`. You can also install Grafana and visualize the metrics.


