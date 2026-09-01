#!/usr/bin/env bash
set -e

echo "Installing read-sync..."
# Clone repository if not already downloaded
# Install dependencies, setup environment
echo "Setting up python environment..."
pip install -e .

echo "read-sync installed successfully! Run 'read-sync --help' to get started."
