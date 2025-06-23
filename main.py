# main.py
#
# This is the primary execution script for the Glyph Protocol project.
# It initializes the InterferometerAgent, loads a specific glyph protocol,
# and triggers the asynchronous process to generate a Schismagram artifact.
#

import asyncio
from interferometer_agent import InterferometerAgent

async def main():
    """
    The main asynchronous function to run the agent.
    """
    try:
        # 1. Initialize the agent. It will automatically load 'config.yaml'
        #    and the secrets from your '.env' file.
        agent = InterferometerAgent()

        # 2. Load the specific glyph protocol you want to activate.
        #    Make sure the path is correct relative to your project root.
        protocol_file_path = "glyphs/acidic_trace_01.protocol.md"
        agent.load_glyph(protocol_file_path)

        # 3. Run the interference process.
        #    This will ping all configured LLM nodes concurrently and
        #    generate the final artifact.
        await agent.generate_interference_pattern()

    except FileNotFoundError as e:
        print(f"\n[FATAL ERROR] A required file was not found: {e}")
        print("Please ensure 'config.yaml' and your protocol file exist in the correct directories.")
    except Exception as e:
        print(f"\n[FATAL ERROR] An unexpected error occurred: {e}")


if __name__ == "__main__":
    # This block allows the script to be run from the command line.
    # It sets up and runs the asyncio event loop.
    #
    # Before running, ensure you have installed the necessary libraries:
    # pip install python-dotenv PyYAML google-generativeai openai

    print("Initializing Glyph Protocol sequence...")
    asyncio.run(main())
    print("\nSequence complete.")
