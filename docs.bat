REM Clean existing builds
rmdir %~dp0docs\book /S /Q
REM Build book
mdbook serve --open %~dp0\docs
