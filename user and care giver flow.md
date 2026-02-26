PART 1: USER FLOW — PATIENT PERSPECTIVE 

Let’s imagine Raj is using With You. 

 

🧍‍♂️ Scenario 1: Raj Taps a Button 

Raj opens the app. 

He sees large buttons: 

Where am I? 

Family Photos 

Who is visiting today? 

Calm Mode 

He taps: 

👉 “Where am I?” 

Shape 

What Happens Behind the Scenes (Simple Explanation) 

The app sends the request to the Backend API. 

The Backend sends it to Aurora (the Orchestrator Agent). 

Aurora sees this is a structured button press. 

Aurora directly calls Harbor (Orientation Agent). 

Harbor looks inside SQLite DB (long-term memory database). 

It finds: 

Home location 

Move year 

Harbor creates a calm answer: 

“You’re at home in Chennai. You moved here in 2018. You’re safe.” 

Before sending it back, the message passes through the Guardrail Engine. 

It checks tone. 

Makes sure nothing harsh is said. 

The message is shown on screen. 

If voice is enabled, Azure Speech reads it out loud. 

That’s it. 

No heavy AI reasoning needed. 

Simple. Fast. Safe. 

Shape 

🎤 Scenario 2: Raj Speaks Freely 

Raj says: 

“Is Anna coming today?” 

Now this is different. 

Shape 

What Happens Behind the Scenes 

Step 1 
Raj speaks into the app. 

Step 2 
Azure Speech converts voice → text. 

Step 3 
Text goes to Aurora. 

Step 4 
Aurora uses Azure OpenAI to: 

Understand the meaning 

Detect emotion 

Identify intent 

Azure OpenAI tells Aurora: 

Intent: event question 

Emotion: neutral 

Step 5 
Aurora routes request to: 
Harbor (Orientation Agent) 

Step 6 
Harbor checks SQLite DB: 

Finds Anna’s visit scheduled at 5 PM 

Step 7 
Harbor creates response: 

“Anna is coming today at 5 PM.” 

Step 8 
Message goes through Guardrail Engine. 

Step 9 
Response sent back. 
If voice mode → Azure Speech reads it aloud. 

Shape 

😟 Scenario 3: Raj Is Anxious 

Raj says: 

“I don’t know where I am… I feel scared.” 

Now emotional logic activates. 

Step 1 
Azure Speech → text 
Step 2 
Aurora uses Azure OpenAI 
Emotion score = high anxiety 

Step 3 
Aurora routes to: 
Solace (Emotional Agent) 

Step 4 
Solace: 

Reads recent interactions from SQLite DB 

Checks repetition pattern via Echo (Memory Intelligence Agent) 

Step 5 
Solace replies: 

“You’re at home. You’re safe. I’m here with you.” 

Step 6 
If anxiety is very high: 
Solace may trigger: 

Calm Mode (music/photo slideshow) 

Caregiver alert 

That is how emotional protection works. 

Shape 

🌿 PART 2: USER FLOW — CAREGIVER PERSPECTIVE 

Now let’s switch to Anna (the daughter). 

She opens the Caregiver Dashboard. 

Shape 

👩‍💻 Scenario 1: Adding Family Information 

Anna wants to add her brother. 

She fills a simple form: 

Name 

Relationship 

Short description 

Upload photo 

Upload voice message (optional) 

She clicks Save. 

Shape 

What Happens Behind the Scenes 

The Dashboard sends data to Backend API. 

Photo is stored in Azure Blob Storage. 

Text information is stored in SQLite DB. 

That data is now available for: 

Roots Agent (identity recognition) 

Harbor Agent (visit scheduling) 

Solace (emotional reinforcement) 

No AI needed here. 
Just structured data storage. 

Shape 

📊 Scenario 2: Viewing Raj’s Cognitive Trends 

Anna opens “Insights”. 

Behind the scenes: 

Guardian Agent collects: 

Anxiety trends 

Repetition frequency 

Orientation questions 

Guardian gets trend data from Echo Agent. 

Echo calculates: 

Weekly confusion spikes 

Emotional average 

Guardian presents summary: 

“Orientation questions increased this week.” 

“Anxiety stable.” 

Simple insights. 
No medical diagnosis. 
Just patterns. 

Shape 

🌿 PART 3: HOW BACKEND TECHNOLOGY WORKS (In Simple Terms) 

Let’s explain the backend like a story. 

Shape 

🧠 Aurora – The Brain Coordinator 

Aurora decides: 

What is the user asking? 

Which agent should respond? 

Is the user anxious? 

Should caregiver be alerted? 

Aurora uses: 
👉 Azure OpenAI for reasoning 

But Aurora does NOT store data. 
It only directs traffic. 

Shape 

🏠 Harbor – The Orientation Specialist 

Harbor answers: 

Date 

Location 

Visits 

Daily structure 

Reads data from: 
👉 SQLite DB 

Shape 

👨‍👩‍👧 Roots – The Identity Specialist 

Handles: 

“Who is this?” 

Family recognition 

Uses: 
👉 SQLite DB 
👉 Blob Storage (photos) 

Shape 

💬 Solace – The Emotional Specialist 

Handles: 

Fear 

Anxiety 

Reassurance 

Uses: 
👉 Azure OpenAI for gentle language 
👉 Echo for emotional history 

Shape 

📖 Legacy – Story Specialist 

Handles: 

Personal history 

Work life 

Life narrative continuity 

Reads: 
👉 SQLite DB 

Shape 

🧠 Echo – The Memory Intelligence Agent 

Echo watches everything. 

It: 

Logs interactions 

Tracks repetition 

Tracks anxiety patterns 

Calculates trends 

Echo writes into: 
👉 SQLite DB 

Echo helps Guardian generate reports. 

Shape 

👩 Guardian – Caregiver Insights Agent 

Guardian: 

Reads trend data from Echo 

Builds simple summary 

Shows caregiver dashboard insights 

Shape 

🌿 PART 4: Why This Architecture Is Balanced 

We use: 

Azure Speech → To make it easy to talk 
Azure OpenAI → To understand meaning 
SQLite DB → To store memory 
Blob Storage → To store photos and audio 
Agents → To separate responsibilities 

We do NOT overcomplicate with: 

Enterprise security layers 

Complex microservices 

20 databases 

Simple but intelligent. 

 

 FINAL SIMPLE SUMMARY 

For Patient: 

Talk or tap → System understands → Specialist agent answers → Calm response → Memory updated. 

For Caregiver: 

Upload structured data → Stored safely → Used by agents → View cognitive trends → Get alerts if needed. 

 