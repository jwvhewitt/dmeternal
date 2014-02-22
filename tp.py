# Test Plots

import narrator
import context

print "Hellow World!"
init = narrator.plots.PlotState(chapter=1, level=1)
nart = narrator.Narrative( init )

if nart.story:
    nart.story.display()
else:
    print "Plot loading failed."

