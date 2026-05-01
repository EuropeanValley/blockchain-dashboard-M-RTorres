"""Starter file for module M2."""

import streamlit as st
import hashlib
import struct

from api.blockchain_client import get_block, get_latest_block


#TINGS TO FIX: Make sure the proof of work works correctly



def render() -> None:
    """Render the M2 panel."""
    st.header("M2 - Block Header Analyzer")
    st.write("Use this module to inspect the fields of one block header and verify the Proof of Work step by step.")

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

    if (st.button("Look up block", key="m2_lookup") or True) and block_hash:
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
            "Version": block.get("version"),
            "Previous Hash": block.get("previousblockhash"),
            "Merkle Root": block.get("merkle_root"),
            "Timestamp": block.get("timestamp"),
            "Bits": block.get("bits"),
            "Nonce": block.get("nonce"),
        }
        for label, value in header_fields.items():
            st.write(f"**{label}:** {value}")

        # Add proof-of-work verification button
        if st.button("Verify Proof of Work", key="m2_verify_pow") or True:
            with st.spinner("Verifying proof of work step by step..."):
                try:
                    # Step 1: Construct the 80-byte block header with correct byte order
                    version = struct.pack("<I", int(block.get("version")))  # Little-endian
                    prev_hash = bytes.fromhex(block.get("previousblockhash"))[::-1]  # Reverse byte order
                    merkle_root = bytes.fromhex(block.get("merkle_root"))[::-1]  # Reverse byte order
                    timestamp = struct.pack("<I", int(block.get("timestamp")))  # Little-endian
                    bits = struct.pack("<I", int(block.get("bits")))  # Little-endian
                    nonce = struct.pack("<I", int(block.get("nonce")))  # Little-endian

                    header = version + prev_hash + merkle_root + timestamp + bits + nonce

                    # Color-coded legend
                    st.write("### Step 1: Constructed 80-byte Block Header")
                    st.markdown(
                        """
                        <style>
                        .legend { display: flex; gap: 10px; margin-bottom: 10px; }
                        .legend-item { display: flex; align-items: center; gap: 5px; }
                        .color-box { width: 15px; height: 15px; display: inline-block; }
                        .version { background-color: #FFDDC1; color: black; }
                        .prev-hash { background-color: #FFABAB; color: black; }
                        .merkle-root { background-color: #FFC3A0; color: black; }
                        .timestamp { background-color: #D5AAFF; color: black; }
                        .bits { background-color: #85E3FF; color: black; }
                        .nonce { background-color: #B9FBC0; color: black; }
                        </style>
                        <div class="legend">
                            <div class="legend-item"><span class="color-box version"></span>Version</div>
                            <div class="legend-item"><span class="color-box prev-hash"></span>Previous Hash</div>
                            <div class="legend-item"><span class="color-box merkle-root"></span>Merkle Root</div>
                            <div class="legend-item"><span class="color-box timestamp"></span>Timestamp</div>
                            <div class="legend-item"><span class="color-box bits"></span>Bits</div>
                            <div class="legend-item"><span class="color-box nonce"></span>Nonce</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # Highlighted block header
                    highlighted_header = (
                        f"<span class='version'>{version.hex()}</span>"
                        f"<span class='prev-hash'>{prev_hash.hex()}</span>"
                        f"<span class='merkle-root'>{merkle_root.hex()}</span>"
                        f"<span class='timestamp'>{timestamp.hex()}</span>"
                        f"<span class='bits'>{bits.hex()}</span>"
                        f"<span class='nonce'>{nonce.hex()}</span>"
                    )
                    st.markdown(f"<code>{highlighted_header}</code>", unsafe_allow_html=True)

                    # Step 2: Compute double SHA256
                    hash1 = hashlib.sha256(header).digest()
                    hash2 = hashlib.sha256(hash1).digest()[::-1].hex()  # Reverse byte order for final hash
                    st.write("### Step 2: Double SHA256 Hash")
                    st.write(f"Hash 1: {hash1.hex()}")
                    st.write(f"Hash 2: {hash2}")

                    # Step 3: Decode 'bits' field into target
                    bits_int = int(block.get("bits"))
                    exponent = (bits_int >> 24) & 0xFF
                    coefficient = bits_int & 0xFFFFFF
                    target = coefficient * (1 << (8 * (exponent - 3)))
                    st.write("### Step 3: Decoded Target")
                    st.write(f"Target: {target:#x}")

                    # Step 4: Compare hash with target
                    hash_int = int(hash2, 16)
                    is_valid = hash_int < target
                    st.write("### Step 4: Proof of Work Verification")
                    st.write(f"Hash Int: {hash_int:#x}")
                    st.write(f"Is Valid Proof of Work: {is_valid}")

                    # Step 5: Count leading zero bits
                    leading_zeros = 0
                    for byte in bytes.fromhex(hash2):
                        if byte == 0:
                            leading_zeros += 8
                        else:
                            leading_zeros += bin(byte).count("0") - 1
                            break
                    st.write("### Step 5: Leading Zero Bits")
                    st.write(f"Leading Zero Bits: {leading_zeros}")

                except Exception as exc:
                    st.error(f"Error during proof-of-work verification: {exc}")
    elif not block_hash:
        st.info("Enter a block hash and click Look up block.")
