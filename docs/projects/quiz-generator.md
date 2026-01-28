# AI-Powered Quiz Generator

An automated quiz system using LangGraph agents. It generates questions, checks if they're any good, and keeps refining them until they meet quality standards.

[Demo Video](https://youtube.com/watch?v=0o1s1O7-G_w) | [GitHub](https://github.com/hasan-ston/Notes_app)

## How It Works

Built a LangGraph agent that generates quiz questions from input material, scores them on clarity and relevance, then re-prompts with feedback if they're not good enough. This feedback loop produces way better questions than just asking once and calling it done.

## Technical Details

**LangGraph Agent Architecture**

The agent runs through multiple nodes:
1. **Generation Node:** Creates quiz questions from the input
2. **Evaluation Node:** Scores questions on clarity, difficulty, and relevance
3. **Refinement Node:** Figures out what's wrong with bad questions and generates improvement suggestions
4. **Decision Node:** Checks if we've hit the quality threshold or need another pass

LangGraph's state management made this way easier to build than I expected. Before using it, I thought managing agent workflows would be a mess.

**OCR Integration**

Added OCR with pyMuPDF so users can upload photos of textbook pages or handwritten notes. OCR quality is hit or miss depending on the image, so I added text preprocessing to clean up garbage before sending it to the LLM. Handwritten notes are especially rough.

**Django Backend**

Built the web interface in Django to handle uploads, run the agent, and store quizzes. Used async views so the long-running agent workflow doesn't block everything else. Without that, the whole app would freeze while generating quizzes.

## What I Learned

Agent frameworks like LangGraph make complex workflows manageable - the state management handles most of the annoying parts. Iterative prompting works way better than single-shot generation, but you need good evaluation metrics or it just spins in circles. OCR is messier than it looks - most of the work is cleaning up the extracted text. Django's async views are essential for anything that takes more than a few seconds. Designing feedback loops for LLMs is tricky because you need to balance quality improvement with not wasting API calls.
