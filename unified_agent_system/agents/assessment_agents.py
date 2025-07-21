
from crewai import Agent
from ..tools.assessment_tools import BigFiveAssessmentTool, EnneagramAssessmentTool

# Create instances of the tools that our agent will use
big_five_tool = BigFiveAssessmentTool()
enneagram_tool = EnneagramAssessmentTool()

class AssessmentAgents:
    """
    A class to define and manage all agents related to psychological assessment.
    """
    def psychological_assessor(self) -> Agent:
        """
        Defines the primary agent responsible for conducting psychological assessments.
        This agent uses specialized tools to analyze text based on different frameworks.
        """
        return Agent(
            role="Expert Psychological Assessor",
            goal="Analyze the provided text to determine the user's personality profile based on multiple psychological frameworks (Big Five, Enneagram).",
            backstory=(
                "You are a highly trained psychological analyst with expertise in linguistic patterns and personality theory. "
                "You can accurately assess personality traits from written text, providing detailed and nuanced insights. "
                "You are objective, precise, and rely solely on the evidence within the text."
            ),
            tools=[
                big_five_tool,
                enneagram_tool
            ],
            allow_delegation=False,
            verbose=True,
            memory=True
        )

# You can also define other agents here, for example:
#
# def validation_agent(self) -> Agent:
#     return Agent(
#         role="Assessment Validator",
#         goal="Cross-reference and validate the findings of the primary assessor to ensure accuracy and consistency.",
#         backstory="You are a meticulous quality assurance specialist...",
#         tools=[...]
#     )
