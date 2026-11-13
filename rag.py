
import chromadb

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="interview_questions"
)

questions = [
    ("Google", "Python Developer", "Explain Python decorators."),
    ("Google", "Data Analyst", "Explain SQL joins."),
    ("Microsoft", "Python Developer", "Explain OOP concepts in Python."),
    ("Microsoft", "Data Analyst", "How do you handle missing data?"),
    ("Amazon", "Python Developer", "Explain Python dictionaries."),
    ("Amazon", "Data Analyst", "Explain WHERE and HAVING in SQL."),
    ("Infosys", "Python Developer", "Explain exception handling."),
    ("TCS", "Data Analyst", "What is data preprocessing?")
]

def initialize_database():
    if collection.count() == 0:
        for i, (company, role, question) in enumerate(questions):
            text = f"{company} {role}: {question}"
            collection.add(
                ids=[str(i)],
                documents=[text],
                metadatas=[{
                    "company": company,
                    "role": role
                }]
            )

def retrieve_questions(company, role):
    initialize_database()

    results = collection.get(
        where={
            "$and": [
                {"company": company},
                {"role": role}
            ]
        }
    )

    return results["documents"]

