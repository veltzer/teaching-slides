##############
# parameters #
##############
# do you want to show the commands executed ?
DO_MKDBG:=0
# do you want dependency on the makefile itself ?!?
DO_ALLDEP:=1
# do you want to do 'ppt' from 'odp'?
DO_ODP_PPT:=0
# do you want to do 'pptx' from 'odp'?
DO_ODP_PPTX:=0
# do you want to do 'pdf' from 'odp'?
DO_ODP_PDF:=1
# do you want to do 'html' from 'mkd'?
DO_MKD_HTM:=1
# do you want to do 'pdf' from 'mkd'?
DO_MKD_PDF:=1
# do you want to do 'pdf' from 'tex'?
DO_TEX_PDF:=1
# do you want to do 'pdf' from 'txt'?
DO_TXT_PDF:=1
# do you want to convert marp to PDF?
DO_MARP_PDF:=1
# do you want to convert marp to PDF?
DO_MARP_PPTX:=0
# do you want to convert marp to HTML?
DO_MARP_HTML:=0
# do spell check on all?
DO_MD_ASPELL:=1
# do you want to check that the md files are pure ASCII?
DO_MD_ASCII:=0
# do you want to run mdl on md files?
DO_MD_MDL:=0
# do you want to run markdownlint on md files?
DO_MD_MARKDOWNLINT:=1
# do you want to convert mermaid diagrams into png?
DO_MERMAID_PNG:=1
# convert drawio images to png?
ifdef GITHUB_WORKFLOW
DO_DRAWIO_PNG:=0
else
DO_DRAWIO_PNG:=1
endif # GITHUB_WORKFLOW
# use mermaid png deps?
DO_MERMAID_DEP:=1
# unite courses pdfs?
DO_COURSES:=1

#############
# templates #
#############
define template
PREREQ_$(1):=$$(addprefix out/,$$(addsuffix .pdf,$$(patsubst %.md,%,$$(wildcard marp/courses/$(1)/*))))
out/marp/courses/$(1).pdf: $$(PREREQ_$(1))
	$$(info doing [$$@])
	$$(Q)pdfunite $$(PREREQ_$(1)) $$@
endef

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

# odps
ODP_SRC:=$(shell find odp -type f -and -name "*.odp")
ODP_BAS:=$(basename $(ODP_SRC))
ODP_PPT:=$(addprefix out/,$(addsuffix .ppt,$(ODP_BAS)))
ODP_PPTX:=$(addprefix out/,$(addsuffix .pptx,$(ODP_BAS)))
ODP_PDF:=$(addprefix out/,$(addsuffix .pdf,$(ODP_BAS)))

# md
MD_SRC:=$(shell find marp -type f -and -name "*.md")
MD_BAS:=$(basename $(MD_SRC))
MD_MDL:=$(addprefix out/,$(addsuffix .mdl,$(MD_BAS)))
MD_ASPELL:=$(addprefix out/,$(addsuffix .aspell,$(MD_BAS)))
MD_ASCII:=$(addprefix out/,$(addsuffix .ascii,$(MD_BAS)))
MD_MARKDOWNLINT:=$(addprefix out/,$(addsuffix .markdownlint,$(MD_BAS)))

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

# drawio
DRAWIO_SRC:=$(shell find drawings -type f -and -name "*.drawio")
DRAWIO_BAS:=$(basename $(DRAWIO_SRC))
DRAWIO_PNG:=$(addprefix out/,$(addsuffix .png,$(DRAWIO_BAS)))

# courses
NAMES:=$(notdir $(patsubst %/,%,$(dir $(wildcard marp/courses/*/))))
TARGET_NAMES:=$(addsuffix .pdf,$(addprefix out/marp/courses/,$(NAMES)))
# warning! no space is allowed after the command in the call function below
$(foreach name, $(NAMES), $(eval $(call template,$(name))))

ifeq ($(DO_MD_MARKDOWNLINT),1)
ALL+=$(MD_MARKDOWNLINT)
endif # DO_MD_MARKDOWNLINT

ifeq ($(DO_COURSES),1)
ALL+=$(TARGET_NAMES)
endif # DO_COURSES

ifeq ($(DO_MD_ASPELL),1)
ALL+=$(MD_ASPELL)
endif # DO_MD_ASPELL

ifeq ($(DO_MD_ASCII),1)
ALL+=$(MD_ASCII)
endif # DO_MD_ASCII

ifeq ($(DO_MD_MDL),1)
ALL+=$(MD_MDL)
endif # DO_MD_MDL

ifeq ($(DO_ODP_PPT),1)
ALL+=$(ODP_PPT)
endif # DO_ODP_PPT

ifeq ($(DO_ODP_PPTX),1)
ALL+=$(ODP_PPTX)
endif # DO_ODP_PPTX

ifeq ($(DO_ODP_PDF),1)
ALL+=$(ODP_PDF)
endif # DO_ODP_PDF

ifeq ($(DO_MARP_PDF),1)
ALL+=$(MARP_PDF)
endif # DO_MARP_PDF

ifeq ($(DO_MARP_PPTX),1)
ALL+=$(MARP_PPTX)
endif # DO_MARP_PPTX

ifeq ($(DO_MARP_HTML),1)
ALL+=$(MARP_HTML)
endif # DO_MARP_HTML

ifeq ($(DO_TEX_PDF),1)
ALL+=$(TEX_PDF)
endif # DO_TEX_PDF

ifeq ($(DO_TXT_PDF),1)
ALL+=$(TXT_PDF)
endif # DO_TXT_PDF

ifeq ($(DO_MERMAID_PNG),1)
ALL+=$(MERMAID_PNG)
endif # DO_MERMAID_PNG

ifeq ($(DO_DRAWIO_PNG),1)
ALL+=$(DRAWIO_PNG)
endif # DO_DRAWIO_PNG

ifeq ($(DO_MERMAID_DEP),1)
MERMAID_PNG_DEP=$(MERMAID_PNG)
else
MERMAID_PNG_DEP=
endif # DO_MERMAID_DEP

# MARP_DEPENDS=marp.config.js
MARP_DEPENDS=
MARP_FLAGS=--engine @marp-team/marp-core --html --allow-local-files --quiet

#########
# rules #
#########
.DEFAULT_GOAL:=all
.PHONY: all
all: $(ALL)
	@true

.PHONY: all_odp_pdf
all_odp_pdf: $(ODP_PDF)

.PHONY: all_odp
all_odp: $(ODP_PPTX) $(ODP_PPT) $(ODP_PDF)

.PHONY: all_mkd
all_mkd: $(MKD_HTM)

.PHONY: all_drawio_png
all_drawio_png: $(DRAWIO_PNG)

.PHONY: all_mdl
all_mdl: $(MD_MDL)

.PHONY: all_markdownlint
all_markdownlint: $(MD_MARKDOWNLINT)

.PHONY: all_mermaid_png
all_mermaid_png: $(MERMAID_PNG)

.PHONY: all_marp_pdf
all_marp_pdf: $(MARP_PDF)

.PHONY: all_courses
all_courses: $(TARGET_NAMES)

.PHONY: debug
debug:
	$(info doing [$@])
	$(info ALL is $(ALL))
	$(info ODP_SRC is $(ODP_SRC))
	$(info ODP_PPT is $(ODP_PPT))
	$(info ODP_PPTX is $(ODP_PPTX))
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
	$(info MD_ASCII is $(MD_ASCII))
	$(info MD_MDL is $(MD_MDL))
	$(info MD_MARKDOWNLINT is $(MD_MARKDOWNLINT))
	$(info MERMAID_SRC is $(MERMAID_SRC))
	$(info MERMAID_BAS is $(MERMAID_BAS))
	$(info MERMAID_PNG is $(MERMAID_PNG))
	$(info DRAWIO_SRC is $(DRAWIO_SRC))
	$(info DRAWIO_BAS is $(DRAWIO_BAS))
	$(info DRAWIO_PNG is $(DRAWIO_PNG))
	$(info NAMES is $(NAMES))
	$(info TARGET_NAMES is $(TARGET_NAMES))
	$(foreach name,$(NAMES),$(info PREREQ_$(name) is $(PREREQ_$(name))))

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
$(ODP_PPTX): out/%.pptx: %.odp
	$(info doing [$@])
	$(Q)rm -f $@
	$(Q)mkdir -p $(dir $@)
	$(Q)pymakehelper only_print_on_error libreoffice --headless --convert-to pptx --outdir $(dir $@) $<
$(ODP_PPT): out/%.ppt: %.odp
	$(info doing [$@])
	$(Q)rm -f $@
	$(Q)mkdir -p $(dir $@)
	$(Q)pymakehelper only_print_on_error libreoffice --headless --convert-to ppt --outdir $(dir $@) $<
$(ODP_PDF): out/%.pdf: %.odp
	$(info doing [$@])
	$(Q)rm -f $@
	$(Q)mkdir -p $(dir $@)
	$(Q)flock /tmp/odp_pdf pymakehelper only_print_on_error libreoffice --headless --convert-to pdf --outdir $(dir $@) $<
$(MKD_HTM): out/%.html: %.mkd
	$(info doing [$@])
	$(Q)rm -f $@
	$(Q)mkdir -p $(dir $@)
	$(Q)markdown $< > $@
$(MKD_PDF): out/%.pdf: %.mkd
	$(info doing [$@])
	$(Q)rm -f $@
	$(Q)mkdir -p $(dir $@)
	$(Q)pandoc -f markdown $< -o $@
$(MARP_PDF): out/%.pdf: %.md $(MARP_DEPENDS) $(MERMAID_PNG_DEP)
	$(info doing [$@])
	$(Q)mkdir -p $(dir $@)
	$(Q)pymakehelper only_print_on_error node_modules/.bin/marp $(MARP_FLAGS) --pdf --output $@ $<
$(MARP_PPTX): out/%.pptx: %.md $(MARP_DEPENDS) $(MERMAID_PNG)
	$(info doing [$@])
	$(Q)mkdir -p $(dir $@)
	$(Q)pymakehelper only_print_on_error node_modules/.bin/marp $(MARP_FLAGS) --pptx --output $@ $<
$(MARP_HTML): out/%.html: %.md $(MARP_DEPENDS) $(MERMAID_PNG)
	$(info doing [$@])
	$(Q)mkdir -p $(dir $@)
	$(Q)pymakehelper only_print_on_error node_modules/.bin/marp $(MARP_FLAGS) --html --output $@ $<
$(MD_ASPELL): out/%.aspell: %.md .aspell.conf .aspell.en.prepl .aspell.en.pws
	$(info doing [$@])
	$(Q)aspell --conf-dir=. --conf=.aspell.conf list < $< | pymakehelper error_on_print sort -u
	$(Q)pymakehelper touch_mkdir $@
$(MD_ASCII): out/%.ascii: %.md
	$(info doing [$@])
	$(Q)pymakehelper error_on_print grep -P -n "[^\x00-\x7F]" $<
	$(Q)pymakehelper touch_mkdir $@
$(MD_MDL): out/%.mdl: %.md .mdlrc .mdl.style.rb
	$(info doing [$@])
	$(Q)GEM_HOME=gems gems/bin/mdl $<
	$(Q)pymakehelper touch_mkdir $@
$(MD_MARKDOWNLINT): out/%.markdownlint: %.md .markdownlint.json
	$(info doing [$@])
	$(Q)node_modules/.bin/markdownlint -c .markdownlint.json $<
	$(Q)pymakehelper touch_mkdir $@
$(MERMAID_PNG): out/%.png: %.mmd .mdlrc .mdl.style.rb
	$(info doing [$@])
	$(Q)mkdir -p $(dir $@)
	$(Q)pymakehelper only_print_on_error node_modules/.bin/mmdc -p .mmdc.config -i $< -o $@
$(DRAWIO_PNG): out/%.png: %.drawio
	$(info doing [$@])
	$(Q)mkdir -p $(dir $@)
	$(Q)pymakehelper only_print_on_error drawio --export --format png --output $@ $<

##########
# alldep #
##########
ifeq ($(DO_ALLDEP),1)
.EXTRA_PREREQS+=$(foreach mk, ${MAKEFILE_LIST},$(abspath ${mk}))
endif # DO_ALLDEP

# .NOTPARALLEL:
ifndef GITHUB_WORKFLOW
MAKEFLAGS+=-j8
# .NOTPARALLEL: all_odp_pdf
endif
