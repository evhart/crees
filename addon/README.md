
# Crisis Event Extraction Service (CREES) Google Sheets Web Add-on
Website: https://evhart.github.io/crees/add-on/

Add-on: [Google Webstore Addon](https://chrome.google.com/webstore/detail/crisis-event-extraction-s/jekdamaeeejebcccbgleijlfamjcbilc?utm_source=permalink)


This directory contains the [CREES add-on]((https://chrome.google.com/webstore/detail/crisis-event-extraction-s/jekdamaeeejebcccbgleijlfamjcbilc?utm_source=permalink)) source code. The add-on can be installed directly on the [Google Webstore](https://chrome.google.com/webstore/detail/crisis-event-extraction-s/jekdamaeeejebcccbgleijlfamjcbilc?utm_source=permalink) or executed locally by copying the add-on files in the script editor (in the Google Sheets menu bar, select: *Tools > Script editor*).



If you use this code/model please cite the following publications and link to this repository:
- *[On Semantics and Deep Learning for Event Detection in Crisis Situations](http://oro.open.ac.uk/49639/)*
Burel, Grégoire; Saif, Hassan; Fernandez, Miriam and Alani, Harith (2017).  In: Workshop on Semantic Deep Learning (SemDeep), at ESWC 2017, 29 May 2017, Portoroz, Slovenia.
- *[Crisis Event Extraction Service (CREES) - Automatic Detection and Classification of Crisis-related Content on Social Media.](http://oro.open.ac.uk/55139/)*
Burel, Grégoire and Alani, Harith (2018). In: 15th International Conference on Information Systems for Crisis Response and Management, 20-23 May 2018, Rochester, NY, USA.

## Usage
The [CREES add-on](https://chrome.google.com/webstore/detail/crisis-event-extraction-s/jekdamaeeejebcccbgleijlfamjcbilc?utm_source=permalink) makes available the following functions:

- *CREES_RELATED*: Identifies if a short text document discusses a crisis event (returns one of the following labels: non-related, related).

- *CREES_EVENT*: Identifies the type of event discussed within a short textual document (returns one of the following labels: bombing, collapse, crash, derailment, earthquake, explosion, fire, flood, haze, meteorite, none, shooting, typhoon, wildfire).

- *CREES_INFO*: Identifies the type of information discussed within a short textual crisis-related document (returns one of the following labels: affected_individuals, caution_and_advice, donations_and_volunteering, infrastructure_and_utilities, not_applicable, not_labeled, other_useful_information, sympathy_and_support).

The full add-on documentation is available on the [CREES website](https://evhart.github.io/crees/add-on/).

### Advanced Usage
When installed, a new entry is added to the Add-ons menu of the Google Sheets page when the add-on is installed.

The Crisis Event Extraction Service (CREES) submenu adds the following entries:

- *Edit API Endpoint*: If you need to use your own publically available CREES API installation, you can modify the default URI of the server API.
- *Reset API Endpoint*: This item resets the API URI address to its default value.
- *About CREES*: This items shows a small description of CREES and the Add-on features.

## References
- *[On Semantics and Deep Learning for Event Detection in Crisis Situations](http://oro.open.ac.uk/49639/)*
Burel, Grégoire; Saif, Hassan; Fernandez, Miriam and Alani, Harith (2017).  In: Workshop on Semantic Deep Learning (SemDeep), at ESWC 2017, 29 May 2017, Portoroz, Slovenia.
- *[Crisis Event Extraction Service (CREES) - Automatic Detection and Classification of Crisis-related Content on Social Media.](http://oro.open.ac.uk/55139/)*
Burel, Grégoire and Alani, Harith (2018). In: 15th International Conference on Information Systems for Crisis Response and Management, 20-23 May 2018, Rochester, NY, USA.
- [COMRADES H2020 European Project](http://www.comrades-project.eu/)


## Acknowledgment
This work has received support from the European Union’s Horizon 2020 research and innovation programme under grant agreement [No 687847](http://cordis.europa.eu/project/rcn/198819_en.html) ([COMRADES](http://www.comrades-project.eu/)).
