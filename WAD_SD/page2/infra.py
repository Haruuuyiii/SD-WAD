# ─────────────────────────────────────────────────────────────
# INFRASTRUCTURE & OBSERVABILITY — infra.py
# Logging, metrics, health monitoring, and alerting
# No external libraries needed — pure Python
#
# Run: python infra.py
# ─────────────────────────────────────────────────────────────

import time
import json
import random
import threading
import os
from datetime import datetime
from collections import defaultdict

LOG_FILE = "app.log"

# ─────────────────────────────────────────────────────────────
# 1. STRUCTURED LOGGER
#    Writes logs in JSON format — easy to send to Datadog/ELK
# ─────────────────────────────────────────────────────────────

class Logger:
    LEVELS = {"DEBUG": 0, "INFO": 1, "WARN": 2, "ERROR": 3}

    def __init__(self, service_name: str, min_level: str = "INFO"):
        self.service   = service_name
        self.min_level = self.LEVELS.get(min_level, 1)

    def _log(self, level: str, message: str, **extra):
        if self.LEVELS.get(level, 0) < self.min_level:
            return
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "level":     level,
            "service":   self.service,
            "message":   message,
            **extra,
        }
        line = json.dumps(entry)

        # Print to console with color
        colors = {"DEBUG": "\033[90m", "INFO": "\033[36m", "WARN": "\033[33m", "ERROR": "\033[31m"}
        reset = "\033[0m"
        print(f"{colors.get(level, '')}{line}{reset}")

        # Append to log file
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")

    def debug(self, msg, **kw): self._log("DEBUG", msg, **kw)
    def info(self,  msg, **kw): self._log("INFO",  msg, **kw)
    def warn(self,  msg, **kw): self._log("WARN",  msg, **kw)
    def error(self, msg, **kw): self._log("ERROR", msg, **kw)


# ─────────────────────────────────────────────────────────────
# 2. METRICS COLLECTOR
#    Tracks counters, gauges, timers — like Prometheus
# ─────────────────────────────────────────────────────────────

class Metrics:
    def __init__(self):
        self.counters = defaultdict(int)       # ever-increasing count
        self.gauges   = defaultdict(float)     # current value (can go up/down)
        self.timings  = defaultdict(list)      # list of durations

    def increment(self, name: str, by: int = 1):
        """Count events: requests, errors, logins..."""
        self.counters[name] += by

    def gauge(self, name: str, value: float):
        """Track a current reading: CPU %, memory MB..."""
        self.gauges[name] = value

    def timing(self, name: str, duration_ms: float):
        """Track how long something takes."""
        self.timings[name].append(duration_ms)

    def summary(self):
        """Print a metrics summary report."""
        print("\n" + "─" * 45)
        print("  METRICS REPORT")
        print("─" * 45)

        print("\n  Counters:")
        for k, v in self.counters.items():
            print(f"    {k:<35} {v}")

        print("\n  Gauges (current value):")
        for k, v in self.gauges.items():
            print(f"    {k:<35} {v:.2f}")

        print("\n  Timings (avg ms / max ms):")
        for k, vals in self.timings.items():
            avg = sum(vals) / len(vals)
            mx  = max(vals)
            print(f"    {k:<35} avg={avg:.1f}ms  max={mx:.1f}ms")

        print("─" * 45 + "\n")


# ─────────────────────────────────────────────────────────────
# 3. HEALTH CHECKER
#    Periodically checks if services are "alive"
# ─────────────────────────────────────────────────────────────

class HealthChecker:
    def __init__(self):
        # service_name → True/False
        self.services = {
            "auth-service":    True,
            "user-service":    True,
            "order-service":   True,
            "notif-service":   True,
            "database":        True,
            "cache":           True,
        }

    def check_all(self) -> dict:
        """
        Simulate health checks.
        In production: make HTTP GET /health to each service.
        """
        results = {}
        for name in self.services:
            # Randomly flip one service offline for demo
            is_healthy = random.random() > 0.15
            self.services[name] = is_healthy
            results[name] = "✅ healthy" if is_healthy else "❌ DOWN"
        return results

    def overall_status(self) -> str:
        results = self.check_all()
        down = [k for k, v in results.items() if "DOWN" in v]
        return results, "DEGRADED" if down else "HEALTHY"


# ─────────────────────────────────────────────────────────────
# 4. ALERTING
#    Sends alerts when something goes wrong
# ─────────────────────────────────────────────────────────────

class Alerting:
    def __init__(self, logger: Logger):
        self.log = logger

    def check_and_alert(self, metrics: Metrics, health: HealthChecker):
        """Run all alert rules."""
        self._alert_high_error_rate(metrics)
        self._alert_slow_responses(metrics)
        self._alert_down_services(health)

    def _alert_high_error_rate(self, metrics: Metrics):
        errors   = metrics.counters.get("http.errors", 0)
        requests = metrics.counters.get("http.requests", 1)
        rate = errors / requests * 100
        if rate > 5:
            self.log.error("ALERT: High error rate!", error_rate=f"{rate:.1f}%")

    def _alert_slow_responses(self, metrics: Metrics):
        timings = metrics.timings.get("http.response_time", [])
        if timings:
            avg = sum(timings) / len(timings)
            if avg > 500:
                self.log.warn("ALERT: Slow response times!", avg_ms=f"{avg:.0f}ms")

    def _alert_down_services(self, health: HealthChecker):
        results, status = health.overall_status()
        for svc, state in results.items():
            if "DOWN" in state:
                self.log.error(f"ALERT: {svc} is DOWN!", service=svc)


# ─────────────────────────────────────────────────────────────
# 5. DEMO — simulate a running system
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 45)
    print("  INFRASTRUCTURE & OBSERVABILITY")
    print("=" * 45 + "\n")

    log     = Logger("api-gateway", min_level="DEBUG")
    metrics = Metrics()
    health  = HealthChecker()
    alerts  = Alerting(log)

    # Simulate 20 incoming HTTP requests
    print("  Simulating 20 HTTP requests...\n")
    for i in range(20):
        duration = random.uniform(50, 900)   # ms
        is_error = random.random() < 0.12   # 12% error rate

        metrics.increment("http.requests")
        metrics.timing("http.response_time", duration)

        if is_error:
            metrics.increment("http.errors")
            log.error("Request failed", path="/api/order", status=500, duration_ms=round(duration))
        else:
            log.info("Request OK", path="/api/user", status=200, duration_ms=round(duration))

        # Simulate CPU & memory gauge
        metrics.gauge("system.cpu_percent",    random.uniform(20, 85))
        metrics.gauge("system.memory_mb",      random.uniform(400, 900))

        time.sleep(0.1)

    # Print metrics summary
    metrics.summary()

    # Run health checks
    print("  Health check results:")
    results, status = health.overall_status()
    for svc, state in results.items():
        print(f"    {svc:<25} {state}")
    print(f"\n  Overall system status: {status}\n")

    # Run alerting
    print("  Running alert checks...")
    alerts.check_and_alert(metrics, health)

    print(f"\n  Logs written to: {LOG_FILE}")
    print("\n✅ Infrastructure & observability demo complete!")
