import re

def parse_text(path: str) -> str:
    """
    Read the .txt file at provided path.
    Remove all unneeded symbols.
    Returns the string of lower case letters (plus 4 symbols).
    """
    # TODO: symbols that are passed through can be changed here (Right now we have these four: ,.-')
    # We can also join:
    # - and _ in one key
    # , and ; in one key
    # . and : in one key
    # ' and ? in one key
    pattern = r"[^a-zA-Z,.\-\:'\s]" 
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()
    content = re.sub(pattern, "", content)
    content = content.lower()
    content = content.replace(" ", "").replace("\n", "").replace("\t", "")
    return content
