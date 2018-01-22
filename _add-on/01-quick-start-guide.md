---
title: "CREES Google Sheets Add-on"
permalink: /add-on/quick-start-guide/
---
![Google Sheets Add-on Example.]({{'' | absolute_url}}/assets/images/addon.png "Google Sheets Add-on Example.")
{: .align-center}


The CREES API is made available as [Google Sheets Add-on](https://chrome.google.com/webstore/detail/crisis-event-extraction-s/jekdamaeeejebcccbgleijlfamjcbilc?utm_source=permalink) in order to integrate with typical analysis worflows. The add-on adds three new spreadsheet functions that can be applied to cells and columns.

The addon needs to be [installed](/add-on/installation/) in order to access the new functions. 
{: .notice--warning}


## Available Functions

The CREES add-on makes available the following functions:

- CREES_RELATED: Identifies if a short text document discusses a crisis event (returns one of the following labels: non-related, related).

- CREES_EVENT: Identifies the type of event discussed within a short textual document (returns one of the following labels: bombing, collapse, crash, derailment, earthquake, explosion, fire, flood, haze, meteorite, none, shooting, typhoon, wildfire).

- CREES_INFO: Identifies the type of information discussed within a short textual crisis-related document (returns one of the following labels: affected_individuals, caution_and_advice, donations_and_volunteering, infrastructure_and_utilities, not_applicable, not_labeled, other_useful_information, sympathy_and_support).

More information about each function can be obtained in the built-in documentation. You can access it by typing in the function name in a spreadsheet cell.
 {: .notice}

## Usage Example

In order to use the *CREES_RELATED*, *CREES_EVENT* or *CREES_INFO* methods you simply need to type the method name in an empty cell and select a cell (e.g., A1) or list of cells (e.g., A1:A10).

For example, for identifying if two documents that are inside the cells A1 and A2 contain crisis-related content (*CREES_RELATED*), you can type the following in an empty cell:
```
= CREES_RELATED(A1:A2)
```

One of the possible annotations for the *CREES_RELATED* will be then displayed in the current cell and the cell below matching the text found in A1 and A2.

![Google Sheets Add-on Example.]({{'' | absolute_url}}/assets/images/addon-example.png "Google Sheets Add-on Example.")
{: .full}


## Limitations

Google puts time limitations concerning the execution of custom Google Sheet functions. As a consequence, the CREES add-on may fail when too many items are annotated at the same time. If you get an error, consider applying the CREES functions to fewer items each time (e.g., 10 items 10 times rather than 100 items at the same time).
{: .notice--warning}