import re

class SymbolicAgent:
    def __init__(self, name="Agent_X"):
        self.name = name
        self.local_environment = {"pH": 7.0}
        self.signal_dampened = False
        self.field_state = None

    def load_protocol(self, filepath):
        with open(filepath, "r") as file:
            data = file.read()

        # Extract key fields from protocol block
        self.protocol = {
            "trigger": self._match(data, r"TRIGGER_ON:\s*(.+)"),
            "condition": self._match(data, r"CONDITION:\s*(.+)"),
            "initiation": self._match(data, r"INITIATION_THRESHOLD:\s*(.+)"),
            "operation": re.findall(r"- (SET_FIELD_STATE|PROPAGATE|PERSISTENCE): (.+)", data),
            "effect": re.findall(r"- PARAMETER: (.+)\n\s+- MODIFIER: (.+)", data),
        }

    def _match(self, text, pattern):
        match = re.search(pattern, text)
        return match.group(1).strip() if match else None

    def execute(self):
        if self.protocol:
            print(f"[{self.name}] Executing protocol: ACIDIC_TRACE_01")
            for op, val in self.protocol["operation"]:
                if op == "SET_FIELD_STATE":
                    self.field_state = val
                elif op == "PROPAGATE" and val == "FALSE":
                    self.signal_dampened = True
                # Future: handle persistence

            for param, mod in self.protocol["effect"]:
                if param == "pH":
                    self._apply_ph_modulation(mod)

            print(f"[{self.name}] Environment pH: {self.local_environment['pH']}")
            print(f"[{self.name}] Signal dampened: {self.signal_dampened}")

    def _apply_ph_modulation(self, modifier):
        # Simple simulation of DECREMENT_BY_FACTOR(x)
        match = re.search(r"DECREMENT_BY_FACTOR\((.+)\)", modifier)
        if match:
            try:
                factor = float(match.group(1)) if match.group(1).replace(".", "", 1).isdigit() else 0.5
            except:
                factor = 0.5
            self.local_environment["pH"] -= factor

# Example usage
if __name__ == "__main__":
    agent = SymbolicAgent("TraceExecutor")
    agent.load_protocol("glyphs/acidic_trace_01.protocol.md")
    agent.execute()
