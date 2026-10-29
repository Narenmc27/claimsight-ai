from typing import TypedDict
from langgraph.graph import StateGraph, START, END

from agents.extraction import extract
from agents.policy_check import check_policy
from agents.fraud_check import check_fraud
from agents.adjudication import adjudicate


class ClaimState(TypedDict, total=False):
    claim: dict
    extracted: dict
    policy: dict
    fraud: dict
    final: dict


def extract_node(state: ClaimState):
    return {"extracted": extract(state["claim"]["description"]).model_dump()}


def policy_node(state: ClaimState):
    return {"policy": check_policy(state["claim"], state["extracted"])}


def fraud_node(state: ClaimState):
    return {"fraud": check_fraud(state["claim"], state["extracted"])}


def adjudicate_node(state: ClaimState):
    return {"final": adjudicate(state["policy"], state["fraud"])}


builder = StateGraph(ClaimState)
builder.add_node("extract", extract_node)
builder.add_node("policy", policy_node)
builder.add_node("fraud", fraud_node)
builder.add_node("adjudicate", adjudicate_node)

builder.add_edge(START, "extract")
builder.add_edge("extract", "policy")
builder.add_edge("extract", "fraud")
builder.add_edge(["policy", "fraud"], "adjudicate")   # waits for BOTH
builder.add_edge("adjudicate", END)

graph = builder.compile()