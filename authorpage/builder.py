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

import toml
from jinja2 import Environment, FileSystemLoader

from .wikidot import normalize


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
            lstrip_blocks=True,
            keep_trailing_newline=True,
        )

        self.directory = directory
        self.template = self.jinja_env.get_template(input_template)
        self.data = self.load_data(data_filename)

    def load_data(self, data_filename: str) -> dict:
        data_path = os.path.join(self.directory, data_filename)

        with open(data_path) as file:
            data = toml.load(file)

        # Hydrate data according to patterns
        base_url = data["base-url"]

        for article in data["articles"]:
            if "slug" not in data:
                data["slug"] = normalize(data["name"])

            if "title" not in data:
                data["title"] = data["name"]

            if "co-authors" not in data:
                data["co-authors"] = []

            if "contest" not in data:
                data["contest"] = None

    def render(self, output_filename: str = "output.ftml"):
        output_path = os.path.join(self.directory, output_filename)
        output_data = self.render_string()

        with open(output_path, "w") as file:
            file.write(output_data)

    def render_string(self) -> str:
        return self.template.render(self.data)
