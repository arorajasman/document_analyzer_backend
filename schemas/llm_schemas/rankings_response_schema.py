from typing_extensions import TypedDict, Annotated
from typing import List


class RankingsResponseItem(TypedDict):

    id: Annotated[str, "Unique UUID of the policy"]

    policy_name: Annotated[str, "Name of the policy. Extraced from the policy_path"] # noqa

    rank: Annotated[str, "Rank given to the policy lower is better"]  # noqa

    match_score: Annotated[
        int,
        "Match score of the policy in percentage. Should be beween 0 to 100",  # noqa
    ]

    reason: Annotated[str, "Reason for the given rank."]

    accuracy: Annotated[
        str,
        "Accuracy of the given rank should be either (very_low, low, mid, high, very_high)",  # noqa
    ]  # noqa

    description: Annotated[
        str, "A brief description ( typically single paragraph ) of the policy generated using the policy documents. Don't get confused with key features" # noqa
    ]

    key_features: Annotated[List[str], "A list of key features of the policy. Per key feature should be a single sentence"] # noqa


class RankingsResponseSchema(TypedDict):
    policy_rankings: Annotated[
        List[RankingsResponseItem], "Array of policies that are ranked."
    ]
