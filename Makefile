##############
# parameters #
##############
# do you want to show the commands executed ?
DO_MKDBG:=0
# do you want dependency on the makefile itself ?!?
DO_ALLDEP:=1
# do you want to do 'ppt' from 'odp'?
DO_FMT_ODP_PPT:=1
# do you want to do 'pdf' from 'odp'?
DO_FMT_ODP_PDF:=1
# do you want to do 'html' from 'mkd'?
DO_FMT_MKD_HTM:=1
# do you want to do 'pdf' from 'mkd'?
DO_FMT_MKD_PDF:=1
# do you want to do 'pdf' from 'tex'?
DO_FMT_TEX_PDF:=1
# do you want to do 'pdf' from 'txt'?
DO_FMT_TXT_PDF:=1
# do the tools?
DO_TOOLS:=1

########
# code #
########
ALL:=

# silent stuff
ifeq ($(DO_MKDBG),1)
Q:=
# we are not silent in this branch
else # DO_MKDBG
Q:=@
#.SILENT:
endif # DO_MKDBG

# dependency on the makefile itself
ifeq ($(DO_ALLDEP),1)
.EXTRA_PREREQS+=$(foreach mk, ${MAKEFILE_LIST},$(abspath ${mk}))
endif # DO_ALLDEP

# tools
ifeq ($(DO_TOOLS),1)
.EXTRA_PREREQS+=tools.stamp
endif # DO_TOOLS

# odps
ODP_SRC:=$(shell find odp -name "*.odp")
ODP_BAS:=$(basename $(ODP_SRC))
ODP_PPT:=$(addprefix out/,$(addsuffix .ppt,$(ODP_BAS)))
ODP_PDF:=$(addprefix out/,$(addsuffix .pdf,$(ODP_BAS)))
ifeq ($(DO_FMT_ODP_PPT),1)
ALL+=$(ODP_PPT)
endif # DO_FMT_ODP_PPT
ifeq ($(DO_FMT_ODP_PDF),1)
ALL+=$(ODP_PDF)
endif # DO_FMT_ODP_PDF

# beamer
TEX_SRC:=$(shell find beamer -name "*.tex")
TEX_BAS:=$(basename $(TEX_SRC))
TEX_PDF:=$(addprefix out/,$(addsuffix .pdf,$(TEX_BAS)))
ifeq ($(DO_FMT_TEX_PDF),1)
ALL+=$(TEX_PDF)
endif # DO_FMT_TEX_PDF

# slidy
TXT_SRC:=$(shell find slidy -name "*.txt")
TXT_BAS:=$(basename $(TXT_SRC))
TXT_PDF:=$(addprefix out/,$(addsuffix .pdf,$(TXT_BAS)))
ifeq ($(DO_FMT_TXT_PDF),1)
ALL+=$(TXT_PDF)
endif # DO_FMT_TXT_PDF

#########
# rules #
#########
.PHONY: all
all: $(ALL)
	@true

tools.stamp:
	$(info doing [$@])
	$(Q)touch $@

# odps
$(ODP_PPT): out/%.ppt: %.odp
	$(info doing [$@])
	$(Q)rm -f $@
	$(Q)mkdir -p $(dir $@)
	$(Q)unoconv --timeout=5 --doctype=presentation --output=$@ --format=ppt $<
	$(Q)chmod 444 $@
$(ODP_PDF): out/%.pdf: %.odp
	$(info doing [$@])
	$(Q)rm -f $@
	$(Q)mkdir -p $(dir $@)
	$(Q)unoconv --timeout=5 --doctype=presentation --output=$@ --format=pdf $<
	$(Q)chmod 444 $@
# markdown
$(MKD_HTM): out/%.html: %.mkd
	$(info doing [$@])
	$(Q)rm -f $@
	$(Q)mkdir -p $(dir $@)
	$(Q)markdown $< > $@
	$(Q)chmod 444 $@
$(MKD_PDF): out/%.pdf: %.mkd
	$(info doing [$@])
	$(Q)rm -f $@
	$(Q)mkdir -p $(dir $@)
	$(Q)pandoc -f markdown $< -o $@
	$(Q)chmod 444 $@
#$(Q)markdown-pdf $< --out $@
#$(Q)pandoc -t beamer $< -o $@
#$(Q)pandoc $< -o $@
# beamer
$(TEX_PDF): out/%.pdf: %.tex
	$(info doing [$@])
	$(Q)mkdir -p $(dir $@)
	$(Q)scripts/wrapper_pdflatex.pl $< $@
	$(Q)rm -f $(basename $@).log $(basename $@).aux $(basename $@).nav $(basename $@).out $(basename $@).snm $(basename $@).toc $(basename $@).vrb
# slidy
$(TXT_PDF): out/%.pdf: %.txt
	$(info doing [$@])
	$(Q)mkdir -p $(dir $@)
	$(Q)a2x -f pdf $<
	$(Q)mv $(basename $<).pdf $@

.PHONY: all_odp
all_odp: $(ODP_PPT) $(ODP_PDF)

.PHONY: all_mkd
all_mkd: $(MKD_HTM)

.PHONY: all_beamer
all_beamer: $(TEX_PDF)

.PHONY: all_slidy
all_slidy: $(TXT_PDF)

.PHONY: debug
debug:
	$(info doing [$@])
	$(info ALL is $(ALL))
	$(info ODP_SRC is $(ODP_SRC))
	$(info ODP_PPT is $(ODP_PPT))
	$(info ODP_PDF is $(ODP_PDF))
	$(info MKD_SRC is $(MKD_SRC))
	$(info MKD_HTM is $(MKD_HTM))
	$(info MKD_PDF is $(MKD_PDF))
	$(info TEX_SRC is $(TEX_SRC))
	$(info TEX_HTM is $(TEX_HTM))
	$(info TXT_SRC is $(TXT_SRC))
	$(info TXT_PDF is $(TXT_PDF))

.PHONY: clean
clean:
	$(info doing [$@])
	$(Q)rm -f $(ALL)

.PHONY: clean_hard
clean_hard:
	$(info doing [$@])
	$(Q)git clean -qffxd
