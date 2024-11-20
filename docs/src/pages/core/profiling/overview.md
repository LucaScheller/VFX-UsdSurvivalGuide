# Debugging & Performance Profiling
Usd ships with extensive debugging and profiling tools. You can inspect the code execution a various levels, which allows you to really pinpoint where the performance issues are.

When starting out these to two interfaces are of interest:

- [Debug Symbols](./debug.md): Enable logging of various API sections to stdout. Especially useful for plugins like asset resolvers or to see how DCCs handle Usd integration.
- [Performance Profiling](./profiling.md): Usd has a powerful performance profiler, which you can also view with Google Chrome's Trace Viewer.