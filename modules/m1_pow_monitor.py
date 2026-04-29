"""Starter file for module M1."""

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from api.blockchain_client import get_time_between_blocks, get_block_history



#THINGS TO FIX: TIME BETWEEN BLOCKS DONT WORK

def render() -> None:
    """Render the M1 panel."""
    st.header("M1 - Proof of Work Monitor")

    # Current Difficulty and Leading-Zero Threshold
    st.subheader("Current Difficulty and Leading-Zero Threshold")
    if st.button("Fetch Current Difficulty", key="m1_difficulty"):
        with st.spinner("Fetching difficulty data..."):
            try:
                difficulty_data = get_block_history(time_period="1m")
                current_difficulty = difficulty_data.get("currentDifficulty")
                if current_difficulty:
                    st.success(f"Current Difficulty: {current_difficulty}")
                    leading_zero_threshold = 2 ** 256 / current_difficulty
                    st.success(f"Leading-Zero Threshold: {leading_zero_threshold:.2e}")
                else:
                    st.warning("Could not fetch current difficulty.")
            except Exception as exc:
                st.error(f"Error fetching difficulty data: {exc}")

    # Time Between Last N Blocks
    st.subheader("Time Between Last N Blocks")
    st.write("Enter the number of blocks and the starting block height to calculate the time differences between blocks.")
    n_blocks = st.number_input("Enter the number of blocks:", min_value=2, max_value=10, value=5)
    #min_height = st.number_input("Enter the minimum block height:", min_value=0, value=0)
    if st.button("Fetch Time Between Blocks", key="m1_time_between_blocks"):
        with st.spinner("Fetching block data..."):
            try:
                time_data = get_time_between_blocks(amount_of_blocks=n_blocks)#(min_height=min_height, max_height=min_height + n_blocks - 1)
                if time_data:
                    st.success("Time differences fetched successfully.")

                    # Convert to DataFrame for plotting
                    df = pd.DataFrame(time_data)
                    st.write(df)

                    # Plot the distribution
                    fig, ax = plt.subplots()
                    ax.hist(df["time_difference"], bins=10, alpha=0.7, color="blue")
                    ax.set_title("Time Between Blocks Distribution")
                    ax.set_xlabel("Time Difference (seconds)")
                    ax.set_ylabel("Frequency")
                    st.pyplot(fig)
                else:
                    st.warning("No data available for the specified range.")
            except Exception as exc:
                st.error(f"Error fetching block data: {exc}")

    # Estimated Current Network Hash Rate
    st.subheader("Estimated Current Network Hash Rate")
    if st.button("Fetch Current Network Hash Rate", key="m1_hashrate"):
        with st.spinner("Fetching network hash rate..."):
            try:
                difficulty_data = get_block_history(time_period="1m")
                current_hashrate = difficulty_data.get("currentHashrate")
                if current_hashrate:
                    st.success(f"Current Network Hash Rate: {current_hashrate:.2e} H/s")
                else:
                    st.warning("Could not fetch current network hash rate.")
            except Exception as exc:
                st.error(f"Error fetching network hash rate: {exc}")