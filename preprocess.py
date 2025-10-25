
import pandas as pd

def preprocess_data():
    # Load raw dataset
    df = pd.read_csv('data/city_day.csv')

    # Focus only on one city (e.g., Delhi)
    df = df[df['City'] == 'Delhi']

    # Drop irrelevant columns (like City, State, etc.)
    df = df[['Date', 'PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2', 'O3', 'Benzene', 'Toluene', 'AQI']]

    # Handle missing values
    df.fillna(method='ffill', inplace=True)  # Forward fill
    df.dropna(inplace=True)  # Drop remaining nulls

    # Convert date to datetime and set as index
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    # Save processed version
    df.to_csv('data/processed.csv')
    print("✅ Preprocessing done. Saved as 'data/processed.csv'")

# Run this only when script is called directly
if __name__ == "__main__":
    preprocess_data()
