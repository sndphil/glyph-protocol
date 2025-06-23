import os
import re

class SymbolicAgent:
    def __init__(self, name="Agent_X"):
        self.name = name
        self.local_environment = {"pH": 7.0}
        self.signal_dampened = False
        self.field_state = None
        self.protocol = {}

    def load_protocol(self, relative_path):
        """Load a protocol file with path resolved relative to this script's location."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(script_dir, "..", relative_path)

        if not os.path.exists(full_path):
            raise FileNotFoundError(f"[{self.name}] Protocol file not found: {full_path}")

        with open(full_path, "r") as file:
            data = file.read()

        # Extract protocol fields from Markdown-style syntax
        self.protocol = {
            "trigger": self._match(data, r"TRIGGER_ON:\s*(.+)"),
            "condition": self._match(data, r"CONDITION:\s*(.+)"),
            "initiation": self._match(data, r"INITIATION_THRESHOLD:\s*(.+)"),
            "operation": re.findall(r"- (SET_FIELD_STATE|PROPAGATE|PERSISTENCE): (.+)", data),
            "effect": re.findall(r"- PARAMETER: (.+)\n\s+- MODIFIER: (.+)", data),
        }

        print(f"[{self.name}] Protocol loaded: {os.path.basename(full_path)}")

    def _match(self, text, pattern):
        match = re.search(pattern, text)
        return match.group(1).strip() if match else None

    def execute(self):
        if not self.protocol:
            print(f"[{self.name}] No protocol loaded. Execution aborted.")
            return

        print(f"[{self.name}] Executing protocol: acidic_trace_01")

        # Execute structural operations
        for op, val in self.protocol.get("operation", []):
            if op == "SET_FIELD_STATE":
                self.field_state = val
            elif op == "PROPAGATE" and val.upper() == "FALSE":
                self.signal_dampened = True
            # Extend here for PERSISTENCE or other operations

        # Apply environmental effects
        for param, mod in self.protocol.get("effect", []):
            if param.lower() == "ph":
                self._apply_ph_modulation(mod)

        print(f"[{self.name}] Environment pH: {self.local_environment['pH']}")
        print(f"[{self.name}] Signal dampened: {self.signal_dampened}")

    def _apply_ph_modulation(self, modifier):
        """Apply changes to the agent's pH environment using symbolic modifiers."""
        match = re.search(r"DECREMENT_BY_FACTOR\((.+)\)", modifier)
        if match:
            try:
                factor = float(match.group(1))
            except ValueError:
                factor = 0.5
            self.local_environment["pH"] -= factor

# Example usage
if __name__ == "__main__":
    agent = SymbolicAgent("TraceExecutor")
    agent.load_protocol("glyphs/acidic_trace_01.protocol.md")
    agent.execute()
