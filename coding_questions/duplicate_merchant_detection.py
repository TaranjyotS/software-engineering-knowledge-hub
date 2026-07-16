'''
Duplicate Merchant Detection

Part 1: Linking Merchant Accounts
---------------------------------
We want to enhance user experience and decision-making by discovering preexisting relationships within merchant data.
Merchants can be clustered based on shared attributes. Given a list of merchants, where each merchant is represented by a
unique ID and a map of attributes, identify the merchants that are directly linked to a given merchantId. Two merchants are 
considered directly linked if they share at least one attribute with an identical value.

Example:
    Merchant of interest: m1
    Expected output: ["m2", "m3", "m6", "m8"]

Part 2: Soft Links
------------------
In a real-world scenario, identical information in a single field does not always justify a direct linkage decision. In this 
part, matching information from multiple fields is used to build a confidence score to make the link decision. If merchantA 
and merchantB have multiple identical fields, add the confidence score for each identical field and compare the total score to 
a confidence threshold. If the total confidence score is at least the threshold value, then the accounts are directly linked.

Example:
    Confidence levels:
        companyName: 50
        email: 30
        phone: 25

    Required link formation confidence level: 55
    Merchant of interest: m1
    Expected output: ["m2"]
'''

def find_related_merchants_verbose(merchants, merchant_of_interest):
    """
    Part 1: Direct links using at least one identical attribute value.

    This is the earlier version with the explicit is_related boolean.

    A merchant is directly linked to the merchant of interest if it shares at
    least one identical non-empty attribute value, excluding merchantId.
    """
    # First, find the merchant record corresponding to the requested ID.
    target_merchant = None

    for merchant in merchants:
        if merchant["merchantId"] == merchant_of_interest:
            target_merchant = merchant
            break

    # If the merchant does not exist, there are no related merchants.
    if target_merchant is None:
        return []

    related_merchants = []

    # Compare each merchant with the merchant of interest.
    for merchant in merchants:
        # A merchant should not be considered related to itself.
        if merchant["merchantId"] == merchant_of_interest:
            continue

        is_related = False

        # Compare all target attributes except the unique merchant ID.
        for attribute, target_value in target_merchant.items():
            if attribute == "merchantId":
                continue

            # Missing or empty values should not create a relationship.
            if target_value is None or target_value == "":
                continue

            if merchant.get(attribute) == target_value:
                is_related = True
                break

        if is_related:
            related_merchants.append(merchant["merchantId"])

    return related_merchants


def find_related_merchants(merchants, merchant_of_interest):
    """
    Part 1: Direct links using at least one identical attribute value.

    This is the simplified version without the is_related flag.

    A merchant is directly linked to the merchant of interest if it shares at
    least one identical non-empty attribute value, excluding merchantId.
    """
    target_merchant = None

    for merchant in merchants:
        if merchant["merchantId"] == merchant_of_interest:
            target_merchant = merchant
            break

    if target_merchant is None:
        return []

    related_merchants = []

    for merchant in merchants:
        if merchant["merchantId"] == merchant_of_interest:
            continue

        for attribute, target_value in target_merchant.items():
            if attribute == "merchantId":
                continue

            if target_value is None or target_value == "":
                continue

            if merchant.get(attribute) == target_value:
                related_merchants.append(merchant["merchantId"])
                break

    return related_merchants


def find_related_merchants_with_confidence(
    merchants,
    merchant_of_interest,
    confidence_levels,
    required_confidence,
):
    """
    Part 2: Soft links using confidence scores.

    A merchant is directly linked to the merchant of interest if the sum of
    confidence scores for identical matching fields is at least the required
    threshold.

    Only fields explicitly present in confidence_levels participate.
    """
    # Find the complete record for the merchant of interest.
    target_merchant = None

    for merchant in merchants:
        if merchant["merchantId"] == merchant_of_interest:
            target_merchant = merchant
            break

    # If the requested merchant does not exist, no links can be calculated.
    if target_merchant is None:
        return []

    related_merchants = []

    # Compare every other merchant against the target merchant.
    for merchant in merchants:
        if merchant["merchantId"] == merchant_of_interest:
            continue

        confidence_score = 0

        # Only fields explicitly present in the confidence map participate.
        for field, confidence in confidence_levels.items():
            target_value = target_merchant.get(field)
            candidate_value = merchant.get(field)

            # Missing or empty values should not create a relationship.
            if target_value is None or target_value == "":
                continue

            if candidate_value == target_value:
                confidence_score += confidence

                # No need to check more fields after reaching the threshold.
                if confidence_score >= required_confidence:
                    related_merchants.append(merchant["merchantId"])
                    break

    return related_merchants


MERCHANTS = [
    {
        "merchantId": "m1",
        "companyName": "Ozan's carpentry",
        "email": "o@carpentry.com",
        "phone": "pn1",
    },
    {
        "merchantId": "m2",
        "companyName": "Ozan's carpentry",
        "email": "ozan@carpentry.com",
        "phone": "pn1",
    },
    {
        "merchantId": "m3",
        "companyName": "O's carpentry",
        "email": "o@carpentry.com",
        "phone": "pn3",
    },
    {
        "merchantId": "m4",
        "companyName": "Leo's hot sauce shop",
        "email": "l@hotsauce.com",
        "phone": "pn4",
    },
    {
        "merchantId": "m5",
        "companyName": "Leo's hot sauce shop",
        "email": "leo@hotsauce.com",
        "phone": "pn5",
    },
    {
        "merchantId": "m6",
        "companyName": "Leo's hot sauce shop",
        "email": "leo@hotsauce.com",
        "phone": "pn1",
    },
    {
        "merchantId": "m7",
        "companyName": "Julia's flowers",
        "email": "julia@flowers.com",
        "phone": "pn6",
    },
    {
        "merchantId": "m8",
        "companyName": "Leo's hot sauce shop",
        "email": "ozan@carpentry.com",
        "phone": "pn1",
    },
    {
        "merchantId": "m9",
        "companyName": "Leo's hot sauce shop",
        "email": "ozan@carpentry.com",
        "phone": "pn7",
    },
]


def run_examples():
    """
    Run Part 1 and Part 2 examples from the prompt.
    """
    part1_verbose_result = find_related_merchants_verbose(MERCHANTS, "m1")
    print("Part 1 verbose:", ", ".join(part1_verbose_result))
    assert part1_verbose_result == ["m2", "m3", "m6", "m8"]

    part1_result = find_related_merchants(MERCHANTS, "m1")
    print("Part 1 simplified:", ", ".join(part1_result))
    assert part1_result == ["m2", "m3", "m6", "m8"]

    confidence_levels = {
        "companyName": 50,
        "email": 30,
        "phone": 25,
    }

    part2_result = find_related_merchants_with_confidence(
        merchants=MERCHANTS,
        merchant_of_interest="m1",
        confidence_levels=confidence_levels,
        required_confidence=55,
    )

    print("Part 2 confidence:", ", ".join(part2_result))
    assert part2_result == ["m2"]

    print("All examples passed.")


if __name__ == "__main__":
    run_examples()
