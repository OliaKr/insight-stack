
import streamlit as st
import asyncio
import re
import pandas as pd
from agent_chat_orchestration import team, task, sales_memory, support_memory, ops_memory

st.set_page_config(
    page_title="InsightSync – Multi-Agent Analyzer", layout="centered")
st.title("InsightSync – Cross-Department Report Analysis")

with st.sidebar:
    st.title("Navigation")
    option = st.selectbox(
        "Select Action", ["Run Analysis", "View Insights", "View Memory"])

if option == "Run Analysis":
    st.header("Run Analysis with AI Agents")
    if st.button("Run Analysis with Agents"):
        with st.spinner("Running agents and generating insights..."):
            result = asyncio.run(team.run(task=task))

            coordinator_messages = [
                msg.content for msg in result.messages if msg.source == "CoordinatorAgent"
            ]

            if coordinator_messages:
                st.success("Insights generated!")
                st.subheader("🧠 Strategic Insights from Coordinator Agent:")

                full_text = "\n".join(coordinator_messages)
                insights = re.split(r'\n(?=\*\*)', full_text.strip())

                for idx, insight in enumerate(insights, 1):
                    st.markdown(f"**Insight {idx}:** {insight.strip()}")
            else:
                st.warning("No insights found from the Coordinator Agent.")

elif option == "View Insights":
    st.header("Strategic Insights")
    st.subheader("View the results of your last analysis here")

    data = {
        "Department": ["Sales", "Support", "Operations"],
        "Insight": ["Increase sales in Q2", "Improve customer service", "Optimize operations"],
    }
    df = pd.DataFrame(data)
    st.dataframe(df)

elif option == "View Memory":
    st.header("Long-Term Memory Snapshots")
    st.subheader("🧠 Retrieved Past Memory")

    st.markdown("**Sales Memory:**")
    for i, mem in enumerate(sales_memory, 1):
        st.markdown(f"{i}. {mem}")

    st.markdown("**Support Memory:**")
    for i, mem in enumerate(support_memory, 1):
        st.markdown(f"{i}. {mem}")

    st.markdown("**Operations Memory:**")
    for i, mem in enumerate(ops_memory, 1):
        st.markdown(f"{i}. {mem}")

st.markdown(
    "Powered by **Azure OpenAI** and built with **Model Context Protocol (MCP)**")
