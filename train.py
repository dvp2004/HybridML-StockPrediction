import os
import coloredlogs
import pandas as pd
from docopt import docopt
import tensorflow as tf
from trading_bot.agent import Agent
from trading_bot.methods import evaluate_model
from trading_bot.utils import (
    format_currency,
    format_position,
    show_eval_result,
    switch_k_backend_device
)

def main(val_stock, model_name, debug):
    """Evaluates the stock trading bot."""
    df = pd.read_csv(val_stock)
    initial_offset = df['Real'][1] - df['Real'][0]

    if model_name is not None:
        agent = Agent(pretrained=True, model_name=model_name)
        profit, history = evaluate_model(agent, df, debug)
        show_eval_result(model_name, profit, initial_offset)
    else:
        raise ValueError("Model name must be specified for evaluation.")

if __name__ == "__main__":
    args = docopt(__doc__)

    val_stock = args["<val-stock>"]
    model_name = args["--model-name"]
    debug = args["--debug"]

    coloredlogs.install(level="DEBUG")
    switch_k_backend_device()

    try:
        main(val_stock, model_name, debug)
    except KeyboardInterrupt:
        print("Aborted!")
