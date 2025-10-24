import yaml
from sentence_transformers import SentenceTransformer
import faiss

# Load agent configuration from YAML
with open("config/agents.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# Filter out disabled agents
agents = [agent for agent in config["agents"] if not agent.get("disabled", False)]

# Create a lookup map using agent name
agent_map = {agent["name"]: agent for agent in agents}

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Prepare embedding texts using keywords + role + goal
agent_texts = [
    " ".join(agent.get("keywords", [])) + " " + agent.get("role", "") + " " + agent.get("goal", "")
    for agent in agents
]
embeddings = model.encode(agent_texts, convert_to_numpy=True)

# Create FAISS index
dim = embeddings.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(embeddings)

# Simple normalization function
def normalize(text):
    return text.lower().strip()

# Hybrid router: keyword match + embedding fallback
def route(user_input):
    user_input_norm = normalize(user_input)

    # Fast path: keyword matching
    for agent in agents:
        keywords = agent.get("keywords", [])
        if any(kw.lower() in user_input_norm for kw in keywords):
            print(f"[Router] Fast path via keywords → Selected agent: {agent['name']}")
            return agent["name"]

    # Fallback: semantic similarity via FAISS
    query_vec = model.encode([user_input_norm])
    D, I = index.search(query_vec, k=1)

    # Threshold check to avoid out-of-scope responses
    threshold = 0.6
    if D[0][0] > threshold:
        print(f"[Router] Distance too high ({D[0][0]:.2f}) → Out-of-scope agent triggered")
        return "agent_test"
    else:
        chosen_agent = agents[I[0][0]]
        
        print(f"[Router] Fallback via embeddings: Selected agent: {chosen_agent} (distance = {D[0][0]:.2f})")
        return chosen_agent

