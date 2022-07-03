#
# data.py
#
# scp-author-page - Tools for generating my author page.
# Copyright (c) 2021-2022 Ammon Smith
#
# scp-author-page is available free of charge under the terms of the MIT
# License. You are free to redistribute and/or modify it under those
# terms. It is distributed in the hopes that it will be useful, but
# WITHOUT ANY WARRANTY. See the LICENSE file for more details.
#

import re

import toml

from .translations import get_translations
from .wikidot import normalize

SCP_NAME_REGEX = re.compile(r"SCP-[1-9]?[0-9]{3}(?:-(?:J|EX))?")


def load_data(data_path: str, log: bool = False) -> dict:
    with open(data_path) as file:
        if log:
            print(f"+ Loading {data_path}")

        data = toml.load(file)

    # Hydrate data according to structures
    if log:
        print(f"+ Hydrating {len(data['articles'])} article entries")

    for article in data["articles"]:
        name = article["name"]

        if "type" not in article:
            if SCP_NAME_REGEX.match(name):
                article["type"] = "scp"
            else:
                raise ValueError(f"No article type specified for '{name}'")

        if article["type"] == "goi-format":
            if "goi" not in article:
                raise ValueError(f"No GoI specified for goi-format document '{name}'")

        if "slug" not in article:
            article["slug"] = normalize(name)
            article["normal-slug"] = True

        if "title" not in article:
            article["title"] = name

        if "co-authors" not in article:
            article["co-authors"] = []

        if "contest" not in article:
            article["contest"] = None

        # Add snake_case version of kebab-case keys
        for kebab_key, value in tuple(article.items()):
            if "-" in kebab_key:
                snake_key = kebab_key.replace("-", "_")
                article[snake_key] = value
                del article[kebab_key]

        # Scrape translations from pages
        article["translations"] = get_translations(article["slug"], log)

    return data
