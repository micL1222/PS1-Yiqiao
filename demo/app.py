"""Local Gradio prototype for the verified information-acquisition game."""

import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import gradio as gr

from demo.demo_logic import render_choice, render_game
from src.information_acquisition_game import ACTIONS


def build_app():
    """Construct the local-only educational interface without launching it."""
    with gr.Blocks(title="Who Pays to Know? Strategic Information Acquisition Before AI Collective Decisions") as app:
        gr.Markdown("# Who Pays to Know?\n## Strategic Information Acquisition Before AI Collective Decisions")
        gr.Markdown(
            "An interactive formal model of costly research, shared information, and free-riding "
            "before a collective decision."
        )
        gr.Markdown(
            "**Evidence status:** This is a formal game-theoretic educational prototype. "
            "It does not simulate or measure actual LLM or human behavior. "
            "Educational effectiveness has not been evaluated."
        )
        with gr.Tab("Play One Strategic Decision"):
            gr.Markdown("Choose A's action after selecting B's action. Compare A's payoff with a unilateral change.")
            with gr.Row():
                play_value = gr.Slider(1, 10, value=4, step=1, label="Information value V")
                play_cost = gr.Slider(0, 10, value=2, step=1, label="Research cost c")
            with gr.Row():
                b_action = gr.Radio(ACTIONS, value="Research", label="Agent B action")
                a_action = gr.Radio(ACTIONS, value="Research", label="Your action as Agent A")
            play_button = gr.Button("Evaluate My Choice")
            play_output = gr.Markdown(label="Choice evaluation")
            play_button.click(render_choice, [play_value, play_cost, b_action, a_action], play_output)
        with gr.Tab("Explore the Full Game"):
            gr.Markdown("Inspect the complete payoff matrix, pure equilibria, and NashPy support-enumeration output.")
            with gr.Row():
                game_value = gr.Slider(1, 10, value=4, step=1, label="Information value V")
                game_cost = gr.Slider(0, 10, value=2, step=1, label="Research cost c")
            game_button = gr.Button("Analyze Game")
            game_output = gr.Markdown(label="Full game analysis")
            game_button.click(render_game, [game_value, game_cost], game_output)
    return app


if __name__ == "__main__":
    build_app().launch(
        server_name="127.0.0.1",
        server_port=int(os.environ.get("DEMO_PORT", "7860")),
        share=False,
        inbrowser=False,
    )
