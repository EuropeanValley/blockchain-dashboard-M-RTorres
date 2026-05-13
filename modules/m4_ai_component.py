"""Starter file for module M4."""

import pandas as pd
from prophet import Prophet
from sklearn.metrics import mean_absolute_error
import streamlit as st


def train_predictor(data: pd.DataFrame) -> dict:
    """
    Train a Prophet model to predict the next difficulty adjustment.

    Args:
        data (pd.DataFrame): DataFrame with columns 'ds' (timestamps) and 'y' (difficulty values).

    Returns:
        dict: A dictionary containing the model, forecast, and evaluation metric.
    """
    # Initialize the model
    model = Prophet()
    model.fit(data)

    # Make future predictions
    future = model.make_future_dataframe(periods=10)  # Predict next 10 adjustments
    forecast = model.predict(future)

    # Evaluate the model
    y_true = data['y']
    y_pred = model.predict(data)['yhat']
    mae = mean_absolute_error(y_true, y_pred)

    return {
        'model': model,
        'forecast': forecast,
        'mae': mae
    }


def render() -> None:
    """Render the M4 panel."""
    st.header("M4 - AI Component")

    st.subheader("Predictor: Difficulty Adjustment")

    # Placeholder for data extraction
    st.markdown("### Data Extraction")
    st.info("Use `get_block_history` to extract data.")

    # Example DataFrame structure
    example_data = pd.DataFrame({
        'ds': pd.date_range(start='2022-01-01', periods=100, freq='D'),
        'y': [i + (i % 5) for i in range(100)]  # Example difficulty values
    })

    # Train the model
    st.markdown("### Model Training")
    result = train_predictor(example_data)
    st.success(f"Model trained successfully! MAE: {result['mae']:.4f}")

    # Display forecast
    st.markdown("### Forecast")
    st.line_chart(result['forecast'][['ds', 'yhat']].set_index('ds'))
