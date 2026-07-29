import streamlit as st
import requests

st.sidebar.code(f"Running file from:\n{__file__}")

# Set page configuration
st.set_page_config(
    page_title="SGL Tech Enterprise AI Compliance Portal",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# SECRETS LOADING LOGIC
# -----------------------------------------------------------------------------
# Safely pull credentials from Streamlit's encrypted memory vault
SECRET_PAT = st.secrets.get("AIRTABLE_PAT", "")
SECRET_BASE = st.secrets.get("AIRTABLE_BASE_ID", "")
SECRET_TABLE = st.secrets.get("AIRTABLE_TABLE_NAME", "Compliance Logs")


# -----------------------------------------------------------------------------
# AIRTABLE INTEGRATION ENGINE
# -----------------------------------------------------------------------------
def save_to_airtable(token, base_id, table_name, file_name, client_name, score, risk, missing_clauses):
    """
    Sends the compliance scorecard metrics directly to an Airtable Base.
    """
    url = f"https://api.airtable.com/v0/{base_id}/{table_name}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Format missing clauses cleanly
    clauses_text = "\n".join([f"- {c}" for c in missing_clauses]) if missing_clauses else "None"

    # Clean data structure matched to your field types
    data = {
        "records": [
            {
                "fields": {
                    "Company Name": client_name,
                    "Compliance Score": f"{float(score) / 100:.2f}",  # Locked decimal format
                    "Risk Level": risk,
                    "Current IT Constraints": f"Deficits found:\n{clauses_text}"
                }
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            st.sidebar.success("✅ Record successfully saved to Airtable!")
        else:
            try:
                error_details = response.json()
                st.sidebar.error(f"❌ Airtable Error ({response.status_code}): {error_details}")
            except:
                st.sidebar.error(f"❌ Airtable Error ({response.status_code}): Page not found. Check ID capitalization.")
    except Exception as e:
        st.sidebar.error(f"🔌 Connection failed: {str(e)}")


# -----------------------------------------------------------------------------
# BACKEND COMPLIANCE ENGINE (SIMULATION)
# -----------------------------------------------------------------------------
def analyze_compliance_backend(uploaded_file) -> dict:
    file_name = uploaded_file.name.lower()

    if "policy" in file_name or "governance" in file_name:
        score = 94
        risk = "Low"
        delta = "Stable"
        missing_clauses = []
    elif "draft" in file_name or "test" in file_name:
        score = 72
        risk = "Medium"
        delta = "-5%"
        missing_clauses = [
            "Mandatory 30-day continuous logging and audit trail specifications.",
            "Explicit cross-border data transfer disclosure clauses.",
            "Human-in-the-loop (HITL) manual override procedures for automated decisions."
        ]
    else:
        score = 58
        risk = "High"
        delta = "-14%"
        missing_clauses = [
            "Data protection officer (DPO) contact and liability sign-off.",
            "Model bias monitoring and mitigation protocols.",
            "Encrypted data retention and automatic purge timelines.",
            "Third-party model API vulnerability patching SLAs."
        ]

    return {
        "client_name": client_name,
        "score": score,
        "risk": risk,
        "delta": delta,
        "missing_clauses": missing_clauses
    }


# -----------------------------------------------------------------------------
# STATE MANAGEMENT
# -----------------------------------------------------------------------------
if "doc_staged" not in st.session_state:
    st.session_state.doc_staged = False
if "staged_file_name" not in st.session_state:
    st.session_state.staged_file_name = None
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None

# Application Title
st.title("SGL Tech Enterprise AI Compliance Portal")

# Sidebar Configuration
with st.sidebar:
    st.header("Authentication")

    # Inputs automatically pull strings from your secrets configuration file
    airtable_pat = st.text_input("Airtable PAT", value=SECRET_PAT, type="password", help="Starts with 'pat.'")
    airtable_base = st.text_input("Airtable Base ID", value=SECRET_BASE, help="Starts with 'app.'")
    airtable_table = st.text_input("Table Name", value=SECRET_TABLE)

    st.divider()
    st.header("Document Ingestion")
    st.markdown("Upload an AI policy, framework, or model card.")

    uploaded_file = st.file_uploader(
        "Upload a document",
        type=["pdf", "docx"],
        help="Supported formats: PDF and DOCX only."
    )

    if uploaded_file is not None:
        if st.session_state.staged_file_name != uploaded_file.name:
            st.session_state.doc_staged = True
            st.session_state.staged_file_name = uploaded_file.name

            # Run analytics
            results = analyze_compliance_backend(uploaded_file)
            st.session_state.analysis_results = results

            # Trigger Airtable write if credentials exist
            if airtable_pat and airtable_base and airtable_table:
                save_to_airtable(
                    token=airtable_pat,
                    base_id=airtable_base,
                    table_name=airtable_table,
                    file_name=uploaded_file.name,
                    client_name=results["client_name"],
                    score=results["score"],
                    risk=results["risk"],
                    missing_clauses=results["missing_clauses"]
                )
            else:
                st.info("ℹ️ Fill out Airtable credentials above to auto-save results.")
    else:
        st.session_state.doc_staged = False
        st.session_state.staged_file_name = None
        st.session_state.analysis_results = None

    st.divider()
    st.subheader("System Status")
    if st.session_state.doc_staged:
        st.success(f"🟢 Staged: {st.session_state.staged_file_name}")
    else:
        st.warning("🔴 No document staged for processing.")

# Create Layout Tabs
tab1, tab2, tab3 = st.tabs([
    "Tab 1: Document Sandbox",
    "Tab 2: Use Case Compliance Scorecard",
    "Tab 3: Ethical Framework Standards"
])

# Content for Tab 1
with tab1:
    st.header("Document Sandbox Q&A")
    if st.session_state.doc_staged:
        st.info(
            f"Ready to analyze: **{st.session_state.staged_file_name}** (Client: {st.session_state.analysis_results['client_name']})")
        query = st.text_input("Ask a question about your staged document:")
        if query:
            st.write(f"Analyzing document context for: '{query}'...")
    else:
        st.info("Please upload a .pdf or .docx file via the sidebar to begin.")

# Content for Tab 2
with tab2:
    st.header("Use Case Compliance Scorecard")

    if st.session_state.doc_staged and st.session_state.analysis_results:
        results = st.session_state.analysis_results
        score = results["score"]
        risk = results["risk"]

        st.write(f"Showing compliance analytics for **{st.session_state.staged_file_name}**:")

        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Overall Compliance Score", value=f"{score}%",
                      delta="+2%" if score >= 85 else results["delta"])
        with col2:
            st.metric(label="Risk Exposure Flag", value=risk,
                      delta="↑ Stable" if risk == "Low" else "⚠️ Action Required",
                      delta_color="normal" if risk == "Low" else "inverse")

        st.divider()
        THRESHOLD = 85

        if score >= THRESHOLD:
            st.success(
                f"🎉 **Compliant Profile:** This document meets the organizational threshold of {THRESHOLD}%. No immediate interventions required.")
        else:
            st.error(
                f"🚨 **Non-Compliant Alert:** This document score ({score}%) has fallen below the mandatory threshold of {THRESHOLD}%.")
            st.subheader("📋 Recommended Actions for Remediation")
            st.markdown(
                "To achieve full organizational compliance, insert or update clauses addressing the following deficits:")

            for clause in results["missing_clauses"]:
                st.markdown(f"- [ ] **Missing Element:** {clause}")

            st.info(
                "💡 *Tip: After editing the source document to include these parameters, re-upload the revised file to update your scorecard metrics.*")
    else:
        st.info("Upload a document to generate its compliance scorecard.")

# Content for Tab 3
with tab3:
    st.header("About This Portal & Ethical Governance Standards")
    st.markdown("This portal tests whether client's current AI policy match existing ethical standards. To use this portal, clients must upload their existing internal AI policy documents, and this app will return a scorecard which describes their compliance score and risk level. The scorecard uses existing AI governance regulations like the NIST AI RMF Framework and the EU AI law. If the compliance score falls below a certain threshold, the portal will return steps on how to update their AI policy so that it complies with existing regulations. There is also a chatbot feature on this portal that clients can use to ask specific questions about their documents. The portal will record the clients compliance score and risk levels onto an AirTable CRM pipeline that tracks the clients.")
