<%!
    import pydmt.helpers.git
    number_odp = pydmt.helpers.git.count_files("odp/**/*.odp")
    number_marp = pydmt.helpers.git.count_files("marp/**/*.md")
    number_mermaid = pydmt.helpers.git.count_files("mermaid/**/*.mmd")
%>${"##"} Number of slide decks

Currently there are ${number_odp} odp files in this repo.
Currently there are ${number_marp} marp files in this repo.
Currently there are ${number_mermaid} mermaid files in this repo.
