
import chromadb

# Connect to persistent ChromaDB
client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="interview_questions"
)

# Company-specific interview question dataset
questions = [
    ("Google", "Python Developer", "Explain Python decorators."),
    ("Google", "Python Developer", "What are Python generators?"),
    ("Google", "Data Analyst", "Explain SQL joins."),
    ("Microsoft", "Python Developer", "Explain OOP concepts in Python."),
    ("Microsoft", "Data Analyst", "How do you handle missing data?"),
    ("Amazon", "Python Developer", "Explain Python dictionaries."),
    ("Amazon", "Data Analyst", "Explain WHERE and HAVING in SQL."),
    ("Infosys", "Python Developer", "Explain exception handling."),
    ("Infosys", "Data Analyst", "Explain data preprocessing."),
    ("TCS", "Data Analyst", "What is data visualization?")
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


def retrieve_questions(company, role, query=None, n=3):
    initialize_database()

    # Agent retrieves questions based on semantic similarity
    search_query = query or f"Interview questions for {role}"

    results = collection.query(
        query_texts=[search_query],
        n_results=min(n, collection.count()),
        where={
            "$and": [
                {"company": company},
                {"role": role}
            ]
        }
    )

    return results["documents"][0] if results["documents"] else []
