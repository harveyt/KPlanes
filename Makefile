#
# Build and deploy scripts for Linux
#
# NOTE: Needs rsvg-convert:
# $ sudo apt install -y librsvg2-bin

SHELL		= /bin/bash
ROOT		= .
ART		= $(ROOT)/Artwork
RELPATH		= GameData/ContractPacks/KPlanes
DEST		= $(ROOT)/$(RELPATH)
TEST_GAME	= /mnt/c/Games/KSP-Dev

SVGPNG		= rsvg-convert --format=png --width=256 --height=160 --keep-aspect-ratio
SVGPNG_SCALED	= rsvg-convert --format=png --width=64 --height=40 --keep-aspect-ratio

KACA_PNG	= $(DEST)/Assets/Flags/KACA.png
KACA_SCALED_PNG	= $(DEST)/Assets/Flags/KACA_scaled.png
KASA_PNG	= $(DEST)/Assets/Flags/KASA.png
KASA_SCALED_PNG	= $(DEST)/Assets/Flags/KASA_scaled.png
README		= $(DEST)/README.md
LICENSE		= $(DEST)/LICENSE

BUILDABLES	= $(KACA_PNG) $(KACA_SCALED_PNG) $(KASA_PNG) $(KASA_SCALED_PNG) $(README) $(LICENSE)

test: build
	@if [[ ! -d $(TEST_GAME) ]]; then \
		echo "No KSP game at $(TEST_GAME)" >&2; \
		echo "Create a KSP game with ModuleManager, ContractConfigurator" >&2; \
		exit 1; \
	fi
	@echo "Updating $(TEST_GAME) with KPlanes..."
	@if [[ ! -d $(TEST_GAME)/$(RELPATH) ]]; then \
		mkdir -p $(TEST_GAME)/$(RELPATH); \
	fi
	rm -rf $(TEST_GAME)/$(RELPATH)
	cp -a $(DEST) $(TEST_GAME)/`dirname $(RELPATH)`
	find $(TEST_GAME)/$(RELPATH) -name '*~' -print | xargs rm -f
	rm -rf $(TEST_GAME)/$(RELPATH)/Groups/Early
	rm -rf $(TEST_GAME)/$(RELPATH)/Groups/Modern
	rm -rf $(TEST_GAME)/$(RELPATH)/Groups/Future

build: $(BUILDABLES) contracts

contracts:
	ROOT=$(ROOT) DEST=$(DEST) ./ContractGen.py

diffs:
	git --no-pager diff --exit-code --no-color -b -- $(DEST)/Groups

clean:
	find GameData -name '*~' -print | xargs rm -f

clobber: clean
	rm -f $(BUILDABLES)

$(README): $(ROOT)/README.md
	cp $< $@

$(LICENSE): $(ROOT)/LICENSE
	cp $< $@

$(KACA_PNG): $(ART)/KACA_logo.svg
	$(SVGPNG) -o $@ $<

$(KACA_SCALED_PNG): $(ART)/KACA_logo.svg
	$(SVGPNG_SCALED) -o $@ $<

$(KASA_PNG): $(ART)/KASA_logo.svg
	$(SVGPNG) -o $@ $<

$(KASA_SCALED_PNG): $(ART)/KASA_logo.svg
	$(SVGPNG_SCALED) -o $@ $<
