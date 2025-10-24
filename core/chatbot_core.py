from langchain_ollama import OllamaLLM
from huggingface_hub import login


from utils.markdown_loader import load_agent_md
import os
from mcp.dispatcher import invoke_mcp


login("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")
class ChatbotCore:
    def __init__(self, model_name='mistralai/Mistral-7B-Instruct-v0.3'):
        #self.llm = OllamaLLM(model=model_name)
        self.llm = model_name

    def identify_use_case(self, user_input, agent_info):
        if not agent_info:
            raise ValueError("Missing agent_info")

        # Load Markdown template using path 
        md_path = os.path.join("agents", agent_info['category'], f"{agent_info['name']}.md")

        _, prompt_template = load_agent_md(md_path)
        # mcp if available
        if agent_info.get("mcp"):
            mcp_result = invoke_mcp(agent_info["name"], user_input)
            mcp_content = mcp_result.get("content", "")
            prompt_template = prompt_template.replace("{{ mcp_content }}", mcp_content)
        
        # Inject user input into the template
        prompt = prompt_template.replace("{{ user_input }}", user_input)

        # Call the LLM
        result = self.llm.invoke(prompt)
        # extract text
        if isinstance(result, dict):
            response = result.get("text", "").strip()
        else:
            response = str(result).strip()
        # return response
        return response
