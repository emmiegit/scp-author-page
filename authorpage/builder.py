#
# builder.py
#
# scp-author-page - Tools for generating my author page.
# Copyright (c) 2021-2022 Ammon Smith
#
# scp-author-page is available free of charge under the terms of the MIT
# License. You are free to redistribute and/or modify it under those
# terms. It is distributed in the hopes that it will be useful, but
# WITHOUT ANY WARRANTY. See the LICENSE file for more details.
#

import os

from jinja2 import Environment, FileSystemLoader

from .data import load_data
from .wikidot import normalize


class Builder:
    __slots__ = (
        "directory",
        "jinja_env",
        "template",
        "data",
        "log",
    )

    def __init__(
        self,
        directory: str,
        data_filename: str = "data.toml",
        input_template: str = "template.j2",
        log: bool = False,
    ):
        if log:
            print("+ Creating jinja environment")

        self.jinja_env = Environment(
            loader=FileSystemLoader(directory),
            autoescape=False,
            trim_blocks=True,
            keep_trailing_newline=True,
        )
        self.jinja_env.filters["normalize"] = normalize

        self.directory = directory
        self.template = self.jinja_env.get_template(input_template)
        self.data = load_data(os.path.join(directory, data_filename), log)
        self.log = log

    def render(self, output_filename: str = "output.ftml"):
        output_path = os.path.join(self.directory, output_filename)
        output_data = self.render_string()

        with open(output_path, "w") as file:
            if self.log:
                print(f"+ Writing to {output_path}")

            file.write(output_data)

    def render_string(self) -> str:
        if self.log:
            print("+ Rendering templates")

        return self.template.render(self.data)
