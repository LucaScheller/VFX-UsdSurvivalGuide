# Source setup
if [ ! $REPO_SOURCED ]
then
    source ../../../setup.sh
fi
# Clear existing build data
rm -R src
rm -R dist
# Invoke usdGenSchema
usdGenSchema schema.usda ./src
# Set plugin path
current_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && (pwd -W 2> /dev/null || pwd))
if [[ "$PXR_PLUGINPATH_NAME" != *"$current_dir/dist"* ]]; then
  export PXR_PLUGINPATH_NAME=$current_dir/dist:${PXR_PLUGINPATH_NAME}
  echo "Added $current_dir/dist to the PXR_PLUGINPATH_NAME environment variable."
fi
#rm -R build
#rm -R dist
#cmake . -B build
#cmake --build build --clean-first              # make clean all
#cmake --install build                          # make install
