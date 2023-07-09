# Source setup
if [ ! $REPO_SOURCED ]
then
    source setup.sh
fi
# Clean existing builds
rm -R ${REPO_ROOT}/docs/book
# Build book
mdbook serve --open ${REPO_ROOT}/docs
