# Performance Profiling
For low level profiling Usd ships with the `trace` profiling module.

This is also what a few DCCs (like Houdini) expose to profile Usd writing/rendering.

![](./GoogleChromeTraceProfiling.jpg#center)

## TL;DR - Profiling In-A-Nutshell
- The trace module offers easy to attach Python decorators (`@Trace.TraceMethod/TraceFunction`) that you can wrap your functions with to expose them to the profiler.
- You can dump the profiling result to .txt or the GoogleChrome tracing format you can open under [`chrome://tracing`](chrome://tracing). Even if you don't attach custom traces, you'll get extensive profiling stats of the underlying Usd API execution.

## Resources
- [Trace Overview](https://openusd.org/dev/api/trace_page_front.html)
- [Trace Details](https://openusd.org/dev/api/trace_page_detail.html)

## Overview
The trace module is made up of two parts:
- `TraceCollector`: A singleton thread-safe recorder of (globale) events.
- `TraceReporter`: Turn event data to meaning full views.

Via the C++ API, you can customize the behavior further, for Python 'only' the global collector is exposed.

First you mark what to trace. You can also mark nothing, you'll still have access to all the default profiling:
~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:profilingTraceAttach}}
```
~~~
Then you enable the collector during the runtime of what you want to trace and write the result to the disk.
~~~admonish info title=""
```python
{{#include ../../../../code/core/elements.py:profilingTraceCollect}}
```
~~~

Here is an example (from the Usd docs) of a report to a .txt file. If you have ever rendered with Houdini this will be similar to when you increase the log levels.
~~~admonish info title=""
```text
Tree view  ==============
   inclusive    exclusive        
  358.500 ms                    1 samples    Main Thread
    0.701 ms     0.701 ms       8 samples    | SdfPath::_InitWithString
    0.003 ms     0.003 ms       2 samples    | {anonymous}::VtDictionaryToPython::convert
  275.580 ms   275.580 ms       3 samples    | PlugPlugin::_Load
    0.014 ms     0.014 ms       3 samples    | UcGetCurrentUnit
    1.470 ms     0.002 ms       1 samples    | UcIsKnownUnit
    1.467 ms     0.026 ms       1 samples    |   Uc::_InitUnitData [initialization]
    1.442 ms     1.442 ms       1 samples    |   | Uc_Engine::GetValue
    0.750 ms     0.000 ms       1 samples    | UcGetValue
    0.750 ms     0.750 ms       1 samples    |   Uc_Engine::GetValue
    9.141 ms     0.053 ms       1 samples    | PrCreatePathResolverForUnit
    0.002 ms     0.002 ms       6 samples    |   UcIsKnownUnit
```
~~~

Here is an example of a report to a Google Chrome trace.json file opened in [`chrome://tracing`](chrome://tracing) in Google Chrome with a custom python trace marked scope.

![](./GoogleChromePythonScopeTraceProfiling.jpg#center)
