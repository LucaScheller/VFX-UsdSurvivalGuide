# Source repo
if [ ! $REPO_SOURCED ]
then
    # Define repo root
    export REPO_SOURCED=1
    export REPO_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && (pwd -W 2> /dev/null || pwd))
    # Source Houdini (This defines what Houdini version to compile against)
    pushd /opt/hfs19.5 > /dev/null
    source houdini_setup
    popd > /dev/null
    export HOUDINI_LMINFO_VERBOSE=1
fi


