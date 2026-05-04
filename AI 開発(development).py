import spacy
import random

state = {
    "last_topic": None,
    "topic_sentiment": {},
    "turn_count": 0,
    "repeat_count": 0,
    "focus": "general"
}

print("---START---")
print("AI is ready.")
nlp = spacy.load("en_core_web_sm")

word_groups = {
    "emotion_positive": ["happy", "good", "fine", "fun", "great", "awesome", "excited", "fantastic", "love", "like", "cool"],
    "emotion_negative": ["sad", "bad", "terrible", "awful", "horrible", "depressed", "angry", "upset", "tired", "hate", "sucks"],
    "topic_hobby": ["game", "music", "radio", "sports", "anime", "study", "coding", "art", "travel", "reading"],
    "topic_school": ["homework", "exam", "test", "classmate", "teacher", "school", "assignment"],
    "topic_tech": ["python", "ai", "computer", "program", "code", "internet", "robot"],
    "topic_food": ["pizza", "sushi", "burger", "salad", "pasta", "cake", "icecream", "chocolate", "fruit", "vegetable"],
    "self": ["i", "me", "my", "mine", "myself"],
    "second_person": ["you", "your", "yours", "yourself"]
}

def extract_topic_by_max(scores):
    topic_categories = [k for k in scores if k.startswith("topic_")]
    if not topic_categories:
        return "general"
    best_topic = max(topic_categories, key=lambda k: scores[k])
    if scores[best_topic] == 0:
        return "general"
    return best_topic.replace("topic_", "")

def get_sentiment(scores):
    if scores["emotion_positive"] > 0:
        return "positive"
    elif scores["emotion_negative"] > 0:
        return "negative"
    else:
        return "neutral"

def update_state(state, topic, sentiment):
    state["turn_count"] += 1
    if state["last_topic"] == topic:
        state["repeat_count"] += 1
    else:
        state["repeat_count"] = 1
    if topic not in state["topic_sentiment"]:
        state["topic_sentiment"][topic] = []
    state["topic_sentiment"][topic].append(sentiment)
    state["last_topic"] = topic

def generate_reply(topic, sentiment, state):
    history = state["topic_sentiment"].get(topic, [])
    if len(history) >= 2 and history[-1] == "negative" and history[-2] == "negative":
        return f"It sounds like {topic} has been bothering you lately. Are you all good?"

    if sentiment == "positive":
        return f"That's great! do you wanna talk about {topic} more? or maybe something else with {topic}?"
    elif sentiment == "negative":
        return f"That sounds tough. It seems like you're having a hard time with {topic}."
    else:
        return f"Thanks for sharing about {topic}."

while True:
    text = input("you: ")
    if text.lower() in ["exit", "quit", "bye"]:
        print("AI: Bye!")
        break

    doc = nlp(text)

    meaningful_tokens = [
        token for token in doc
        if token.pos_ not in ["PUNCT", "SPACE"] and token.is_alpha
    ]

    understanding = "low" if len(meaningful_tokens) < 2 else "ok"

    scores = {key: 0 for key in word_groups}
    unknown_words = []

    for token in meaningful_tokens:
        lemma = token.lemma_.lower()
        matched = False

        for category, words in word_groups.items():
            if lemma in words:
                scores[category] += 1
                matched = True

        if not matched:
            unknown_words.append(lemma)

    if "?" in text:
        intent = "question"
    elif scores["emotion_negative"] > 0:
        intent = "complaint"
    else:
        intent = "statement"

    print("\n---Analysis---")
    print("Understanding:", understanding)
    print("intent:", intent)
    print("Scores:")
    for k, v in scores.items():
        print(f"  {k}: {v}")

    topic = extract_topic_by_max(scores)

    if unknown_words:
        topic = " ".join(unknown_words)

    sentiment = get_sentiment(scores)
    update_state(state, topic, sentiment)
    reply = generate_reply(topic, sentiment, state)

    print("\nAI:", reply)
