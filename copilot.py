import os
import json
import requests
import matplotlib.pyplot as plt
from openai import OpenAI
from simple_salesforce import Salesforce

client = OpenAI()

MY_DOMAIN = os.environ["SF_MY_DOMAIN"] 

def get_salesforce_connection():
    auth_url = f"{MY_DOMAIN}/services/oauth2/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": os.environ["SF_CLIENT_ID"],
        "client_secret": os.environ["SF_CLIENT_SECRET"]
    }
    response = requests.post(auth_url, data=payload)
    response.raise_for_status()
    auth_data = response.json()
    return Salesforce(instance_url=auth_data["instance_url"], session_id=auth_data["access_token"])

sf = get_salesforce_connection()


def get_schema() -> str:
    # Return field names for the most commonly used objects
    objects_to_describe = ["Opportunity", "Account", "Case"]
    schema_parts = []
    for obj_name in objects_to_describe:
        desc = getattr(sf, obj_name).describe()
        fields = [f["name"] for f in desc["fields"]]
        schema_parts.append(f"{obj_name} fields: {', '.join(fields)}")
    return "\n".join(schema_parts)


def run_soql(query: str) -> str:
    result = sf.query(query)
    records = result["records"]
    # strip Salesforce's internal metadata field
    cleaned = [{k: v for k, v in r.items() if k != "attributes"} for r in records]
    return str(cleaned)


def make_chart(title: str, labels: list, values: list, chart_type: str = "bar") -> str:
    plt.figure(figsize=(8, 5))
    if chart_type == "line":
        plt.plot(labels, values, marker="o", color="#4C72B0")
    else:
        plt.bar(labels, values, color="#4C72B0")
    plt.title(title)
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    filename = "chart_output.png"
    plt.savefig(filename)
    plt.close()
    return f"Chart saved as {filename}"


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_schema",
            "description": "Returns available fields for Opportunity, Account, and Case objects. Call this first if unsure what fields exist.",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_soql",
            "description": "Run a SOQL query (Salesforce's query language, similar to SQL but with differences) against real Salesforce data. Use SELECT ... FROM ObjectName WHERE ... syntax. If unsure of exact picklist values (like StageName or Status), first run a query like SELECT StageName FROM Opportunity GROUP BY StageName to see real values before filtering.",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "make_chart",
            "description": "Generate and save a chart image to visualize query results when comparing multiple values.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "labels": {"type": "array", "items": {"type": "string"}},
                    "values": {"type": "array", "items": {"type": "number"}},
                    "chart_type": {"type": "string", "enum": ["bar", "line"]}
                },
                "required": ["title", "labels", "values"]
            }
        }
    }
]


def ask(question: str):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a Salesforce data analyst agent with access to real CRM data via SOQL. "
                "SOQL is similar to SQL but does not support SELECT * or some SQL functions. "
                "Never guess exact picklist values (StageName, Status, etc) — check real values first. "
                "Use standard Salesforce object/field names (Opportunity, Account, Case, StageName, Amount, etc)."
            )
        },
        {"role": "user", "content": question}
    ]

    for _ in range(6):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools
        )
        msg = response.choices[0].message

        if not msg.tool_calls:
            print("\nAnswer:", msg.content)
            return

        messages.append(msg)

        for call in msg.tool_calls:
            args = json.loads(call.function.arguments)

            if call.function.name == "get_schema":
                result = get_schema()
                print("AI checked schema")
            elif call.function.name == "make_chart":
                result = make_chart(args["title"], args["labels"], args["values"], args.get("chart_type", "bar"))
                print("AI generated a chart:", args["title"])
            else:
                print("AI ran SOQL:", args["query"])
                try:
                    result = run_soql(args["query"])
                except Exception as e:
                    result = f"Query failed with error: {str(e)}"
                if result == "[]":
                    result = "Query returned no rows. Check exact picklist values first."

            print("Result:", result)

            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": result
            })

    print("Hit max steps without a final answer.")


ask("Which opportunity owner has the most closed-won revenue, and show it as a chart")