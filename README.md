<img width="1536" height="1024" alt="ChatGPT Image Sep 9, 2026, 08_04_43 AM" src="https://github.com/user-attachments/assets/fb967935-8b51-4762-ad5e-a923f8761807" />

**Agentic Commerce POC — AI-powered Photography Shopping Assistant**

Python ✅ AI/LLM ✅ Agentic AI ✅ RAG ✅ Tool Calling ✅ FastAPI ✅ APIs ✅ Adobe Commerce/Magento Ready ✅ Enterprise Integration

## Overview

`ai-commerce-agent` is a small Agentic Commerce proof of concept that demonstrates how an AI shopping assistant can understand customer requirements, search products, check inventory, and add products to a shopping cart using natural language.

The demo uses a fictional photography equipment store with simulated product, inventory and cart data.

### Example

> "I'm a wedding photographer. I need portable lighting under £1,000. Find something suitable, check stock and add it to my cart."

The AI agent can:

- Understand customer requirements
- Search the product catalogue
- Retrieve relevant business knowledge using RAG
- Check product inventory
- Recommend suitable products
- Add products to the cart using a controlled tool

---

## Architecture

```text
Customer
   ↓
Web UI
   ↓
FastAPI
   ↓
AI Agent / Gemini
   │
   ├── RAG → Product & Business Knowledge
   │
   └── Tools
        ├── Search Products
        ├── Check Inventory
        └── Add to Cart
                 ↓
              SQLite

## Project Structure
			  
ai-commerce-agent/
│
├── app/
│   ├── agent.py          # AI agent & tool calling
│   ├── database.py       # SQLite database
│   ├── main.py           # FastAPI application
│   ├── rag.py            # Knowledge retrieval
│   └── tools.py          # Commerce tools
│
├── data/
│   ├── products.json     # Demo products
│   └── knowledge.json    # Business knowledge
│
├── static/
│   └── index.html        # Simple web UI
│
├── .env
├── .env.example
├── requirements.txt
└── README.md
# Execution Process

## 1. Customer Sends a Request

The customer enters a natural-language request through the web UI.

Example:

```text
I'm a wedding photographer.
I need portable lighting under £1,000.
Find a suitable product, check stock and add one to my cart.
```

---

## 2. Request Goes to FastAPI

The browser sends the request to:

```text
POST /chat
```

FastAPI receives the message and calls:

```text
run_agent()
```

---

## 3. Agent Retrieves Knowledge — RAG

The agent first searches the local knowledge base.

```text
Customer Request
       ↓
search_knowledge()
       ↓
knowledge.json
```

RAG provides business knowledge such as:

* Delivery information
* Warranty information
* Product guidance
* Photography recommendations

**RAG provides knowledge, not actions.**

---

## 4. LLM Understands the Request

Gemini receives:

```text
Customer message
       +
Retrieved knowledge
       +
Available tools
```

The LLM decides what needs to be done.

For example:

```text
Customer needs:
- Wedding photography
- Portable lighting
- Budget < £1,000
```

The agent may decide to call:

```text
search_products()
```

---

## 5. Agent Calls the Commerce Tool

The tool searches the demo product catalogue.

```text
Gemini
  ↓
search_products()
  ↓
products.json
```

Example result:

```text
Godox AD200 Pro II
Price: £316
Portable: Yes
Stock: 8
```

The tool result is returned to Gemini.

---

## 6. Agent Checks Inventory

If the customer asks for availability, Gemini calls:

```text
check_inventory(product_id=1)
```

Flow:

```text
Gemini
   ↓
check_inventory()
   ↓
SQLite / Product Data
   ↓
Stock = 8
```

The agent can now tell the customer that the product is available.

---

## 7. Agent Adds Product to Cart

If the customer requests the purchase/cart action, Gemini calls:

```text
add_to_cart(
    product_id=1,
    quantity=1
)
```

The tool validates:

```text
Product exists?
       ↓
In stock?
       ↓
Requested quantity available?
       ↓
Add to SQLite cart
```

Only after the tool succeeds does the agent tell the customer that the product was added.

---

## 8. Final Response

The tool results are returned to Gemini.

Gemini converts the results into a natural-language response.

Example:

```text
The Godox AD200 Pro II is a good fit for wedding
and location photography. It costs £316 and 8 units
are currently available.

I've added 1 unit to your cart.
```

---

# Complete Execution Flow

```text
Customer
   │
   │ Natural language request
   ↓
Web UI
   │
   ↓
FastAPI /chat
   │
   ↓
AI Agent
   │
   ├──────────────→ RAG
   │                 │
   │                 ↓
   │           knowledge.json
   │                 │
   │                 ↓
   │          Business Knowledge
   │
   ↓
Gemini LLM
   │
   │ Decides which tool to use
   ↓
Commerce Tools
   │
   ├── search_products()
   │
   ├── check_inventory()
   │
   └── add_to_cart()
   │
   ↓
SQLite / Demo Data
   │
   ↓
Tool Result
   │
   ↓
Gemini
   │
   ↓
Final Customer Response
```

---

# What Each Layer Does

| Layer   | Responsibility               |
| ------- | ---------------------------- |
| Web UI  | Customer interaction         |
| FastAPI | API/request handling         |
| Agent   | Orchestration                |
| Gemini  | Reasoning and tool selection |
| RAG     | Retrieve business knowledge  |
| Tools   | Execute controlled actions   |
| JSON    | Demo product catalogue       |
| SQLite  | Demo cart storage            |

## Simple Interview Explanation

> "The customer sends a natural-language request to FastAPI. The agent retrieves relevant business knowledge using RAG and sends the request, knowledge and available tools to the Gemini LLM. The LLM decides which tool is required, such as product search or inventory check. The tool executes the operation against the demo commerce data and returns the result to the LLM. The LLM then generates the final response for the customer."

**Key concept:**

```text
LLM = Reasoning
Agent = Orchestration
RAG = Knowledge
Tools = Actions
FastAPI = API Layer
Magento/Adobe Commerce = Production Commerce Backend
```
