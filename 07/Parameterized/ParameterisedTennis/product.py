import re


def determine_product(parsed_args):
    """ Determines product version and type of product to be registered

    Args:
        parsed_args (object): parsed user input

    Returns:
        (action-type (str), product-structure (object))
    """
    # RAS can not handle "/" and "+" in the URL. They are adding support for it.
    product_number = parsed_args.product_number.replace(" ", "").replace("/", "%2F")

    if parsed_args.arm_url:
        arm_url = parsed_args.arm_url.replace("+", "%2B")
        product_version = re.findall(r"\d+\.\d+\.\d+[+-]?\d*", arm_url)[0]
        product_version = product_version.replace("+", "%2B")
        arm_product = {
            "type": "arm",
            "arm-url": arm_url,
            "prod-number": product_number,
            "prod-version": product_version
        }
        return arm_product
    elif parsed_args.gerrit_url and \
            re.match(r'^[a-z]+\:\/\/[a-z]{6}.[a-z]{8}.(se|com)\/a\/[A-Z,a-z].*', parsed_args.gerrit_url):
        if parsed_args.gerrit_commit_id and re.match(r'(\d|\D){40}', parsed_args.gerrit_commit_id):
            git_product = {
                "type": "git",
                "git-url": parsed_args.gerrit_url,
                "commit-id": parsed_args.gerrit_commit_id,
                "prod-number": product_number,
                "prod-version": parsed_args.product_version
            }
            return git_product
        else:
            raise ValueError(f"Please pass a valid commit-id for the product, \
                                    current value is : {parsed_args.gerrit_commit_id}")
    else:
        raise ValueError(f"URL provided is not valid or incorrectly formatted {parsed_args.gerrit_url}")