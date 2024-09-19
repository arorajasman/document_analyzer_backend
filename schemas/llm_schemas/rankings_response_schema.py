from typing_extensions import TypedDict, Annotated


class RankingsResponseSchema(TypedDict):

    policy_name: Annotated[str, "Name of the policy."]

    rank: Annotated[str, "Rank given to the policy (should be between 0 and 9)"] # noqa

    reason: Annotated[str, "Reason for the given rank."]

    accuracy: Annotated[str, 'Accuracy of the given rank should be either (very_low, low, mid, high, very_high)'] # noqa
