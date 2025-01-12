
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.database import log_sentiment, fetch_sentiment_logs_with_time, get_connection  # Import database logging function, fetching function

get_connection()
print("Success: get_connection Ended")

log_sentiment("Happy")
print("Endd")

logs = fetch_sentiment_logs_with_time()
print(logs.head(3))
print("Endddd")