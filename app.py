import re
import streamlit as st
from PyPDF2 import PdfReader

st.set_page_config(page_title="Smart Resume Analyzer", page_icon="📄")

st.title("📄 Smart Resume Analyzer")
st.caption("Upload your resume, paste a job description, and instantly see your match score, missing skills, and suggestions for improvement.")
# -------------------- UI --------------------
left, right = st.columns(2)

with left:
    st.subheader("Paste Job Description")
    job_des = st.text_area(
        "Paste the Job Description here",
        height=250
    )

with right:
    st.subheader("Upload Resume")
    uploaded_file = st.file_uploader(
        "Upload Your Resume",
        type=["pdf"]
    )

analyze = st.button("Analyze Resume")

# -------------------- Analyze --------------------
if analyze:

    if not job_des.strip():
        st.warning("Please paste a Job Description.")
        st.stop()

    if uploaded_file is None:
        st.warning("Please upload your resume.")
        st.stop()

    st.success("Resume Uploaded Successfully!")

    # Read Resume
    reader = PdfReader(uploaded_file)
    text = ""

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted

    # Load skills
    with open("skills.txt", "r") as f:
        skills = [skill.strip() for skill in f.readlines()]

    # -------------------- Skills Found --------------------
    found = []

    for skill in skills:
        if skill.lower() in text.lower():
            found.append(skill)

    # -------------------- JD Skills --------------------
    jd_skills = []

    for skill in skills:
        if skill.lower() in job_des.lower():
            jd_skills.append(skill)

    # -------------------- Missing Skills --------------------
    missing = []

    for skill in jd_skills:
        if skill.lower() not in text.lower():
            missing.append(skill)

    # -------------------- Score --------------------
    if len(jd_skills) > 0:
        score = ((len(jd_skills) - len(missing)) / len(jd_skills)) * 100
    else:
        score = 0

    # -------------------- Results --------------------
    st.divider()

    st.subheader("Skills in Resume")
    st.write(found)

    st.subheader("Required Skills")
    st.write(jd_skills)

    st.subheader("Missing Skills")
    st.write(missing)

    st.subheader("📊 Resume Match Score")
    st.progress(score / 100)
    st.write(f"### {score:.0f}/100")

    st.subheader("Recommended Next Steps")

    if missing:
        for skill in missing:
            st.write(f"• Learn **{skill}**")
    else:
        st.success("🎉 Excellent! Your resume matches the Job Description.")
