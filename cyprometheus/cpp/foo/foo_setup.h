#pragma once

#include <memory>

#include <prometheus/registry.h>

void CreatePrometeusRegistryInternal();

extern "C" void CreatePrometheusRegistry();

std::string GetMetricsAsString();
