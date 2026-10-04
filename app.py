import os
import re

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Research Studio",
    page_icon="R",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    :root {
        --ink: #17251f;
        --muted: #718078;
        --green: #1f6b50;
        --green-light: #e9f3ed;
        --line: #e7ece8;
        --paper: #fbfcfa;
    }
    .stApp {
        background:
            radial-gradient(ellipse at 88% 0%, rgba(218, 237, 223, .52), transparent 32rem),
            var(--paper);
        color: var(--ink);
    }
    [data-testid="stSidebar"] {
        background: #f3f7f3;
        border-right: 1px solid var(--line);
    }
    .block-container {
        max-width: 1120px;
        padding-top: 2.5rem;
        padding-bottom: 4rem;
    }
    .eyebrow {
        color: var(--green);
        font-size: .76rem;
        font-weight: 750;
        letter-spacing: .16em;
        text-transform: uppercase;
        margin-bottom: .65rem;
    }
    .hero-title {
        color: var(--ink);
        font-size: clamp(2.5rem, 6vw, 4.3rem);
        font-weight: 720;
        letter-spacing: -.065em;
        line-height: 1.02;
        margin: 0;
    }
    .hero-copy {
        color: var(--muted);
        font-size: 1.08rem;
        line-height: 1.65;
        margin: 1rem 0 1.6rem;
        max-width: 650px;
    }
    .section-label {
        color: var(--muted);
        font-size: .78rem;
        font-weight: 700;
        letter-spacing: .11em;
        text-transform: uppercase;
        margin: 1.25rem 0 .5rem;
    }
    .result-card {
        background: white;
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 1.2rem 1.35rem;
        min-height: 106px;
    }
    .result-label {
        color: var(--muted);
        font-size: .76rem;
        font-weight: 700;
        letter-spacing: .08em;
        text-transform: uppercase;
        margin-bottom: .55rem;
    }
    .result-value {
        color: var(--ink);
        font-size: 1.08rem;
        font-weight: 650;
    }
    div[data-testid="stForm"] {
        background: white;
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: 1.25rem 1.4rem 1.4rem;
    }
    div.stButton > button[kind="primary"],
    div[data-testid="stFormSubmitButton"] button {
        background: var(--green);
        border: 1px solid var(--green);
        border-radius: 10px;
        color: white;
        font-weight: 650;
        min-height: 2.8rem;
    }
    div.stButton > button[kind="primary"]:hover,
    div[data-testid="stFormSubmitButton"] button:hover {
        background: #18563f;
        border-color: #18563f;
        color: white;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: .5rem;
        border-bottom: 1px solid var(--line);
    }
    .stTabs [data-baseweb="tab"] {
        color: var(--muted);
        font-weight: 650;
    }
    .stTabs [aria-selected="true"] {
        color: var(--green) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("## Research Studio")
    st.caption("A multi-agent workflow for turning a question into a reviewed report.")
    st.divider()
    st.markdown("### Workflow")
    st.markdown(
        """
        1. **Search** — finds recent sources
        2. **Read** — extracts useful page content
        3. **Write** — drafts a structured report
        4. **Review** — critiques the final draft
        """
    )
    st.divider()
    st.markdown("### API configuration")
    missing_keys = [
        name
        for name in ("OPENAI_API_KEY", "TAVILY_API_KEY")
        if not os.getenv(name)
    ]
    if missing_keys:
        st.warning(
            "Add `OPENAI_API_KEY` and `TAVILY_API_KEY` to your `.env` file "
            "before starting a research run."
        )
    else:
        st.success("OpenAI and Tavily keys detected.")
    st.caption("Keys are read from environment variables and are never shown here.")

st.markdown('<div class="eyebrow">Multi-agent research workspace</div>', unsafe_allow_html=True)
st.markdown('<h1 class="hero-title">Good research starts<br>with a better question.</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-copy">Give your research team a topic. Search, reading, writing, '
    "and review agents will work together to produce a clear, source-backed report.</p>",
    unsafe_allow_html=True,
)

st.markdown('<div class="section-label">Start a research run</div>', unsafe_allow_html=True)
with st.form("research_form"):
    topic = st.text_area(
        "Research topic",
        placeholder="For example: How is AI changing the global energy sector?",
        height=100,
        max_chars=500,
        label_visibility="collapsed",
    )
    submitted = st.form_submit_button("Run research", type="primary", use_container_width=True)

if submitted:
    if not topic.strip():
        st.warning("Enter a research topic to get started.")
    elif missing_keys:
        st.error("The required API keys are missing. Add them to `.env`, then restart the app.")
    else:
        st.session_state.pop("research_result", None)
        with st.spinner("Your agents are researching, reading, writing, and reviewing..."):
            from src.pipeline.pipeline import run_research_pipeline

            st.session_state["research_result"] = run_research_pipeline(topic.strip())
            st.session_state["research_topic"] = topic.strip()

result = st.session_state.get("research_result")
if result:
    st.markdown('<div class="section-label">Research workspace</div>', unsafe_allow_html=True)
    st.subheader(st.session_state.get("research_topic", "Research report"))

    metric_columns = st.columns(3)
    for column, label, value in zip(
        metric_columns,
        ("Search agent", "Reader agent", "Report review"),
        ("Complete", "Complete", "Complete"),
    ):
        with column:
            st.markdown(
                f'<div class="result-card"><div class="result-label">{label}</div>'
                f'<div class="result-value">{value}</div></div>',
                unsafe_allow_html=True,
            )

    st.write("")
    report_tab, review_tab, sources_tab = st.tabs(
        ["Final report", "Critic review", "Research notes"]
    )
    with report_tab:
        report = result.get("report", "")
        st.markdown(report or "The writer agent did not return a report.")
        if report:
            filename = re.sub(
                r"[^a-zA-Z0-9_-]+", "-", st.session_state.get("research_topic", "report").lower()
            ).strip("-")
            st.download_button(
                "Download report",
                data=report,
                file_name=f"{filename or 'research-report'}.md",
                mime="text/markdown",
            )

    with review_tab:
        st.markdown(result.get("feedback") or "The critic agent did not return feedback.")

    with sources_tab:
        search_results = result.get("search_results", "")
        scraped_content = result.get("scraped_content", "")
        with st.expander("Search results", expanded=True):
            st.markdown(search_results or "No search results were returned.")
        with st.expander("Scraped page content"):
            st.markdown(scraped_content or "No page content was returned.")
elif not submitted:
    st.markdown('<div class="section-label">What you will get</div>', unsafe_allow_html=True)
    preview_columns = st.columns(3)
    previews = (
        ("01 / Discover", "Recent web research with useful source context."),
        ("02 / Synthesize", "A structured report built from search and extracted content."),
        ("03 / Improve", "A separate critic review to highlight strengths and gaps."),
    )
    for column, (label, description) in zip(preview_columns, previews):
        with column:
            st.markdown(
                f'<div class="result-card"><div class="result-label">{label}</div>'
                f'<div class="result-value">{description}</div></div>',
                unsafe_allow_html=True,
            )

