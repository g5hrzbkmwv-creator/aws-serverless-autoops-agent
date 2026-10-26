# aws-serverless-autoops-agent
This project transforms a CLI-based Python AI Agent into a enterprise-ready, web-accessible API and modern chat UI. Built on top of **Amazon Bedrock** and the **Strands Agent Framework**, the system leverages **AgentCore Gateway** via **Model Context Protocol (MCP)** for dynamic tool discovery and execution. 

## 🚀 Key Architecture Highlights
1. **Serverless Microservice Conversion**:
   - Replaced interactive CLI `input()` loops with stateless, RESTful API endpoints managed by FastAPI and `mangum`.

2. **Dynamic Tooling via Model Context Protocol (MCP)**:
   - Eliminates hardcoded tools by dynamically fetching and binding operational MCP tools from AgentCore Gateway during request lifecycles.

3. **Production Hardening & Edge Case Handling**:
   - **API Gateway Timeout Alignment**: Managed execution windows to strictly comply with API Gateway’s 29-second hard timeout constraint.
   - **Binary Compatibility Fixes**: Resolved Pydantic/`pydantic-core` C-extension platform mismatches (`Runtime.ImportModuleError`) using Docker-compiled Lambda Layers for Linux targets (`x86_64`/`aarch64`).

4. **Thinking Process & Output Separation**:
   - Implemented regex-based stream and payload parsing (in both Python backend and JS client) to isolate `<thinking>` internal reasoning tags from end-user UI outputs.

## 🛠 Tech Stack
### **Backend & Cloud Infrastructure**
- **Language**: Python 3.11+
- **AI & Agent Orchestration**: Strands Agent Framework, Model Context Protocol (MCP) SDK
- **LLM Foundation Model**: Amazon Bedrock (`amazon.nova-pro-v1:0`)
- **Serverless Compute & Networking**: AWS API Gateway, AWS Lambda, AWS Lambda Layers
- **HTTP Client**: `httpx` (Async HTTP Transport for MCP)

### **Frontend UI**
- **Core Library**: React 18+
- **Build Tool**: Vite
- **Styling & Icons**: Tailwind CSS, Lucide Icons
- **Environment Management**: Vite Environment Variables (`import.meta.env`)