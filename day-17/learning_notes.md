# Day 17 learning notes

A lifecycle stage describes where a lead is in the GTM process; a routing
queue describes who should handle it. They are separate decisions. This
exercise uses explicit thresholds and reasons so sales operations can explain
why a lead was routed.

The rules prioritize an explicit demo request as SQL, then use a documented
score threshold for MQL. Geography and employee segment select a queue. Missing
or out-of-range scores stay at Lead and receive a review reason rather than
being silently qualified.
