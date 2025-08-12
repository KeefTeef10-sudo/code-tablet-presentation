import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

def forecast_budget(transactions_csv, months_ahead=3):
    df = pd.read_csv(transactions_csv)
    df['Month'] = pd.to_datetime(df['Date']).dt.month
    monthly = df.groupby('Month')['Amount'].sum().reset_index()

    X = np.array(monthly['Month']).reshape(-1, 1)
    y = monthly['Amount'].values
    model = LinearRegression().fit(X, y)

    future_months = np.array([(monthly['Month'].max() + i) % 12 or 12
                              for i in range(1, months_ahead+1)]).reshape(-1, 1)
    forecast = model.predict(future_months)
    return dict(zip(future_months.flatten(), forecast))

if __name__ == "__main__":
    # Example usage:
    # print(forecast_budget("transactions.csv"))
    pass
