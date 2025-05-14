
import streamlit as st
import asyncio
import re
import pandas as pd
from pathlib import Path
from agent_chat_orchestration import prepare_team_and_task, sales_memory, support_memory, ops_memory, sales_text, support_text, ops_text

# הגדרת Streamlit page config
st.set_page_config(
    page_title="InsightStack – Cross-Department Report Analysis", layout="centered")

st.markdown("""
<h1 style='text-align: center;'>🤖 InsightStack – Cross-Department Report Analysis</h1>
<p style='text-align: center;'>Your autonomous agent system for business report analysis</p>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
if "view" not in st.session_state:
    st.session_state.view = None

with col1:
    if st.button("🔍 Run Analysis"):
        st.session_state.view = "run"
with col2:
    if st.button("📊 View Insights"):
        st.session_state.view = "insights"
with col3:
    if st.button("🧠 View Memory"):
        st.session_state.view = "memory"

st.divider()

# שימוש ב-Streamlit Cache לטעינת דוחות


@st.cache_data
def load_reports():
    return sales_text, support_text, ops_text


# אם הדוחות כבר נטענים ממקורות אחרים, נשמור אותם כאן ב-cached memory
sales_text, support_text, ops_text = load_reports()

if st.session_state.view == "run":
    st.subheader("Analyze Department Reports with AI Agents")
    if st.button("▶️ Run Now"):
        with st.spinner("Running agents..."):
            team, task = prepare_team_and_task()
            result = asyncio.run(team.run(task=task))
            messages = [
                msg.content for msg in result.messages if msg.source == "CoordinatorAgent"]
            if messages:
                st.success("Insights generated!")
                insights = re.split(r'\n(?=\*\*)', messages[0].strip())
                for idx, insight in enumerate(insights, 1):
                    st.markdown(f"**Insight {idx}:** {insight.strip()}")
                st.session_state.insights = insights
            else:
                st.warning(
                    "No insights returned – check if reports are available.")

elif st.session_state.view == "insights":
    st.subheader("📊 Last Insights")
    if "insights" in st.session_state:
        for idx, insight in enumerate(st.session_state.insights, 1):
            st.markdown(f"**Insight {idx}:** {insight.strip()}")
    else:
        df = pd.DataFrame({
            "Department": ["Sales", "Support", "Operations"],
            "Insight": ["Increase sales in Q2", "Improve customer service", "Optimize logistics"]
        })
        st.dataframe(df)

elif st.session_state.view == "memory":
    st.subheader("🧠 Long-Term Memory Snapshots")
    st.markdown("**Sales Memory:**")
    for i, mem in enumerate(sales_memory, 1):
        st.markdown(f"{i}. {mem}")
    st.markdown("**Support Memory:**")
    for i, mem in enumerate(support_memory, 1):
        st.markdown(f"{i}. {mem}")
    st.markdown("**Operations Memory:**")
    for i, mem in enumerate(ops_memory, 1):
        st.markdown(f"{i}. {mem}")

else:
    image_path = Path(__file__).parent / "assets" / "agent_insights.png"
    if image_path.exists():
        st.image(image_path, use_container_width=True)
    else:
        st.warning(f"🔍 Image not found at: {image_path}")
    st.markdown("*Powered by Azure OpenAI + MCP + RAG + Autonomous Agents*")

# הצגת הדוחות הגולמיים רק אם נדרש
with st.expander("🔍 View Raw Department Reports"):
    st.code(sales_text, language="markdown")
    st.code(support_text, language="markdown")
    st.code(ops_text, language="markdown")

st.markdown("""
<hr style="margin-top:3em;"/>
<p style="text-align: center; color: gray;">
Built using Azure OpenAI, Redis, Streamlit and Autogen AgentChat.
</p>
""", unsafe_allow_html=True)
