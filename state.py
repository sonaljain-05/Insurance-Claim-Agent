from typing import TypedDict

class ClaimState(TypedDict, total=False):
    claim: dict
    documents: str
    eligibility: str
    fraud: str
    summary: str
    decision: str