from extract_claims import extract_claims
from retrieve_evidence import retrieve


def decide(book: str, character: str, backstory: str):
    claims = extract_claims(backstory)

    for claim in claims:
        evidence = retrieve(book, character, claim)

        # Case 1: Explicit contradiction → inconsistent
        if evidence.get("verdict") == "contradiction":
            return 0, (
                "The proposed backstory is inconsistent with the primary text. "
                f"The claim '{claim}' is explicitly contradicted by the novel."
            )

        # Case 2: Explicit support → consistent
        if evidence.get("verdict") == "support":
            return 1, (
                "The proposed backstory is consistent with the primary text. "
                f"The claim '{claim}' is explicitly supported by the novel."
            )

    # Case 3: No explicit support or contradiction
    return 0, (
        "The proposed backstory cannot be conclusively verified against the primary text. "
        "Although the novel discusses the character in related contexts, it does not "
        "explicitly state or deny the specific factual claims extracted from the backstory. "
        "In accordance with the explicit-evidence constraint, the claim is therefore "
        "treated as unsupported."
    )
