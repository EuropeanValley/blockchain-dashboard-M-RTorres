"""Starter file for module M3."""

import pandas as pd
import plotly.express as px
import streamlit as st

from api.blockchain_client import get_block_history


def render() -> None:
    """Render the M3 panel."""
    st.header("M3 - Difficulty History")
    st.write("Use this module to plot the evolution of Bitcoin difficulty and hashrate over a specified time period.")

    # Allow the user to select a time period
    time_period = st.selectbox(
        "Select time period",
        options=["1m", "3m", "6m", "1y", "2y", "3y", "All"],
        index=0,
        key="m3_time_period"
    )

    if st.button("Load difficulty and hashrate chart", key="m3_load") or True:
        with st.spinner("Fetching data..."):
            try:
                # Fetch data for the selected time period
                data = get_block_history(time_period)

                # Extract relevant data
                #hashrates = data.get("hashrates", [])
                difficulties = data.get("difficulty", [])
                current_hashrate = data.get("currentHashrate")
                current_difficulty = data.get("currentDifficulty")

                if not difficulties:#not hashrates or 
                    st.warning("No data available for the selected time period.")
                    return


                #st.write(f"Dificulty list: {difficulties}")

                # Extract relevant data from difficulties
                timestamps = [entry["time"] for entry in difficulties]
                difficulty_values = [entry["difficulty"] for entry in difficulties]

                ## Ensure hashrates and difficulties are of the same length
                #min_length = min(len(hashrates), len(difficulty_values))
                #hashrates = hashrates[:min_length]
                #timestamps = timestamps[:min_length]
                #difficulty_values = difficulty_values[:min_length]

                # Create a DataFrame for plotting
                df = pd.DataFrame({
                    "Timestamp": pd.to_datetime(timestamps, unit="s"),
                    #"Hashrate": hashrates,
                    "Difficulty": difficulty_values,
                })

                # Plot difficulty and hashrate over time
                fig = px.line(df, x="Timestamp", y="Difficulty", title="Bitcoin Mining Difficulty")
                fig.add_scatter(x=df["Timestamp"], y=df["Difficulty"], mode="lines", name="Difficulty")

                # Display current values
                #st.metric("Current Hashrate", f"{current_hashrate} EH/s")
                #st.metric("Current Difficulty", f"{current_difficulty}")

                st.plotly_chart(fig, use_container_width=True)
            except Exception as exc:
                st.error(f"Error loading chart: {exc}")
    else:
        st.info("Click Load difficulty and hashrate chart to display the chart.")
