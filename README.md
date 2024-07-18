# Trading Bot

## Overview

This repository contains a Python-based high-frequency trading bot that utilizes the Relative Strength Index (RSI) and N-day Moving Average (NMA) algorithms to make trading decisions in simulated environments. The bot aims to maximize profits by dynamically adjusting to market conditions.

## Features

- **RSI Calculation**: Computes the Relative Strength Index to gauge overbought (RSI > 70) or oversold (RSI < 30) market conditions.
- **NMA Calculation**: Calculates the N-day Moving Average to identify trend directions over a specified period.
- **Decision Making**: Implements buying and selling decisions based on RSI and NMA signals.
- **Real-time Updates**: Interacts with a simulated trading environment to receive market updates and execute trades.

## Requirements

- Python 3.x
- Dependencies listed in `requirements.txt`
- Access to simulated trading environment for testing and deployment

## Setup

1. **Clone Repository:**
   ```bash
   git clone https://github.com/your-username/trading-bot.git
   cd trading-bot
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configuration:**
   - Ensure correct paths and access to training datasets and simulated trading interface.

## Usage

### Training and Testing

- Utilize provided training datasets to develop and test trading algorithms.
- Implement variations of RSI and NMA strategies to optimize performance.
- Use simulated trading environments like `tradingview.com` for initial testing.

### Deployment

- Connect the bot to a simulated trading interface using command line instructions.
- Monitor bot performance and adjust strategies based on simulated trading results.

### Evaluation

- Evaluate bot performance based on profitability metrics and comparison with other trading strategies.
- Ensure strategies are adaptive and resilient to market changes to avoid overfitting.

## Architecture

- **Bot Class**: Implements main logic for decision-making using RSI and NMA algorithms.
- **BotState Class**: Manages state information including timebank, candle updates, and stack management.
- **Candle and Chart Classes**: Handle candlestick data and chart updates for market analysis.
