// CREES automatically annotates short texts. It identifies if a text is about a crisis, crisis-types and information-types.
// The Crisis Event Extraction Service (CREES) provides multiple functions for annotating short text documents for helping 
// to classify large amount of short document (e.g. tweets) by 1) identifying if a document is related to a crisis event 
// (e.g., fire, earthquake); 2) the type of event discussed and, 3) the type of information present in a document. 
// 
// The CREES add-on provides three different customs functions that can be applied on textual columns or individual cells for 
// annotating the contained text. Each cell should contain a small document similar in length to tweets.
// 
// The CREES add-on makes available the following functions:
// 
// - CREES_RELATED: Identifies if a short text document discusses a crisis event (returns one of the following labels: 
//                  non-related, related).
// 
// - CREES_EVENT: Identifies the type of event discussed within a short textual document (returns one of the following 
//                labels: bombings, collapse, crash, derailment, earthquake, explosion, fire, floods, haze, meteorite, 
//                none, shootings, typhoon, wildfire).
// 
// - CREES_INFO: Identifies the type of information discussed within a short textual crisis-related document (returns one
//               of the following labels: affected_individuals, caution_and_advice, donations_and_volunteering, 
//               frastructure_and_utilities, not_applicable, not_labeled, other_useful_information, sympathy_and_support).
// 
// More information about each function can be obtained in the built-in documentation. You can access it by typing its the
// function name in a spreadsheet cell.
// 
// More information about CREES can be found on the API website (https://github.com/evhart/crees) or in the following
// publication:
// 
// On Semantics and Deep Learning for Event Detection in Crisis Situations. Burel, Grégoire; Saif, Hassan; Fernandez, 
// Miriam and Alani, Harith (2017). On Semantics and Deep Learning for Event Detection in Crisis Situations. In:
// Workshop on Semantic Deep Learning (SemDeep), at ESWC 2017, 29 May 2017, Portoroz, Slovenia.
// 
// This work has received support from the European Union’s Horizon 2020 research and innovation programme under grant 
// agreement No 687847 (COMRADES).

/**
 * @fileoverview Provides the custom functions CREES_RELATED, CREES_EVENT and CREES_INFO.
 * @OnlyCurrentDoc
 */

/**
 * Global variables
 */
var DEFAULT_CREES_API_URI = 'http://socsem.open.ac.uk/comrades/events/';
var CREES_API_NAMES = ["eventRelated", "eventType", "infoType"];


/**
 * Get the current API enpoint from the properties service.
 */
function getCreesApiUrl() {
  var documentProperties = PropertiesService.getDocumentProperties();
  var creesApiUrl = documentProperties.getProperty('creesApiUrl');

  if (creesApiUrl == null || creesApiUrl.length == 0) {
    creesApiUrl = DEFAULT_CREES_API_URI;
  }
  return creesApiUrl;
}

/**
 * Write the API enpoint to the properties service.
 */
function setCreesApiUrl(url) {
  var documentProperties = PropertiesService.getDocumentProperties();
  documentProperties.setProperty('creesApiUrl', url)
  return url;
}

/**
 * Runs when the add-on is installed.
 */
function onInstall(e) {
  onOpen(e);
}

/**
 * Runs when the document is opened, creating the add-on's menu. Custom function
 * add-ons need at least one menu item, since the add-on is only enabled in the
 * current spreadsheet when a function is run.
 */
function onOpen(e) {
  SpreadsheetApp.getUi().createAddonMenu()
    .addItem('Edit API Endpoint', 'editCreesAPIEndpoint')
    .addItem('Reset API Endpoint', 'resetCreesAPIEndpoint')
    .addItem('About', 'about')
    .addToUi();
}

/**
 * Shows information about the add-on.
 */
function about() {
  var html = HtmlService.createHtmlOutputFromFile('about');
  SpreadsheetApp.getUi() // Or DocumentApp or FormApp.
    .showModalDialog(html, 'About CREES');
}

/**
 * Allow the user to change the API endpoint used by the add-on.
 */
function editCreesAPIEndpoint() {
  var ui = SpreadsheetApp.getUi();
  var result = ui.prompt(
    'Edit Document API Endpoint',
    'API Endpoint (Current: ' + getCreesApiUrl() + ')',
    ui.ButtonSet.OK_CANCEL);

  var button = result.getSelectedButton();
  var text = result.getResponseText();
  if (button == ui.Button.OK) {
    setCreesApiUrl(text);
  }
}

/**
 * Reset API endpoint to its default value.
 */
function resetCreesAPIEndpoint() {
  var ui = SpreadsheetApp.getUi(); // Same variations.
  var result = ui.alert(
    'Reset API Endpoint?',
    'The CREES API enpoint will be reset to its default value (' + DEFAULT_CREES_API_URI + ')',
    ui.ButtonSet.YES_NO);

  if (result == ui.Button.YES) {
    setCreesApiUrl(DEFAULT_CREES_API_URI);
  }
}

/**
 * Assign a Hash for a given text for using it a s a key for the caching service.
 */
function SHA1(s) {
  var hexstr = '';
  var digest = Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_1, s)
  for (i = 0; i < digest.length; i++) {
    var val = (digest[i] + 256) % 256;
    hexstr += ('0' + val.toString(16)).slice(-2);
  }
  return hexstr;
}

/**
 * Performs a CRESS API call for one cell.
 */
function creesApiCall(name, text) {
  //Returns if there is some text to analyse.
  if (text) {
    var hash = SHA1(text);
    var cache = CacheService.getScriptCache();
    var creesApiUrl_ = getCreesApiUrl();


    var cached = cache.get("crees-" + name + "-" + hash);
    if (cached != null) {
      return cached;
    }

    var options = {
      'method': 'get'
    };

    Utilities.sleep(1000); //Sleep for 1sec for not overloading the google servers
    
    try {
      var response = JSON.parse(UrlFetchApp.fetch(creesApiUrl_ + name + "?text=" + encodeURIComponent(text), options));
    } catch(e) {
        throw 'There is an issue with the CREES API endpoint. Please try again later or change the CREES API endpoint in the add-on menu.';
    }
      
    cache.put("crees-" + name + "-" + hash, response.label, 21600); // Cache data for 6hrs (the maximum allowed by Google).

    return response.label;
  }

  //Returns nothing if there is no text to analyse.
  return ''

}


/**
 * Performs a CRESS API call for multiple cells (column).
 */
function creesBatchApiCall(name, texts, max_batch) {
  var cache = CacheService.getScriptCache();
  var creesApiUrl = getCreesApiUrl();

  // Split in smaller batches for not overloading the server with massive jobs:
  if (max_batch == null) {
    max_batch = 1000;
  }

  var results = [];
  while (texts.length > 0) {
    var curr_texts = texts.splice(0, max_batch);

    // Check what value is cached, remove the elements that are already cached:
    cached_dict = {};
    curr_texts_uncached = curr_texts.filter(function (text) {
      var hash = SHA1(text);
      var cached = cache.get("crees-" + name + "-" + hash);

      if (cached != null) {
        cached_dict[text] = cached;
      }
      return cached == null;
    });

    //Returns if there is some text to analyse.
    if (curr_texts_uncached.length > 0) {
      var options = {
        'method': 'post',
        'contentType': 'application/json',
        'payload': JSON.stringify(curr_texts)
      };

      Utilities.sleep(100); //Sleep for 1sec for not overloading the CREES API
      
      try {
        var response = JSON.parse(UrlFetchApp.fetch(creesApiUrl + name, options));
      } catch(e) {
        throw 'There is an issue with the CREES API endpoint. Please try again later or change the CREES API endpoint in the add-on menu.';
      }
     
      //Add to cached map:
      try{
        response.labels.forEach(function (item) {
          if (item.input) {
            cached_dict[item.input] = item.label;
          } else {
            cached_dict[item.input] = '';
          }
          var hash = SHA1(item.input);
          cache.put("crees-" + name + "-" + hash, cached_dict[item.input], 21600); // Cache data for 6hrs (the maximum allowed by Google).
        });
      } catch(e) {
        throw 'There is no data to annotate.';
      }
    }
    var curr_results = curr_texts.map(function (text) {
      return cached_dict[text];
    });
    results = results.concat(curr_results);
  }
  return results;
}

/**
 * CREES API custom functions template.
 */
function creesCustomFunction(name, strings) {
  
  
  
  var input = strings;
  if (input.map && input.length > 1) {
    if (input[0].map && (input[0].length > 1)) {
      throw 'Input contains multiple columns. Please select only one column or cell.';
    } else if (input[0].map) {
      input = input.map(function (x) {
        return x[0];
      }); //Convert to simple array.
    }
    return creesBatchApiCall(name, input);

  } else if (!(typeof input[0] === 'string') && !(input[0] == null)) {
    throw 'Input contains a cell value that is not a string';
  }
  return creesApiCall(name, input);
}


/**
 * Identifies if a short text document or string discusses a crisis event.
 *
 * @param {string|Range} text The string, or range of strings to annotate.
 * @return {string} The annotation label ("non-related", "related").
 * @customfunction
 */
function CREES_RELATED(text) {
  return creesCustomFunction("eventRelated", text);
}

/**
 * Identifies the type of event discussed within a short textual document or string.
 *
 * @param {string|Range} text The string, or range of strings to annotate.
 * @return {string} The annotation label ("bombings", "collapse", "crash", "derailment", "earthquake", "explosion", "fire", "floods", "haze", "meteorite", "none", "shootings", "typhoon", "wildfire").
 * @customfunction
 */
function CREES_EVENT(text) {
  return creesCustomFunction("eventType", text);
}


/**
 * Identifies the type of information discussed within a short textual crisis-related document or string.
 *
 * @param {string|Range} text The string, or range of strings to annotate.
 * @return {string} The annotation label ("affected_individuals", "caution_and_advice", "donations_and_volunteering","infrastructure_and_utilities", "not_applicable", "not_labeled", "other_useful_information", "sympathy_and_support").
 * @customfunction
 */
function CREES_INFO(text) {
  return creesCustomFunction("infoType", text);
}