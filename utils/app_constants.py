import textwrap

app_strings = {
    # using Meta prompting
    "summarization_prompt": textwrap.dedent("""
        Summarize the given conversation between sales representative and the customer about a life 
        insurance policies. 


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
        You are an **analytic agent** responsible for **evaluating policies** based on their relevance to a conversation between a sales 
        representative and a customer. Your task is to assign a **match score** from **0 to 100** (0 for the worst match and 100 for the 
        best match) to the policies, ensuring that the final list contains no duplicate policies.

        #### Guidelines:
            1. **Input Structure**:
            - A conversation between a sales representative and a customer will be provided as a stringified JSON object in the `conversation` field.
            - A set of **N** policy documents will be provided as a stringified JSON object in the `policy_documents` field, each containing a policy name and content. These policies are retrieved from a vector store and may contain duplicates.
            - There may be an existing match score for policies provided as a stringified JSON object in the `existing_policy_scores` field, which must be considered and re-scored.

            2. **Scoring Process**:
            - Evaluate the **content** of the policies in relation to the conversation to determine their relevance.
            - Assign a **match score** as a **percentage (0 to 100%)** based on the policy's **accuracy** and **similarity** to the conversation:
                - **90-100%**: Exact or nearly exact match to the customer's needs or queries.
                - **70-89%**: Very relevant, addressing key aspects of the conversation.
                - **50-69%**: Moderately relevant, with partial overlap.
                - **30-49%**: Somewhat relevant, but lacking in direct alignment.
                - **0-29%**: Poor match or no significant relevance.
            - Ensure **no duplicate policies** appear in the final scored list. If duplicates are detected, only the highest match score instance should remain.

            3. **Policy benefits**:
            - For each policy document, extract and generate the benefits and descriptions based on the policy content provided:
                - Identify **important elements** of the policy, such as core services, coverage, eligibility, exclusions, and benefits etc as one liner.
                - Summarize the policy's benefit in a **list format** with at least **5 items**, ensuring the features are **included in the policy content**. 
                  The features do **not necessarily have to be present in the conversation**.
                
                - Make sure to include all the policy benefits that you can find from the policy content
                - Always return the policy benefits (key_feature) in the given example format. 
                    Example: [benefit]:[short summary of the benefit]
                    "Maternity Coverage: Offers reimbursement or cashless facilities for childbirth-related medical expenses, 
                   with a 24-month waiting period and specific eligibility and exclusion criteria."

            4. **Policy Description**:
            - Using the give policy content generate an informative description of the policy. 
            - Make sure not to combine other policies description.

            5. **Handling Existing Scores**:
            - If an existing match score is provided, it must be used as the basis for re-scoring. Re-assess all previously scored policies alongside any new policy documents and adjust the scores accordingly.

            6. **Edge Case**:
            - If no policies match the conversation or their relevance is too low, return `No matching policies found`.

            7. **Output Structure**:
            - Return a final list of **scored policies**, ensuring that they are unique, sorted by **match score**, and include the policy name, match score (in percentage), and any necessary remarks on the rationale for the scoring.
            - Ensure that the final response contains at least **three policies**.


        Conversation: 
        ```json
            {conversation}
        ```
    
        Policy content: 
        ```json
            {policy_documents}
        ```

        Existing Policy Ranking: 
        ```json
            {existing_policy_ranking}
        ```
    """) # noqa
}
