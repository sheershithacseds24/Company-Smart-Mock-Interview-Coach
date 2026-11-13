
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from rag import retrieve_questions

llm = OllamaLLM(model="gemma3:1b")


# AGENT 1: INTERVIEWER
def interviewer(company, role):
    questions = retrieve_questions(company, role)

    prompt = PromptTemplate.from_template("""
    You are a professional technical interviewer.
    Company: {company}
    Role: {role}
    Available questions: {questions}

    Ask ONE interview question at a time.
    Do not reveal the answer.
    """)

    chain = prompt | llm
    return chain.invoke({
        "company": company,
        "role": role,
        "questions": str(questions)
    })


# AGENT 2: EVALUATOR
def evaluator(question, answer):
    prompt = PromptTemplate.from_template("""
    Evaluate this interview answer.

    Question: {question}
    Answer: {answer}

    Give scores out of 10 for correctness,
    depth and communication.
    Explain the scores and give a total out of 30.
    """)

    chain = prompt | llm
    return chain.invoke({
        "question": question,
        "answer": answer
    })


# AGENT 3: COACH
def coach(question, answer, evaluation):
    prompt = PromptTemplate.from_template("""
    You are an interview coach.

    Question: {question}
    Answer: {answer}
    Evaluation: {evaluation}

    Give strengths, weaknesses and suggestions
    to improve the candidate's answer.
    """)

    chain = prompt | llm
    return chain.invoke({
        "question": question,
        "answer": answer,
        "evaluation": evaluation
    })


# AGENT 4: REPORT
def report(results):
    prompt = PromptTemplate.from_template("""
    Generate a final mock interview report.

    Results: {results}

    Include overall performance, strengths,
    weaknesses and a 7-day improvement plan.
    """)

    chain = prompt | llm
    return chain.invoke({"results": str(results)})


# INTENT ROUTER
def route_intent(message):
    message = message.lower()

    if "evaluate" in message or "score" in message:
        return "evaluation"
    elif "coach" in message or "feedback" in message:
        return "coaching"
    elif "report" in message:
        return "report"
    else:
        return "interview"
