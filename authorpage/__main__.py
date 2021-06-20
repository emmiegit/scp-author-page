#
# __main__.py
#
# scp-author-page - Tools for generating my author page.
# Copyright (c) 2021 Ammon Smith
#
# scp-author-page is available free of charge under the terms of the MIT
# License. You are free to redistribute and/or modify it under those
# terms. It is distributed in the hopes that it will be useful, but
# WITHOUT ANY WARRANTY. See the LICENSE file for more details.
#

import sys

from .builder import Builder

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(f"Usage: {sys.argv[0]} <directory...>")
        sys.exit(1)

    for directory in sys.argv[1:]:
        builder = Builder(directory)
        builder.render()
