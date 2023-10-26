REM Source setup
set REPO_ROOT=%~dp0
REM Clean existing build
rmdir %REPO_ROOT%docs\book /S /Q
REM Build book
mdbook serve --open %REPO_ROOT%docs