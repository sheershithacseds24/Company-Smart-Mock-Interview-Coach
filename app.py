
import streamlit as st
from agents import interviewer, evaluator, coach, report

st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Company-Smart Mock Interview Coach")
st.write("Your personal AI-powered interview preparation assistant.")

st.sidebar.header("Interview Settings")

company = st.sidebar.selectbox(
    "Select Company",
    ["Google", "Microsoft", "Amazon", "Infosys", "TCS"]
)

role = st.sidebar.selectbox(
    "Select Job Role",
    ["Python Developer", "Data Analyst"]
)

if "question" not in st.session_state:
    st.session_state.question = ""

if "results" not in st.session_state:
    st.session_state.results = []

st.divider()

st.header("📝 Mock Interview")

st.write("**Company:**", company)
st.write("**Role:**", role)

if st.button("Start Interview"):
    with st.spinner("Interviewer Agent is preparing a question..."):
        st.session_state.question = interviewer(company, role)

if st.session_state.question:

    st.subheader("Interview Question")
    st.info(st.session_state.question)

    answer = st.text_area(
        "Enter your answer:",
        height=150
    )

    if st.button("Submit Answer"):
        if answer.strip():

            with st.spinner("Evaluating your answer..."):

                evaluation = evaluator(
                    st.session_state.question,
                    answer
                )

                feedback = coach(
                    st.session_state.question,
                    answer,
                    evaluation
                )

                st.session_state.results.append({
                    "question": st.session_state.question,
                    "answer": answer,
                    "evaluation": evaluation,
                    "feedback": feedback
                })

                st.subheader("📊 Evaluator Agent")
                st.write(evaluation)

                st.subheader("💡 Coach Agent")
                st.write(feedback)

        else:
            st.warning("Please enter your answer.")

st.divider()

st.header("📑 Interview Performance Report")

if st.button("Generate Final Report"):

    if st.session_state.results:

        with st.spinner("Generating your report..."):
            final_report = report(st.session_state.results)

        st.subheader("Your Interview Report")
        st.write(final_report)

    else:
        st.warning("Complete at least one interview question first.")

st.divider()

st.caption("Powered by Gemma 3 | LangChain | ChromaDB")
