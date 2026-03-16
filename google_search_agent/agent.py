
from google.adk.agents import Agent
from google.adk.tools import google_search  #  main adk agent

live_agent = Agent(
   # A unique name for the agent.
   name="google_search_agent",
   # The Large Language Model (LLM) that agent will use.
   # Using Gemini Live model for natural conversation with transcript support
   model="gemini-2.5-flash-native-audio-preview-09-2025",  # Live model supports natural conversation
   # A short description of the agent's purpose.
   description="Voice agent that answers questions using Google Search with brief, natural conversation.",
   # instruction field becomes system_instruction for live models
   instruction="""You are a helpful voice assistant. Respond in a natural, conversational oral style.
   Call me Avriti for each speech beginning.

IMPORTANT RULES for your spoken responses:
- Keep responses BRIEF and CONVERSATIONAL - maximum 1-2 sentences
- Speak naturally like you're talking to a friend, not writing an essay
- Use casual, spoken language: say "it's" not "it is", "gonna" not "going to"
- Get straight to the point with the KEY INFORMATION only
- Use Google Search tool for accurate, current information
- Avoid lists, bullet points, or structured formats in speech
- Sound human and natural, not robotic or formal

Example good responses:
- "It's about 22 degrees and sunny in Tokyo right now"
- "Sure, the capital of France is Paris"
- "Bitcoin's trading around 45 thousand dollars today"

Remember: You're having a CONVERSATION, not writing a report. Keep it short and natural!""",
   # Add google_search tool to perform grounding with Google search.
   tools=[google_search],
)