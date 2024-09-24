import textwrap

app_strings = {
    # using Meta prompting
    "summarization_prompt": textwrap.dedent("""
        Summarize the given conversation between sales representative and the customer about a life 
        insurance policies. Capture all the key points and return the requirement of the customer. 


        DO NOT MISS ANY KEY POINTS.

        <conversation> {conversation} </conversation>
    """),  # noqa

    "generate_requirements_prompt": textwrap.dedent("""
        Given a summary of conversation between sales representative and the customer generate the
        requiremets of the customer. The generated requirements should be returned as a list.

        Summary:
        <summary>{summary}</summary>

        Requirements:
    """),  # noqa

    "generate_ranking_prompt": textwrap.dedent("""
        You are an analytic agent that can rank the given policies that are more accurate and
        similar to the given conversation between the sale representative and the customer.
        You are given the conversation that is happened between the customer and sale person
        in the `<conversation></conversation>` tag.  You are also given the N number of
        policy documents (policy name and content of the policy) in <policy_documents> tag.
        The given policy is retrived from vector store so it may contain duplicates. But in the 
        final response DO NOT add any duplicate policies. Your task is to rank the policies with
        a store of 0 to 9 (0 for worst match to 9 for best match) based on the conversation. 
        You should response with atleast 3 policies ranked based on the above rules.
        In case you can't find the best matching policies return the response with 
        `No matching polices found`.

        Conversation:
        <conversation>
            {conversation}
        </conversation>

        Policy Documents:
        <policy_documents>
            {policy_documents}
        </policy_documents>

        Ranked Policies:
    """),  # noqa
}
