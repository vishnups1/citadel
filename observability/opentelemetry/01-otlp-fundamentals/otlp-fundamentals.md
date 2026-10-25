
OTLP (OpenTelemetry Protocol) is not just a format. It is a **complete wire protocol** that defines below things

- The `Data Model/Schema`: What metrics, traces and logs look like (defined via `Protocol Buffers/Protobuf` definitions)
	- `.proto` files
	- https://github.com/open-telemetry/opentelemetry-proto/blob/main/opentelemetry/proto/trace/v1/trace.proto
	- https://github.com/open-telemetry/opentelemetry-proto/blob/main/opentelemetry/proto/metrics/v1/metrics.proto
	- https://github.com/open-telemetry/opentelemetry-proto/blob/main/opentelemetry/proto/logs/v1/logs.proto
- The `Serialization Formats` (Encodings): How that data is packed into bytes across the wire.
	- `Protobuf` (default & recommended)
	- `JSON`
- The `Transports`: How those bytes travel across the network.
	- `OTLP/gRPC + Protobuf` (HTTP/2, Port `4317`)
		- `application/x-protobuf` Sending binary-serialized `Protobuf` payloads over `gRPC`
	- `OTLP/HTTP + Protobuf` (HTTP/1.1 or 2, Port `4318`)
		- `application/x-protobuf` Sending binary-serialized `Protobuf` payloads over `HTTP`
	- `OTLP/HTTP + JSON` (HTTP/1.1 or 2, Port `4318`)
		- `application/json` Sending human-readable (JSON) mapping of the exact same `Protobuf` schema over `HTTP`

### Schemas (JSON)

In OpenTelemetry (OTLP/HTTP+JSON), payloads correspond to the Proto3 JSON mapping of 
- `ExportTraceServiceRequest`
- `ExportMetricsServiceRequest`
- `ExportLogsServiceRequest`

Key things to remember:

- Resource (Who? is generating the Spans, Metrics and Logs)
	- `resourceSpans.resource.attributes[{"key": "service.name", "value": "checkout"}]`
	- `resourceMetrics.resource.attributes[{"key": "service.name", "value": "checkout"}]`
	- `resourceLogs.resource.attributes[{"key": "service.name", "value": "checkout"}]`
- Scope (Within a service, which component is producing the span, metric, log)
	- `resourceSpans.scopeSpans[0].scope.name` and `resourceSpans.scopeSpans[0].scope.version`
	- `resourceMetrics.scopeMetrics[0].scope.name` and `resourceMetricsscopeMetrics[0].scope.version`
	- `resourceLogs.scopeLogs[o].scope.name` and `resourceLogs.scopeLogs[o].scope.version`

#### Traces `/v1/traces`

```json
{
  "resourceSpans": [
    {
      "resource": {
        "attributes": [
          {
            "key": "service.name",
            "value": { "stringValue": "account-service" }
          },
          {
            "key": "service.version",
            "value": { "stringValue": "1.4.0" }
          }
        ],
        "droppedAttributesCount": 0
      },
      "scopeSpans": [
        {
          "scope": {
            "name": "io.opentelemetry.spring-webmvc",
            "version": "2.1.0"
          },
          "spans": [
            {
              "traceId": "4bf92f3577b34da6a3ce929d0e0e4736",
              "spanId": "00f067aa0ba902b7",
              "parentSpanId": "5fb397be34d23b0f",
              "name": "GET /api/users/{id}",
              "kind": 2,
              "startTimeUnixNano": "1710000000000000000",
              "endTimeUnixNano": "1710000000050000000",
              "attributes": [
                {
                  "key": "http.response.status_code",
                  "value": { "intValue": "200" }
                },
                {
                  "key": "http.request.method",
                  "value": { "stringValue": "GET" }
                }
              ],
              "droppedAttributesCount": 0,
              "events": [
                {
                  "timeUnixNano": "1710000000010000000",
                  "name": "db_lookup_start",
                  "attributes": [
                    { "key": "query.cached", "value": { "boolValue": false } }
                  ]
                }
              ],
              "droppedEventsCount": 0,
              "links": [],
              "status": {
                "code": 1
              }
            }
          ]
        }
      ]
    }
  ]
}
```

#### Metrics `/v1/metrics`

```json
{
  "resourceMetrics": [
    {
      "resource": {
        "attributes": [
          {
            "key": "service.name",
            "value": { "stringValue": "account-service" }
          }
        ]
      },
      "scopeMetrics": [
        {
          "scope": {
            "name": "io.opentelemetry.jvm",
            "version": "1.0.0"
          },
          "metrics": [
            {
              "name": "http.server.requests",
              "description": "Total number of HTTP requests",
              "unit": "{requests}",
              "sum": {
                "aggregationTemporality": 2,
                "isMonotonic": true,
                "dataPoints": [
                  {
                    "startTimeUnixNano": "1710000000000000000",
                    "timeUnixNano": "1710000060000000000",
                    "asInt": "1542",
                    "attributes": [
                      {
                        "key": "http.response.status_code",
                        "value": { "intValue": "200" }
                      }
                    ]
                  }
                ]
              }
            },
            {
              "name": "jvm.memory.used",
              "description": "Current JVM memory used",
              "unit": "By",
              "gauge": {
                "dataPoints": [
                  {
                    "timeUnixNano": "1710000060000000000",
                    "asDouble": 536870912.0,
                    "attributes": [
                      {
                        "key": "jvm.memory.type",
                        "value": { "stringValue": "heap" }
                      }
                    ]
                  }
                ]
              }
            }
          ]
        }
      ]
    }
  ]
}
```

#### Logs `/v1/logs`

```json
{
  "resourceLogs": [
    {
      "resource": {
        "attributes": [
          {
            "key": "service.name",
            "value": { "stringValue": "account-service" }
          }
        ]
      },
      "scopeLogs": [
        {
          "scope": {
            "name": "ch.qos.logback.classic",
            "version": "1.4.14"
          },
          "logRecords": [
            {
              "timeUnixNano": "1710000000025000000",
              "observedTimeUnixNano": "1710000000026000000",
              "severityNumber": 9,
              "severityText": "INFO",
              "body": {
                "stringValue": "User 12345 successfully logged in from 10.0.1.20"
              },
              "attributes": [
                {
                  "key": "user.id",
                  "value": { "stringValue": "12345" }
                },
                {
                  "key": "client.ip",
                  "value": { "stringValue": "10.0.1.20" }
                }
              ],
              "droppedAttributesCount": 0,
              "flags": 1,
              "traceId": "4bf92f3577b34da6a3ce929d0e0e4736",
              "spanId": "00f067aa0ba902b7"
            }
          ]
        }
      ]
    }
  ]
}
```
