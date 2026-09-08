import json
from pathlib import Path


KNOWLEDGE_FILE = Path("data/knowledge.json")


def search_knowledge(query: str):

    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as file:
        documents = json.load(file)

    query_words = set(query.lower().split())

    results = []

    for document in documents:

        text = (
            document["title"] + " " +
            document["content"]
        ).lower()

        score = sum(
            1 for word in query_words
            if word in text
        )

        if score > 0:
            results.append({
                "title": document["title"],
                "content": document["content"],
                "score": score
            })

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results[:3]