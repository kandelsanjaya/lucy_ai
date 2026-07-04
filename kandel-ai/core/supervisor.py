"""
KANDEL AI - Supervisor Agent
Designed by Kandel Sanjaya

Routes a user query through: Memory -> RAG -> Web Search -> LLM synthesis,
and writes the result back into long-term memory. Also detects greetings
and language automatically.
"""
import time
from langdetect import detect, DetectorFactory
from services.llm_provider import chat_completion, stream_completion
from services.web_search import web_search
from memory.memory_store import recall_relevant_memory, save_memory
from rag.retriever import hybrid_search

DetectorFactory.seed = 0

GREETINGS = {"hi", "hello", "hey", "namaste", "yo", "hola", "bonjour", "salut", "hii", "helo"}


def detect_language(text: str) -> str:
    try:
        return detect(text)
    except Exception:
        return "en"


def is_greeting(text: str) -> bool:
    stripped = text.strip().lower().rstrip("!.?")
    return stripped in GREETINGS or len(stripped.split()) <= 2 and any(g in stripped for g in GREETINGS)


def route_query(user_id: int, query: str, has_documents: bool = False):
    """Decide which pipeline stage supplies context. Returns (agent_name, context, sources)."""
    memories = recall_relevant_memory(user_id, query)
    if memories:
        context = "\n".join([f"Q: {m['question']}\nA: {m['answer']}" for m in memories])
        return "Memory Agent", context, [{"title": "Long-term memory", "url": "", "best": True}]

    if has_documents:
        results = hybrid_search(user_id, query)
        if results:
            context = "\n\n".join([r["text"] for r in results])
            sources = [{"title": r["source"], "url": "", "best": i == 0} for i, r in enumerate(results)]
            return "RAG Agent", context, sources

    results = web_search(query)
    if results:
        context = "\n\n".join([f"{r['title']}: {r['snippet']}" for r in results])
        sources = [{"title": r["title"], "url": r["url"], "best": r.get("best", False)} for r in results]
        return "Web Search Agent", context, sources

    return "General Chat Agent", "", []


def build_system_prompt(language_hint: str, context: str, agent: str) -> str:
    base = (
        "You are KANDEL AI, a helpful, precise, and friendly multi-agent AI assistant "
        "designed by Kandel Sanjaya. Always answer in the same language the user wrote in, "
        "unless they explicitly ask for translation. Be concise but thorough. "
        f"You are currently operating as the {agent}."
    )
    if context:
        base += (
            f"\n\nUse the following retrieved context if relevant:\n{context}\n\n"
            "If the context doesn't answer the question, say so plainly and answer from your "
            "own knowledge instead of guessing."
        )
    else:
        base += (
            "\n\nIf you are not confident you know the correct, up-to-date answer, say so "
            "explicitly instead of guessing - the app will automatically fall back to a live "
            "web search in that case."
        )
    return base


UNCERTAIN_PHRASES = [
    "i don't know", "i do not know", "i'm not sure", "i am not sure",
    "i don't have information", "i do not have information", "i cannot confirm",
    "as of my knowledge", "i don't have access to real-time", "unable to verify",
]


def _seems_uncertain(answer: str) -> bool:
    lowered = answer.lower()
    return any(p in lowered for p in UNCERTAIN_PHRASES)


def answer_query(user_id: int, query: str, chat_history: list, has_documents: bool = False, stream: bool = False):
    start = time.time()
    language = detect_language(query)
    agent, context, sources = route_query(user_id, query, has_documents)

    system_prompt = build_system_prompt(language, context, agent)
    messages = [{"role": "system", "content": system_prompt}]
    messages += chat_history[-8:]
    messages.append({"role": "user", "content": query})

    if stream:
        gen, model = stream_completion(messages)
        return {"agent": agent, "sources": sources, "model": model, "stream": gen, "start_time": start}

    answer, model = chat_completion(messages)

    # If the model admits it doesn't know and we haven't already tried the web, search now.
    if agent != "Web Search Agent" and _seems_uncertain(answer):
        results = web_search(query)
        if results:
            context = "\n\n".join([f"{r['title']}: {r['snippet']}" for r in results])
            sources = [{"title": r["title"], "url": r["url"], "best": r.get("best", False)} for r in results]
            agent = "Web Search Agent"
            retry_messages = [{"role": "system", "content": build_system_prompt(language, context, agent)}]
            retry_messages += chat_history[-8:]
            retry_messages.append({"role": "user", "content": query})
            answer, model = chat_completion(retry_messages)

    elapsed = time.time() - start

    # Write back to long-term memory for future recall
    save_memory(
        user_id,
        question=query,
        answer=answer,
        topic=agent,
        summary=answer[:200],
        keywords=query.split()[:8],
    )

    confidence = 0.92 if agent in ("RAG Agent", "Memory Agent") else 0.8 if agent == "Web Search Agent" else 0.75

    return {
        "agent": agent,
        "sources": sources,
        "model": model,
        "answer": answer,
        "response_time": round(elapsed, 2),
        "confidence": confidence,
        "language": language,
    }
