"""Starter file for module M2."""

import streamlit as st
import hashlib

from api.blockchain_client import get_block, get_latest_block


#TINGS TO FIX: Make sure the proof of work works correctly



def render() -> None:
    """Render the M2 panel."""
    st.header("M2 - Block Header Analyzer")
    st.write("Use this module to inspect the fields of one block header.")

    # Add a button to fetch the latest block hash
    if st.button("Use latest block hash", key="m2_latest_hash"):
        with st.spinner("Fetching latest block hash..."):
            try:
                latest_block = get_latest_block()
                st.session_state["m2_hash"] = latest_block.get("id")
            except Exception as exc:
                st.error(f"Error fetching latest block: {exc}")

    block_hash = st.text_input(
        "Block hash",
        placeholder="Enter a block hash",
        key="m2_hash",
    )

    if st.button("Look up block", key="m2_lookup") and block_hash:
        with st.spinner("Fetching data..."):
            try:
                block = get_block(block_hash)
                st.session_state["m2_block"] = block  # Store block data in session state
            except Exception as exc:
                st.error(f"Error fetching block: {exc}")

    # Display block data if available
    block = st.session_state.get("m2_block")
    if block:
        st.subheader("Block header fields")
        header_fields = {
            "Hash": block.get("id"),
            "Height": block.get("height"),
            "Timestamp": block.get("timestamp"),
            "Nonce": block.get("nonce"),
            "Bits": block.get("bits"),
            "Merkle root": block.get("merkle_root"),
            "Previous block": block.get("previousblockhash"),
        }
        for label, value in header_fields.items():
            st.write(f"**{label}:** {value}")

        # Add proof-of-work verification button
        if st.button("Verify Proof of Work", key="m2_verify_pow"):
            with st.spinner("Verifying proof of work..."):
                try:
                    # Construct the block header
                    header = (
                        block.get("previousblockhash", "") +
                        block.get("merkle_root", "") +
                        str(block.get("timestamp", "")) +
                        str(block.get("bits", "")) +
                        str(block.get("nonce", ""))
                    ).encode("utf-8")

                    # Compute double SHA256
                    hash1 = hashlib.sha256(header).digest()
                    hash2 = hashlib.sha256(hash1).hexdigest()
                    
                    # Decode the 'bits' field into the full target value
                    try:
                        bits = int(block.get("bits"))  # Ensure 'bits' is treated as a decimal number
                        exponent = (bits >> 24) & 0xFF  # Extract the first byte (exponent)
                        coefficient = bits & 0xFFFFFF  # Extract the last three bytes (coefficient)
                        target = coefficient * (1 << (8 * (exponent - 3)))  # Compute the full target
                    except ValueError:
                        st.error("Invalid 'bits' field: Unable to decode target.")
                        return

                    # Verify if hash is below the target
                    is_valid = int(hash2, 16) < target

                    # Count leading zero bits
                    leading_zeros = len(hash2) - len(hash2.lstrip("0")) * 4

                    # Display results
                    st.write(f"**Computed Hash:** {hash2}")
                    st.write(f"**Is Valid Proof of Work:** {is_valid}")
                    st.write(f"**Leading Zero Bits:** {leading_zeros}")

                except Exception as exc:
                    st.error(f"Error during proof-of-work verification: {exc}")
    elif not block_hash:
        st.info("Enter a block hash and click Look up block.")
