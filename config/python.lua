local shared = dofile("config/shared.lua")
install_requires = {"asciidoc"}
build_requires = shared.BUILD
test_requires = shared.TEST
requires = {}
for _, v in ipairs(install_requires) do requires[#requires + 1] = v end
for _, v in ipairs(build_requires) do requires[#requires + 1] = v end
for _, v in ipairs(test_requires) do requires[#requires + 1] = v end
