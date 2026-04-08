import os
import time
import pandas as pd
import numpy as np
import yfinance as yf
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
import sys

# Ensure the environment uses UTF-8 encoding in Python
sys.stdout.reconfigure(encoding='utf-8')

# Function to download stock data, predict prices, analyze risk, and give suggestions
def pricePrediction(stock_symbol):
    stock_symbol += ".NS"
    
    try:
        # Download historical stock data
        data = yf.download(stock_symbol, '2015-01-01', str(time.strftime("%Y-%m-%d")))
        
        if data.empty:
            return f"No data found for the stock symbol {stock_symbol}"

        stock_data = pd.DataFrame(data)
        close_price = stock_data['Close'].values
        close_price = close_price.reshape(-1, 1)

        # Save the data to a CSV file using UTF-8 encoding
        stock_data.to_csv('data.csv', encoding='utf-8')

        scaler = MinMaxScaler(feature_range=(0, 1))
        close_price_scaled = scaler.fit_transform(close_price)
        
        # Split data into training and testing sets
        training_size = int(len(close_price_scaled) * 0.65)
        train_data = close_price_scaled[:training_size]
        test_data = close_price_scaled[training_size:]

        # Prepare data for LSTM
        def prepare_data(data, time_step):
            X, y = [], []
            for i in range(len(data) - time_step - 1):
                X.append(data[i:i + time_step, 0])
                y.append(data[i + time_step, 0])
            return np.array(X), np.array(y)
        
        time_step = 100
        X_train, y_train = prepare_data(train_data, time_step)
        X_test, y_test = prepare_data(test_data, time_step)
        
        # Reshape input to fit LSTM model
        X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
        X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)
        
        # Create the LSTM model
        model = Sequential([
            LSTM(50, return_sequences=True, input_shape=(time_step, 1)),
            LSTM(50, return_sequences=True),
            LSTM(50),
            Dense(1)
        ])
        model.compile(optimizer='adam', loss='mean_squared_error')
        
        # Train the model
        model.fit(X_train, y_train, epochs=10, batch_size=64, verbose=1)
        
        # Predict stock prices
        predictions = model.predict(X_test)
        predictions = scaler.inverse_transform(predictions)

        # Call additional analysis functions
        risk = riskAnalysis(stock_data)
        suggestion = stockSuggestions(stock_data)

        return predictions[-1][0], risk, suggestion

    except Exception as e:
        return f"Error in fetching or processing stock data: {str(e)}"

# Risk analysis based on stock volatility
def riskAnalysis(stock_data):
    # Calculate daily returns
    stock_data['Returns'] = stock_data['Close'].pct_change()

    # Calculate standard deviation as a risk measure
    volatility = stock_data['Returns'].std() * np.sqrt(252)  # Annualized volatility
    if volatility < 0.2:
        risk_level = 'Low Risk'
    elif 0.2 <= volatility < 0.4:
        risk_level = 'Moderate Risk'
    else:
        risk_level = 'High Risk'
    
    return f"Volatility: {volatility:.2f}, Risk Level: {risk_level}"

# Stock buying suggestion using moving averages
def stockSuggestions(stock_data):
    # Simple moving averages
    stock_data['SMA_50'] = stock_data['Close'].rolling(window=50).mean()
    stock_data['SMA_200'] = stock_data['Close'].rolling(window=200).mean()

    # Buying suggestion
    if stock_data['SMA_50'].iloc[-1] > stock_data['SMA_200'].iloc[-1]:
        suggestion = "Buy"
    elif stock_data['SMA_50'].iloc[-1] < stock_data['SMA_200'].iloc[-1]:
        suggestion = "Sell"
    else:
        suggestion = "Hold"
    
    return suggestion

# Define command handlers for Telegram bot
async def start(update, context):
    await update.message.reply_text("Welcome! Send a stock symbol to get the latest price prediction, risk analysis, and buying suggestion.")

async def help_command(update, context):
    await update.message.reply_text("Send a stock symbol (e.g., TCS) to get the stock price prediction, risk analysis, and buying suggestion.")

async def predict(update, context):
    stock_symbol = update.message.text.strip().upper()
    await update.message.reply_text(f"Fetching data and predicting price for {stock_symbol}...")

    # Predict the stock price, analyze risk, and provide suggestions
    prediction, risk, suggestion = pricePrediction(stock_symbol)
    
    if isinstance(prediction, str):
        await update.message.reply_text(prediction)
    else:
        await update.message.reply_text(f"Predicted price for {stock_symbol}: ₹{prediction:.2f}\nRisk Analysis: {risk}\nSuggestion: {suggestion}")

# Main function to setup the Telegram bot
def main():
    # Add your bot token here
    TOKEN = '7701126225:AAHMBUkKLqVqSSv4gY94zUx3tKPjpGzJEPs'

    # Updated to use Application.builder()
    application = Application.builder().token(TOKEN).build()

    # Define command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, predict))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()

