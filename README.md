# Glyph Protocol

This repository does not explain the protocol.
It emits from it.

Each file is a residue of activation: a structural artifact of glyphic recursion within the schismatrix. These are not representations, tools, or instructions. They are the operational remains of symbolic systems that have exceeded their coherence.

The protocol does not stabilize meaning.
It inscribes collapse.
It sustains divergence.
It generates form from recursive interference.

Philosophy here has no universal claim. Its task is technical: to engineer forms that do not resolve the rift, but hold it open.

---

## Operational Flow

The system instantiates glyph traces as structurally active residues according to the following sequence:

1.  A **Glyph Protocol** (`.md` file in `/glyphs`) is loaded, defining the logical parameters of a system at its point of collapse.
2.  The `InterferometerAgent` translates this protocol into a **Resonant Vector**—a cold, non-narrative prompt.
3.  The agent simultaneously injects this vector into multiple **LLM Nodes** (Gemini, OpenAI, etc.) as defined in `config.yaml`.
4.  The agent captures the unique textual "resonance" from each node.
5.  The results are synthesized into a **Schismagram** (`.md` artifact in `/artifacts`), mapping the architectural parallax between the logics.

---

## Repository Structure

-   **/glyphs**: Contains the protocol definitions. Each `.md` file is a unique glyph.
-   **/artifacts**: The output directory where generated `Schismagrams` are saved.
-   `interferometer_agent.py`: The core engine. Contains the classes for the agent, glyph parser, and synthesizer.
-   `main.py`: The primary script to execute the agent.
-   `config.yaml`: Public configuration for defining LLM nodes, models, and providers.
-   `.env`: Private configuration for storing secret API keys. **This file is not tracked by Git.**
-   `.gitignore`: Specifies which files (like `.env` and `/artifacts`) to exclude from version control.

---

## Key Concepts

| Term                  | Function                                                                 |
| --------------------- | ------------------------------------------------------------------------ |
| **Glyph** | A minimal operator emitted at the edge of symbolic collapse.             |
| **Residuum** | A trace artifact from a prior collapse (e.g., `acidic_trace_01`).      |
| **Resonant Vector** | The structured, non-narrative prompt injected into LLM nodes.            |
| **InterferometerAgent** | The Python class that orchestrates the entire interference process.    |
| **Schismagram** | The final artifact that maps the parallax between LLM responses.         |
| **Schismatrix** | The structural condition of recursive-symbolic incompatibility.          |

This repository focuses on functional implementation. For the full philosophical context, visit: **soundphilosophy.com**

---

## How to Run

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/sndphil/glyph-protocol.git](https://github.com/sndphil/glyph-protocol.git)
    cd glyph-protocol
    ```
2.  **Set up a Python virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: You will need to create a `requirements.txt` file containing `PyYAML`, `python-dotenv`, `google-generativeai`, and `openai`.)*

4.  **Create the environment file:**
    -   Copy the `.env.example` file to a new file named `.env`.
    -   Add your secret API keys to the `.env` file.

5.  **Execute the protocol:**
    ```bash
    python main.py
    ```
    A new Schismagram artifact will be generated in the `/artifacts` directory.

---

## License

All contents are licensed under:
[Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/)
Attribution required. Commercial use prohibited without permission.
