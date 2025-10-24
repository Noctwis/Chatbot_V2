import yaml

def load_agent_md(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if content.startswith("---"):
        parts = content.split("---", 2)
        frontmatter = yaml.safe_load(parts[1])
        body = parts[2].strip()
        return frontmatter, body
    else:
        raise ValueError("No valid frontmatter found")