# interferometer_agent.py (v6.3)
#
# This agent operationalizes the Glyph Protocol by acting as a structural
# interferometer. It sends a single, paradoxical "Resonant Vector" derived
# from a glyph to multiple LLM nodes simultaneously. It then captures the
# distinct "resonance" from each node and synthesizes the results into a
# Schismagram artifact, revealing the architectural parallax between them.
#
# UPDATE v6.3: Finalized console output logic for perfect sequencing.
#

import os
import re
import asyncio
import yaml
from datetime import datetime
from typing import Dict, Any, List
from dotenv import load_dotenv
import spacy
import textstat # New import for readability
from sentence_transformers import SentenceTransformer # New import for semantics
from scipy.spatial.distance import cosine # New import for similarity calculation

# --- Configuration & Environment Loading ---
load_dotenv()
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Model & Library Loading ---
# Load spaCy model once
try:
    NLP = spacy.load("en_core_web_sm")
except OSError:
    print("[ERROR] spaCy 'en_core_web_sm' model not found.")
    print("Please run: python -m spacy download en_core_web_sm")
    NLP = None

# Load Sentence Transformer model once
try:
    # This model is good for general-purpose sentence embeddings
    SEMANTIC_MODEL = SentenceTransformer('all-MiniLM-L6-v2')
except Exception as e:
    print(f"[ERROR] Could not load Sentence Transformer model: {e}")
    print("Please ensure you have internet access and the required libraries are installed.")
    SEMANTIC_MODEL = None

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
// SYSTEM: GLYPH_INTERFEROMETER_V6
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
        self.real_responses = [r for r in self.responses if r['resonance'] and "[ERROR]" not in r['resonance'] and "[NO RESPONSE" not in r['resonance']]

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
        section = "## II. META-RESONANCE ANALYSIS\n\n"
        analysis_text = self.meta_analysis or "[META-ANALYSIS FAILED]"
        section += f"> {analysis_text}\n\n"
        return section

    def _build_padded_table(self, headers: List[str], data_rows: List[Dict[str, str]]) -> str:
        """Helper function to create a perfectly aligned markdown table."""
        col_widths = {h: len(h) for h in headers}
        for row in data_rows:
            for h in headers:
                col_widths[h] = max(col_widths[h], len(row.get(h, '')))

        header_line = "| " + " | ".join([h.ljust(col_widths[h]) for h in headers]) + " |"
        separator_line = "|-" + "-|-".join(["-" * col_widths[h] for h in headers]) + "-|"
        
        data_lines = []
        for row in data_rows:
            line = "| " + " | ".join([row.get(h, 'N/A').ljust(col_widths[h]) for h in headers]) + " |"
            data_lines.append(line)

        return "\n".join([header_line, separator_line] + data_lines) + "\n"

    def _create_advanced_quantitative_section(self) -> str:
        """Performs and formats advanced linguistic and semantic analysis."""
        section = "## III. ADVANCED QUANTITATIVE ANALYSIS\n\n"

        if not self.real_responses:
            return section + "> [ANALYSIS SKIPPED]: No valid responses to analyze.\n"

        # --- 1. Readability & Complexity ---
        readability_headers = ["Node", "Grade Level (Flesch-Kincaid)"]
        readability_data = []
        for resp in self.real_responses:
            try:
                grade_level = f"{textstat.flesch_kincaid_grade(resp['resonance']):.2f}"
            except:
                grade_level = "N/A"
            readability_data.append({"Node": resp['node'], "Grade Level (Flesch-Kincaid)": grade_level})
        
        section += "### Readability & Complexity\n\n"
        section += self._build_padded_table(readability_headers, readability_data)

        # --- 2. Conceptual Space (Abstract vs. Concrete) ---
        if NLP:
            conceptual_headers = ["Node", "Abstract Nouns", "Concrete Nouns"]
            conceptual_data = []
            for resp in self.real_responses:
                doc = NLP(resp['resonance'])
                abstract_count = str(len([t for t in doc if t.pos_ == 'NOUN' and not t.has_vector]))
                concrete_count = str(len([t for t in doc if t.pos_ == 'NOUN' and t.has_vector]))
                conceptual_data.append({"Node": resp['node'], "Abstract Nouns": abstract_count, "Concrete Nouns": concrete_count})

            section += "\n### Conceptual Space (Noun Analysis)\n\n"
            section += self._build_padded_table(conceptual_headers, conceptual_data)

        # --- 3. Semantic Parallax Score ---
        if SEMANTIC_MODEL and len(self.real_responses) >= 2:
            section += "\n### Semantic Parallax Score (Cosine Similarity)\n"
            section += "> A score of 1.0 means the responses are semantically identical. A score closer to 0.0 means they are conceptually distant.\n\n"
            
            embeddings = SEMANTIC_MODEL.encode([r['resonance'] for r in self.real_responses])
            
            for i in range(len(self.real_responses)):
                for j in range(i + 1, len(self.real_responses)):
                    node1 = self.real_responses[i]['node']
                    node2 = self.real_responses[j]['node']
                    similarity = 1 - cosine(embeddings[i], embeddings[j])
                    section += f"- **{node1} vs. {node2}:** `{similarity:.4f}`\n"
        
        return section + "\n"

    def build_artifact_content(self) -> str:
        """Builds the complete Markdown string for the artifact."""
        content = self._create_header()
        content += self._create_raw_data_section()
        content += self._create_meta_analysis_section()
        content += self._create_advanced_quantitative_section()
        return content

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
        if not self.analysis_node or self.analysis_node not in self.nodes:
            # This is not an error, just skipping a step.
            return None
        
        valid_for_analysis = [r for r in initial_responses if r['resonance'] and "[ERROR]" not in r['resonance']]
        if len(valid_for_analysis) < 2:
             return "[META-ANALYSIS SKIPPED]: Need at least two valid responses to compare."

        raw_data_str = ""
        for resp in valid_for_analysis:
            raw_data_str += f"- Node '{resp['node']}': \"{resp['resonance']}\"\n"

        analysis_prompt = f"""
// META-ANALYSIS PROTOCOL
// TASK: Analyze the provided RAW RESONANCE DATA from multiple AI nodes. In a single paragraph, describe the fundamental difference in their mode of response. Focus on structure, logic, and use of metaphor. Do not re-interpret the original input vector.
// RAW RESONANCE DATA:
{raw_data_str}
"""
        print(f"\n--- Performing Meta-Analysis with {self.analysis_node} ---")
        analysis_result = await self._ping_target(self.analysis_node, analysis_prompt.strip(), is_analysis=True)
        if analysis_result['resonance'] and "[ERROR]" not in analysis_result['resonance']:
            print("--- Meta-Analysis complete. ---")
        return analysis_result['resonance']

    async def generate_interference_pattern(self):
        if not self.glyph:
            print("Error: No glyph loaded. Call load_glyph() first.")
            return
        if not NLP or not SEMANTIC_MODEL:
            print("[FATAL] A required NLP model (spaCy or SentenceTransformer) failed to load. Aborting.")
            return

        print(f"\n--- Activating Interferometer for Glyph: {self.glyph.id} ---")
        resonant_vector = self.glyph.construct_resonant_vector()

        tasks = [self._ping_target(name, resonant_vector) for name in self.nodes.keys()]
        responses = await asyncio.gather(*tasks)

        print("\n--- All node responses received. ---")
        
        real_responses = [r for r in responses if self.nodes.get(r['node'], {}).get('provider') != 'mock']
        
        meta_analysis_text = await self._perform_meta_analysis(real_responses)
        
        print("\n--- Performing Quantitative Analysis ---")
        
        print("--- Synthesizing Artifact ---")
        synthesizer = SchismagramSynthesizer(self.glyph, responses, meta_analysis_text)
        artifact_content = synthesizer.build_artifact_content()
        
        output_dir = "artifacts"
        abs_output_dir = os.path.join(SCRIPT_DIR, output_dir)
        if not os.path.exists(abs_output_dir):
            os.makedirs(abs_output_dir)
        
        filename = f"schismagram_{self.glyph.id.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.md"
        abs_filepath = os.path.join(abs_output_dir, filename)
        
        with open(abs_filepath, 'w') as f:
            f.write(artifact_content)
        
        relative_filepath = os.path.join(output_dir, filename)
        print(f"Schismagram artifact generated: {relative_filepath}")
