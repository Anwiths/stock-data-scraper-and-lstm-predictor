# Stock Data Scraper and LSTM Prediction System

An end-to-end stock analysis system that combines web scraping, machine learning, and real-time interaction using a Telegram bot.

This project collects stock data from Tickertape, processes historical market data, and uses an LSTM (Long Short-Term Memory) neural network to predict stock prices. It also performs risk analysis and provides buy/sell suggestions through a Telegram bot interface.

---

## Features

- Web scraping of stock data from Tickertape
- Historical stock data retrieval using yfinance
- LSTM-based deep learning model for price prediction
- Risk analysis using volatility calculations
- Buy/Sell/Hold suggestions using moving averages
- Telegram bot integration for real-time interaction

---

## Project Structure

.
├── scraper.py(code1.py)    # Scrapes stock data from Tickertape  
├── predictor.py(code2.py)  # LSTM model and prediction logic  
├── bot.py(telegram bot)    # Telegram bot integration  
├── stockDataset_v1.csv     # Scraped dataset  
├── data.csv                # Historical stock data  
├── requirements.txt        # Dependencies  
└── README.md  

---

## How It Works

1. Data Collection  
   Scrapes stock listings from Tickertape and extracts stock details such as symbol, industry, market cap, and risk level.

2. Data Processing  
   Fetches historical stock data using yfinance and prepares it for time-series modeling.

3. Model Training  
   Uses an LSTM neural network to learn patterns in stock price movements.

4. Prediction and Analysis  
   Predicts future stock prices, evaluates risk using volatility, and generates buy/sell/hold suggestions.

5. User Interaction  
   Telegram bot accepts stock symbols and returns predictions, risk analysis, and suggestions.

---

## Technologies Used

- Python  
- Pandas, NumPy  
- BeautifulSoup  
- yfinance  
- TensorFlow / Keras  
- Scikit-learn  
- Telegram Bot API  

---

## Installation

git clone https://github.com/your-username/stock-data-scraper-and-lstm-predictor.git  
cd stock-data-scraper-and-lstm-predictor  

pip install -r requirements.txt  

---

## Usage

Run the scraper:

python scraper.py  

Run the Telegram bot:

python bot.py  

Send a stock symbol (e.g., TCS) in Telegram to receive prediction results.

---

## Important Notes

- Do not expose API keys or bot tokens in the code. Use environment variables.  
- This project is for educational purposes only and not financial advice.  
- The model retrains on each request and is not optimized for production use.  

---

## Future Improvements

- Save and reuse trained models  
- Add evaluation metrics such as RMSE  
- Improve prediction accuracy with additional features  
- Deploy as a web application or API  
- Integrate real-time streaming data  

---

## License

This project is intended for educational use.
