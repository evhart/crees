---
title: "CREES API"
permalink: /api/quick-start-guide/
---


The [COMRADES](http://www.comrades-project.eu/) CREES Services (Crisis Event Extraction Service) provide a rest API for annotating short text documents (e.g. tweets) by 1) identifying if a document is related to a crisis; 2) the type of event discussed and, 3) the type of information present in a document:

### <i class='fas fa-info-circle'></i> Event Relatedness
Determines if a document is related to a crisis situation.


### <i class='fas fa-calendar'></i> Event Type
Determines the type of crisis discussed in a document. CREES can identify the following types of event from short social media posts:
<ul style="margin: auto; width: 90%; height: 200px; display:flex; flex-direction: column; flex-wrap: wrap;">
  <li>Bombings</li>
  <li>Building collapse</li>
  <li>Crash</li>
  <li>Derailment</li>
  <li>Earthquake</li>
  <li>Explosion</li>
  <li>Fire</li>
  <li>Floods</li>
  <li>Haze</li>
  <li>Meteorite</li>
  <li>Shootings</li>
  <li>Typhoon</li>
  <li>Wildfire</li>
</ul>


### <i class='fas fa-question-circle'></i> Information Category
Determines the type of information discussed in a document.
<ul style="margin: auto; width: 90%; height: 300px; display:flex; flex-direction: column; flex-wrap: wrap;">
 <li>Affected individuals (people trapped, casualties, etc.)</li>
 <li>Caution and advice (general information)</li>
 <li>Donations and volunteering (people offering help)</li>
 <li>Infrastructure and utilities (damage to infrastructure)</li>
 <li>Other useful information (non categorised useful information)</li>
 <li>Sympathy and support (moral support, prayers, etc.)</li>
</ul>

## APIs Usage

![CREES API]({{'' | absolute_url}}/assets/images/api-screen.png "CREES API")
{: .full}

The CREES API exposes 3 services that can be tested using a web browser. By default, they are accessible under */comrades*. Each method can be accessed using a *GET* query with the *text* parameter or a *POST* query that can be used for annotating more than one document. The methods are the following:

1) ***/comrades/events/eventRelated***: Determines if a document is related to a crisis sitution. The following labels are returned: *"non-related", "related"*.

2) ***/comrades/events/eventType***: Determines the type of crisis discussed in a document. The following labels are returned: *"bombings", "collapse", "crash", "derailment", "earthquake", "explosion", "fire", "floods", "haze", "meteorite", "none", "shootings", "typhoon"* and *"wildfire"*.

3) ***/comrades/events/infoType***: Determines the type of information discussed in a document. The following labels are returned: *"affected_individuals", "caution_and_advice", "donations_and_volunteering", "infrastructure_and_utilities", "not_applicable", "not_labeled", "other_useful_information"* and *"sympathy_and_support"*.


## Usage Example

Each method returns a similar JSON object. For example:
```sh
curl -G http://127.0.0.1/comrades/events/infoType  \
--data-urlencode 'text=If you are evacuating please dont wait, take your pets when you evacuate #HighParkFire'
```
```json
{
    "classifier": "CNN",
    "input": "if you are evacuating please dont wait, take your pets when you evacuate ",
    "label": "caution_and_advice",
    "version": 0.3
}
```

Although the *GET* method only accepts one document as input, you can use the *POST* version in order to annotate more than one document by submitting a JSON array containning a list of documents to annotate. Each method returns a similar JSON object. For example:

```sh
 curl -X POST http://127.0.0.1/comrades/events/eventRelated  --header 'Content-Type: application/json' -d '["If you are evacuating please dont wait, take your pets when you evacuate #HighParkFire", "AAPL, NBA playoffs 2013, New York Post, West Texas, ..."]'
```
```json
{  
   "labels": [  
      {  
         "input": "If you are evacuating please dont wait, take your pets when you evacuate #HighParkFire",
         "label": "related"
      },
      {  
         "input": "AAPL, NBA playoffs 2013, New York Post, West Texas, ...",
         "label": "non-related"
      }
   ],
   "classifier": "CNN",
   "version": 0.3
}
```
