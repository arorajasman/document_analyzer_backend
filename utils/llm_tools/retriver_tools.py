from langchain.tools.retriever import create_retriever_tool


def policy_retriver_tool(retriver): 
    return create_retriever_tool(
        retriver,
        "policy_search_retriver",
        "Search for information about policies. For any policy related tasks you must use this tool", # noqa
    )
