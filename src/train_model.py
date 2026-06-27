import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score
import xgboost as xgb
import pickle
import os

def train_model():
    # Load data
    df = pd.read_csv('data/sales_data.csv')
    print("Data loaded:", df.shape)
    
    # Feature Engineering
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.month
    df['day_of_week'] = df['date'].dt.dayofweek
    df['quarter'] = df['date'].dt.quarter
    
    # Encode categoricals
    le_category = LabelEncoder()
    le_region = LabelEncoder()
    df['category_encoded'] = le_category.fit_transform(df['category'])
    df['region_encoded'] = le_region.fit_transform(df['region'])
    
    # Features & Target
    features = ['month', 'day_of_week', 'quarter', 'quantity', 
                'price', 'discount', 'category_encoded', 'region_encoded']
    X = df[features]
    y = df['revenue']
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train
    model = xgb.XGBRegressor(
        n_estimators=200,
        learning_rate=0.1,
        max_depth=6,
        random_state=42
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"MAE: {mae:.2f}")
    print(f"R2 Score: {r2:.2f}")
    
    # Save model & encoders
    os.makedirs('models', exist_ok=True)
    with open('models/model.pkl', 'wb') as f:
        pickle.dump(model, f)
    with open('models/le_category.pkl', 'wb') as f:
        pickle.dump(le_category, f)
    with open('models/le_region.pkl', 'wb') as f:
        pickle.dump(le_region, f)
    
    print("Model saved successfully!")
    return model, mae, r2

if __name__ == "__main__":
    train_model()