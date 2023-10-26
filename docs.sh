# Source setup
export REPO_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && (pwd -W 2> /dev/null || pwd))
# Clean existing builds
rm -R ${REPO_ROOT}/docs/book
# Build book
mdbook serve --open ${REPO_ROOT}/docs
