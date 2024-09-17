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
# do you want to convert marp to PDF?
DO_MARP_PDF:=1
# do you want to convert marp to PDF?
DO_MARP_PPTX:=0
# do you want to convert marp to HTML?
DO_MARP_HTML:=0
# do spell check on all?
DO_MD_ASPELL:=1
# do you want to convert mermaid diagrams into png?
DO_MERMAID_PNG:=1

########
# code #
########
# UNOPATH=UNOPATH="$(shell ls -d /opt/libreoffice*)"
# UNOPYTHON=$(UNOPATH)/program/python
UNOPATH=
UNOPYTHON=/usr/bin/python
UNOTIMEOUT=30
UNOWARNINGS=PYTHONWARNINGS="ignore::DeprecationWarning"

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

# odps
ODP_SRC:=$(shell find odp -name "*.odp")
ODP_BAS:=$(basename $(ODP_SRC))
ODP_PPT:=$(addprefix out/,$(addsuffix .ppt,$(ODP_BAS)))
ODP_PDF:=$(addprefix out/,$(addsuffix .pdf,$(ODP_BAS)))

# md
MD_SRC:=$(shell find marp -type f -and -name "*.md")
MD_BAS:=$(basename $(MD_SRC))
MD_MDL:=$(addprefix out/,$(addsuffix .mdl,$(MD_BAS)))
MD_ASPELL:=$(addprefix out/,$(addsuffix .aspell,$(MD_BAS)))

# marp
MARP_SRC:=$(shell find marp -type f -and -name "*.md")
MARP_BAS:=$(basename $(MARP_SRC))
MARP_PDF:=$(addprefix out/,$(addsuffix .pdf,$(MARP_BAS)))
MARP_PPTX:=$(addprefix out/,$(addsuffix .pptx,$(MARP_BAS)))
MARP_HTML:=$(addprefix out/,$(addsuffix .html,$(MARP_BAS)))

# mermaid
MERMAID_SRC:=$(shell find mermaid -type f -and -name "*.mmd")
MERMAID_BAS:=$(basename $(MERMAID_SRC))
MERMAID_PNG:=$(addprefix out/,$(addsuffix .png,$(MERMAID_BAS)))

ifeq ($(DO_MD_ASPELL),1)
ALL+=$(MD_ASPELL)
endif # DO_MD_ASPELL

ifeq ($(DO_FMT_ODP_PPT),1)
ALL+=$(ODP_PPT)
endif # DO_FMT_ODP_PPT

ifeq ($(DO_FMT_ODP_PDF),1)
ALL+=$(ODP_PDF)
endif # DO_FMT_ODP_PDF

ifeq ($(DO_MARP_PDF),1)
ALL+=$(MARP_PDF)
endif # DO_MARP_PDF

ifeq ($(DO_MARP_PPTX),1)
ALL+=$(MARP_PPTX)
endif # DO_MARP_PPTX

ifeq ($(DO_MARP_HTML),1)
ALL+=$(MARP_HTML)
endif # DO_MARP_HTML

ifeq ($(DO_FMT_TEX_PDF),1)
ALL+=$(TEX_PDF)
endif # DO_FMT_TEX_PDF

ifeq ($(DO_FMT_TXT_PDF),1)
ALL+=$(TXT_PDF)
endif # DO_FMT_TXT_PDF

ifeq ($(DO_MERMAID_PNG),1)
ALL+=$(MERMAID_PNG)
endif # DO_MERMAID_PNG

# MARP_DEPENDS=marp.config.js
MARP_DEPENDS=
MARP_FLAGS=--engine @marp-team/marp-core --html --allow-local-files --quiet

#########
# rules #
#########
.PHONY: all
all: $(ALL)
	@true

.PHONY: all_odp
all_odp: $(ODP_PPT) $(ODP_PDF)

.PHONY: all_mkd
all_mkd: $(MKD_HTM)

.PHONY: debug
debug:
	$(info doing [$@])
	$(info UNOPATH is $(UNOPATH))
	$(info UNOPYTHON is $(UNOPYTHON))
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
	$(info MARP_SRC is $(MARP_SRC))
	$(info MARP_BAS is $(MARP_BAS))
	$(info MARP_PDF is $(MARP_PDF))
	$(info MARP_PPTX is $(MARP_PPTX))
	$(info MARP_HTML is $(MARP_HTML))
	$(info MD_SRC is $(MD_SRC))
	$(info MD_BAS is $(MD_BAS))
	$(info MD_ASPELL is $(MD_ASPELL))
	$(info MD_MDL is $(MD_MDL))
	$(info MERMAID_SRC is $(MERMAID_SRC))
	$(info MERMAID_BAS is $(MERMAID_BAS))
	$(info MERMAID_PNG is $(MERMAID_PNG))

.PHONY: clean
clean:
	$(info doing [$@])
	$(Q)rm -f $(ALL)

.PHONY: clean_hard
clean_hard:
	$(info doing [$@])
	$(Q)git clean -qffxd

.PHONY: spell_many
spell_many:
	$(info doing [$@])
	$(Q)aspell_many.sh $(MD_SRC)

############
# patterns #
############
# odps
$(ODP_PPT): out/%.ppt: %.odp
	$(info doing [$@])
	$(Q)rm -f $@
	$(Q)mkdir -p $(dir $@)
	$(Q)$(UNOWARNINGS) $(UNOPATH) $(UNOPYTHON) /usr/bin/unoconv --timeout=$(UNOTIMEOUT) --doctype=presentation --output=$@ --format=ppt $<
	$(Q)chmod 444 $@
$(ODP_PDF): out/%.pdf: %.odp
	$(info doing [$@])
	$(Q)rm -f $@
	$(Q)mkdir -p $(dir $@)
	$(Q)$(UNOWARNINGS) $(UNOPATH) $(UNOPYTHON) /usr/bin/unoconv --timeout=$(UNOTIMEOUT) --doctype=presentation --output=$@ --format=pdf $<
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
# marp
$(MARP_PDF): out/%.pdf: %.md $(MARP_DEPENDS)
	$(info doing [$@])
	$(Q)mkdir -p $(dir $@)
	$(Q)pymakehelper only_print_on_error node_modules/.bin/marp $(MARP_FLAGS) --pdf --output $@ $<
$(MARP_PPTX): out/%.pptx: %.md $(MARP_DEPENDS)
	$(info doing [$@])
	$(Q)mkdir -p $(dir $@)
	$(Q)pymakehelper only_print_on_error node_modules/.bin/marp $(MARP_FLAGS) --pptx --output $@ $<
$(MARP_HTML): out/%.html: %.md $(MARP_DEPENDS)
	$(info doing [$@])
	$(Q)mkdir -p $(dir $@)
	$(Q)pymakehelper only_print_on_error node_modules/.bin/marp $(MARP_FLAGS) --html --output $@ $<
# aspell
$(MD_ASPELL): out/%.aspell: %.md .aspell.conf .aspell.en.prepl .aspell.en.pws
	$(info doing [$@])
	$(Q)aspell --conf-dir=. --conf=.aspell.conf list < $< | pymakehelper error_on_print sort -u
	$(Q)pymakehelper touch_mkdir $@
# mermaid
$(MERMAID_PNG): out/%.png: %.mmd
	$(info doing [$@])
	$(Q)mkdir -p $(dir $@)
	$(Q)pymakehelper only_print_on_error node_modules/.bin/mmdc -p .mmdc.config -i $< -o $@
