PREFIX ?= /usr/local
BINDIR ?= $(PREFIX)/bin
SHAREDIR ?= $(PREFIX)/share/read-sync

install:
	@echo "Installing read-sync to $(BINDIR)..."
	@pip install -e .
	@echo "✓ Successfully installed read-sync."

uninstall:
	@echo "Uninstalling read-sync..."
	@pip uninstall -y read-sync
	@echo "✓ Successfully uninstalled read-sync."
