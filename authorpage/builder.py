#
# builder.py
#
# scp-author-page - Tools for generating my author page.
# Copyright (c) 2021 Ammon Smith
#
# scp-author-page is available free of charge under the terms of the MIT
# License. You are free to redistribute and/or modify it under those
# terms. It is distributed in the hopes that it will be useful, but
# WITHOUT ANY WARRANTY. See the LICENSE file for more details.
#

import os
import re

import toml
from jinja2 import Environment, FileSystemLoader

from .wikidot import normalize

SCP_NAME_REGEX = re.compile(r"SCP-[1-9]?[0-9]{3}(?:-(?:J|EX))?")

class Builder:
    __slots__ = (
        "directory",
        "jinja_env",
        "template",
        "data",
    )

    def __init__(
        self,
        directory: str,
        data_filename: str = "data.toml",
        input_template: str = "template.j2",
    ):
        self.jinja_env = Environment(
            loader=FileSystemLoader(directory),
            autoescape=False,
            keep_trailing_newline=True,
        )

        self.directory = directory
        self.template = self.jinja_env.get_template(input_template)
        self.data = self.load_data(data_filename)

    def load_data(self, data_filename: str) -> dict:
        data_path = os.path.join(self.directory, data_filename)

        with open(data_path) as file:
            data = toml.load(file)

        # Hydrate data according to structures
        base_url = data["base-url"]

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

            if "title" not in article:
                article["title"] = name

            if "co-authors" not in article:
                article["co-authors"] = []

            if "contest" not in article:
                article["contest"] = None

        return data

    def render(self, output_filename: str = "output.ftml"):
        output_path = os.path.join(self.directory, output_filename)
        output_data = self.render_string()

        with open(output_path, "w") as file:
            file.write(output_data)

    def render_string(self) -> str:
        return self.template.render(self.data)
