import streamlit as st
import uuid
from langgraph.types import Command
from graph import claim_graph

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Insurance Claim Agent",
    page_icon="🛡️",
    layout="centered"
)

# ---------- CUSTOM UI ----------
st.markdown("""
<style>

.stApp {
    background-color: #6DA889;
    background-image:
        radial-gradient(#b8dcd7 1px, transparent 1px);
    background-size: 22px 22px;
}

/* Main card */
.block-container {
    max-width: 850px;
    padding-top: 2rem;
}

/* Header */
.header {
    background: #075e54;
    padding: 22px;
    border-radius: 18px;
    color: white;
    text-align: center;
    margin-bottom: 20px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.15);
}

.header h1 {
    margin: 0;
    font-size: 30px;
}

.header p {
    margin: 5px 0 0;
    opacity: 0.85;
}

/* Custom Green Box (Approved) */
.custom-green-box {
    background-color: #155724;
    color: #D4EDDA;
    border: 2px solid #28A745;
    padding: 14px 18px;
    border-radius: 10px;
    font-weight: bold;
    font-size: 18px;
    margin-bottom: 15px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
}

/* Custom Red Box (Rejections) */
.custom-red-box {
    background-color: #721C24;
    color: #F8D7DA;
    border: 2px solid #DC3545;
    padding: 14px 18px;
    border-radius: 10px;
    font-weight: bold;
    font-size: 18px;
    margin-bottom: 15px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
}

/* Custom Yellow/Amber Box (Human Approval Required) */
.custom-yellow-box {
    background-color: #856404;
    color: #FFF3CD;
    border: 2px solid #FFC107;
    padding: 14px 18px;
    border-radius: 10px;
    font-weight: bold;
    font-size: 18px;
    margin-bottom: 15px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
}

/* Custom Dark Blue Box with Gold Text (Claim Summary) */
.custom-blue-gold-box {
    background-color: #002B49;
    color: #FFD700;
    border: 2px solid #FFD700;
    padding: 16px;
    border-radius: 12px;
    font-weight: bold;
    font-size: 16px;
    line-height: 1.5;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    margin-bottom: 15px;
}

/* Button */
.stButton > button {
    width: 100%;
    border-radius: 12px;
    background: #128c7e;
    color: white;
    border: none;
    padding: 10px;
    font-weight: bold;
}

.stButton > button:hover {
    background: #075e54;
    color: white;
}

</style>
""", unsafe_allow_html=True)


# ---------- HEADER ----------
st.markdown("""
<div class="header">
    <h1>🛡️ Insurance Claim Agent</h1>
    <p>Fast • Secure • Smart Claim Processing</p>
</div>
""", unsafe_allow_html=True)


# ---------- CLAIM FORM ----------
st.subheader("👤 Customer Details")

name = st.text_input("Customer Name")
amount = st.number_input(
    "Claim Amount",
    min_value=0,
    step=1000
)

policy = st.selectbox(
    "Policy Status",
    ["Active", "Expired"]
)

st.markdown("### 📄 Required Documents")

documents = []

if st.checkbox("📋 Claim Form"):
    documents.append("Claim Form")

if st.checkbox("📑 Policy Document"):
    documents.append("Policy Document")

if st.checkbox("🪪 Identity Proof"):
    documents.append("Identity Proof")


# ---------- PROCESS CLAIM ----------
if st.button("🚀 Process Claim"):

    claim = {
        "name": name,
        "amount": amount,
        "policy": policy,
        "documents": documents
    }

    thread_id = str(uuid.uuid4())

    st.session_state["thread_id"] = thread_id

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    result = claim_graph.invoke(
        {"claim": claim},
        config=config
    )

    st.session_state["result"] = result


# ---------- RESULT ----------
if "result" in st.session_state:

    result = st.session_state["result"]

    st.subheader("📊 Claim Result")

    decision = result.get("decision")

    if decision == "APPROVED":
        st.markdown('<div class="custom-green-box">✅ CLAIM APPROVED</div>', unsafe_allow_html=True)

    elif decision == "REJECTED":
        st.markdown('<div class="custom-red-box">❌ CLAIM REJECTED</div>', unsafe_allow_html=True)

    elif decision == "APPROVED BY HUMAN":
        st.markdown('<div class="custom-green-box">👨‍💼 APPROVED BY HUMAN</div>', unsafe_allow_html=True)

    elif decision == "REJECTED BY HUMAN":
        st.markdown('<div class="custom-red-box">👨‍💼 REJECTED BY HUMAN</div>', unsafe_allow_html=True)

    else:
        st.markdown('<div class="custom-yellow-box">⏳ HUMAN APPROVAL REQUIRED</div>', unsafe_allow_html=True)

        human_decision = st.radio(
            "Human Reviewer Decision",
            [
                "APPROVED BY HUMAN",
                "REJECTED BY HUMAN"
            ]
        )

        if st.button("✅ Submit Human Decision"):

            thread_id = st.session_state["thread_id"]

            config = {
                "configurable": {
                    "thread_id": thread_id
                }
            }

            result = claim_graph.invoke(
                Command(resume=human_decision),
                config=config
            )

            st.session_state["result"] = result

            st.rerun()


    # ---------- DETAILS ----------
    st.markdown("### 📝 Claim Summary")
    
    summary_text = result.get("summary", "")
    st.markdown(f'<div class="custom-blue-gold-box">{summary_text}</div>', unsafe_allow_html=True)

    st.markdown("### 📄 Document Verification")
    st.write(result.get("documents", ""))

    st.markdown("### 🔍 Eligibility Check")
    st.write(result.get("eligibility", ""))

    st.markdown("### 🛡️ Fraud Detection")
    st.write(result.get("fraud", ""))