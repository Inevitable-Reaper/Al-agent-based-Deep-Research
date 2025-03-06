# Deep Research AI Agentic System

## Overview
This project implements a **Deep Research AI Agentic System** using **LangChain, LangGraph, and Tavily Search API**. The system consists of multiple agents working together to:

1. **Collect research data** from the web using Tavily.
2. **Generate a concise summary** of the collected data using Mistral AI.
3. **Execute the workflow** using LangGraph's state-based execution.

## Features
- **Automated Web Research**: Uses Tavily API to fetch research data based on a given query.
- **LLM-Powered Summarization**: Mistral AI generates structured summaries from raw research data.
- **Graph-Based Workflow**: LangGraph organizes the research and answer-drafting steps.
- **Modular and Extensible**: The system allows easy expansion with additional agents or functionalities.


## Code Structure

- `research_agent.py`: Handles web research using Tavily.
- `answer_drafting_agent.py`: Summarizes research findings using Mistral AI.
- `main.py`: Orchestrates the research and summarization workflow.

## Dependencies
- `langchain`
- `langgraph`
- `langchain-mistralai`
- `langchain-community`
- `tavily`


