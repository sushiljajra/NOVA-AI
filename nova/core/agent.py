import json
from typing import List, Dict, Any, Optional
from nova.config import SYSTEM_PROMPT, CANDIDATE_GEMINI_MODELS
from nova.tools import AVAILABLE_TOOLS, TOOL_MAP
from nova.core.ui import print_warning

class NovaAgent:
    """Base class for ECLIPSE brain implementations."""
    def interact(self, user_input: str) -> str:
        raise NotImplementedError

class GeminiNovaAgent(NovaAgent):
    def __init__(self, api_key: str, model: str = "gemini-3.5-flash-lite"):
        from google import genai
        from google.genai import types

        self.client = genai.Client(api_key=api_key)
        self.types = types
        self.candidate_models = list(CANDIDATE_GEMINI_MODELS)
        if model not in self.candidate_models:
            self.candidate_models.insert(0, model)
            
        self.active_model = self.candidate_models[0]
        self.chat = None
        self._init_chat(self.active_model)

    def _init_chat(self, model_name: str):
        self.active_model = model_name
        self.chat = self.client.chats.create(
            model=model_name,
            config=self.types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                tools=AVAILABLE_TOOLS,
                temperature=0.2,
            )
        )

    def interact(self, user_input: str) -> str:
        last_exception = None

        # Try active model, fallback to alternative candidate models if 404, 503, or 429 quota exhaustion
        for idx in range(len(self.candidate_models)):
            current_model = self.active_model
            try:
                response = self.chat.send_message(user_input)
                return response.text or "Operation completed, Sir."

            except Exception as e:
                err_str = str(e)
                last_exception = e
                # Check for 404 (deprecated), 503 (high demand), or 429 (quota exceeded)
                is_recoverable = any(code in err_str for code in [
                    "404", "503", "429",
                    "RESOURCE_EXHAUSTED", "UNAVAILABLE", "NOT_FOUND", "Quota exceeded"
                ])

                if is_recoverable:
                    next_models = [m for m in self.candidate_models if m != current_model]
                    if next_models:
                        next_model = next_models[0]
                        print_warning(f"Engine {current_model} rate-limited or unavailable. Rerouting to {next_model}...")
                        # Rotate candidates so current failed model is moved to back
                        self.candidate_models.remove(current_model)
                        self.candidate_models.append(current_model)
                        self._init_chat(next_model)
                        continue
                raise e

        if last_exception:
            raise last_exception
        return "I was unable to establish a stable neural connection to the model, Sir."


class OpenAINovaAgent(NovaAgent):
    def __init__(self, api_key: str, model: str = "gpt-4o", base_url: Optional[str] = None):
        from openai import OpenAI
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    def interact(self, user_input: str) -> str:
        self.messages.append({"role": "user", "content": user_input})
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages
        )
        msg = response.choices[0].message
        self.messages.append(msg.model_dump(exclude_unset=True))
        return msg.content or "Operation completed, Sir."

