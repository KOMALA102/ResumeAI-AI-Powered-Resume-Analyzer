import streamlit as st
import fitz
import re

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="ResumeAI",
    page_icon="📄",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>
    .main {
        padding: 2rem;
    }

    .title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #666;
        margin-bottom: 30px;
    }

    .metric-card {
        padding: 20px;
        border-radius: 12px;
        background-color: #f5f7fa;
        text-align: center;
        margin-bottom: 15px;
    }

    .metric-number {
        font-size: 32px;
        font-weight: bold;
    }

    .metric-label {
        font-size: 15px;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="title">📄 ResumeAI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-Powered Resume Analysis Platform</div>',
    unsafe_allow_html=True
)

st.divider()

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.header("Resume Analyzer")

    st.write(
        "Upload your resume and analyze "
        "your skills and experience."
    )

    st.divider()

    st.info(
        "Supported format: PDF"
    )

# --------------------------------------------------
# UPLOAD RESUME
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload your resume",
    type=["pdf"]
)

# --------------------------------------------------
# JOB DESCRIPTION
# --------------------------------------------------

job_description = st.text_area(
    "Paste Job Description",
    height=180,
    placeholder="Paste the job description here..."
)

# --------------------------------------------------
# PDF TEXT EXTRACTION
# --------------------------------------------------

def extract_text_from_pdf(uploaded_file):

    document = fitz.open(
        stream=uploaded_file.read(),
        filetype="pdf"
    )

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text


# --------------------------------------------------
# SKILL DATABASE
# --------------------------------------------------

SKILLS = [
    "python",
    "java",
    "javascript",
    "typescript",
    "c++",
    "c",
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "fastapi",
    "flask",
    "django",
    "react",
    "html",
    "css",
    "git",
    "github",
    "docker",
    "aws",
    "azure",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "pandas",
    "numpy",
    "tensorflow",
    "pytorch",
    "power bi",
    "excel"
]


# --------------------------------------------------
# SKILL DETECTION
# --------------------------------------------------

def find_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS:

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text):
            found_skills.append(skill)

    return found_skills


# --------------------------------------------------
# ANALYZE BUTTON
# --------------------------------------------------

if uploaded_file:

    st.success(
        f"Resume uploaded: {uploaded_file.name}"
    )

    if st.button(
        "🔍 Analyze Resume",
        type="primary"
    ):

        with st.spinner("Analyzing resume..."):

            resume_text = extract_text_from_pdf(
                uploaded_file
            )

            resume_skills = find_skills(
                resume_text
            )

            job_skills = find_skills(
                job_description
            )

            # Calculate match

            if job_skills:

                matched_skills = [
                    skill
                    for skill in job_skills
                    if skill in resume_skills
                ]

                missing_skills = [
                    skill
                    for skill in job_skills
                    if skill not in resume_skills
                ]

                score = int(
                    len(matched_skills)
                    / len(job_skills)
                    * 100
                )

            else:

                matched_skills = []
                missing_skills = []
                score = 0

        # --------------------------------------------------
        # RESULTS
        # --------------------------------------------------

        st.divider()

        st.header("Resume Analysis")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Match Score",
                f"{score}%"
            )

        with col2:
            st.metric(
                "Skills Found",
                len(resume_skills)
            )

        with col3:
            st.metric(
                "Missing Skills",
                len(missing_skills)
            )

        st.divider()

        # --------------------------------------------------
        # DETECTED SKILLS
        # --------------------------------------------------

        st.subheader("✅ Detected Skills")

        if resume_skills:

            st.write(
                ", ".join(
                    skill.title()
                    for skill in resume_skills
                )
            )

        else:

            st.warning(
                "No recognized skills were found."
            )

        # --------------------------------------------------
        # MATCHED SKILLS
        # --------------------------------------------------

        st.subheader("🎯 Matched Job Skills")

        if matched_skills:

            st.write(
                ", ".join(
                    skill.title()
                    for skill in matched_skills
                )
            )

        else:

            st.info(
                "No matching skills found."
            )

        # --------------------------------------------------
        # MISSING SKILLS
        # --------------------------------------------------

        st.subheader("⚠️ Recommended Skills")

        if missing_skills:

            for skill in missing_skills:
                st.write(f"• {skill.title()}")

        else:

            st.success(
                "No missing skills detected!"
            )

        # --------------------------------------------------
        # RESUME TEXT
        # --------------------------------------------------

        with st.expander(
            "View Extracted Resume Text"
        ):

            st.text(
                resume_text
            )

else:

    st.info(
        "👆 Upload a PDF resume to begin analysis."
    )