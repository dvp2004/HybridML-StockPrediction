"""
Script for evaluating Stock Trading Bot.

Usage:
  eval.py <eval-stock> [--window-size=<window-size>] [--model-name=<model-name>] [--debug]

Options:
  --window-size=<window-size>   Size of the n-day window stock data representation used as the feature vector. [default: 10]
  --model-name=<model-name>     Name of the pretrained model to use (will eval all models in `models/` if unspecified).
  --debug                       Specifies whether to use verbose logs during eval operation.
"""

import os
import pandas as pd
import coloredlogs
from docopt import docopt
import tensorflow as tf
from trading_bot.agent import Agent
from trading_bot.methods import evaluate_model
from trading_bot.utils import show_eval_result, switch_k_backend_device



def main(eval_stock, model_name, debug):
    """Evaluates the stock trading bot."""
    df = pd.read_csv(eval_stock)
    initial_offset = df['Real'][1] - df['Real'][0]

    if model_name is not None:
        agent = Agent(pretrained=True, model_name=model_name)
        profit, history = evaluate_model(agent, df, debug)
        show_eval_result(model_name, profit, initial_offset)
    else:
        raise ValueError("Model name must be specified for evaluation.")


if __name__ == "__main__":
    args = docopt(__doc__)

    eval_stock = args["<eval-stock>"]
    model_name = args["--model-name"]
    debug = args["--debug"]

    coloredlogs.install(level="DEBUG")
    switch_k_backend_device()

    try:
        main(eval_stock, model_name, debug)
    except KeyboardInterrupt:
        print("Aborted")
