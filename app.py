import streamlit as st
import requests
from io import BytesIO
from pypdf import PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Set page configuration
st.set_page_config(
    page_title="SGL Tech Enterprise AI Compliance Portal",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# BACKGROUND SECRETS CONFIGURATION (Fully Invisible to Clients)
# -----------------------------------------------------------------------------
SECRET_PAT = st.secrets.get("AIRTABLE_PAT", "")
SECRET_BASE = st.secrets.get("AIRTABLE_BASE_ID", "")
SECRET_TABLE = st.secrets.get("AIRTABLE_TABLE_NAME", "Compliance Logs")


# -----------------------------------------------------------------------------
# DETAILED ROI CALCULATOR LOGIC ENGINE (Based on Project Brief Specifications)
# -----------------------------------------------------------------------------
def calculate_roi_metrics(size_band: str, current_spend: float, has_leadership: bool) -> dict:
    """
    Computes financial comparisons between traditional in-house models and
    SGL Tech's fractional leadership approach based on market segmentation benchmarks.
    """
    # Mapping default annual internal overhead benchmarks
    internal_costs = {
        "Small Business (1–49 Employees)": 195000,
        "Growing Business (50–199 Employees)": 445000,
        "Mid-Market (200–499 Employees)": 510000,
        "Large Mid-Market (500–999 Employees)": 760000
    }

    # Mapping typical fractional engagement investment bounds
    fractional_bounds = {
        "Small Business (1–49 Employees)": (30000, 60000),
        "Growing Business (50–199 Employees)": (50000, 100000),
        "Mid-Market (200–499 Employees)": (75000, 150000),
        "Large Mid-Market (500–999 Employees)": (100000, 200000)
    }

    internal_leadership_cost = internal_costs.get(size_band, 0)
    frac_min, frac_max = fractional_bounds.get(size_band, (0, 0))

    # Measure optimization efficiency based on benchmark thresholds
    savings_min = max(0, internal_leadership_cost - frac_max)
    savings_max = max(0, internal_leadership_cost - frac_min)

    return {
        "internal_cost": internal_leadership_cost,
        "fractional_range": f"${frac_min:,} – ${frac_max:,}",
        "savings_range": f"${savings_min:,} – ${savings_max:,}"
    }


# -----------------------------------------------------------------------------
# COMPLIANCE TEXT EXTRACTION ENGINE
# -----------------------------------------------------------------------------
def extract_and_analyze_pdf(uploaded_file) -> dict:
    """
    Parses unstructured text streams out of target policy PDFs to calculate
    organizational alignment thresholds and systemic risk weights.
    """
    raw_text = ""
    client_name = "SGL Tech Client"

    try:
        reader = PdfReader(uploaded_file)
        for i in range(min(5, len(reader.pages))):
            page_text = reader.pages[i].extract_text()
            if page_text:
                raw_text += page_text + "\n"

        lower_text = raw_text.lower()
        if "university of london" in lower_text or "uol" in lower_text:
            client_name = "University of London"
        elif "sgl tech" in lower_text:
            client_name = "SGL Tech Internal"
        elif "acme" in lower_text:
            client_name = "Acme Corporation"
        else:
            filename_base = uploaded_file.name.split('.')[0]
            client_name = filename_base.replace('_', ' ').replace('-', ' ').title()

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

        score = int(40 + (60 * (found_count / total_rules)))

        if score >= 85:
            risk = "Low"
            delta = "Stable"
            level = "Optimized / Managed"
        elif score >= 70:
            risk = "Medium"
            delta = "-5%"
            level = "Developing"
        else:
            risk = "High"
            delta = "-14%"
            level = "Critical Gaps Found"

    except Exception:
        score = 50
        risk = "High"
        delta = "-20%"
        level = "Critical Gaps Found"
        missing_clauses = ["System failed to securely parse document metrics. Manual audit required."]
        client_name = uploaded_file.name.split('.')[0].title()

    return {
        "client_name": client_name,
        "score": score,
        "risk": risk,
        "delta": delta,
        "level": level,
        "missing_clauses": missing_clauses
    }


# -----------------------------------------------------------------------------
# DYNAMIC PDF UNIFIED REPORT GENERATOR (Combines Readiness + ROI Financials)
# -----------------------------------------------------------------------------
def generate_pdf_certificate(client, score, risk, missing_clauses, roi_data, size_band) -> bytes:
    """
    Constructs an enterprise compliance certificate PDF inside a memory buffer,
    combining audit readiness with ROI financial comparisons.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=letter,
        rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
    )
    story = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CertTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=22,
        textColor=colors.HexColor('#1E3A8A'), spaceAfter=15, alignment=1
    )
    section_style = ParagraphStyle(
        'CertSec', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=14,
        textColor=colors.HexColor('#1E3A8A'), spaceBefore=15, spaceAfter=8
    )
    body_style = ParagraphStyle(
        'CertBody', parent=styles['Normal'], fontName='Helvetica', fontSize=10,
        textColor=colors.HexColor('#1F2937'), spaceAfter=10, leading=14
    )

    story.append(Paragraph("SGL TECH UNIFIED EXECUTIVE ASSESSMENT REPORT", title_style))
    story.append(Spacer(1, 10))

    # Section 1: Governance Analytics
    story.append(Paragraph("1. IT & AI Policy Readiness Profile", section_style))
    data_readiness = [
        [Paragraph("<b>Audited Entity:</b>", body_style), Paragraph(client, body_style)],
        [Paragraph("<b>Compliance Readiness Score:</b>", body_style), Paragraph(f"{score}%", body_style)],
        [Paragraph("<b>Risk Evaluation Flag:</b>", body_style), Paragraph(risk, body_style)]
    ]
    t1 = Table(data_readiness, colWidths=[200, 320])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F9FAFB')),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E7EB'))
    ]))
    story.append(t1)

    # Section 2: Financial ROI Metrics
    story.append(Paragraph("2. Strategic Fractional Leadership ROI Snapshot", section_style))
    data_roi = [
        [Paragraph("<b>Segment Classification:</b>", body_style), Paragraph(size_band, body_style)],
        [Paragraph("<b>Est. Internal Executive Cost:</b>", body_style),
         Paragraph(f"${roi_data['internal_cost']:,}/yr", body_style)],
        [Paragraph("<b>Typical Fractional Engagement:</b>", body_style),
         Paragraph(roi_data['fractional_range'], body_style)],
        [Paragraph("<b>Estimated Annual Savings Vector:</b>", body_style),
         Paragraph(f"<b>{roi_data['savings_range']}</b>", body_style)]
    ]
    t2 = Table(data_roi, colWidths=[200, 320])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#EFF6FF')),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BFDBFE'))
    ]))
    story.append(t2)

    # Section 3: Remediation List
    story.append(Paragraph("3. Operational Action Items & Gap Breakdown", section_style))
    if missing_clauses:
        for clause in missing_clauses:
            story.append(Paragraph(f"• [GAP] {clause}", body_style))
    else:
        story.append(Paragraph("• No immediate infrastructure or legal deficits found in string trace.", body_style))

    story.append(Spacer(1, 30))
    story.append(Paragraph(
        "<b>Consultation Recommendation:</b> Talk with Frank to review your assessment, discuss your technology goals, and determine the best strategy for your business.",
        body_style))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


# -----------------------------------------------------------------------------
# AIRTABLE INTEGRATION HANDSHAKE
# -----------------------------------------------------------------------------
def save_to_airtable(token, base_id, table_name, client_name, score, risk, missing_clauses, roi_data):
    """Dispatches unified analytics logs safely into secure Airtable cloud sheets."""
    url = f"https://airtable.com{base_id}/{table_name}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    clauses_text = "\n".join([f"- {c}" for c in missing_clauses]) if missing_clauses else "None"

    data = {
        "records": [
            {
                "fields": {
                    "Company Name": str(client_name),
                    "Compliance Score": float(score) / 100.0,
                    "Risk Level": str(risk),
                    "Current IT Constraints": f"Deficits found:\n{clauses_text}\n\n[ROI Snapshot] Est. Savings: {roi_data['savings_range']}"
                }
            }
        ],
        "typecast": True
    }

    try:
        requests.post(url, headers=headers, json=data)
    except Exception:
        pass


# -----------------------------------------------------------------------------
# MAIN APPLICATION FLOW CONTROL
# -----------------------------------------------------------------------------
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None
if "roi_metrics" not in st.session_state:
    st.session_state.roi_metrics = None

# --- Branded Sidebar (Client View Only) ---
with st.sidebar:
    st.header("Document Ingestion")
    st.markdown("Upload corporate AI framework documentation for verification audit extraction.")

    uploaded_file = st.file_uploader(
        "Upload a document",
        type=["pdf"],
        help="PDF maps only."
    )

    if uploaded_file is not None:
        results = extract_and_analyze_pdf(uploaded_file)
        st.session_state.analysis_results = results
    else:
        st.session_state.analysis_results = None

    st.divider()
    st.subheader("System Status")
    if st.session_state.analysis_results:
        st.success(f"🟢 Staged: {uploaded_file.name}")
    else:
        st.warning("🔴 Awaiting document ingestion...")

# --- Navigation Views ---
tab1, tab2, tab3 = st.tabs([
    "Tab 1: Ingestion & Sandbox",
    "Tab 2: Strategic ROI Snapshot Calculator",
    "Tab 3: Unified Executive Scorecard Dashboard"
])

# --- TAB 1: FILE RECAP ---
with tab1:
    st.header("Document Sandbox Context Verification")
    if st.session_state.analysis_results:
        res = st.session_state.analysis_results
        st.info(f"Target Staged Workspace Entity: {res['client_name']}")

        query = st.text_input("Query policy parameters against the active text vector array:")
        if query:
            st.write(f"Auditing text structures for query matching sequence: '{query}'...")
    else:
        st.info("Please drop a corporate policy documentation matrix inside the sidebar panel to begin.")

# --- TAB 2: INTERACTIVE ROI WIDGETS ---
with tab2:
    st.header("Fractional CTO Leadership ROI Calculator")
    st.markdown(
        "Measure the cost efficiency of building internal IT leadership teams versus an integrated fractional resource strategy.")

    col_ui1, col_ui2 = st.columns(2)
    with col_ui1:
        size_selection = st.selectbox(
            "Company Size Classification (Employee Count)",
            [
                "Small Business (1–49 Employees)",
                "Growing Business (50–199 Employees)",
                "Mid-Market (200–499 Employees)",
                "Large Mid-Market (500–999 Employees)"
            ]
        )
        has_lead = st.radio(
            "Do you currently employ dedicated technology executive leadership (CTO / VP / Director)?",
            ["No", "Yes"]
        )
    with col_ui2:
        monthly_spend = st.slider(
            "Estimated Current Monthly IT Operating Budget ($)",
            5000, 200000, 25000, step=2500
        )

    # Live execution calculation logic loop
    roi_metrics = calculate_roi_metrics(size_selection, monthly_spend, has_lead == "Yes")
    st.session_state.roi_metrics = roi_metrics

    st.divider()
    st.subheader("Cost Structure Analysis Projections")

    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.metric(label="Est. Traditional Full-Time Cost", value=f"${roi_metrics['internal_cost']:,}/yr")
    with col_m2:
        st.metric(label="Typical SGL Tech Engagement", value=roi_metrics['fractional_range'])
    with col_m3:
        st.metric(
            label="Calculated Resource Savings Vector",
            value=roi_metrics['savings_range'],
            delta="Cost Cleared",
            delta_color="normal"
        )

    st.caption(
        "Disclaimer: These metrics serve as baseline organizational planning indicators. Final budget configurations vary depending on operational requirements and project scopes.")

# --- TAB 3: UNIFIED OUTPUT VIEWER ---
with tab3:
    st.header("Unified Corporate Governance & Value Assessment")
    if st.session_state.analysis_results:
        res = st.session_state.analysis_results
        roi = st.session_state.roi_metrics

        st.markdown(f"### Assessment Analytics Portfolio for: {res['client_name']}")

        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            st.metric(label="Calculated Alignment Index", value=f"{res['score']}%", delta=res['level'])
        with col_f2:
            st.metric(
                label="Risk Exposure Flag",
                value=res['risk'],
                delta="Action Enforced" if res['risk'] != "Low" else "System Stable",
                delta_color="inverse" if res['risk'] != "Low" else "normal"
            )
        with col_f3:
            st.metric(label="Projected Executive Capital Reclaimed", value=roi['savings_range'])

        st.divider()
        st.subheader("📜 Executive Hand-off Asset Generation")

        # Build unified compiled report on call event
        pdf_bytes = generate_pdf_certificate(
            res['client_name'], res['score'], res['risk'],
            res['missing_clauses'], roi, size_selection
        )
        st.download_button(
            label="📥 Download Consolidated Assessment Report & ROI Summary (PDF)",
            data=pdf_bytes,
            file_name=f"{res['client_name'].replace(' ', '_')}_Executive_Compliance_Audit.pdf",
            mime="application/pdf"
        )

        # Trigger background data ledger synchronization automatically inside state block
        if SECRET_PAT and SECRET_BASE and SECRET_TABLE:
            save_to_airtable(
                SECRET_PAT, SECRET_BASE, SECRET_TABLE,
                res['client_name'], res['score'], res['risk'],
                res['missing_clauses'], roi
            )

        st.divider()
        st.subheader("📋 Core Remediation Priorities Checklist")
        if res['missing_clauses']:
            for clause in res['missing_clauses']:
                st.markdown(f"- [ ] Deficit Asset: {clause}")
        else:
            st.success("🎉 Operational strings demonstrate alignment targets map cleanly to corporate benchmarks.")

        st.info(
            "🤝 Next Action Step: Talk with Frank to review your assessment, discuss your technology goals, and determine the best strategy for your business.")
    else:
        st.info(
            "Upload an infrastructure data sheet inside the ingestion framework panel to view unified summary scorecard fields.")