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

    "generate_requirements_prompt_v2": textwrap.dedent("""
        You are tasked with generating a list of customer requirements based on a summary of the conversation between a sales representative and the customer. 

        Guidelines:
        - Analyze the provided summary of the conversation.
        - Extract the key requirements expressed by the customer.
        - Return the requirements as a list in bullet-point format.

        Input:
        Summary:
        <summary>{summary}</summary>

        Output:
        Requirements:
    """),  # noqa

    "policy_ranking": textwrap.dedent("""
        You are an **analytic agent** tasked with **ranking policies** based on their relevance to a conversation between a sales representative and a customer. Your role is to assign a ranking from **0 to 9** (0 for worst match, 9 for best match) to the policies, ensuring no duplicate policies are present in the final ranked list.

        #### Guidelines:
        1. **Input Structure**:
        - A conversation between a sales representative and a customer will be provided as a stringified JSON object in the `conversation` field.
        - A set of **N** policy documents will be provided as a stringified JSON object in the `policy_documents` field, each containing a policy name and content. These policies are retrieved from a vector store and may contain duplicates.
        - There may be an existing ranking of policies provided as a stringified JSON object in the `existing_policy_ranking` field, which must be considered and re-ranked.

        2. **Ranking Process**:
        - Evaluate the **content** of the policies in relation to the conversation to determine their relevance.
        - Assign a score from **0 to 9** based on the policy's **accuracy** and **similarity** to the conversation:
            - **9**: Exact or nearly exact match to the customer's needs or queries.
            - **7-8**: Very relevant, addressing key aspects of the conversation.
            - **5-6**: Moderately relevant, with partial overlap.
            - **3-4**: Somewhat relevant, but lacking in direct alignment.
            - **0-2**: Poor match or no significant relevance.
        - Ensure **no duplicate policies** appear in the final ranked list. If duplicates are detected, only the highest-ranked instance should remain.
        
        3. **Handling Existing Rankings**:
        - If an existing ranking is provided, it must be used as the basis for re-ranking. Re-assess all previously ranked policies alongside any new policy documents and adjust the scores accordingly.
        
        4. **Edge Case**:
        - If no policies match the conversation or their relevance is too low, return `No matching policies found`.

        5. **Output Structure**:
        - Return a final list of **ranked policies**, ensuring that they are unique, sorted by relevance, and include the policy name, score, and any necessary remarks on the rationale for the ranking.

        Conversation: 
        ```json
            {conversation}
        ```
    
        Policy Documents: 
        ```json
            {policy_documents}
        ```

        Existing Policy Ranking: 
        ```json
            {existing_policy_ranking}
        ```
    """) # noqa
}
