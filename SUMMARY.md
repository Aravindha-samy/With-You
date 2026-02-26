# With You - Project Summary

## Quick Setup Summary

To run the "With You" project, you'll need to set up both the Python backend and the Next.js frontend.

### Backend Setup (FastAPI)

1.  **Navigate to the backend directory:**
    ```bash
    cd WithYou/backend
    ```

2.  **Create and activate a Python virtual environment:**
    ```bash
    # For Windows
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1

    # For macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Seed the database with initial data:**
    ```bash
    python seed_data.py
    ```

5.  **Run the backend server:**
    ```bash
    uvicorn main:app --reload
    ```
    The backend will be running at `http://127.0.0.1:8000`.

### Frontend Setup (Next.js)

1.  **Navigate to the frontend directory in a new terminal:**
    ```bash
    cd WithYou/frontend
    ```

2.  **Install dependencies using pnpm:**
    ```bash
    pnpm install
    ```

3.  **Run the frontend development server:**
    ```bash
    pnpm dev
    ```
    The frontend will be running at `http://localhost:3000`.

4.  **Open the application:**
    Open your web browser and navigate to `http://localhost:3000`.

---

## Technical Highlights

### 1. The "Cognitive Mesh": A Multi-Agent System for Emotional Safety

The core of our implementation is the **Cognitive Mesh**, a multi-agent architecture where each AI agent has a distinct, specialized role. Instead of a monolithic chatbot, we created a team of agents (Aurora, Harbor, Roots, Solace, Echo, Guardian, Legacy) that collaborate to provide holistic cognitive support.

**Technical Decision**: We chose this architecture to enforce a separation of concerns at the AI level. This allows for:
- **Targeted Prompt Engineering**: Each agent's system prompt is highly focused, leading to more accurate and safer responses. For example, `Solace` is an expert in de-escalation, while `Harbor` is an expert in providing grounding information.
- **Maintainability and Scalability**: It's easier to debug, refine, or replace a single agent without affecting the entire system.
- **Safety and Guardrails**: The orchestrator, `Aurora`, acts as a central routing and safety layer, assessing intent and emotion *before* dispatching to a specialized agent. This prevents inappropriate or emotionally jarring responses.

We are most proud of how this architecture directly serves the project's primary goal: protecting the user's emotional safety and dignity.

### 2. Identity-First AI and Proactive De-escalation

Our system is built on an **identity-first** principle. The AI is designed to never correct the user harshly or remind them of their memory loss.

**Technical Decision**: We implemented this through a combination of prompt design and intelligent routing.
- **Behavioral Guardrails**: Agents like `Harbor` and `Roots` have strict rules in their prompts, such as "Never say 'You forgot'" and "Never say 'As I told you before.'"
- **Proactive Emotional Routing**: The `Aurora` orchestrator analyzes the emotional content of every user utterance. If the anxiety score exceeds a certain threshold, the request is immediately routed to the `Solace` agent, which is specialized in emotional regulation. This allows the system to de-escalate a situation proactively rather than reacting to it after the fact.

This proactive approach to emotional safety is a key technical achievement that differentiates "With You" from standard conversational AI.

### 3. Dual-Mode Interaction for Cognitive Accessibility

We recognized that users with cognitive decline have varying abilities and needs. To address this, we designed two distinct interaction modes.

**Technical Decision**:
- **Structured Navigation (Button Mode)**: This mode bypasses complex AI reasoning. Button presses are mapped to direct API calls that trigger specific agents (e.g., "Where am I?" -> `Harbor`). This provides a fast, stable, and predictable experience for users who may be overwhelmed by open-ended conversation.
- **Free Speech Mode**: This mode leverages the full power of the Cognitive Mesh, using Azure Speech and Azure OpenAI for users who are more comfortable speaking naturally.

This dual-mode approach makes the application more accessible and adaptable to the user's changing cognitive state, ensuring it remains a useful tool throughout their journey. It represents a thoughtful blend of simple, deterministic logic and advanced AI reasoning to create a user-centric experience.

---

## Challenges & Learnings

### Challenge 1: Designing for Emotional Safety, Not Just Accuracy

**The Challenge**: Our biggest challenge was moving beyond the traditional goal of chatbot accuracy to prioritize emotional safety. A standard AI might bluntly correct a user or fail to recognize subtle signs of distress, which would be harmful to someone with cognitive decline. We couldn't just build a Q&A bot; we had to build an empathetic companion. How do you program empathy and dignity?

**What We Learned**:
-   **Specialization is Key**: We learned that a single, monolithic AI cannot be an expert in everything. Our initial attempts with a single agent often led to generic or tonally inappropriate responses. This led us to develop the **Cognitive Mesh**, our multi-agent architecture. By creating specialized agents like `Solace` (for emotional regulation) and `Roots` (for identity), we could craft highly-focused system prompts and guardrails for each one.
-   **Prompt Engineering as Empathy**: Crafting the system prompts became an exercise in applied empathy. We spent a significant amount of time on the behavioral guardrails, explicitly forbidding phrases like "You forgot" or "I already told you." We learned that for this application, the *constraints* you put on the AI are more important than the knowledge you give it.
-   **Orchestration is the Safety Net**: The `Aurora` agent became our most critical component. We learned that having an intelligent router to first assess intent and, more importantly, *emotion*, was the key to preventing harmful interactions. By routing high-anxiety queries to `Solace` *before* attempting to answer a factual question, the system can prioritize de-escalation over information, which is a fundamental shift from conventional AI design.

### Challenge 2: Balancing Simplicity with Intelligence

**The Challenge**: The user interface had to be radically simple for the patient, yet the backend system was complex. How could we create an experience that was both powerful and accessible, catering to users who might be overwhelmed by technology?

**What We Learned**:
-   **One Size Doesn't Fit All**: We quickly realized that a single mode of interaction was insufficient. This led to the creation of our **dual-mode system**.
    1.  **Structured Navigation (Button Mode)** provides a safe, predictable, and low-cognitive-load path. It's deterministic and bypasses complex AI, which is crucial for users in a state of confusion.
    2.  **Free Speech Mode** offers the full power of the AI for users who are able to communicate more naturally.
-   **Accessibility is More Than UI**: We learned that for AI applications, accessibility isn't just about large fonts and buttons. It's about providing **multiple, adaptable pathways for interaction**. The system must adapt to the user's cognitive state, not the other way around. This design decision made the application more inclusive and useful across different stages of cognitive ability.

### Challenge 3: Preventing "AI Hallucinations" in a High-Stakes Context

**The Challenge**: Large language models can "hallucinate" or invent information. In a medical or emotional support context, providing fabricated information about a person's life or schedule would be confusing and potentially dangerous.

**What We Learned**:
-   **Grounding the AI in a "Single Source of Truth"**: We learned that the AI should not be the source of truth; it should be an *interpreter* of the truth. Our agents are designed to be heavily grounded in the structured data from our **SQLite database**.
-   **Separation of Roles**: The `Legacy` (story) and `Roots` (identity) agents are strictly instructed to only use information from the database. They are not allowed to infer or create new "memies." The `Echo` agent's role is simply to log interactions and compute trends, not to generate narrative content.
-   **The Power of Structured Data**: This challenge reinforced the importance of a well-designed database schema. By having the caregiver input structured, factual data, we create a reliable foundation that the AI can draw from. The AI's job is to present this data in a gentle, conversational, and context-aware manner, not to invent it. This significantly reduces the risk of harmful hallucinations and ensures the continuity of the user's true personal story.
