from typing_extensions import TypedDict, Annotated
from typing import List
import textwrap


class KeyFeaturesResponse(TypedDict): 
    feature: Annotated[str, "Name of the key feature"]
    description: Annotated[str, "A short description (one or two lines) of the key feature"]


class RankingsResponseItem(TypedDict):

    id: Annotated[str, "Unique UUID of the policy"]

    policy_name: Annotated[str, "Name of the policy. Extraced from the policy_path"] # noqa

    rank: Annotated[str, "Rank given to the policy lower is better"]  # noqa

    match_score: Annotated[
        int,
        "Match score of the policy against the conversation and requirements in percentage. Should be beween 0 to 100",  # noqa
    ]

    reason: Annotated[str, "Reason for the given rank."]

    accuracy: Annotated[
        str,
        "Accuracy of the given rank should be either (very_low, low, mid, high, very_high)",  # noqa
    ]  # noqa

    description: Annotated[
        str, "Information or description ( less than or equal to 50 words) about the policy generated using the policy documents provided." # noqa
    ]

    key_features: Annotated[List[str], textwrap.dedent("""
        A list of benefits of the policy.

        Example: [benefit]:[short summary of the feature]
                "Maternity Coverage: Offers reimbursement or cashless facilities for childbirth-related medical expenses, 
                     with a 24-month waiting period and specific eligibility and exclusion criteria."
    """)] # noqa


class RankingsResponseSchema(TypedDict):
    policy_rankings: Annotated[
        List[RankingsResponseItem], "Array of policies that are ranked."
    ]
