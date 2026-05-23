from langchain.agents import initialize_agent, AgentType
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import search_web, scrape_web
from dotenv import load_dotenv

load_dotenv()

# =========================
# LLM Setup
# =========================

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

# =========================
# Search Agent
# =========================

def build_search_agent():
    return initialize_agent(
    tools=[search_web],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)

# =========================
# Reader Agent
# =========================

def build_reader_agent():
    return initialize_agent(
        tools=[scrape_web],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True
    )

# =========================
# Writer Agent
# =========================

writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a professional research report writer."
    ),

    (
        "human",
        """
Write a detailed research report on the topic below.

Topic:
{topic}

Research Notes:
{research}

Structure the report as:

1. Introduction
2. Main Findings
3. Conclusion
4. References

Be detailed, factual, and professional.
"""
    ),
])

writer_chain = writer_prompt | llm | StrOutputParser()

# =========================
# Critic Agent
# =========================

critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a critical reviewer who evaluates research reports."
    ),

    (
        "human",
        """
Critique the following research report based on:

1. Accuracy of information
2. Clarity and coherence
3. Academic quality
4. Effectiveness of arguments

Also score each criterion out of 10.

Report:
{report}
"""
    ),
])

critic_chain = critic_prompt | llm | StrOutputParser()