
def merge_software(software: list, new_software: list) -> list:
    """ Merge two lists of software actions

    Args:
        software (list(dict)): Original list to merge over
        new_software (list(dict)): new list to use to merge over

    Returns:
        list(dict): merged list of software actions
    """

    merge_software = []

    merge: dict = {}

    for original in software:

        merge.update({
            original['name']: original
        })

    for new in new_software:

        merge.update({
            new['name']: new
        })

    for key, value in merge.items():

        merge_software = merge_software + [ value ]

    return merge_software