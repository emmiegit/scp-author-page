#
# wikidot.py
#
# scp-author-page - Tools for generating my author page.
# Copyright (c) 2021 Ammon Smith
#
# scp-author-page is available free of charge under the terms of the MIT
# License. You are free to redistribute and/or modify it under those
# terms. It is distributed in the hopes that it will be useful, but
# WITHOUT ANY WARRANTY. See the LICENSE file for more details.
#

# Based on https://github.com/scpwiki/wikidot-normalize/blob/master/src/normal.rs

import re

NON_NORMAL_REGEX = re.compile(r"[^a-z0-9\-:-]")
MULTIPLE_DASHES = re.compile(r"-{2,}")
MULTIPLE_COLONS = re.compile(r":{2,}")
COLON_DASH = re.compile(r"(:-)|(-:)")
UNDERSCORE_DASH = re.compile(r"(_-)|(-_)")
LEADING_OR_TRAILING_COLON = re.compile(r"(^:)|(:$)")


def normalize(text: str) -> str:
    # Remove leading and trailing whitespace
    text = text.strip()

    # Remove leading slash, if present
    if text.startswith("/"):
        text = text[1:]

    # Lowercase ASCII alphabetic characters
    text = text.lower()

    # Replace non-nomral characters
    text = NON_NORMAL_REGEX.sub("-", text)

    # Merge multiple dashes and colons into one.
    text = MULTIPLE_DASHES.sub("-", text)
    text = MULTIPLE_COLONS.sub(":", text)

    # Remove any leading or trailing dashes next to colons or underscores.
    text = COLON_DASH.sub(":", text)
    text = UNDERSCORE_DASH.sub("_", text)

    # Remove any leading or trailing colons.
    text = LEADING_OR_TRAILING_COLON.sub("", text)

    # Remove explicit _default category, if it exists.
    if text.startswith("_default:"):
        text = text[9:]

    return text
