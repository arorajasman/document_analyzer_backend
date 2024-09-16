# constant strings for the project
app_strings = {
    # using Meta prompting
    "summarization_prompt": """  
Summarize the given conversation between sales representative and the customer about a life 
insurance policies. Capture all the key points and return the requirement of the customer. 


DO NOT MISS ANY KEY POINTS.

<conversation> {conversation} </conversation>
""",  # noqa

    "generate_requirements_prompt": """
Given a summary of conversation between sales representative and the customer generate the requiremets 
of the customer. The generate requirements should be returned as a list.

Summary:
<summary>{summary}</summary>

Requirements:

    """,  # noqa
}
