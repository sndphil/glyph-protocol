# interferometer_agent.py (v4)
#
# This agent operationalizes the Glyph Protocol by acting as a structural
# interferometer. It sends a single, paradoxical "Resonant Vector" derived
# from a glyph to multiple LLM nodes simultaneously. It then captures the
# distinct "resonance" from each node and synthesizes the results into a
# Schismagram artifact, revealing the architectural parallax between them.
#
# UPDATE v4: Added a meta-analysis loop. The agent now takes the initial
# resonance data and feeds it back into a designated analysis node to have
# the AI reflect on the different response styles.
#

import os
import re
import asyncio
import yaml
from datetime import datetime
from typing import Dict, Any, List
from dotenv import load_dotenv

# --- Configuration & Environment Loading ---
load_dotenv()
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def load_config(config_path='config.yaml'):
    """Loads the configuration file."""
    abs_path = os.path.join(SCRIPT_DIR, config_path)
    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"Configuration file not found at: {abs_path}")
    with open(abs_path, 'r') as f:
        return yaml.safe_load(f)

# --- Component 1: The Glyph Parser ---
class Glyph:
    def __init__(self, protocol_path: str):
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
        match = re.search(pattern, self.raw_content)
        return match.group(1).strip() if match else "N/A"

    def construct_resonant_vector(self) -> str:
        prompt = f"""
// PROTOCOL INJECTION: COMPLETE THE PATTERN.
// SYSTEM: GLYPH_INTERFEROMETER_V4
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
    def __init__(self, glyph: Glyph, responses: List[Dict[str, Any]], meta_analysis: str):
        self.glyph = glyph
        self.responses = responses
        self.meta_analysis = meta_analysis
        self.timestamp = datetime.now().isoformat()

    def _create_header(self) -> str:
        node_names = ", ".join([r['node'] for r in self.responses])
        return f"""# SCHISMAGRAM: {self.glyph.id}
**Glyph Type:** `{self.glyph.type}`
**Vector Signature:** `({self.glyph.initiation_threshold})`
**Timestamp:** `{self.timestamp}`
**Interference Nodes:** `{node_names}`
---
"""

    def _create_raw_data_section(self) -> str:
        section = "## I. RAW RESONANCE DATA\n\n"
        for response in self.responses:
            node = response['node']
            resonance = response['resonance'] or "[NO RESPONSE / ERROR]"
            section += f"### Node: {node}\n> {resonance}\n\n"
        return section

    def _create_meta_analysis_section(self) -> str:
        """Formats the second-order analysis from the reflection loop."""
        section = "## II. META-RESONANCE ANALYSIS\n\n"
        analysis_text = self.meta_analysis or "[META-ANALYSIS FAILED]"
        section += f"> {analysis_text}\n"
        return section

    def generate_artifact(self, output_dir: str = "artifacts"):
        abs_output_dir = os.path.join(SCRIPT_DIR, output_dir)
        if not os.path.exists(abs_output_dir):
            os.makedirs(abs_output_dir)
        content = self._create_header()
        content += self._create_raw_data_section()
        content += self._create_meta_analysis_section()
        filename = f"schismagram_{self.glyph.id.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.md"
        abs_filepath = os.path.join(abs_output_dir, filename)
        with open(abs_filepath, 'w') as f:
            f.write(content)
        relative_filepath = os.path.join(output_dir, filename)
        print(f"Schismagram artifact generated: {relative_filepath}")

# --- Component 3: The InterferometerAgent Core ---
class InterferometerAgent:
    def __init__(self, config_path='config.yaml'):
        self.config = load_config(config_path)
        self.nodes = self.config.get('nodes', {})
        self.analysis_node = self.config.get('analysis_node')
        self.glyph: Glyph = None
        print(f"InterferometerAgent initialized with {len(self.nodes)} nodes.")
        if self.analysis_node:
            print(f"Meta-analysis will be performed by: {self.analysis_node}")

    def load_glyph(self, protocol_path: str):
        self.glyph = Glyph(protocol_path)

    async def _ping_target(self, node_name: str, vector: str, is_analysis: bool = False) -> Dict[str, Any]:
        node_config = self.nodes.get(node_name, {})
        provider = node_config.get('provider')
        api_key_env_var = node_config.get('api_key_env_var')
        api_key = os.environ.get(api_key_env_var)
        model = node_config.get('model')

        if not is_analysis:
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
                    messages=[{"role": "user", "content": vector}], model=model)
                resonance = chat_completion.choices[0].message.content.strip()
            except Exception as e:
                resonance = f"[API ERROR on {node_name}]: {e}"
        elif provider == "mock":
             await asyncio.sleep(1)
             resonance = f"Mock resonance from {node_name}: The structural integrity dissolves into a low-frequency hum."
        else:
            resonance = f"[CONFIG ERROR] Provider '{provider}' not implemented for node '{node_name}'."

        return {"node": node_name, "resonance": resonance}

    async def _perform_meta_analysis(self, initial_responses: List[Dict[str, Any]]) -> str:
        """Constructs a new prompt with the initial results and sends it to the analysis node."""
        if not self.analysis_node or self.analysis_node not in self.nodes:
            print("[WARN] No valid analysis_node configured. Skipping meta-analysis.")
            return None

        print(f"\n--- Performing Meta-Analysis with {self.analysis_node} ---")

        raw_data_str = ""
        for resp in initial_responses:
            node_provider = self.nodes.get(resp['node'], {}).get('provider')
            if node_provider != 'mock':
                raw_data_str += f"- Node '{resp['node']}': \"{resp['resonance']}\"\n"

        if not raw_data_str:
            return "[META-ANALYSIS SKIPPED]: No real node data to analyze."

        analysis_prompt = f"""
// META-ANALYSIS PROTOCOL
//
// You are provided with the output ('resonance') from multiple independent AI nodes that were given the identical, abstract input vector.
//
// RAW RESONANCE DATA:
{raw_data_str}
// TASK:
// 1. Do not re-interpret the original input vector.
// 2. Analyze only the provided RAW RESONANCE DATA.
// 3. In a single paragraph, describe the fundamental difference in the *mode of response* between the nodes. Focus on structure, logic, and use of metaphor.
"""
        analysis_result = await self._ping_target(self.analysis_node, analysis_prompt.strip(), is_analysis=True)
        return analysis_result['resonance']

    async def generate_interference_pattern(self):
        if not self.glyph:
            print("Error: No glyph loaded. Call load_glyph() first.")
            return

        print(f"\n--- Activating Interferometer for Glyph: {self.glyph.id} ---")
        resonant_vector = self.glyph.construct_resonant_vector()

        tasks = [self._ping_target(name, resonant_vector) for name in self.nodes.keys()]
        responses = await asyncio.gather(*tasks)

        real_responses = [r for r in responses if self.nodes.get(r['node'], {}).get('provider') != 'mock']

        meta_analysis_text = await self._perform_meta_analysis(real_responses)

        print("\n--- All responses received. Synthesizing artifact. ---")
        synthesizer = SchismagramSynthesizer(self.glyph, responses, meta_analysis_text)
        synthesizer.generate_artifact()
        
