#
# Build and deploy scripts for Linux
#

ROOT	= .
DEST	= $(ROOT)/GameData/ContractPacks/KPlanes

build:
	cp $(ROOT)/README.md $(DEST)
	cp $(ROOT)/LICENSE $(DEST)
