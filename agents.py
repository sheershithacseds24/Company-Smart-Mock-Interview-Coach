
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from rag import retrieve_questions

llm = OllamaLLM(model="gemma3:1b")


# COMMON FUNCTION TO RUN SYSTEM AND USER PROMPTS
def run_agent(system_prompt, user_prompt, **kwargs):
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", user_prompt)
    ])

    chain = prompt | llm
    return chain.invoke(kwargs)


# AGENT 1: INTERVIEWER
def interviewer(company, role):

    # Agentic RAG: retrieve when interview practice needs questions
    questions = retrieve_questions(
        company,
        role,
        query=f"Technical interview questions for {role}"
    )

    return run_agent(
        "You are an experienced corporate technical interviewer. "
        "Ask one clear question at a time. Do not provide answers.",
        """Conduct an interview for {company}.
        Job role: {role}
        Retrieved question bank: {questions}

        Ask one relevant question based on the retrieved context.
        Keep the question concise.""",
        company=company,
        role=role,
        questions=str(questions)
    )


# AGENT 2: EVALUATOR
def evaluator(question, answer):
    return run_agent(
        """You are a strict but fair technical interview evaluator.
        Evaluate only the candidate's answer.
        Do not inflate scores.""",
        """Evaluate this answer.

        Question: {question}
        Candidate answer: {answer}

        Score each category out of 10:
        1. Correctness
        2. Depth of knowledge
        3. Communication

        Calculate the total out of 30.
        Also calculate the average out of 10.
        Give strengths and weaknesses.
        Return a consistent score.""",
        question=question,
        answer=answer
    )


# AGENT 3: COACH
def coach(question, answer, evaluation):
    return run_agent(
        """You are a personalised interview coach.
        Be encouraging, practical and constructive.""",
        """Question: {question}
        Candidate answer: {answer}
        Evaluation: {evaluation}

        Provide:
        1. Strengths
        2. Areas for improvement
        3. An improved sample answer
        4. Preparation tips

        Do not re-evaluate or change the scores.""",
        question=question,
        answer=answer,
        evaluation=evaluation
    )


# AGENT 4: REPORT
def report(results):
    return run_agent(
        """You are a professional interview report generator.
        Summarise the candidate's actual performance.
        Do not invent scores or interview results.""",
        """Generate a final interview report from:
        {results}

        Include:
        1. Overall performance
        2. Strengths
        3. Weaknesses
        4. Topics to revise
        5. A focused 7-day improvement plan.

        Use clear headings. Avoid repeating the full conversation.""",
        results=str(results)
    )


# INTENT DETECTION
def route_intent(message):
    message = message.lower()

    if any(word in message for word in ["evaluate", "score", "grade"]):
        return "evaluation"

    elif any(word in message for word in ["coach", "feedback", "improve"]):
        return "coaching"

    elif any(word in message for word in ["report", "summary", "performance"]):
        return "report"

    elif any(word in message for word in ["interview", "question", "practice"]):
        return "interview"

    return "unknown"


# FUNCTIONAL INTENT ROUTER
def route_request(message, company, role, question="", answer="", results=None):
    intent = route_intent(message)

    if intent == "interview":
        return interviewer(company, role)

    elif intent == "evaluation":
        return evaluator(question, answer)

    elif intent == "coaching":
        return coach(question, answer, "Previous evaluation")

    elif intent == "report":
        return report(results or [])

    return "Please specify whether you need interview practice, evaluation, coaching or a report."
