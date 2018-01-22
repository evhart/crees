---
layout: splash
classes:
  - landing

author_profile: false

header:
  overlay_filter: rgba(46, 87, 87, 0.5)
  overlay_image: https://images.unsplash.com/photo-1514514188727-ff38e839635e?auto=format&fit=crop&w=1834&q=80
  caption: "Photo by [William Topa](https://unsplash.com/photos/x9AZgR25G-k?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/search/photos/emergency?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)."
  cta_label: "<i class='fas fa-play'></i> Learn more"
  cta_url: "/api/quick-start-guide/"


excerpt: 'Automatic classification and filtering of crisis-related social media posts for situation awarness.'


title: "Crisis Event Extraction Service (CREES)"

intro: 
  - excerpt: "CREES provides a Web API and accessible tools for automatically filtering and classifying social media documents during emergency crises."

intro2: 
  - excerpt: 'CREES is hosted on [GiHub](https://github.com/evhart/crees), free and open-source and can be installed on a personal computer or server. <br/><br/> {::nomarkdown}<iframe style="display: inline-block;" src="https://ghbtns.com/github-btn.html?user=evhart&repo=crees&type=star&count=true&size=large" frameborder="0" scrolling="0" width="160px" height="30px"></iframe> <iframe style="display: inline-block;" src="https://ghbtns.com/github-btn.html?user=evhart&repo=crees&type=fork&count=true&size=large" frameborder="0" scrolling="0" width="158px" height="30px"></iframe>{:/nomarkdown}'


feature_row:
  - image_path: /assets/images/api.png
    alt: "CREES API"
    #title: "CREES API"
    excerpt: "The CREES API detect crisis-related documents, event types and the information discussed in documents."
    url: "/api/quick-start-guide"
    btn_label: "Learn More"
    btn_class: "btn--inverse"

  - image_path: /assets/images/sheets.png
    alt: "Google Sheets Add-on"
    #title: "CREES Google Sheets"
    excerpt: "CREES is integratated into Google Sheets as a add-on and can be used for automatically annotating spreadsheets documents."
    url: "/add-on/quick-start-guide"
    btn_label: "Learn More"
    btn_class: "btn--inverse"

  - image_path: /assets/images/comrades.png
    alt: "COMRADES Platforme"
    #title: "CREES and COMRADES"
    excerpt: "CREES is integrated into the Ushahidi platform as part of the COMRADES platform."
    url: "http://www.comrades-project.eu/"
    btn_label: "Learn More"
    btn_class: "btn--inverse"
---

{% include feature_row id="intro" type="center" %}

{% include feature_row %}

{% include feature_row id="intro2" type="center" %}
