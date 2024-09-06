<%!
    import pydmt.helpers.git
    number_odp = pydmt.helpers.git.count_files("odp/**/*.odp")
    number_marp = pydmt.helpers.git.count_files("marp/**/*.md")
%>${"##"} Number of slide decks

Currently there are ${number_odp} odp slide decks in this repo.
Currently there are ${number_marp} marp files in this repo.
