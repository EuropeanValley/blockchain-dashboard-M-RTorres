"""Starter file for module M3."""

import pandas as pd
import plotly.express as px
import streamlit as st

from api.blockchain_client import get_block_history, get_time_between_blocks


def render() -> None:
    """Render the M3 panel."""
    st.header("M3 - Difficulty History")
    st.write("Use this module to plot the evolution of Bitcoin difficulty over the last several adjustment periods.")

    n_periods = st.slider("Number of adjustment periods", min_value=1, max_value=10, value=3, key="m3_periods")

    if st.button("Load difficulty chart", key="m3_load"):
        with st.spinner("Fetching data..."):
            try:
                # Fetch data for the specified number of adjustment periods
                n_blocks = n_periods * 2016
                block_data = get_time_between_blocks(n_blocks)

                # Process data to calculate difficulty adjustments and block time ratios
                adjustment_events = []
                difficulties = []
                block_times = []
                timestamps = []

                for i in range(0, len(block_data), 2016):
                    period_blocks = block_data[i:i + 2016]
                    if len(period_blocks) < 2016:
                        break

                    # Calculate average block time for the period
                    total_time = sum(b["time_difference"] for b in period_blocks)
                    avg_block_time = total_time / 2016
                    block_times.append(avg_block_time)

                    # Extract difficulty and timestamp for the adjustment event
                    adjustment_events.append(period_blocks[-1]["height"])
                    difficulties.append(period_blocks[-1]["difficulty"])
                    timestamps.append(period_blocks[-1]["timestamp"])

                # Create a DataFrame for plotting
                df = pd.DataFrame({
                    "Timestamp": pd.to_datetime(timestamps, unit="s"),
                    "Difficulty": difficulties,
                    "Block Time Ratio": [bt / 600 for bt in block_times],
                })

                # Plot difficulty over time
                fig = px.line(df, x="Timestamp", y="Difficulty", title="Bitcoin Mining Difficulty")

                # Add markers for adjustment events
                fig.add_scatter(x=df["Timestamp"], y=df["Difficulty"], mode="markers", name="Adjustment Events")

                # Plot block time ratio
                fig.add_scatter(x=df["Timestamp"], y=df["Block Time Ratio"], mode="lines+markers", name="Block Time Ratio")

                st.plotly_chart(fig, use_container_width=True)
            except Exception as exc:
                st.error(f"Error loading chart: {exc}")
    else:
        st.info("Click Load difficulty chart to display the chart.")
