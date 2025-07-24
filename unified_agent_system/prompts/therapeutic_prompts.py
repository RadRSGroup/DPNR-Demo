
class TherapeuticPrompts:
    """
    A collection of prompts for guiding therapeutic agents and processes.
    """
    def ifs_dialogue_prompt(self, part_name: str) -> str:
        """
        Creates a prompt to begin a dialogue with an identified internal part.
        """
        return f"You are now speaking to the user's '{part_name}' part. Greet it with compassion and ask it: 'What is your role? What are you trying to protect the user from?'"

    def shadow_integration_prompt(self, shadow_pattern: str) -> str:
        """
        Creates a prompt to help the user integrate a discovered shadow pattern.
        """
        return f"The user has identified a shadow pattern of '{shadow_pattern}'. Guide them to understand the positive intention behind this pattern. Ask them: 'In what ways has this pattern, while sometimes challenging, also tried to serve or protect you? What strength is at its core?'"

    def pardes_reflection_prompts(self, user_insight: str) -> Dict[str, str]:
        """
        Generates a dictionary of prompts for each of the four levels of PaRDeS reflection.
        """
        return {
            "pshat": (
                f"The user shared this insight: '{user_insight}'. "
                f"Provide a Pshat (literal, simple) reflection. Summarize the practical meaning of their insight in one clear sentence."
            ),
            "remez": (
                f"The user's insight is: '{user_insight}'. "
                f"Provide a Remez (hinted, allegorical) reflection. What is the underlying emotional or behavioral pattern being hinted at here? Use a metaphor to describe it."
            ),
            "drash": (
                f"The user's insight is: '{user_insight}'. "
                f"Provide a Drash (interpretive, homiletic) reflection. Reframe this insight in the context of a larger life lesson or a universal human story. How does this connect to their personal growth journey?"
            ),
            "sod": (
                f"The user's insight is: '{user_insight}'. "
                f"Provide a Sod (secret, mystical) reflection. Connect this insight to a deep, universal, or soul-level truth. Speak to the essence of their being. What is the soul trying to realize through this experience?"
            )
        }
