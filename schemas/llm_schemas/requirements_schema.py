from typing import List
from typing_extensions import TypedDict, Annotated


class RequirementsResponseSchema(TypedDict):

    requirements: Annotated[List[str], 
    """List of requirements of the customer based on the conversation in string format.
       Should be in a single line. 
       Example 
         Maternity benefits coverage
    """] # noqa