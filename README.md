# AI CRM Copilot

An AI agent that answers natural language questions about Salesforce CRM data by autonomously writing and executing SOQL queries, self-correcting on errors, and generating charts which is built to demonstrate applied AI agent design on top of real enterprise CRM data.

## What it does

- Takes a plain English question (e.g. "Which rep has the most closed-won revenue?")
- Discovers the Salesforce schema on its own (no hardcoded field lists)
- Writes and executes real SOQL queries against a live Salesforce org
- Self corrects when a query fails or returns unexpected results, by inspecting real data before retrying
- Automatically generates a chart when the question calls for one
- Authenticates via OAuth 2.0 Client Credentials Flow (Salesforce's current machine-to-machine auth standard, migrated from the deprecated Connected App / SOAP login model)

## Why I built this

I spent 3 years working on Salesforce Health Cloud and Service Cloud implementations as a Business/SaaS Analyst. This project combines that domain background with hands-on AI agent development, moving beyond using AI as a chat assistant into building a tool that autonomously reasons about and acts on real business data.

## Architecture

1. User asks a question in plain English
2. LLM (GPT-4o-mini) decides which tool to call: check schema, run SOQL, or generate a chart
3. Tool executes against a real Salesforce org via the REST API
4. Result (or error) is returned to the LLM
5. LLM either adjusts its approach or gives a final answer
6. Loop continues until a final answer is reached (max 6 steps)

## Tech stack

- Python
- OpenAI API (function/tool calling)
- Salesforce REST API + SOQL
- OAuth 2.0 Client Credentials Flow (via External Client App)
- matplotlib

## Setup

1. Clone this repo
2. Create a virtual environment and install dependencies: `pip install -r requirements.txt`
3. Set environment variables: `OPENAI_API_KEY`, `SF_CLIENT_ID`, `SF_CLIENT_SECRET`, `SF_MY_DOMAIN`
4. Run: `python copilot.py`

## Example

**Question:** "Which opportunity owner has the most closed-won revenue, and show it as a chart"

The agent autonomously: queries opportunities, hits a SOQL syntax error on its first attempt, corrects it, resolves the numeric owner ID into a readable name via a follow-up query, and generates a bar chart, all without being told any of these intermediate steps.
