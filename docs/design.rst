================
Design Rationale
================

Explicit Event Firing
---------------------

Events are manually fired rather than doing something implicit with, for
example, signals. This is for two reasons:

1. In the case of events that track changes to model objects, we often want to
   tell the user exactly what changed. Pre- or post-save signals don't give us
   the original state of the object necessary to determine this, so we would
   have to backtrack, hit the database again, and just generally make a mess
   just to save one or two lines of event-firing code.
2. Implicitness could easily lead to accidental spam, such as during
   development or data migration.

If you still want implicitness, it's trivial to register a signal handler that
fires an event.
