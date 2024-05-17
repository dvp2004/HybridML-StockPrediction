import os
import logging
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler


def format_position(price):
    """Formats the position value."""
    return ('-$' if price < 0 else '+$') + '{0:.2f}'.format(abs(price))


def format_currency(price):
    """Formats the currency value."""
    return '${0:.2f}'.format(abs(price))


def show_train_result(result, val_position, initial_offset):
    """Displays training results."""
    if val_position == initial_offset or val_position == 0.0:
        logging.info(f'Episode {result[0]}/{result[1]} - Train Position: {format_position(result[2])}  Val Position: USELESS  Train Loss: {result[3]:.4f}')
    else:
        logging.info(f'Episode {result[0]}/{result[1]} - Train Position: {format_position(result[2])}  Val Position: {format_position(val_position)}  Train Loss: {result[3]:.4f}')


def show_eval_result(profit, initial_offset):
    """Displays evaluation results."""
    if profit == initial_offset or profit == 0.0:
        logging.info(f'USELESS\n')
    else:
        logging.info(f'{format_position(profit)}\n')


def get_stock_data(stock_file):
    """Reads stock data from a CSV file."""
    df = pd.read_csv(stock_file)
    return list(df['Adj Close'])


def switch_k_backend_device():
    """Switches the Keras backend device."""
    if os.environ.get('CUDA_VISIBLE_DEVICES') is None:
        logging.info("Switching to CPU for TensorFlow")
        os.environ['CUDA_VISIBLE_DEVICES'] = '-1'