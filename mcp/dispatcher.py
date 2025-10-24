import yaml
import requests

def invoke_mcp(agent_name, user_input):
    with open("config/agents.yaml", "r", encoding="utf-8") as f:
        yaml_file = yaml.safe_load(f)
    config = yaml_file.get(agent_name)
    if not config:
        return {"error": f"Aucun MCP défini pour l'agent '{agent_name}'"}

    payload = {
        "name": config["name"],
        "params": {
            **config.get("params", {}),
            "query": user_input
        }
    }

    try:
        response = requests.post(config["endpoint"], json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}