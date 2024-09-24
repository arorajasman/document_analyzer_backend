from typing_extensions import TypedDict, Annotated
from typing import List


class RankingsResponseItem(TypedDict):

    policy_name: Annotated[str, "Name of the policy."]

    rank: Annotated[str, "Rank given to the policy lower is better"] # noqa

    match_score: Annotated[int, "Match score of the policy in percentage. Should be beween 0 to 100"]

    reason: Annotated[str, "Reason for the given rank."]

    accuracy: Annotated[str, 'Accuracy of the given rank should be either (very_low, low, mid, high, very_high)'] # noqa

    description: Annotated[str, 'A brief description of the policy fetch from the vector store.']

    key_features: Annotated[List[str], "A list of key features of the policy"]

class RankingsResponseSchema(TypedDict): 
    policy_rankings: Annotated[List[RankingsResponseItem], 'Array of policies that are ranked.']
