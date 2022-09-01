#
# translations.py
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

import requests

WIKIDOT_URL_REGEX = re.compile(r"https?://([a-z0-9\-]+)\.wikidot\.com/(.+)")

CROM_ENDPOINT = "https://api.crom.avn.sh/graphql"
CROM_WIKIDOT_URL = "http://scp-wiki.wikidot.com"
CROM_QUERY = """
query InterwikiQuery($url: URL!) {
    page(url: $url) {
        translations {
            url
        }
    }
}
"""

CROM_HEADERS = {
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

LANGUAGE_CODES = {
    "scp-wiki-cn": "CN",
    "scp-cs": "CS",
    "scp-wiki-de": "DE",
    "scp-el": "EL",
    "lafundacionscp": "ES",
    "fondationscp": "FR",
    "scp-idn": "ID",
    "scp-int": "INT",
    "fondazionescp": "IT",
    "scp-jp": "JP",
    "scpko": "KO",
    "scp-pl": "PL",
    "scp-pt-br": "PT",
    "scp-ru": "RU",
    "scp-th": "TH",
    "scp-ukrainian": "UA",
    "scp-vn": "VN",
    "scp-zh-tr": "ZH",
}


def get_translations(slug, log: bool = False):
    if log:
        print(f"+ Pulling translations for {slug}")

    # Make request
    r = requests.post(
        CROM_ENDPOINT,
        headers=CROM_HEADERS,
        json={
            "query": CROM_QUERY,
            "variables": {
                "url": f"{CROM_WIKIDOT_URL}/{slug}",
            },
        },
    )
    r.raise_for_status()
    response_data = r.json()
    translations = []

    if "errors" in response_data:
        raise ValueError(response_data["errors"])

    for data in response_data["data"]["page"]["translations"]:
        url = data["url"]
        match = WIKIDOT_URL_REGEX.fullmatch(url)
        if match is None:
            raise ValueError(f"Received Wikidot URL doesn't match regex: {url}")

        site_slug = match[1]
        translations.append(
            {
                "url": url,
                "language_code": LANGUAGE_CODES[site_slug],
            }
        )

    translations.sort(key=lambda translation: translation["language_code"])

    return translations
