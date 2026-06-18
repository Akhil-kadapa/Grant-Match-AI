from dotenv import load_dotenv
import google.generativeai as genai
import os
from pypdf import PdfReader
import streamlit as st
import pandas as pd
import sqlite3
import json
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# -------------------------
# Load Environment Variables
# -------------------------

load_dotenv()

# -------------------------
# Embedding Model
# -------------------------

@st.cache_resource
def load_embedding_model():
    return SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

embedding_model = load_embedding_model()

# -------------------------
# Gemini Model
# -------------------------

genai.configure(
    api_key=os.getenv("GOOGLE_API_KEY")
)

gemini_model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

# -------------------------
# Load Filters
# -------------------------
@st.cache_data
def load_filters():

    conn = sqlite3.connect("grants.db")

    categories = pd.read_sql(
        "SELECT DISTINCT category FROM grants_new",
        conn
    )["category"].tolist()

    organizations = pd.read_sql(
        "SELECT DISTINCT organization FROM grants_new",
        conn
    )["organization"].tolist()

    eligibilities = pd.read_sql(
        "SELECT DISTINCT eligibility FROM grants_new",
        conn
    )["eligibility"].tolist()

    conn.close()

    return (
        ["All"] + sorted(categories),
        ["All"] + sorted(organizations),
        ["All"] + sorted(eligibilities)
    )

# -------------------------
# Search Grants
# -------------------------

def search_grants(
    min_funding,
    category,
    organization,
    eligibility
):

    conn = sqlite3.connect("grants.db")

    query = """
    SELECT *
    FROM grants_new
    WHERE funding_amount >= ?
    """

    params = [min_funding]

    if category != "All":
        query += " AND category = ?"
        params.append(category)

    if organization != "All":
        query += " AND organization = ?"
        params.append(organization)

    if eligibility != "All":
        query += " AND eligibility = ?"
        params.append(eligibility)

    df = pd.read_sql(
        query,
        conn,
        params=params
    )

    conn.close()

    return df

# -------------------------
# Calculate Matches
# -------------------------

def calculate_matches(
    mission,
    df
):

    mission_embedding = embedding_model.encode(
        mission
    )

    results = []

    for _, row in df.iterrows():

        grant_embedding = json.loads(
            row["embedding"]
        )

        score = cosine_similarity(
            [mission_embedding],
            [grant_embedding]
        )[0][0]

        results.append(
            (
                row["grant_name"],
                score,
                row["organization"],
                row["funding_amount"],
                row["description"],
                row["category"]
            )
        )

    return results

# -------------------------
# Sort Results
# -------------------------

def sort_results(
    results,
    sort_by
):

    if sort_by == "Match Score":

        results.sort(
            key=lambda x: x[1],
            reverse=True
        )

    elif sort_by == "Funding Amount (High to Low)":

        results.sort(
            key=lambda x: x[3],
            reverse=True
        )

    elif sort_by == "Funding Amount (Low to High)":

        results.sort(
            key=lambda x: x[3]
        )

    elif sort_by == "Organization (A-Z)":

        results.sort(
            key=lambda x: x[2]
        )

    return results

def create_pdf_report(
    mission,
    explanation,
    results,
    min_funding,
    category,
    organization,
    eligibility,
    sort_by
):

    filename = "GrantMatch_Report.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    # -------------------------
    # Title
    # -------------------------

    story.append(
        Paragraph("<b>GrantMatch AI Report</b>", styles["Title"])
    )

    # -------------------------
    # Mission
    # -------------------------

    story.append(
        Paragraph("<b>Mission</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(mission, styles["BodyText"])
    )

    # -------------------------
    # Search Filters
    # -------------------------

    story.append(
        Paragraph("<b>Search Filters</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(
            f"""
Minimum Funding: ${min_funding:,}<br/>
Category: {category}<br/>
Organization: {organization}<br/>
Eligibility: {eligibility}<br/>
Sort By: {sort_by}
""",
            styles["BodyText"]
        )
    )

    # -------------------------
    # AI Explanation
    # -------------------------

    story.append(
        Paragraph("<b>AI Explanation</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(
            explanation if explanation else
            "AI explanation could not be generated because the Gemini API was unavailable or the quota limit was exceeded.",
            styles["BodyText"]
        )
    )

    # -------------------------
    # Top Matching Grants
    # -------------------------

    story.append(
        Paragraph("<b>Top Matching Grants</b>", styles["Heading2"])
    )

    for rank, grant in enumerate(results[:5], start=1):

        story.append(
            Paragraph(
                f"""
<b>{rank}. {grant[0]}</b><br/>

Match Score: {grant[1] * 100:.1f}%<br/>

Organization: {grant[2]}<br/>

Category: {grant[5]}<br/>

Funding Amount: ${grant[3]:,}<br/>

Description: {grant[4]}
""",
                styles["BodyText"]
            )
        )

    doc.build(story)

    return filename

# -------------------------
# Display Results
# -------------------------

def display_results(
        results,
        mission
        ):

    st.subheader("🤖 AI Explanation")

    if not results:

         st.warning(
            "No matching grants found."
         )

         return

    top_grant = results[0]

    explanation = generate_ai_explanation(
        mission,
        top_grant[0],
        top_grant[4]
)

    if explanation:
        st.success(explanation)

    pdf_file = create_pdf_report(
    mission,
    explanation,
    results,
    min_funding,
    category,
    organization,
    eligibility,
    sort_by
    )

    with open(pdf_file, "rb") as file:

        st.download_button(
        label="📄 Download PDF Report",
        data=file,
        file_name="GrantMatch_Report.pdf",
        mime="application/pdf"
    )

    st.subheader("📊 Search Statistics")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Matches",
        len(results)
    )

    col2.metric(
        "Top Match",
        f"{results[0][1] * 100:.1f}%"
    )

    col3.metric(
        "Organizations",
        len(set(grant[2] for grant in results))
    )

    st.subheader("🏆 Top Matching Grants")

    for rank, grant in enumerate(
        results[:5],
        start=1
    ):

        with st.expander(
            f"#{rank} {grant[0]}",
            expanded=(rank == 1)
        ):

            st.write(
                f"**Match Score:** {grant[1] * 100:.1f}%"
            )

            st.progress(
                min(int(grant[1] * 100), 100)
            )

            st.write(
                f"**Organization:** {grant[2]}"
            )

            st.write(
                f"**Category:** {grant[5]}"
            )

            st.write(
                f"**Funding Amount:** ${grant[3]:,}"
            )

            st.write(
                f"**Description:** {grant[4]}"
            )

# -------------------------
# AI Explanation
# -------------------------

def generate_ai_explanation(
    mission,
    grant_name,
    description
):

    prompt = f"""
Mission:
{mission}

Grant:
{grant_name}

Grant Description:
{description}

Explain in 2-3 sentences why this grant is a good match for the mission.
"""

    try:
        response = gemini_model.generate_content(prompt)
        return response.text

    except Exception as e:

        st.error("⚠️ Gemini API Error")

        st.exception(e)

        st.info(
            "The grant results below are still ranked using semantic similarity. "
            "Only the AI explanation could not be generated."
        )

        return None

# -------------------------
# Streamlit UI
# -------------------------

st.title("GrantMatch AI")

uploaded_file = st.file_uploader(
    "Upload Mission PDF",
    type=["pdf"]
)

pdf_text = ""

if uploaded_file:

    reader = PdfReader(uploaded_file)

    for page in reader.pages:

        text = page.extract_text()

        if text:
            pdf_text += text

mission = st.text_area(
    "Describe your nonprofit mission",
    value=pdf_text if uploaded_file else ""
)

min_funding = st.number_input(
    "Minimum Funding Amount",
    min_value=0,
    value=0,
    step=1000
)

categories, organizations, eligibilities = load_filters()

category = st.selectbox(
    "Grant Category",
    categories
)

organization = st.selectbox(
    "Organization",
    organizations
)

eligibility = st.selectbox(
    "Eligibility",
    eligibilities
)

sort_by = st.selectbox(
    "Sort Results By",
    [
        "Match Score",
        "Funding Amount (High to Low)",
        "Funding Amount (Low to High)",
        "Organization (A-Z)"
    ]
)

# -------------------------
# Find Grants
# -------------------------

if st.button("Find Grants"):

    if not mission:

        st.warning(
            "Please enter a mission statement."
        )
        st.stop()

    with st.spinner("🔍 Finding the best matching grants..."):

        df = search_grants(
            min_funding,
            category,
            organization,
            eligibility
        )

        if df.empty:

            st.warning(
                "No grants found for the selected filters."
            )
            st.stop()

        results = calculate_matches(
            mission,
            df
        )

        results = sort_results(
            results,
            sort_by
        )

        display_results(
            results,
            mission
        )