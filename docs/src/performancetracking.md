
import pxr
import os

trace_dir_path = os.path.dirname(hou.hipFile.path())
# The pxr.Trace.Collector() returns a singleton
# The default traces all go to TraceCategory::Default, this is not configureable via
# Python
collector = pxr.Trace.Collector()
collector.Clear()
# Start recording events.
collector.enabled = True
collector.pythonTracingEnabled = False

class Bar():
    @pxr.Trace.TraceMethod
    def foo(self):
        print("Bar.foo")

@pxr.Trace.TraceFunction
def foo(stage):
    with pxr.Trace.TraceScope("InnerScope"):
        bar = Bar()
        for prim in stage.Traverse():
            prim.HasAttribute("test")
        stage = pxr.Usd.Stage.Open("/opt/hfs19.5.605/houdini/usd/assets/pig/pig.usd")
foo(stage)
# Stop recording events.
collector.enabled = False
# Print the ASCII report
global_reporter = pxr.Trace.Reporter.globalReporter
global_reporter.Report(os.path.join(trace_dir_path, "report.trace"))
global_reporter.ReportChromeTracingToFile(os.path.join(trace_dir_path,"report.json"))
> Open in Google Chrome chrome://tracing/

## StopWatch
import pxr
sw = pxr.Tf.Stopwatch()
sw.Start()
sw.Stop()
sw.Start()
sw.Stop()
print(sw.GetMilliseconds(), sw.sampleCount)
sw.Reset()
sw.AddFrom(other_sw) # Add sampleCount + accumulated time
