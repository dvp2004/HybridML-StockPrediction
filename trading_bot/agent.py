import random
from collections import deque
import numpy as np

class Agent:
    """ Stock Trading Bot """

    def __init__(self, initial_capital=10000, max_trade_percent=0.5, buy_threshold=0.02, sell_threshold=-0.02, sell_high_threshold=0.05):
        self.initial_capital = initial_capital
        self.balance = initial_capital
        self.max_trade_percent = max_trade_percent
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold
        self.sell_high_threshold = sell_high_threshold  # New threshold for selling high
        self.inventory = []  # Stores the predicted prices on the days stocks were bought

    def act(self, relative_change):
        if not self.inventory:  # Buy on the first day or if no inventory
            if self.balance > 1.05 * self.initial_capital:  # Check if balance is 5% more than initial money
                return "HOLD"  # Hold if balance is more than 5% more than initial money and no inventory
            return "BUY"
    
        # print(f"Relative Change: {relative_change}, Sell High Threshold: {self.sell_high_threshold}")
        if relative_change > self.sell_high_threshold:  # Condition to sell when relative change is high
            return "SELL"
        elif relative_change < -self.sell_high_threshold: 
            return "BUY"
        elif relative_change > self.buy_threshold:
            return "BUY"
        elif relative_change < self.sell_threshold:
            return "SELL"
        else:
            return "HOLD"

    def buy(self, current_price, n_shares, predicted_price):
        total_cost = current_price * n_shares
        if total_cost <= self.balance:
            self.balance -= total_cost
            self.inventory.extend([predicted_price] * n_shares)  # Store predicted price per share bought
            return n_shares, total_cost
        return 0, 0

    def sell(self, current_price, n_shares):
        n_shares = min(n_shares, len(self.inventory))
        if n_shares == 0:
            return 0, 0
        total_revenue = current_price * n_shares
        self.balance += total_revenue
        self.inventory = self.inventory[n_shares:]  # Remove sold predicted prices from the inventory
        return n_shares, total_revenue

    def average_predicted_buy_price(self):
        if not self.inventory:
            return 0
        return sum(self.inventory) / len(self.inventory)  # Calculate average of stored predicted prices

    def calculate_total_assets(self, current_price):
        total_assets = self.balance + len(self.inventory) * current_price
        return total_assets
    


    

