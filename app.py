import streamlit as st
import time
from datetime import datetime

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="ResearchMind",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================
# SESSION STATE
# ==============================
defaults = {
    "result": None,
    "running": False,
    "history": []
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ==============================
# HELPERS
# ==============================
def esc(text):
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )

# ==============================
# GLOBAL CSS
# ==============================
st.markdown("""
<style>

/* Hide Streamlit UI */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
[data-testid="stToolbar"] {display:none;}

/* Main App */
.stApp{
    background:#020617;
    color:white;
}

/* Main container */
.block-container{
    max-width:1300px;
    padding-top:2rem;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"]{
    gap:20px;
}

.stTabs [data-baseweb="tab"]{
    background:#0f172a;
    border-radius:12px;
    padding:12px 20px;
    color:white;
}

.stTabs [aria-selected="true"]{
    background:#1e293b !important;
    color:#38bdf8 !important;
}

/* Scrollbar */
::-webkit-scrollbar{
    width:8px;
}

::-webkit-scrollbar-thumb{
    background:#334155;
    border-radius:20px;
}

/* Report Styling */
.report-box{
    background:#0f172a;
    padding:35px;
    border-radius:20px;
    border:1px solid #334155;
    line-height:1.9;
    font-size:18px;
    color:#e2e8f0;
}

/* Search cards */
.card{
    background:#0f172a;
    border:1px solid #334155;
    border-radius:20px;
    padding:25px;
    margin-bottom:20px;
}

.result-card{
    background:#0f172a;
    border:1px solid #334155;
    border-radius:20px;
    padding:25px;
    margin-bottom:20px;
}

/* Metric cards */
.metric-card{
    background:#0f172a;
    border:1px solid #334155;
    border-radius:18px;
    padding:25px;
    text-align:center;
}

/* Critic Card */
.critic-card {
    background:#0f172a;
    border:1px solid #334155;
    border-radius:20px;
    padding:35px;
    line-height:1.9;
    font-size:18px;
    color:#cbd5e1;
}

/* Section title */
.section-title{
    font-size:32px;
    font-weight:700;
    margin-bottom:20px;
}

/* Links */
a{
    color:#38bdf8 !important;
    text-decoration: none;
}
a:hover {
    text-decoration: underline;
}

/* History cards */
.history-card{
    background:#0f172a;
    border:1px solid #334155;
    border-radius:15px;
    padding:18px;
    margin-bottom:12px;
}

</style>
""", unsafe_allow_html=True)

# ==============================
# HERO SECTION
# ==============================
st.markdown("""
<div style="
background:linear-gradient(135deg,#0f172a,#1e293b);
padding:50px;
border-radius:25px;
border:1px solid #334155;
margin-bottom:35px;
">

<h1 style="
font-size:64px;
margin:0;
color:white;
font-weight:800;
">
🔬 ResearchMind
</h1>

<p style="
font-size:22px;
margin-top:12px;
color:#cbd5e1;
">
AI Multi-Agent Research System
</p>

<p style="
font-size:18px;
margin-top:18px;
color:#94a3b8;
line-height:1.8;
max-width:900px;
">
Search • Scrape • Analyze • Critique — powered by multiple AI agents.
Generate fully researched reports instantly with modern AI workflows.
</p>

</div>
""", unsafe_allow_html=True)

# ==============================
# SEARCH BAR
# ==============================
topic = st.text_input(
    "Research Topic",
    placeholder="Enter any topic..."
)

c1, c2, c3 = st.columns([2,1,1])

with c1:
    run_btn = st.button(
        "🚀 Run Search",
        use_container_width=True
    )

with c2:
    if st.button("🧹 Clear", use_container_width=True):
        st.session_state.result = None
        st.rerun()

with c3:
    st.metric("History", len(st.session_state.history))
# ==============================
# PIPELINE RUNNER
# ==============================
if run_btn and topic:

    st.session_state.running = True

    from tools import search_web, scrape_web
    from agents import writer_chain, critic_chain

    progress = st.progress(0)
    status = st.empty()

    state = {}
    start = time.time()

    try:
        # ==============================
        # STEP 1 - SEARCH
        # ==============================
        status.info("🔎 Searching the web...")
        progress.progress(20)

        search_results = search_web.invoke(topic)

        if not isinstance(search_results, list):
            search_results = []

        state["search_results"] = search_results

        # ==============================
        # STEP 2 - SCRAPE
        # ==============================
        status.info("📄 Scraping sources...")
        progress.progress(45)

        scraped = []

        for r in search_results[:3]:
            try:
                url = r.get("url", "")
                if url:
                    content = scrape_web.invoke(url)

                    # Handle blocked websites
                    blocked_phrases = [
                        "Enable JavaScript",
                        "enable javascript",
                        "disable any ad blocker",
                        "Access Denied",
                        "Just a moment",
                        "Verify you are human",
                        "Cloudflare",
                        "Read timed out",
                        "403 Forbidden",
                    ]

                    if any(p.lower() in str(content).lower() for p in blocked_phrases):
                        content = """
⚠ This website blocks automated scraping.
The source uses anti-bot protection, JavaScript verification, or request filtering.
Try another source.
"""
                    scraped.append(f"\nSOURCE URL: {url}\n\n{content}")

            except Exception as e:
                scraped.append(f"\nSOURCE URL: {url}\n\nError scraping: {str(e)}")

        state["reader_insights"] = "\n\n".join(scraped)

        # ==============================
        # STEP 3 - REPORT
        # ==============================
        status.info("✍️ Writing AI research report...")
        progress.progress(75)

        combined = f"""
SEARCH RESULTS:
{state['search_results']}

SCRAPED CONTENT:
{state['reader_insights']}
"""

        report = writer_chain.invoke({
            "topic": topic,
            "research": combined
        })

        state["report"] = report

        # ==============================
        # STEP 4 - CRITIQUE
        # ==============================
        status.info("🧠 Running AI critique...")
        progress.progress(90)

        feedback = critic_chain.invoke({
            "report": report
        })

        state["feedback"] = feedback
        progress.progress(100)

        total = round(time.time() - start, 1)
        status.success(f"✅ Research completed in {total}s")

        st.session_state.result = state
        st.session_state.running = False

        st.session_state.history.append({
            "topic": topic,
            "timestamp": datetime.now().strftime("%H:%M"),
            "duration": total,
            "results": len(search_results)
        })

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.session_state.running = False

# ==============================
# RENDER RESULTS (Safe-wrapped inside Session Condition)
# ==============================
if st.session_state.result:

    state = st.session_state.result

    sr = state.get("search_results", [])
    ins = state.get("reader_insights", "")
    report = state.get("report", "")
    fb = state.get("feedback", "")

    word_count = len(str(report).split())

    st.divider()

    # ==============================
    # METRICS DISPLAY
    # ==============================
    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric("Sources Found", len(sr))

    with m2:
        st.metric("URLs Scraped", min(3, len(sr)))

    with m3:
        st.metric("Words Written", word_count)

    with m4:
        st.metric("Characters Scraped", len(ins))

    st.divider()

    # ==============================
    # TABS CREATION
    # ==============================
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔎 Search Results",
        "📄 Scraped Sources",
        "📘 Research Report",
        "🧠 Critic Evaluation"
    ])

    # ==============================
    # TAB 1 — SEARCH RESULTS
    # ==============================
    with tab1:
        st.markdown('<div class="section-title">Search Results</div>', unsafe_allow_html=True)
        
        if sr:
            for i, r in enumerate(sr, 1):
                st.markdown(f"""
                <div class="result-card">
                    <h3>Result {i}</h3>
                    <a href="{r.get('url', '#')}" target="_blank">
                        {r.get('title', 'No Title Available')}
                    </a>
                    <p style="color:#cbd5e1; margin-top:8px;">{r.get('snippet', 'No description available.')}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No search results to display.")

    # ==============================
    # TAB 2 — SCRAPED CONTENT
    # ==============================
    with tab2:
        st.markdown('<div class="section-title">Scraped Content</div>', unsafe_allow_html=True)

        if ins:
            import re

            scraped_contents = ins.split("SOURCE URL:")
            for i, content in enumerate(scraped_contents[1:], 1):
                lines = content.strip().split("\n")
                url = lines[0] if lines else "Unknown URL"
                
                # Combine lines into a raw string block
                raw_text = "\n".join(lines[1:]).replace("**", "")

                # 1. Strip markdown links '[text](url)' into just 'text'
                clean_text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', raw_text)
                
                # 2. Strip Wikipedia citation brackets like [1], [10], etc.
                clean_text = re.sub(r'\[\s*\d+\s*\]', '', clean_text)
                
                # 3. Strip structural markdown headings (#, ##, ###)
                clean_text = re.sub(r'#+\s*', '', clean_text)
                
                # 4. Strip stray parenthetical link descriptions like "Task (computing)" or "Arthur Samuel (...)"
                clean_text = re.sub(r'"[^"|)]+\([^)]+\)"', '', clean_text)
                clean_text = re.sub(r'\([^)]+\s+\([^)]+\)\)', '', clean_text)
                
                # 5. Wipe out standalone urls or stray bracket symbols
                clean_text = re.sub(r'https?://\S+', '', clean_text)
                clean_text = clean_text.replace("[", "").replace("]", "")

                # Flatten into a seamless, clean paragraph layout
                clean_paragraph = " ".join(clean_text.split())

                st.markdown(f"""
                <div class="card">
                    <h3 style="color:#4ade80; margin-bottom: 5px;">✓ Source {i}</h3>
                    <p style="color:#38bdf8; margin-bottom: 15px;">{url}</p>
                    <p style="
                        color:#e2e8f0; 
                        line-height:1.8; 
                        font-size:16px; 
                        text-align: justify;
                    ">
                        {clean_paragraph[:2500]}...
                    </p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No reader insights available.")
    # ==============================
    # TAB 3 — RESEARCH REPORT
    # ==============================
    with tab3:
        st.markdown('<div class="section-title">Research Report</div>', unsafe_allow_html=True)

        clean_report = report.replace("**", "")
        st.markdown(f"""
        <div class="critic-card">
            {clean_report}
        </div>
        """, unsafe_allow_html=True)

    # ==============================
    # TAB 4 — CRITIC EVALUATION
    # ==============================
    with tab4:
        st.markdown('<div class="section-title">Critic Evaluation</div>', unsafe_allow_html=True)
        clean_feedback = fb.replace("**", "")
        st.markdown(f"""
        <div class="critic-card">
            {clean_feedback}
        </div>
        """, unsafe_allow_html=True)

# ==============================
# GLOBAL HISTORY (Kept global so it renders on initial page loads)
# ==============================
if st.session_state.history:
    st.divider()
    st.markdown('<div class="section-title">🕘 Research History</div>', unsafe_allow_html=True)

    for item in reversed(st.session_state.history[-5:]):
        st.markdown(f"""
        <div class="history-card">
            <h4 style="margin:0;color:white;">{esc(item['topic'])}</h4>
            <p style="margin-top:10px; color:#94a3b8;">
                ⏱ {item['duration']} sec &nbsp;&nbsp;|&nbsp;&nbsp;
                📄 {item['results']} sources &nbsp;&nbsp;|&nbsp;&nbsp;
                🕒 {item['timestamp']}
            </p>
        </div>
        """, unsafe_allow_html=True) 