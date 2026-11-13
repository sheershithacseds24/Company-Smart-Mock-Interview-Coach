
import streamlit as st
from agents import (
    interviewer, evaluator, coach, report,
    route_intent, route_request
)

st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Company-Smart Mock Interview Coach")
st.caption("Agentic AI-powered company-specific interview preparation")

# SIDEBAR
st.sidebar.header("Interview Settings")

company = st.sidebar.selectbox(
    "Select Company",
    ["Google", "Microsoft", "Amazon", "Infosys", "TCS"]
)

role = st.sidebar.selectbox(
    "Select Job Role",
    ["Python Developer", "Data Analyst"]
)

# SESSION STATE
defaults = {
    "question": "",
    "results": [],
    "evaluation": "",
    "feedback": "",
    "answer": "",
    "final_report": ""
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

st.divider()

# INTERVIEWER AGENT
st.header("📝 Mock Interview")

st.write(f"**Company:** {company}")
st.write(f"**Job Role:** {role}")

if st.button("Start / Next Interview Question"):
    with st.spinner("Interviewer Agent is working..."):
        st.session_state.question = interviewer(company, role)
        st.session_state.evaluation = ""
        st.session_state.feedback = ""
        st.session_state.answer = ""

if st.session_state.question:
    st.subheader("Interview Question")
    st.info(st.session_state.question)

    answer = st.text_area(
        "Enter your answer:",
        key="answer",
        height=150
    )

    if st.button("Submit Answer"):
        if answer.strip():
            with st.spinner("Evaluator and Coach Agents are working..."):

                evaluation = evaluator(
                    st.session_state.question,
                    answer
                )

                feedback = coach(
                    st.session_state.question,
                    answer,
                    evaluation
                )

                st.session_state.evaluation = evaluation
                st.session_state.feedback = feedback

                st.session_state.results.append({
                    "question": st.session_state.question,
                    "answer": answer,
                    "evaluation": evaluation,
                    "feedback": feedback
                })
        else:
            st.warning("Please enter your answer.")

# DISPLAY EVALUATION
if st.session_state.evaluation:
    st.divider()
    st.subheader("📊 Evaluator Agent")
    st.write(st.session_state.evaluation)

    st.subheader("💡 Coach Agent")
    st.write(st.session_state.feedback)

# FINAL REPORT
st.divider()
st.header("📑 Interview Performance Report")

if st.button("Generate Final Report"):
    if st.session_state.results:
        with st.spinner("Report Agent is working..."):
            st.session_state.final_report = report(
                st.session_state.results
            )
    else:
        st.warning("Complete an interview first.")

if st.session_state.final_report:
    st.markdown(st.session_state.final_report)

# FUNCTIONAL INTENT ROUTING
st.divider()
st.header("🤖 Agentic Intent Detection and Routing")

st.write(
    "Enter a request and the system will identify your intent "
    "and route it to the appropriate AI agent."
)

request = st.text_input(
    "What would you like the AI assistant to do?",
    placeholder="Example: Give me feedback on my answer"
)

if st.button("Detect Intent and Execute"):
    if request.strip():
        intent = route_intent(request)

        st.success(f"Detected Intent: {intent.upper()}")

        if intent == "interview":
            with st.spinner("Interviewer Agent is working..."):
                response = route_request(
                    request, company, role
                )
            st.write(response)

        elif intent in ["evaluation", "coaching"]:
            if not st.session_state.question or not st.session_state.answer:
                st.warning("Complete an interview answer first.")
            else:
                with st.spinner("Selected agent is working..."):
                    response = route_request(
                        request,
                        company,
                        role,
                        question=st.session_state.question,
                        answer=st.session_state.answer,
                        results=st.session_state.results
                    )
                st.write(response)

        elif intent == "report":
            if st.session_state.results:
                with st.spinner("Report Agent is working..."):
                    response = route_request(
                        request,
                        company,
                        role,
                        results=st.session_state.results
                    )
                st.write(response)
            else:
                st.warning("Complete an interview first.")

        else:
            st.info(
                "Please ask for interview practice, evaluation, "
                "coaching or a report."
            )
    else:
        st.warning("Please enter a request.")

st.divider()
st.caption(
    "Powered by Gemma 3 | LangChain | ChromaDB | Streamlit"
)
