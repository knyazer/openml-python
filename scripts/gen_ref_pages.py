"""Generate the code reference pages.

based on https://github.com/mkdocstrings/mkdocstrings/blob/33aa573efb17b13e7b9da77e29aeccb3fbddd8e8/docs/recipes.md
but modified for lack of "src/" file structure.

"""

from pathlib import Path
import shutil

import mkdocs_gen_files

nav = mkdocs_gen_files.Nav()

root = Path(__file__).parent.parent
src = root / "openml"

for path in sorted(src.rglob("*.py")):
    module_path = path.relative_to(root).with_suffix("")
    doc_path = path.relative_to(src).with_suffix(".md")
    full_doc_path = Path("reference", doc_path)

    parts = tuple(module_path.parts)

    if parts[-1] == "__init__":
        parts = parts[:-1]
        doc_path = doc_path.with_name("index.md")
        full_doc_path = full_doc_path.with_name("index.md")
    elif parts[-1] == "__main__":
        continue

    nav[parts] = doc_path.as_posix()

    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        identifier = ".".join(parts)
        print("::: " + identifier, file=fd)

    mkdocs_gen_files.set_edit_path(full_doc_path, path.relative_to(root))

    with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
        nav_file.writelines(nav.build_literate_nav())

nav = mkdocs_gen_files.Nav()
examples_dir = root / "examples"
examples_doc_dir = root / "docs" / "examples"
for path in sorted(examples_dir.rglob("*.py")):
    dest_path = Path("examples") / path.relative_to(examples_dir)
    with mkdocs_gen_files.open(dest_path, "w") as dest_file:
        print(path.read_text(), file=dest_file)

    new_relative_location = Path("../") / dest_path
    nav[new_relative_location.parts[2:]] = new_relative_location.as_posix()

    with mkdocs_gen_files.open("examples/SUMMARY.md", "w") as nav_file:
        nav_file.writelines(nav.build_literate_nav())
