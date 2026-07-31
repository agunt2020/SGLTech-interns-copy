import requests
from io import BytesIO
import streamlit as st
from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="SGL Tech Enterprise AI Compliance Portal",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# SECTIONS & CLOUD INTEGRATION SECRETS
# -----------------------------------------------------------------------------
SECRET_PAT = st.secrets.get("AIRTABLE_PAT", "")
SECRET_BASE = st.secrets.get("AIRTABLE_BASE_ID", "")
SECRET_TABLE = st.secrets.get("AIRTABLE_TABLE_NAME", "Compliance Logs")


# -----------------------------------------------------------------------------
# COMPLIANCE TEXT EXTRACTION ENGINE
# -----------------------------------------------------------------------------
def extract_and_analyze_pdf(uploaded_file) -> dict:
    """Parses live PDF text streams to extract client info and score compliance."""
    raw_text = ""
    client_name = "SGL Tech Client"

    try:
        reader = PdfReader(uploaded_file)
        # Scan the first few pages to extract text content
        for i in range(min(5, len(reader.pages))):
            page_text = reader.pages[i].extract_text()
            if page_text:
                raw_text += page_text + "\n"

        # 1. Client Identity Parsing Logic
        lower_text = raw_text.lower()
        if "university of london" in lower_text or "uol" in lower_text:
            client_name = "University of London"
        elif "sgl tech" in lower_text:
            client_name = "SGL Tech Internal"
        elif "acme" in lower_text:
            client_name = "Acme Corporation"
        else:
            # Fallback: Clean up filename if no match is found inside text
            filename_base = uploaded_file.name.split('.')[0]
            client_name = filename_base.replace('_', ' ').replace('-', ' ').title()

        # 2. Compliance Scoring Audit Engine
        required_guardrails = {
            "Mandatory continuous audit trail specifications": [
                "audit trail", "logging", "continuous logging"
            ],
            "Explicit cross-border data transfer disclosure clauses": [
                "cross-border", "data transfer", "international transfer"
            ],
            "Human-in-the-loop (HITL) manual override procedures": [
                "human-in-the-loop", "hitl", "manual override"
            ],
            "Data protection officer (DPO) contact and liability sign-off": [
                "dpo", "data protection officer", "liability"
            ],
            "Model bias monitoring and mitigation protocols": [
                "bias monitoring", "mitigation", "algorithmic bias"
            ],
            "Encrypted data retention and automatic purge timelines": [
                "retention timeline", "purge", "encrypted retention"
            ],
            "Third-party model API vulnerability patching SLAs": [
                "vulnerability patching", "sla", "third-party model"
            ]
        }

        missing_clauses = []
        found_count = 0
        total_rules = len(required_guardrails)

        for clause, keywords in required_guardrails.items():
            if any(kw in lower_text for kw in keywords):
                found_count += 1
            else:
                missing_clauses.append(clause)

        # Calculate score proportional to passed guardrails (scaled 40% to 100%)
        score = int(40 + (60 * (found_count / total_rules)))

        if score >= 85:
            risk = "Low"
            delta = "Stable"
        elif score >= 70:
            risk = "Medium"
            delta = "-5%"
        else:
            risk = "High"
            delta = "-14%"

    except Exception:
        # Secure fallback configuration if file extraction fails
        score = 50
        risk = "High"
        delta = "-20%"
        missing_clauses = ["System failed to securely parse document metrics. Manual audit required."]
        client_name = uploaded_file.name.split('.')[0].title()

    return {
        "client_name": client_name,
        "score": score,
        "risk": risk,
        "delta": delta,
        "missing_clauses": missing_clauses
    }


# -----------------------------------------------------------------------------
# DYNAMIC PDF CERTIFICATE GENERATOR
# -----------------------------------------------------------------------------
def generate_pdf_certificate(client, score, risk, missing_clauses) -> bytes:
    """Constructs an enterprise compliance certificate PDF inside a memory buffer."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=letter,
        rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
    )
    story = []
    styles = getSampleStyleSheet()

    # Custom Brand Aesthetics
    title_style = ParagraphStyle(
        'CertTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=24,
        textColor=colors.HexColor('#1E3A8A'), spaceAfter=15, alignment=1
    )
    subtitle_style = ParagraphStyle(
        'CertSub', parent=styles['Normal'], fontName='Helvetica', fontSize=12,
        textColor=colors.HexColor('#4B5563'), spaceAfter=30, alignment=1
    )
    body_style = ParagraphStyle(
        'CertBody', parent=styles['Normal'], fontName='Helvetica', fontSize=11,
        textColor=colors.HexColor('#1F2937'), spaceAfter=12, leading=16
    )

    # Header Elements
    story.append(Paragraph("SGL TECH ENTERPRISE COMPLIANCE AUDIT CERTIFICATE", title_style))
    story.append(Paragraph("Official Governance Statement for Corporate AI Alignment Verification", subtitle_style))
    story.append(Spacer(1, 15))

    # Layout Data Table
    status_text = "APPROVED" if score >= 85 else "REMEDIATION REQUIRED"
    data = [
        [Paragraph("<b>Audited Entity:</b>", body_style), Paragraph(client, body_style)],
        [Paragraph("<b>Overall Compliance Score:</b>", body_style), Paragraph(f"{score}%", body_style)],
        [Paragraph("<b>Risk Profile Evaluation:</b>", body_style), Paragraph(risk, body_style)],
        [Paragraph("<b>Status Classification:</b>", body_style), Paragraph(status_text, body_style)]
    ]

    t = Table(data, colWidths=[200, 300])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F3F4F6')),
        ('PADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D1D5DB')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t)
    story.append(Spacer(1, 25))

    # Gap Listing Breakdown
    story.append(Paragraph("<b>Identified Operational Constraints & Gaps:</b>", body_style))
    if missing_clauses:
        for clause in missing_clauses:
            story.append(Paragraph(f"• [MIA] {clause}", body_style))
    else:
        story.append(
            Paragraph("• None. This document maps completely to baseline corporate ethical standards.", body_style))

    story.append(Spacer(1, 40))
    notice_text = (
        "<font color='#6B7280'><i>Notice: This credential verifies evaluation logs recorded "
        "on the automated SGL Tech Compliance cloud ledger network. Certification parameters "
        "are valid relative to systemic thresholds active at runtime.</i></font>"
    )
    story.append(Paragraph(notice_text, body_style))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


# -----------------------------------------------------------------------------
# AIRTABLE INTEGRATION HANDSHAKE
# -----------------------------------------------------------------------------
def save_to_airtable(token, base_id, table_name, file_name, client_name, score, risk, missing_clauses):
    url = "https://airtable.com"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    clauses_text = "\n".join([f"- {c}" for c in missing_clauses]) if missing_clauses else "None"

    # Clean payload mapped strictly to your populated parameters
    data = {
        "records": [
            {
                "fields": {
                    "Company Name": str(client_name),
                    "Compliance Score": float(score) / 100.0,  # Sends decimal matching percentage logic
                    "Risk Level": str(risk),
                    "Current IT Constraints": f"Deficits found:\n{clauses_text}"
                }
            }
        ],
        "typecast": True  # 🚀 CRITICAL FIX: Tells Airtable to auto-format select options and data values
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            st.sidebar.success("✅ Log synchronized to Airtable!")
        else:
            # Clean logging block showing exactly which column is throwing a naming/formatting error
            st.sidebar.error(f"❌ Ledger Sync Error ({response.status_code}): {response.text}")
    except Exception as e:
        st.sidebar.error(f"🔌 Network ledger handshake interrupted: {str(e)}")


# -----------------------------------------------------------------------------
# CORE MAIN APPLICATION FLOW
# -----------------------------------------------------------------------------
def main():
    # Initialize Persistent Session State Contexts
    if "doc_staged" not in st.session_state:
        st.session_state.doc_staged = False
    if "staged_file_name" not in st.session_state:
        st.session_state.staged_file_name = None
    if "analysis_results" not in st.session_state:
        st.session_state.analysis_results = None

    # Main Application Banner UI Element
    st.title("SGL Tech Enterprise AI Compliance Portal")

    # -------------------------------------------------------------------------
    # SIDEBAR CONTROL WORKFLOW
    # -------------------------------------------------------------------------
    with st.sidebar:
        st.header("Document Ingestion")
        st.markdown("Upload corporate AI framework files or policy guidelines for audit validation.")

        uploaded_file = st.file_uploader(
            "Upload a document",
            type=["pdf"],
            help="Supported formats: Systemic PDF structures only."
        )

        if uploaded_file is not None:
            if st.session_state.staged_file_name != uploaded_file.name:
                st.session_state.doc_staged = True
                st.session_state.staged_file_name = uploaded_file.name

                # Run Real Audit Parsing Logic
                results = extract_and_analyze_pdf(uploaded_file)
                st.session_state.analysis_results = results

                # Background Cloud Synchronization Handshake
                if SECRET_PAT and SECRET_BASE and SECRET_TABLE:
                    save_to_airtable(
                        token=SECRET_PAT,
                        base_id=SECRET_BASE,
                        table_name=SECRET_TABLE,
                        file_name=uploaded_file.name,
                        client_name=results["client_name"],
                        score=results["score"],
                        risk=results["risk"],
                        missing_clauses=results["missing_clauses"]
                    )
        else:
            st.session_state.doc_staged = False
            st.session_state.staged_file_name = None
            st.session_state.analysis_results = None

        st.divider()
        st.subheader("System Status")
        if st.session_state.doc_staged:
            st.success(f"🟢 Staged: {st.session_state.staged_file_name}")
        else:
            st.warning("🔴 Awaiting document ingestion...")

    # -------------------------------------------------------------------------
    # CENTRAL LAYOUT DASHBOARD TABS
    # -------------------------------------------------------------------------
    tab1, tab2, tab3 = st.tabs([
        "Tab 1: Document Sandbox",
        "Tab 2: Use Case Compliance Scorecard",
        "Tab 3: Ethical Framework Standards"
    ])

    # --- Tab 1: Document Sandbox ---
    with tab1:
        st.header("Document Sandbox Q&A")
        if st.session_state.doc_staged:
            st.info(
                f"Staged System Focus: {st.session_state.staged_file_name} | Entity: {st.session_state.analysis_results['client_name']}")
            query = st.text_input("Query specific processing behaviors or guardrail alignments:")
            if query:
                st.write(f"Analyzing text array contexts for query string: '{query}'...")
        else:
            st.info("Ingest a policy documentation layout in the sidebar workflow window to initiate.")

    # --- Tab 2: Use Case Compliance Scorecard ---
    with tab2:
        st.header("Use Case Compliance Scorecard")
        if st.session_state.doc_staged and st.session_state.analysis_results:
            results = st.session_state.analysis_results
            score = results["score"]
            risk = results["risk"]
            client = results["client_name"]

            st.write(f"Displaying extracted structural analysis parameters for {client}:")

            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    label="Calculated Alignment Score",
                    value=f"{score}%",
                    delta="Target Met" if score >= 85 else results["delta"]
                )
            with col2:
                st.metric(
                    label="Assigned Risk Rating Profile",
                    value=risk,
                    delta="Stable Systemic Track" if risk == "Low" else "Remediation Enforced",
                    delta_color="normal" if risk == "Low" else "inverse"
                )

            st.divider()

            # Action Step: Dynamic PDF Certificate Generation Box
            st.subheader("📜 Compliance Verification Output")
            pdf_data = generate_pdf_certificate(client, score, risk, results["missing_clauses"])
            st.download_button(
                label=f"📥 Download Official Compliance Certificate ({client})",
                data=pdf_data,
                file_name=f"{client.replace(' ', '_')}_AI_Compliance_Certificate.pdf",
                mime="application/pdf"
            )

            st.divider()

            THRESHOLD = 85
            if score >= THRESHOLD:
                st.success(
                    "🎉 Compliant Profile Status: Evaluated data strings map cleanly to systemic governance criteria.")
            else:
                st.error(
                    f"🚨 Non-Compliance Violation Warning: Evaluated architecture sits below the {THRESHOLD}% clearance target.")

            st.subheader("📋 Targeted Remediations Required")
            for clause in results["missing_clauses"]:
                st.markdown(f"- [ ] Deficit Found: {clause}")
        else:
            st.info("Ingest an official asset overview mapping file to calculate automated verification indices.")

    # --- Tab 3: Ethical Framework Standards ---
    with tab3:
        st.header("⚖️ Platform Core Architecture & Ethical Governance Standards")
        st.markdown(
            "This platform acts as an automated governance gatekeeper designed to audit corporate AI policies...")
        st.divider()

        col_step1, col_step2, col_step3 = st.columns(3)
        with col_step1:
            st.info(
                "📂 1. Document Ingestion\n\nAccepts unstructured enterprise governance documents via raw .pdf data structures.")
        with col_step2:
            st.warning(
                "🧠 2. Compliance Processing\n\nEvaluates systemic text strings using signature keywords to audit operational maturity.")
        with col_step3:
            st.success(
                "📊 3. Cloud Ledger Synchronization\n\nPushes evaluated scoring profiles, risk vectors, and gap listings instantly to external Airtable infrastructure via REST API payloads.")


if __name__ == "__main__":
    main()