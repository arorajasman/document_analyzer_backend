from typing import List
from typing_extensions import TypedDict, Annotated

class RequirementsResponseSchema(TypedDict):

    requirements: Annotated[List[str], "List of requirements of the customer in string format"]