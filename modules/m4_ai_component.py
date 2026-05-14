"""Starter file for module M4."""

import pandas as pd
from prophet import Prophet
from sklearn.metrics import mean_absolute_error
import streamlit as st
from api.blockchain_client import get_block_history


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

    # Make future predictions for one year
    future = model.make_future_dataframe(periods=365)  # Predict next 365 days
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

    # Allow the user to select a time period
    st.markdown("### Data Extraction")
    time_period = st.selectbox(
        "Select time period",
        options=["1m", "3m", "6m", "1y", "2y", "3y", "All"],
        index=0,
        key="m4_time_period"
    )

    if st.button("Load and Train Model", key="m4_load"):
        with st.spinner("Fetching data..."):
            try:
                # Fetch data for the selected time period
                data = get_block_history(time_period)

                # Extract relevant data
                difficulties = data.get("difficulty", [])

                if not difficulties:
                    st.warning("No data available for the selected time period.")
                    return

                # Extract relevant data from difficulties
                timestamps = [entry["time"] for entry in difficulties]
                difficulty_values = [entry["difficulty"] for entry in difficulties]

                # Create a DataFrame for training
                df = pd.DataFrame({
                    "ds": pd.to_datetime(timestamps, unit="s"),
                    "y": difficulty_values,
                })

                # Train the model
                st.markdown("### Model Training")
                result = train_predictor(df)
                st.success(f"Model trained successfully! MAE: {result['mae']:.4f}")

                # Display forecast
                st.markdown("### Forecast")
                forecast = result['forecast']

                # Separate historical and forecasted data
                historical = forecast[forecast['ds'] <= df['ds'].max()]
                future = forecast[forecast['ds'] > df['ds'].max()]

                # Plot historical and forecasted data
                chart_data = pd.DataFrame({
                    "ds": pd.concat([historical['ds'], future['ds']]),
                    "yhat": pd.concat([historical['yhat'], future['yhat']]),
                    "Type": ["Historical"] * len(historical) + ["Forecast"] * len(future)
                })

                st.line_chart(
                    chart_data.pivot(index="ds", columns="Type", values="yhat")
                )

            except Exception as exc:
                st.error(f"Error loading data or training model: {exc}")
