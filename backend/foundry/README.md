# With You - System Design and Development Guide

This document provides a comprehensive overview of the "With You" application, an identity-first AI architecture designed as a persistent emotional memory companion for individuals with cognitive decline.

## 1. Architecture

The "With You" application is built on a **Cognitive Mesh** architecture, a system of multiple intelligent agents working collaboratively in the background. This architecture is designed to be simple, robust, and emotionally safe.

### Core Components:

*   **Frontend Application**: A user-facing application with a simple interface, featuring large buttons for structured navigation and a voice interface for free speech interaction.
*   **Backend API**: The central point of communication between the frontend and the agentic backend.
*   **Agent Orchestrator (Aurora)**: The central intelligence that interprets user intent and routes requests to the appropriate specialized agent.
*   **Specialized Agents**: A suite of agents, each with a specific responsibility, such as orientation, identity, or emotional regulation.
*   **Database**: A simple and structured database to store memories, relationships, events, and cognitive metrics.
*   **Blob Storage**: For storing binary data like photos and audio messages.
*   **Guardrail Engine**: A safety layer that all messages pass through to ensure the tone is gentle and not harsh.

### Technology Stack:

*   **Speech-to-Text/Text-to-Speech**: Azure Speech Services
*   **AI Reasoning and Language Understanding**: Azure OpenAI
*   **Data Storage**: SQLite for structured data.
*   **File Storage**: Azure Blob Storage for photos and audio.

### Operating Modes:

The system has two primary operating modes:

1.  **Mode A - Structured Navigation (Button Mode)**: This mode is used when the user interacts with predefined buttons. It's a fast, stable, and controlled interaction that doesn't require advanced AI reasoning. The flow is direct: `Button Tap -> Aurora -> Correct Agent -> Stored Information -> Response`.

2.  **Mode B - Free Speech Mode**: This mode is activated when the user speaks naturally. It involves a more complex workflow where the user's voice is converted to text, analyzed for intent and emotion by Aurora, and then routed to the appropriate agent. This mode enables emotional understanding, anxiety detection, and context-aware responses.

## 2. Agents

The Cognitive Mesh consists of seven specialized agents:

1.  **Aurora - The Orchestrator**: The central coordinator that analyzes user intent and emotional state to route requests to the correct agent. It does not store memory but directs intelligence.

2.  **Harbor - The Orientation Agent**: Responsible for keeping the patient grounded by answering questions about time, date, location, and daily schedules. It is designed to handle repeated questions gently.

3.  **Roots - The Identity & Relationship Agent**: Protects the user's relational identity by answering questions about people, relationships, and shared memories.

4.  **Solace - The Emotional Intelligence Agent**: Detects and regulates emotional distress by monitoring tone of voice, word patterns, and anxiety signals. It can activate a "Calm Mode" or alert a caregiver if needed.

5.  **Echo - The Memory Layer Agent**: Responsible for long-term memory preservation. It stores conversation history, tracks emotional trends, and detects cognitive patterns to enable predictive anxiety detection.

6.  **Guardian - The Caregiver Agent**: Acts as a co-pilot for the caregiver, providing daily cognitive summaries, emotional trend insights, and escalation alerts through a simple analytics dashboard.

7.  **Legacy - The Story Continuity Agent**: Maintains the user's life narrative by gently reinforcing personal history and stories when the user talks about their past.

## 3. Tools

The agents utilize a set of tools to perform their functions:

*   **Azure Speech**: For converting spoken language to text and vice-versa.
*   **Azure OpenAI**: For natural language understanding, intent recognition, and emotional analysis.
*   **SQLite Database**: To read and write structured data such as user profiles, relationships, events, and conversation history.
*   **Azure Blob Storage**: For storing and retrieving photos and audio files associated with memories and relationships.

## 4. Workflows

### Patient Workflows:

*   **Structured Interaction**:
    1.  User taps a button (e.g., "Where am I?").
    2.  Request is sent to Aurora.
    3.  Aurora routes to the appropriate agent (e.g., Harbor).
    4.  The agent retrieves information from the database.
    5.  A calm response is generated and displayed.

*   **Free Speech Interaction**:
    1.  User speaks to the app.
    2.  Azure Speech converts voice to text.
    3.  Aurora analyzes the text for intent and emotion.
    4.  Aurora routes to the correct agent.
    5.  The agent processes the request and generates a response.
    6.  The response is spoken back to the user.

*   **Anxious Interaction**:
    1.  User expresses fear or anxiety.
    2.  Aurora detects high anxiety and routes to Solace.
    3.  Solace provides a reassuring response.
    4.  If anxiety is very high, Calm Mode is activated, or a caregiver is alerted.

### Caregiver Workflows:

*   **Adding Information**:
    1.  Caregiver fills out a form to add family information.
    2.  Data is saved to the database and blob storage.
    3.  This information is then available to the agents.

*   **Viewing Insights**:
    1.  Caregiver opens the "Insights" dashboard.
    2.  The Guardian agent collects and analyzes trend data from the Echo agent.
    3.  A summary of cognitive and emotional trends is presented.

## 5. Project Ideas

*   **Frontend Development**: Create the user interface for the patient and caregiver dashboards based on the described functionality.
*   **Backend Development**: Implement the backend API and the agentic workflows.
*   **Database and Storage Setup**: Set up and manage the SQLite database and Azure Blob Storage.
*   **Agent Implementation**: Develop and train the individual agents based on the provided prompts and specifications.
*   **Testing and Evaluation**: Create a framework for testing the system's performance, accuracy, and emotional safety.

## 6. Development Approaches

A phased, iterative approach is recommended to manage complexity and ensure a high-quality, safe, and robust application.

### Phase 1: Foundation and Core Infrastructure

1.  **Project Setup**:
    *   Initialize a Git repository for version control.
    *   Create the directory structure for the backend service, including folders for agents, workflows, and tools (`src/agents`, `src/workflow`, `src/tools`).
    *   Set up a Python virtual environment and create a `requirements.txt` file for dependencies.

2.  **Infrastructure Setup**:
    *   Provision core Azure resources: Azure Blob Storage for media and Azure AI Services (for Speech and OpenAI).
    *   Define the SQLite database schema for all required tables (Users, Relationships, Events, Interactions, CognitiveMetrics). Create an initialization script.

3.  **Backend API Scaffolding**:
    *   Implement a basic web server (e.g., using Flask or FastAPI).
    *   Create an initial API endpoint (e.g., `/api/health`) to verify the server is running.

### Phase 2: Implement the First End-to-End Workflow (Structured Navigation)

1.  **Implement the Simplest Agent (Harbor)**:
    *   Start with the `Harbor` (Orientation) agent as it has clear, structured data dependencies.
    *   Implement the logic for `Harbor` to connect to the SQLite database and retrieve orientation information (location, date, events).

2.  **Develop a Basic Orchestrator (Aurora)**:
    *   Create a simplified version of `Aurora` that can handle a direct request from a button press. For this phase, it can directly route any "where am I" type request to `Harbor` without complex AI reasoning.

3.  **Build the Workflow**:
    *   Implement the "Structured Navigation" (Button Mode) workflow.
    *   Create an API endpoint (e.g., `/api/interact/button`) that takes a button identifier.
    *   This endpoint should pass the request to `Aurora`, which then calls `Harbor`, gets the response, and returns it.

4.  **Introduce the Guardrail Engine**:
    *   Create a basic `Guardrail Engine` as a function or class that all responses must pass through. Initially, it can perform simple checks, like ensuring no negative keywords are present.

### Phase 3: Introduce Free Speech and Emotional Intelligence

1.  **Integrate Speech Services**:
    *   Integrate Azure Speech SDK for speech-to-text conversion in a test client or frontend.

2.  **Enhance the Orchestrator (Aurora)**:
    *   Upgrade `Aurora` to call the Azure OpenAI service.
    *   Use the `agents and prompts.md` document to build the system prompt for `Aurora` to perform intent classification and emotional analysis. It should now be able to distinguish between different types of questions (e.g., orientation vs. identity).

3.  **Implement a Second Agent (Roots)**:
    *   Develop the `Roots` (Identity & Relationship) agent.
    *   Implement its logic to fetch data from the database and photo URLs from Azure Blob Storage.

4.  **Implement the Solace Agent**:
    *   Develop the `Solace` (Emotional Intelligence) agent. This is a critical safety component.
    *   Implement its logic to detect distress signals and provide calming, reassuring responses.
    *   Integrate the escalation logic to flag for a caregiver alert.

### Phase 4: Add Memory, Story, and Caregiver Features

1.  **Implement the Memory Layer (Echo)**:
    *   Develop the `Echo` agent. This agent will not respond to the user but will be called by other agents to log interactions.
    *   Implement the logic to write conversation history, emotional scores, and repetition counts to the `Interactions` and `CognitiveMetrics` tables.

2.  **Develop Legacy and Guardian Agents**:
    *   Implement the `Legacy` (Story Continuity) agent to reinforce the user's personal narrative.
    *   Implement the `Guardian` (Caregiver) agent, which reads from the `CognitiveMetrics` table (populated by `Echo`) to generate summaries and trends.

3.  **Build the Caregiver Dashboard API**:
    *   Create API endpoints for the caregiver dashboard to add/edit user and relationship data.
    *   Create an endpoint that allows the caregiver to request insights from the `Guardian` agent.

### Phase 5: Testing, Refinement, and Deployment

1.  **Comprehensive Testing**:
    *   Write unit tests for each agent and tool.
    *   Write integration tests for each workflow.
    *   Perform end-to-end testing with a sample frontend application.
    *   Focus on "red team" testing: try to elicit unsafe or incorrect responses to test the guardrails.

2.  **Deployment**:
    *   Containerize the application using Docker.
    *   Deploy the backend service to a suitable Azure service (e.g., Azure App Service or Azure Container Apps).

3.  **Monitoring and Iteration**:
    *   Set up logging and monitoring to track the performance and behavior of the agents in production.
    *   Use this data to iteratively refine the agent prompts, logic, and guardrails.

## 7. Prerequisites

*   An Azure subscription to use Azure Speech and Azure OpenAI services.
*   A development environment with Python for the backend.
*   Familiarity with building applications that interact with REST APIs.
*   Knowledge of database management (SQLite).

## 8. Best Practices

*   **Privacy and Security**: Ensure all user data is handled securely and privately.
*   **Ethical AI**: Adhere to ethical AI principles, especially when dealing with a vulnerable user group. The system should never diagnose or replace professional medical advice.
*   **Clear and Simple Language**: All user-facing communication should be simple, clear, and gentle.
*   **Robust Error Handling**: Implement robust error handling to ensure the system is reliable and never admits uncertainty to the patient.
*   **Regularly Update Prompts**: The prompts for the agents should be regularly reviewed and updated to improve their performance and adapt to new findings.

## 9. Requirements

*   **Functional Requirements**:
    *   User and caregiver authentication.
    *   Patient-facing UI with button and voice input.
    *   Caregiver-facing dashboard for data entry and insights.
    *   Implementation of all seven agents with their specified functionalities.
    *   Integration with Azure services.
*   **Non-Functional Requirements**:
    *   **High Availability**: The system should be highly available and reliable.
    *   **Low Latency**: Responses, especially in free speech mode, should have low latency to feel natural.
    *   **Scalability**: The architecture should be scalable to handle multiple users.
    *   **Security**: Strong security measures to protect sensitive user data.

## 10. Evaluation

*   **Agent Performance**:
    *   **Intent Recognition Accuracy**: Measure how accurately Aurora routes requests.
    *   **Response Relevance**: Evaluate the relevance and correctness of the agents' responses.
    *   **Emotional Tone**: Assess whether the tone of the responses is consistently calm and reassuring.
*   **User Experience**:
    *   **Ease of Use**: Gather feedback from users and caregivers on the ease of use of the application.
    *   **Emotional Impact**: Assess the emotional impact of the application on patients. Does it reduce anxiety and confusion?
*   **System Metrics**:
    *   **Response Time**: Measure the latency of the system.
    *   **Uptime**: Track the availability of the service.

## 11. Resources

*   **Azure Portal**: For managing Azure services.
*   **Azure AI Studio**: For developing and managing Azure OpenAI models and deployments.
*   **Python**: For backend development.
*   **SQLite Documentation**: For database management.
*   **VS Code**: As the recommended IDE for development.
*   **GitHub**: For version control.
