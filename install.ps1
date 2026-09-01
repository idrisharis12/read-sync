Write-Host "Installing read-sync..."
# Clone repository if not already downloaded
# Install dependencies, setup environment
Write-Host "Setting up python environment..."
pip install -e .

Write-Host "read-sync installed successfully! Run 'read-sync --help' to get started."
