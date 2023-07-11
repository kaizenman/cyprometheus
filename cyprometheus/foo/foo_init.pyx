# cython: language_level=3
# distutils: language = c++

cdef extern from "foo/foo_setup.h":
    void CreatePrometheusRegistry()

from libcpp.string cimport string
cdef extern from "foo/foo_setup.h":
    string GetMetricsAsString()

def py_create_prometheus_registry():
    CreatePrometheusRegistry()

def py_get_metrics():
    return GetMetricsAsString().decode('utf-8')