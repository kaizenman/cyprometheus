"""
This module runs a Flask web application with two endpoints:
    * `/` - A test endpoint that returns a "Hello World!" message.
    * `/metrics` - An endpoint that returns combined Python and C++ application metrics.

This application also sets up appropriate signal handling for clean shutdowns and integrates with
the Prometheus monitoring system.
"""

import os
import signal
import gzip
import sys
from io import BytesIO
from flask import Flask, request, jsonify, abort
from prometheus_client import make_wsgi_app, Counter
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.wrappers import Response

from cyprometheus.foo.foo_init import py_create_prometheus_registry, py_get_metrics

# Create a counter metric
request_count = Counter('python_app_requests_total', 'Total Python app requests')

app = Flask(__name__)
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})


@app.route("/", methods=["POST"])
def hello() -> Response:
    """
    Test endpoint that returns a "Hello World!" message.
    
    Returns:
        Response: A JSON response with a "Hello World!" message.
    """
    return jsonify({"message": "Hello World!"})


@app.route("/metrics", methods=["GET"])
def metrics() -> Response:
    """
    Returns the application's metrics, which are a combination of Python and C++ metrics.
    
    The Python metrics are obtained through Prometheus' WSGI application and the C++ metrics
    are obtained from a custom method.

    Returns:
        Response: A plain text response containing the combined Python and C++ metrics.
    """
    # Increment the counter (Python metrics)
    request_count.inc()

    # Obtain C++ metrics
    cpp_metrics = py_get_metrics()

    # Obtain Python metrics
    metrics_app = make_wsgi_app()
    raw_python_metrics = Response.from_app(metrics_app, request.environ).get_data()

    # Decompress response if it's gzipped
    if raw_python_metrics[:2] == b'\x1f\x8b':  # gzip magic number
        with gzip.GzipFile(fileobj=BytesIO(raw_python_metrics)) as f:
            python_metrics = f.read().decode('utf-8')
    else:
        python_metrics = raw_python_metrics.decode('utf-8')

    # Combine and return metrics
    return Response(cpp_metrics + "\n" + python_metrics, mimetype='text/plain')


def signal_handler(sig, frame):
    """
    Signal handler for clean application shutdown.

    Args:
        sig (int): The signal number.
        frame (frame): The current stack frame.
    """
    sys.exit(0)


if __name__ == "__main__":
    # Setup signal handling for clean shutdowns
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Create C++ Prometheus registry
    py_create_prometheus_registry()

    try:
        app.run(host="0.0.0.0", port=5050, debug=False)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)
