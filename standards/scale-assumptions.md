# Default Scale Assumptions

Baseline assumptions for performance and scalability analysis. Override these if the project's documentation or configuration specifies different values.

## Defaults

| Metric | Default Value |
|--------|--------------|
| Concurrent users | 1,000 |
| Records per table | 100,000 |
| Response time (p95) | 100ms |
| Memory budget per instance | 512MB |
| Database connections per pool | 20 |

## How to Override

If the project contains any of these, use their values instead:
- Load test configs (k6, JMeter, Gatling)
- Performance SLAs in docs or README
- Infrastructure configs (Kubernetes limits, Docker memory)
- Database connection pool settings
