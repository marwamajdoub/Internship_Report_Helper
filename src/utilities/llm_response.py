from transformers import pipeline

qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")

def generate_answer(query: str, contexts: list[str]) -> str:
    context = "\n\n".join(contexts)
    
    result = qa_pipeline({
        "question": query,
        "context": context
    })
    
    return result["answer"]
