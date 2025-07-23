class ReportingPrompts:
    @staticmethod
    def weekly_summary_description():
        return (
            "Synthesize the user's weekly interactions, assessments, and therapeutic insights "
            "into a comprehensive 'Weekly Soul Summary'. This summary should highlight key themes, "
            "progress, challenges, and emerging patterns from their engagement with various agents. "
            "Focus on actionable insights and compassionate reflection."
        )

    @staticmethod
    def weekly_summary_expected_output():
        return (
            "A well-structured 'Weekly Soul Summary' document, approximately 500-700 words, "
            "divided into sections such as: 'Key Insights from the Week', 'Progress & Growth Areas', "
            "'Challenges & Reflections', and 'Looking Ahead'. The tone should be encouraging, "
            "insightful, and deeply empathetic, reflecting the user's unique journey."
        )