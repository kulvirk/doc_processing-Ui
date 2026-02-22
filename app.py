import streamlit as st
import tempfile
import os
from io import BytesIO
from PyPDF2 import PdfReader

# ======================================================
# DEMO PIPELINE — Replace with your real run() function
# ======================================================

def run_pipeline(pdf_path, pages=None):
    """
    Replace this with your actual pipeline.
    For demo: returns same PDF as debug output.
    """
    return pdf_path


# ======================================================
# STREAMLIT CONFIG
# ======================================================

st.set_page_config(
    page_title="PDF Parts Extractor",
    page_icon="📄",
    layout="wide"
)

st.title("📄 PDF Viewer + Page Selection + Debug Viewer")

# ======================================================
# FILE UPLOAD
# ======================================================

uploaded_file = st.file_uploader(
    "Upload PDF Manual",
    type=["pdf"]
)

# ======================================================
# MAIN LOGIC
# ======================================================

if uploaded_file is not None:

    pdf_bytes = uploaded_file.getvalue()

    # Save to temp file for pipeline use
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    temp_file.write(pdf_bytes)
    temp_file.close()

    pdf_path = temp_file.name

    # --------------------------------------------------
    # GET PAGE COUNT
    # --------------------------------------------------
    reader = PdfReader(BytesIO(pdf_bytes))
    total_pages = len(reader.pages)

    st.success(f"Total Pages: {total_pages}")

    # --------------------------------------------------
    # PAGE SELECTION
    # --------------------------------------------------
    page_options = list(range(1, total_pages + 1))

    selected_pages = st.multiselect(
        "Select pages to process (random allowed)",
        options=page_options,
        default=st.session_state.get("pages_to_process", [])
    )

    if st.button("Save Page List"):
        st.session_state["pages_to_process"] = selected_pages
        st.success("Page list saved!")

    st.write("📌 Selected Pages:",
             st.session_state.get("pages_to_process", []))

    # --------------------------------------------------
    # LAYOUT — PDF VIEWER
    # --------------------------------------------------
    left, right = st.columns([2, 1])

    with left:
        st.subheader("Uploaded PDF")

        # ⭐ SAFE BUILT-IN VIEWER
        st.pdf(pdf_bytes, key="uploaded_pdf")  #st.pdf(pdf_bytes)

    with right:
        st.info("Use scroll / zoom controls inside viewer")

    # --------------------------------------------------
    # RUN PIPELINE
    # --------------------------------------------------
    st.divider()

    if st.button("🚀 Run Processing"):

        pages = st.session_state.get("pages_to_process", None)

        debug_pdf_path = run_pipeline(
            pdf_path=pdf_path,
            pages=pages
        )

        st.session_state["debug_pdf_path"] = debug_pdf_path

        st.success("Processing complete!")

# ======================================================
# SHOW DEBUG PDF AFTER EXECUTION
# ======================================================

if "debug_pdf_path" in st.session_state:

    st.divider()
    st.subheader("🛠 Debug PDF")

    with open(st.session_state["debug_pdf_path"], "rb") as f:
        debug_bytes = f.read()

    st.pdf(debug_bytes, key="debug_pdf") #st.pdf(debug_bytes)

    st.download_button(
        "⬇ Download Debug PDF",
        debug_bytes,
        file_name="debug_output.pdf"
    )

