from langgraph.graph import StateGraph,START,END
from langgraph.types import interrupt
from langgraph.checkpoint.memory import MemorySaver
from agents import document_agent,eligibility_agent,fraud_agent,summary_agent,human_agent
from state import ClaimState

def documents(state):
    return {"documents":document_agent(state["claim"])}

def eligibility(state):
    return {"eligibility":eligibility_agent(state["claim"])}

def fraud(state):
    return {"fraud":fraud_agent(state["claim"])}

def summary(state):
    results=[state["documents"],state["eligibility"],state["fraud"]]
    return {"summary":summary_agent(state["claim"],results)}

def decision(state):
    if state["documents"]=="Documents Missing":
        return "reject"
    if state["eligibility"]=="Not Eligible":
        return "reject"
    if state["fraud"]=="High Risk":
        return "human"
    return "approve"

def approve(state):
    return {"decision":"APPROVED"}

def reject(state):
    return {"decision":"REJECTED"}

def human(state):
    answer=interrupt("Human approval required. Choose APPROVE or REJECT.")
    return {"decision":human_agent(answer)}

graph=StateGraph(ClaimState)

graph.add_node("documents",documents)
graph.add_node("eligibility",eligibility)
graph.add_node("fraud",fraud)
graph.add_node("summary",summary)
graph.add_node("approve",approve)
graph.add_node("reject",reject)
graph.add_node("human",human)

graph.add_edge(START,"documents")
graph.add_edge(START,"eligibility")
graph.add_edge(START,"fraud")

graph.add_edge("documents","summary")
graph.add_edge("eligibility","summary")
graph.add_edge("fraud","summary")

graph.add_conditional_edges("summary",decision,{"approve":"approve","reject":"reject","human":"human"})

graph.add_edge("approve",END)
graph.add_edge("reject",END)
graph.add_edge("human",END)

memory=MemorySaver()
claim_graph=graph.compile(checkpointer=memory)