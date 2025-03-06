import os

from langchain_community.tools import TavilySearchResults
from langchain_mistralai import ChatMistralAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Optional

# Set API keys
os.environ["MISTRAL_API_KEY"] = "DkDE3Ra8ZtfrWyCJmf9ESllQ3pzLhl9H"
os.environ["TAVILY_API_KEY"] = "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"

# Define the Research Agent
class ResearchAgent:
    def __init__(self):
        self.search_tool = TavilySearchResults(max_results=5)
    
    def fetch_research_data(self, query):
        results = self.search_tool.invoke(query)
        return results

# Define the Answer Drafting Agent
class AnswerDraftingAgent:
    def __init__(self):
        self.llm = ChatMistralAI(model="open-mistral-nemo", temperature=0.5)
    
    def generate_summary(self, research_data):
        # Print research_data to inspect its structure
        print("Raw Research Data:", research_data)
        
        # Modify to match Tavily search result structure
        combined_text = "\n".join([
            f"{result['content']} (Source: {result['url']})" 
            for result in research_data
        ])
        
        # Create messages directly
        messages = [
            SystemMessage(content="You are an AI assistant that summarizes research findings. Provide a concise and informative summary of the research data."),
            HumanMessage(content="Synthesize the following research data into a coherent summary:\n" + combined_text)
        ]
        
        # Invoke LLM with messages
        response = self.llm.invoke(messages)
        return response.content

# Define State as a TypedDict
class ResearchState(TypedDict):
    query: str
    research_data: List[dict]
    summary: Optional[str]

# Create graph workflow
def research_node(state: ResearchState):
    research_agent = ResearchAgent()
    return {"research_data": research_agent.fetch_research_data(state["query"])}

def draft_answer_node(state: ResearchState):
    drafting_agent = AnswerDraftingAgent()
    summary = drafting_agent.generate_summary(state["research_data"])
    return {"summary": summary}

# Setup graph
graph = StateGraph(ResearchState)
graph.add_node("research", research_node)
graph.add_node("draft_answer", draft_answer_node)

graph.add_edge("research", "draft_answer")
graph.add_edge("draft_answer", END)
graph.set_entry_point("research")

# Compile graph
compiled_graph = graph.compile()

# Test the system
if __name__ == "__main__":
    query = "Latest advancements in Quantum Computing"
    initial_state = {
        "query": query,
        "research_data": [],
        "summary": None
    }
    
    final_state = compiled_graph.invoke(initial_state)
    
    print("\n🔍 Research Data Collected:\n", final_state["research_data"])
    print("\n📄 Generated Summary:\n", final_state["summary"])