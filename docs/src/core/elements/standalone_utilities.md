# Standalone Utilities
Usd ships with a small set of commandline utilities. Below you find a short summary of the most important ones:

## TL;DR - Commandline Utilites In-A-Nutshell
~~~admonish tip
The following are a must have for anyone using Usd in production:
- [usdmanager](http://www.usdmanager.org/): Your go-to Usd ascii editing app
- [usdview](http://www.usdmanager.org/): Your go-to standalone Usd 3d viewing/debugging app
    - [TheGrill/Grill](https://github.com/thegrill/grill): A Usd View plugin to view composition arcs
~~~

## Resources
- [Commandline Utilities](https://openusd.org/release/toolset.html)
- External Tools:
    - [usdmanager](http://www.usdmanager.org/): A Usd ascii editing app
    - [TheGrill/Grill](https://github.com/thegrill/grill): A Usd View plugin to view composition arcs

## Overview
The most notable ones are:
- [usdstitch](https://openusd.org/release/toolset.html#usdstitch): Combine multiple files into a single file. This combines the data, with the first file getting the highest strength and so forth. A typical use case is when you are exporting a layer per frame from a DCC and then need to combine it to a single file.
- [usdstitchclips](https://openusd.org/release/toolset.html#usdstitchclips): Create a file that links to multiple files for a certain time range (for example per frame). Unlike 'usdstitch' this does not combine the data, instead it creates a file (and few sidecar files to increase data lookup performance) that has a mapping what file to load per frame/a certain time range.
- [usddiff](https://openusd.org/release/toolset.html#usddiff): Opens the diff editor of your choice with the difference between two .usd files. This is super useful to debug for example render .usd files with huge hierarchies, where a visual 3d diff is to expensive or where looking for a specific attribute would take to long, because you don't know where to start.
- [usdGenSchema]: This commandline tool helps us generate our own schemas (Usd speak for classes) without having to code them ourselves in C++. Head over to our [schema](../plugins/schemas.md) section for a hands on example.
- [usdrecord](https://openusd.org/release/toolset.html#usdrecord): A simple hydra to OpenGL proof of concept implementation. If you are interested in the the high level render API, this is good starting point to get a simple overview. 
- [usdview](https://openusd.org/release/toolset.html#usdview): A 3d viewer for Usd stages. If you are interested in the high level render API of Usd/Hydra, feel free to dive into the source code, as the Usd View exposes 99% of the functionality of the high level api. It is a great 'example' to learn and a good starting point if you want to integrate it into your apps with a handful of Qt widgets ready to use.

Most of these tools actually are small python scripts, so you can dive in and inspect them!

There are also a few very useful tools from external vendors:
- [usdmanager](http://www.usdmanager.org/): A Usd text editor from DreamWorksAnimation that allows you to interactively browse your Usd files. This is a must have of anyone using Usd!
- [TheGrill/Grill](https://github.com/thegrill/grill): A super useful Usd View plugin that allows you to visualize the layer stack/composition arcs. A must have when trying to debug complicated value resolution issues. For a visual overview check out this [link](https://grill.readthedocs.io/en/latest/views.html).


