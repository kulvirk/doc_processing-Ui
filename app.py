import streamlit as st
import tempfile
import os
import base64
import streamlit.components.v1 as components

from run_pipeline import run

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="Parts Extractor",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Parts Extractor — PDF → Excel")

# ======================================================
# HELPER: SCROLLABLE PDF VIEWER (WORKS EVERYWHERE)
# ======================================================

def pdf_viewer(file_bytes: bytes, height: int = 900):
    """Ultra-reliable PDF viewer (works on Cloud + Chrome + Edge)"""

    b64 = base64.b64encode(file_bytes).decode("utf-8")

    pdf_display = f"""
    <iframe
        src="data:application/pdf;base64,{b64}"
        width="100%"
        height="{height}"
        style="border:1px solid #ccc;"
        type="application/pdf">
    </iframe>
    """

    components.html(pdf_display, height=height + 20)

# ======================================================
# FILE UPLOAD
# ======================================================

uploaded_file = st.file_uploader(
    "Upload PDF Manual",
    type=["pdf"]
)

# ======================================================
# MAIN APP
# ======================================================

if uploaded_file is not None:

    file_bytes = uploaded_file.read()

    # Save uploaded PDF to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file_bytes)
        pdf_path = tmp.name

    st.success("PDF uploaded successfully")

    # ==================================================
    # LAYOUT
    # ==================================================

    left_col, right_col = st.columns(2)

    # ------------------ INPUT PDF ----------------------

    with left_col:
        st.subheader("📥 Input PDF Preview")
        pdf_viewer(file_bytes)

    # ==================================================
    # RUN EXTRACTION
    # ==================================================

    if st.button("▶ Run Extraction"):

        with st.spinner("Processing PDF..."):

            # Your pipeline must return:
            # output_xlsx_path, debug_pdf_path
            output_xlsx, debug_pdf = run(pdf_path=pdf_path)

        st.success("Extraction complete")

        # ==================================================
        # DOWNLOAD EXCEL
        # ==================================================

        if output_xlsx and os.path.exists(output_xlsx):
            with open(output_xlsx, "rb") as f:
                st.download_button(
                    label="⬇ Download Excel",
                    data=f,
                    file_name=os.path.basename(output_xlsx),
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        else:
            st.error("Excel output not found")

        # ==================================================
        # DEBUG PDF VIEW
        # ==================================================

        with right_col:
            st.subheader("🛠 Debug PDF Preview")

            if debug_pdf and os.path.exists(debug_pdf):

                with open(debug_pdf, "rb") as f:
                    debug_bytes = f.read()

                pdf_viewer(debug_bytes)

                st.download_button(
                    label="⬇ Download Debug PDF",
                    data=debug_bytes,
                    file_name=os.path.basename(debug_pdf),
                    mime="application/pdf"
                )

            else:
                st.info("No debug PDF generated")

    # ==================================================
    # CLEANUP TEMP FILE
    # ==================================================

    try:
        os.unlink(pdf_path)
    except Exception:
        pass

