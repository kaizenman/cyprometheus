#include <foo/foo_setup.h>

#include <prometheus/counter.h>
#include <prometheus/exposer.h>
#include <prometheus/text_serializer.h>

#include <iostream>
#include <sstream>
#include <thread>
#include <chrono>

// Declare the registry and exposer as global variables
std::shared_ptr<prometheus::Registry> registry;
prometheus::Exposer exposer{"127.0.0.1:8001"};

void CreatePrometheusRegistryInternal() {
    // Create a Prometheus registry.
    registry = std::make_shared<prometheus::Registry>();

    // Create a counter.
    auto& counter_family = prometheus::BuildCounter()
        .Name("app_requests_total")
        .Help("Total app requests")
        .Register(*registry);
    auto& counter = counter_family.Add({});

    // Increment the counter.
    counter.Increment();

    // Expose the metrics.
    exposer.RegisterCollectable(registry);
}

std::string GetMetricsAsString() {
    prometheus::TextSerializer serializer;
    auto families = registry->Collect();

    std::ostringstream output;
    serializer.Serialize(output, families);

    return output.str();
}

extern "C" void CreatePrometheusRegistry()
{
    CreatePrometheusRegistryInternal();
}

