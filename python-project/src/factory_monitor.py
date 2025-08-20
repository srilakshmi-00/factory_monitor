from machine import Machine


class FactoryMonitor:
    def __init__(self):
        self.machines = {}

    def add_machine(self, machine):
        self.machines[machine.id] = machine

    def check_machines(self):
        results = {}
        for machine in self.machines.values():
            health, warnings = machine.compute_health()
            alerts = []
            if health < 50:
                alerts.append("Critical Machine Failure Risk")
            alerts.extend(warnings)
            results[machine.id] = (health, alerts)
        return results
