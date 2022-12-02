#
# Build and deploy scripts for Linux
#
# NOTE: Needs rsvg-convert:
# $ sudo apt install -y librsvg2-bin

ROOT		= .
ART		= $(ROOT)/Artwork
DEST		= $(ROOT)/GameData/ContractPacks/KPlanes

SVGPNG		= rsvg-convert --format=png --width=256 --height=160 --keep-aspect-ratio
SVGPNG_SCALED	= rsvg-convert --format=png --width=64 --height=40 --keep-aspect-ratio

KACA_PNG	= $(DEST)/Assets/Flags/KACA.png
KACA_SCALED_PNG	= $(DEST)/Assets/Flags/KACA_scaled.png
KASA_PNG	= $(DEST)/Assets/Flags/KASA.png
KASA_SCALED_PNG	= $(DEST)/Assets/Flags/KASA_scaled.png
README		= $(DEST)/README.md
LICENSE		= $(DEST)/LICENSE

BUILDABLES	= $(KACA_PNG) $(KACA_SCALED_PNG) $(KASA_PNG) $(KASA_SCALED_PNG) $(README) $(LICENSE)

build: $(BUILDABLES)

clobber:
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
