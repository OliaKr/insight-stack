
import asyncio
import os
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from autogen_agentchat.teams import MagenticOneGroupChat
from autogen_agentchat.conditions import FunctionalTermination
from autogen_agentchat.messages import BaseChatMessage
from autogen_core.model_context import TokenLimitedChatCompletionContext
from memory_utils import save_report_to_memory, retrieve_similar_memories
import requests

load_dotenv()


def fetch_report(endpoint_name):
    base_url = "http://localhost:8000"
    url = f"{base_url}/{endpoint_name}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get("report", "")
    except Exception as e:
        print(f"Error fetching {endpoint_name}: {e}")
        return "Failed to fetch report."


model_client = AzureOpenAIChatCompletionClient(
    azure_deployment=os.getenv("AZURE_DEPLOYMENT_ID"),
    model="gpt-4o-mini",
    api_key=os.getenv("AZURE_API_KEY"),
    api_version=os.getenv("AZURE_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    temperature=0
)

short_context = TokenLimitedChatCompletionContext(
    model_client, token_limit=100)
coordinator_context = TokenLimitedChatCompletionContext(
    model_client, token_limit=400)

sales_agent = AssistantAgent(
    name="SalesAgent",
    description="Analyzes sales reports.",
    system_message="Summarize the sales report in 3–5 bullet points focused on performance and issues.",
    model_client=model_client,
    model_context=short_context,
)

support_agent = AssistantAgent(
    name="SupportAgent",
    description="Analyzes support tickets and feedback.",
    system_message="Summarize the support report in 3–5 points focused on customer issues and resolutions.",
    model_client=model_client,
    model_context=short_context,
)

ops_agent = AssistantAgent(
    name="OpsAgent",
    description="Analyzes operational issues.",
    system_message="Summarize the operations report in 3–5 points focused on efficiency and delays.",
    model_client=model_client,
    model_context=short_context,
)

coordinator_agent = AssistantAgent(
    name="CoordinatorAgent",
    description="Combines insights into 5 unique business insights.",
    system_message=(
        "You are the CoordinatorAgent responsible for generating **exactly 4 distinct strategic insights** "
        "based only on the latest summaries from the Sales, Support, and Operations agents. "
        "Do not repeat similar points across insights. Do not generate multiple insight groups. "
        "Each insight must be unique and focus on a different high-level issue or opportunity. "
        "Each insight must begin with a bolded section title (e.g., **Customer Experience**, **Sales Strategy**), "
        "followed by 2–3 concise, action-oriented sentences in a consistent tone. "
        "Only generate one block of four insights. Do not respond again unless explicitly prompted. "
        "Use only the specific content provided by the sales/support/ops agents. Do not generate general advice. "
        "Reference the actual events or metrics mentioned in the summaries. "
        "When writing insights, do NOT use the word 'agent' to refer to people. Instead, use terms like 'sales team', 'support staff', or 'operations team'. "
        "- Use **real figures, metrics, or events** mentioned in the summaries (e.g., Sales in the US increased by 20%, Delivery SLA improved from 78% to 91%, CRM glitches delayed follow-ups by 24 hours). "
        "- DO NOT suggest 'conducting analysis' or 'implementing a system' unless it is in direct response to a described issue in the summaries. "
        "- Focus on interpreting what already happened and deriving concrete insights from those events. "
        "- Avoid repeating vague actions like improve communication or gather feedback unless those already appeared in the summaries."
    ),
    model_client=model_client,
    model_context=coordinator_context,
)

sales_text = fetch_report("sales-report")
support_text = fetch_report("support-report")
ops_text = fetch_report("ops-report")

save_report_to_memory("memory:sales", sales_text)
save_report_to_memory("memory:support", support_text)
save_report_to_memory("memory:operations", ops_text)

sales_memory = retrieve_similar_memories(
    "memory:sales", "sales performance", top_k=2)
support_memory = retrieve_similar_memories(
    "memory:support", "customer issues", top_k=2)
ops_memory = retrieve_similar_memories(
    "memory:operations", "operational delays", top_k=2)

task = "\n".join([
    "Please analyze these reports:",
    "",
    "=== Past Memory: ===",
    f"Sales: {' '.join(sales_memory)}",
    f"Support: {' '.join(support_memory)}",
    f"Operations: {' '.join(ops_memory)}",
    "",
    "=== Current Reports ===",
    "",
    f"=== Sales Report ===\n{sales_text}",
    "",
    f"=== Support Report ===\n{support_text}",
    "",
    f"=== Operations Report ===\n{ops_text}",
    "",
    "Each domain agent should summarize their respective report.",
    "Then the CoordinatorAgent should integrate all summaries into **exactly 5 strategic insights**."
])


def coordinator_responded_once(messages):
    return sum(
        1 for msg in messages if isinstance(msg, BaseChatMessage) and msg.source == "CoordinatorAgent"
    ) >= 1


termination = FunctionalTermination(coordinator_responded_once)

team = MagenticOneGroupChat(
    [sales_agent, support_agent, ops_agent, coordinator_agent],
    model_client=model_client,
    termination_condition=termination
)


async def main():
    result = await team.run(task=task)

    print("\n=== Full Agent Conversation ===\n")
    for msg in result.messages:
        print(f"[{msg.source}]:\n{msg.content}\n")

    count = sum(1 for msg in result.messages if msg.source ==
                "CoordinatorAgent")
    print(f"\n🧠 CoordinatorAgent appeared {count} times.\n")

    if count > 1:
        print("Warning: CoordinatorAgent responded multiple times.")

    insights = [
        msg.content for msg in result.messages if msg.source == "CoordinatorAgent"]

    if insights:
        print("\n🧠 Strategic Insights from Coordinator Agent:\n")
        print("\n".join(insights))
    else:
        print("No insights returned by CoordinatorAgent.")

if __name__ == "__main__":
    asyncio.run(main())
