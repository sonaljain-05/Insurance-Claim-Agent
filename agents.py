import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY")
)

def document_agent(claim):
    if len(claim["documents"]) == 3:
        return "Documents OK"
    return "Documents Missing"

def eligibility_agent(claim):
    if claim["policy"] == "Active":
        return "Eligible"
    return "Not Eligible"

def fraud_agent(claim):
    if claim["amount"] > 100000:
        return "High Risk"
    return "Low Risk"

def summary_agent(claim, results):
    prompt = f"""
Give a very short summary of this insurance claim.

Customer: {claim["name"]}
Amount: {claim["amount"]}
Policy: {claim["policy"]}
Results: {results}
"""
    return llm.invoke(prompt).content

def human_agent(decision):
    return decision