#
# translations.py
#
# scp-author-page - Tools for generating my author page.
# Copyright (c) 2021 Ammon Smith
#
# scp-author-page is available free of charge under the terms of the MIT
# License. You are free to redistribute and/or modify it under those
# terms. It is distributed in the hopes that it will be useful, but
# WITHOUT ANY WARRANTY. See the LICENSE file for more details.
#

import requests
from bs4 import BeautifulSoup

INTERWIKI_URL = "https://interwiki.scpdb.org/"
INTERWIKI_WIKI = "scp-wiki"
INTERWIKI_LANGUAGE = "en"

LANGUAGE_CODES = {
    "中文": "CN",
    "Česky": "CS",
    "Français": "FR",
    "Deutsch": "DE",
    "International": "INT",
    "Italiano": "IT",
    "日本語": "JP",
    "한국어": "KO",
    "Polski": "PL",
    "Português": "PT",
    "Русский": "RU",
    "Español": "ES",
    "ภาษาไทย": "TH",
    "繁體中文": "ZH",
    "Українська": "UK",
    "Tiếng Việt": "VN",
}


def get_translations(slug, log: bool = False):
    if log:
        print(f"+ Scraping translations for {slug}")

    # Make request
    r = requests.get(
        INTERWIKI_URL,
        params={
            "wiki": INTERWIKI_WIKI,
            "lang": INTERWIKI_LANGUAGE,
            "page": slug,
        },
    )
    r.raise_for_status()

    # Scrape HTML
    translations = []

    soup = BeautifulSoup(r.text, "html.parser")
    for entry in soup.find_all("div", class_="interwiki__entry"):
        anchor = entry.find("a")

        url = anchor["href"]
        language_name = anchor.contents[0]
        language_code = LANGUAGE_CODES[language_name]

        translations.append(
            {
                "url": url,
                "language_name": language_name,
                "language_code": language_code,
            }
        )

    return translations
