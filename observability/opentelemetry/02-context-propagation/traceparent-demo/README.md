# traceparent-demo

This demo showcases the usage of the `traceparent` HTTP header for context propagation in distributed tracing.

#### Docker Compose

```bash
podman compose -f ./docker-compose.yaml up --build
```

#### Test

##### Scenario 1: No traceparent header

In this scenario, we make a request without providing the `traceparent` header. The server generates a new trace context.

```bash
→ curl -s localhost:8080 | jq "."
{
  "message": "Hello, World!",
  "traceparent_received": "00-73f28b192aa1bb86f622f74a18522c39-e034874bf9f67b49-01",
  "tracestate_received": null
}
```

```console
[app]   | INFO:     [app]   received traceparent=00-3de1af71a3c284a96668838327da0572-e2658f062f6bbc5a-01
[app]   | INFO:     10.89.1.3:36662 - "GET / HTTP/1.0" 200 OK
[nginx] | [nginx] incoming_traceparent="00-3de1af71a3c284a96668838327da0572-e2658f062f6bbc5a-01" trace_id=3de1af71a3c284a96668838327da0572 span_id=e2658f062f6bbc5a parent_span_id=- parent_sampled=0 "GET / HTTP/1.1" 200
```

##### Scenario 2: With traceparent header

In this scenario, we make a request with the `traceparent` header. The server continues the trace context provided.

```bash
→ curl -s -H "traceparent: 00-73f28b192aa1bb86f622f74a18522c39-e034874bf9f67b49-01" localhost:8080 | jq "."
{
  "message": "Hello, World!",
  "traceparent_received": "00-73f28b192aa1bb86f622f74a18522c39-e034874bf9f67b49-01",
  "tracestate_received": null
}
```

```console
[app]   | INFO:     [app]   received traceparent=00-73f28b192aa1bb86f622f74a18522c39-55a0011978db650d-01
[app]   | INFO:     10.89.1.3:40844 - "GET / HTTP/1.0" 200 OK
[nginx] | [nginx] incoming_traceparent="00-73f28b192aa1bb86f622f74a18522c39-55a0011978db650d-01" trace_id=73f28b192aa1bb86f622f74a18522c39 span_id=55a0011978db650d parent_span_id=e034874bf9f67b49 parent_sampled=1 "GET / HTTP/1.1" 200
```