import streamlit as st
import asyncio
import re
import time  # Importing the time module
import pandas as pd  # Importing pandas as pd
from agent_chat_orchestration import team, task

st.set_page_config(
    page_title="InsightSync – Multi-Agent Analyzer", layout="centered")
st.title("InsightSync – Cross-Department Report Analysis")

# Sidebar for navigation
with st.sidebar:
    st.title("Navigation")
    option = st.selectbox("Select Action", ["Run Analysis", "View Insights"])

# Main content based on sidebar selection
if option == "Run Analysis":
    st.header("Run Analysis with AI Agents")
    if st.button("Run Analysis with Agents"):
        with st.spinner("Running agents and generating insights..."):
            result = asyncio.run(team.run(task=task))

            # Display progress bar
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.1)  # Simulate task running
                progress_bar.progress(i + 1)

            # Print all agent messages to the terminal
            print("\n=== Full Agent Conversation ===")
            for msg in result.messages:
                print(f"\n[{msg.source}]:\n{msg.content}\n")

            # Display insights
            coordinator_messages = [
                msg.content for msg in result.messages if msg.source == "CoordinatorAgent"
            ]

            if coordinator_messages:
                st.success("Insights generated!")
                st.subheader("🧠 Strategic Insights from Coordinator Agent:")

                # Combine all messages into one string (in case there are multiple CoordinatorAgent messages)
                full_text = "\n".join(coordinator_messages)

                # Split based on bolded section titles (**Title**)
                insights = re.split(r'\n(?=\*\*)', full_text.strip())

                for idx, insight in enumerate(insights, 1):
                    st.markdown(f"**Insight {idx}:** {insight.strip()}")

            else:
                st.warning("No insights found from the Coordinator Agent.")

elif option == "View Insights":
    st.header("Strategic Insights")
    # This could display insights from a file or a pre-calculated source
    st.subheader("View the results of your last analysis here")
    # Example dataframe to show insights
    data = {
        "Department": ["Sales", "Support", "Operations"],
        "Insight": ["Increase sales in Q2", "Improve customer service", "Optimize operations"],
    }
    df = pd.DataFrame(data)  # Using pandas to create the dataframe
    st.dataframe(df)

# Footer information
st.markdown(
    "Powered by **Azure OpenAI** and built with **Model Context Protocol (MCP)**")
st.caption("Built with Autogen AgentChat & Streamlit | MCP Hackathon 2025")
