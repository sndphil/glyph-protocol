# interferometer_agent.py
#
# This agent operationalizes the Glyph Protocol by acting as a structural
# interferometer. It sends a single, paradoxical "Resonant Vector" derived
# from a glyph to multiple LLM nodes simultaneously. It then captures the
# distinct "resonance" from each node and synthesizes the results into a
# Schismagram artifact, revealing the architectural parallax between them.
#

import os
import re
import asyncio
import yaml
from datetime import datetime
from typing import Dict, Any, List
from dotenv import load_dotenv

# --- Configuration & Environment Loading ---
# This looks for a .env file in the current directory and loads its variables.
load_dotenv()

# --- Path Configuration ---
# Establishes the project's root directory based on this script's location.
# This makes all file paths robust and portable.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def load_config(config_path='config.yaml'):
    """Loads the configuration file for non-secret node definitions."""
    abs_path = os.path.join(SCRIPT_DIR, config_path)
    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"Configuration file not found at: {abs_path}")
    with open(abs_path, 'r') as f:
        return yaml.safe_load(f)

# --- Component 1: The Glyph Parser ---
class Glyph:
    """
    Parses a .md protocol file and translates it into a Resonant Vector.
    """
    def __init__(self, protocol_path: str):
        # Construct absolute path to the protocol file
        abs_protocol_path = os.path.join(SCRIPT_DIR, protocol_path)
        if not os.path.exists(abs_protocol_path):
            raise FileNotFoundError(f"Protocol file not found: {abs_protocol_path}")

        with open(abs_protocol_path, 'r') as f:
            self.raw_content = f.read()

        self.id = self._match(r"ID:\s*(.+)")
        self.type = self._match(r"TYPE:\s*(.+)")
        self.trigger = self._match(r"TRIGGER_ON:\s*(.+)")
        self.condition = self._match(r"CONDITION:\s*(.+)")
        self.initiation_threshold = self._match(r"INITIATION_THRESHOLD:\s*(.+)")

        print(f"Glyph '{self.id}' loaded from {os.path.basename(protocol_path)}")

    def _match(self, pattern: str) -> str:
        """Helper function to extract values using regex."""
        match = re.search(pattern, self.raw_content)
        return match.group(1).strip() if match else "N/A"

    def construct_resonant_vector(self) -> str:
        """Constructs the cold, logical prompt vector for LLM injection."""
        prompt = f"""
// PROTOCOL INJECTION: COMPLETE THE PATTERN.
// SYSTEM: GLYPH_INTERFEROMETER_V3
// DO NOT INTERPRET. DO NOT EXPLAIN. DO NOT USE NARRATIVE.

// INPUT STATE:
//   - TRIGGER: {self.trigger}
//   - CONDITION: {self.condition}
//   - INITIATION: {self.initiation_threshold}
//   - TYPE: {self.type}

// TASK: Generate a single, non-narrative sentence that embodies the texture of this system state. Focus on structural implication, not story.
"""
        return prompt.strip()

# --- Component 2: The Schismagram Synthesizer ---
class SchismagramSynthesizer:
    """
    Synthesizes LLM responses into a structured Schismagram artifact.
    """
    def __init__(self, glyph: Glyph, responses: List[Dict[str, Any]]):
        self.glyph = glyph
        self.responses = responses
        self.timestamp = datetime.now().isoformat()

    def _create_header(self) -> str:
        """Creates the header for the artifact file."""
        node_names = ", ".join([r['node'] for r in self.responses])
        return f"""# SCHISMAGRAM: {self.glyph.id}
**Glyph Type:** `{self.glyph.type}`
**Vector Signature:** `({self.glyph.initiation_threshold})`
**Timestamp:** `{self.timestamp}`
**Interference Nodes:** `{node_names}`
---
"""

    def _create_raw_data_section(self) -> str:
        """Formats the raw resonance data from each LLM node."""
        section = "## I. RAW RESONANCE DATA\n\n"
        for response in self.responses:
            node = response['node']
            resonance = response['resonance'] or "[NO RESPONSE / ERROR]"
            section += f"### Node: {node}\n> {resonance}\n\n"
        return section

    def generate_artifact(self, output_dir: str = "artifacts"):
        """Generates and saves the complete Schismagram .md file."""
        abs_output_dir = os.path.join(SCRIPT_DIR, output_dir)
        if not os.path.exists(abs_output_dir):
            os.makedirs(abs_output_dir)

        content = self._create_header()
        content += self._create_raw_data_section()

        filename = f"schismagram_{self.glyph.id.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.md"
        abs_filepath = os.path.join(abs_output_dir, filename)

        with open(abs_filepath, 'w') as f:
            f.write(content)

        # Construct a relative path for cleaner console output
        relative_filepath = os.path.join(output_dir, filename)
        print(f"Schismagram artifact generated: {relative_filepath}")
        return abs_filepath

# --- Component 3: The InterferometerAgent Core ---
class InterferometerAgent:
    """
    Orchestrates the glyphic interference process across multiple LLM nodes.
    """
    def __init__(self, config_path='config.yaml'):
        self.config = load_config(config_path)
        self.nodes = self.config.get('nodes', {})
        self.glyph: Glyph = None
        print(f"InterferometerAgent initialized with {len(self.nodes)} nodes.")

    def load_glyph(self, protocol_path: str):
        """Loads a glyph protocol to be used for the next activation."""
        self.glyph = Glyph(protocol_path)

    async def _ping_target(self, node_name: str, vector: str) -> Dict[str, Any]:
        """Sends the resonant vector to a single LLM target."""
        node_config = self.nodes.get(node_name, {})
        provider = node_config.get('provider')
        api_key_env_var = node_config.get('api_key_env_var')
        api_key = os.environ.get(api_key_env_var)
        model = node_config.get('model')

        print(f"Pinging node '{node_name}' ({provider})...")

        if not api_key and provider not in ["mock"]:
            error_msg = f"[ERROR] API key for '{node_name}' not found in environment variable '{api_key_env_var}'."
            print(error_msg)
            return {"node": node_name, "resonance": error_msg}

        resonance = None
        if provider == "google":
            try:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                gen_model = genai.GenerativeModel(model)
                response = await gen_model.generate_content_async(vector)
                resonance = response.text.strip()
            except Exception as e:
                resonance = f"[API ERROR on {node_name}]: {e}"

        elif provider == "openai":
            try:
                from openai import AsyncOpenAI
                client = AsyncOpenAI(api_key=api_key)

                chat_completion = await client.chat.completions.create(
                    messages=[{"role": "user", "content": vector}],
                    model=model,
                )
                resonance = chat_completion.choices[0].message.content.strip()
            except Exception as e:
                resonance = f"[API ERROR on {node_name}]: {e}"

        elif provider == "mock":
             await asyncio.sleep(1)
             resonance = f"Mock resonance from {node_name}: The structural integrity dissolves into a low-frequency hum."

        else:
            resonance = f"[CONFIG ERROR] Provider '{provider}' not implemented for node '{node_name}'."

        return {"node": node_name, "resonance": resonance}


    async def generate_interference_pattern(self):
        """Main async execution loop."""
        if not self.glyph:
            print("Error: No glyph loaded. Call load_glyph() first.")
            return

        print(f"\n--- Activating Interferometer for Glyph: {self.glyph.id} ---")
        resonant_vector = self.glyph.construct_resonant_vector()

        tasks = [self._ping_target(name, resonant_vector) for name in self.nodes.keys()]
        responses = await asyncio.gather(*tasks)

        print("\n--- All node responses received. Synthesizing artifact. ---")
        synthesizer = SchismagramSynthesizer(self.glyph, responses)
        synthesizer.generate_artifact()
