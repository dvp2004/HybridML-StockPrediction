import os
import logging
import numpy as np
from tqdm import tqdm
from trading_bot.utils import format_currency, format_position

def count_action(history):
    # Count the total BUY, SELLS, and HOLDS in history
    actions = np.array(history)[:, 2]
    counts = np.unique(actions, return_counts=True) # Count the unique actions
    counts = list(zip(counts[0], counts[1])) # Zip the unique actions with their counts
    print(counts)

def evaluate_model(agent, data, debug=False):
    history = []

    for index, row in tqdm(data.iterrows(), total=data.shape[0] - 1):
        current_date = row['date']
        current_real_price = row['Real']
        predicted_price_current_day = row['Predicted']
        predicted_price_next_day = data.iloc[index + 1]['Predicted'] if index + 1 < len(data) else predicted_price_current_day

        # Calculate relative change using the average of predicted buy prices
        avg_predicted_buy_price = agent.average_predicted_buy_price()
        relative_change = (predicted_price_next_day - avg_predicted_buy_price) / avg_predicted_buy_price if avg_predicted_buy_price != 0 else 0

        action = agent.act(relative_change)
        n_shares = round(agent.balance * agent.max_trade_percent / current_real_price)

        if action in ["BUY", "SELL"] and n_shares > 0:
            if action == "BUY":
                bought_shares, cost = agent.buy(current_real_price, n_shares, predicted_price_current_day)
                history.append((current_date, current_real_price, action, bought_shares))
                # if debug:
                #     logging.debug(f"Bought {bought_shares} shares at: {current_real_price} on {current_date}")
            elif action == "SELL":
                sold_shares, revenue = agent.sell(current_real_price, len(agent.inventory))
                history.append((current_date, current_real_price, action, sold_shares))
                # if debug:
                #     logging.debug(f"{action} {sold_shares} shares at: {current_real_price} on {current_date}")

        else:  # HOLD or if no shares were bought/sold
            history.append((current_date, current_real_price, "HOLD", 0))
            # if debug:
            #     logging.debug(f"Hold at: {current_real_price} on {current_date}")

    final_assets = agent.calculate_total_assets(current_real_price)
    return history, final_assets




# def evaluate_model(agent, data, debug=False):
#     history = []
#     k=100

#     for index, row in tqdm(data.iterrows(), total=data.shape[0] - 1):  # Loop until the second last row
#         current_date = row['date']
#         current_price = row['Real']
#         predicted_price_current_day = row['Predicted']
#         predicted_price_next_day = data.iloc[index + 1]['Predicted'] if index + 1 < len(data) else predicted_price_current_day

#         relative_change = (predicted_price_next_day - predicted_price_current_day) / predicted_price_current_day if predicted_price_current_day != 0 else 0

#         action = agent.act(relative_change)
#         # n_shares = int(agent.balance * agent.max_trade_percent // current_price)

#         if len(history) != 0: # If not first day of trade
#             if action == "BUY":  # Profit predicted, consider buying
#                 print("DOES IT COME HERED!")
#                 n_shares = abs(relative_change * k * (agent.balance * agent.max_trade_percent / current_price))
#                 print(n_shares)
#                 n_shares = int(min(n_shares, agent.balance * agent.max_trade_percent / current_price))  # Convert to integer
#                 print("Buy, n_shares: ", n_shares)

#             elif action == "SELL":  # Predicted price is lower, consider selling
#                 print("selllllllllllllll!")

#                 n_shares = abs(relative_change * k * len(agent.inventory))
#                 n_shares = int(min(n_shares, len(agent.inventory)))  # Convert to integer
#                 print("Sell, n_shares: ", n_shares)

#         else: # First day of trade
#             n_shares = 1
#             print("Buy, n_shares: ", n_shares)


#         if action == "BUY" and n_shares > 0:
#             bought_shares, cost = agent.buy(current_price, n_shares)
#             history.append((current_date, current_price, "BUY", bought_shares))

#             # if debug:
#                 # logging.debug(f"Bought {bought_shares} shares at: {current_price} on {current_date}")
        
#         elif action == "SELL" and agent.inventory:
#             sold_shares, revenue = agent.sell(current_price, len(agent.inventory))
#             history.append((current_date, current_price, "SELL", sold_shares))

#             # if debug:
#                 # logging.debug(f"Sold {sold_shares} shares at: {current_price} on {current_date}")
        
#         else:  # HOLD or if no shares were bought/sold
#             history.append((current_date, current_price, "HOLD", 0))
#             # if debug:
#                 # logging.debug(f"Hold at: {current_price} on {current_date}")

#         if debug:
#             print(f"Date: {current_date}, Current Price: {current_price}, Relative Change: {relative_change:.2%}, Action: {action}, Total Stocks: {len(agent.inventory)}, Total Balance: {format_currency(agent.balance)}")

#     final_assets = agent.calculate_total_assets(current_price) 
#     # book_value = agent.calculate_book_value()
#     # selling_profit = final_assets - agent.balance  # Profit from selling shares
#     return history, final_assets






