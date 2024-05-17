import os
import math
import logging
import numpy as np

def sigmoid(x):
    """Performs sigmoid operation."""
    try:
        return 1 - 1 / (1 + math.exp(x))
    except OverflowError as err:
        logging.error(f"Overflow error in sigmoid for x={x}: {err}")
        return 0.0 if x < 0 else 1.0
