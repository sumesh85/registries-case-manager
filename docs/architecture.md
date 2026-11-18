# registries-case-manager: Architecture diagram

The main components in the order a case meets them. Details are in [design.md](design.md).

```mermaid
flowchart TB
    SRC[("1. Domain systems")]
    DET["2. Detectors"]
    CASES[("3. Case store")]
    AGENT["4. Agent"]
    CHECK["5. Record checks"]
    DASH["6. Staff dashboard"]
    EXEC["7. Executor"]
    LOG[("8. Decision log")]

    KNOW["Knowledge"]
    LLM["LLM"]
    TOOLS["MCP tools (read-only)"]

    SRC -->|"read"| DET
    DET -->|"open a case"| CASES
    CASES -->|"case to investigate"| AGENT
    AGENT -->|"diagnosis + proposed fix"| CHECK
    CHECK -->|"checked proposal"| DASH
    DASH -->|"approved fix"| EXEC
    EXEC -->|"apply fix"| SRC
    EXEC -->|"every step recorded"| LOG

    KNOW --> AGENT
    LLM <--> AGENT
    TOOLS <--> AGENT
    TOOLS -.->|"read"| SRC
```

1. **Domain systems** hold the data: databases, files and logs.
2. **Detectors** read that data and find something wrong.
3. The **case store** keeps one case per problem, with its evidence.
4. The **agent** investigates the case. It uses the domain's **knowledge**, the **LLM**, and read-only
   **MCP tools** to look at more data.
5. **Record checks** make sure every claim in the diagnosis is backed by evidence.
6. **Staff** approve or reject the proposed fix on the **dashboard**.
7. The **executor** applies approved fixes. It is the only part that writes.
8. The **decision log** records every step, from detection to fix.
