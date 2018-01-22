---
layout: single
classes:
  - landing

author_profile: false

title: "About CREES"
permalink: /about/


header:
  overlay_filter: rgba(46, 87, 87, 0.5)
  overlay_image: https://images.unsplash.com/photo-1493852303730-955ff798ba12?auto=format&fit=crop&w=1138&q=80
  caption: "Photo by [Braden Hopkins](https://unsplash.com/photos/4WJcte5CByc?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/search/photos/emergency?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)."



excerpt: 'Crisis Event Extraction Service'

---


The CRESS API is a multilclass CNN classifier that is trained on the [CrisisLexT26 data](https://github.com/sajao/CrisisLex/tree/master/data/CrisisLexT26). The model extends  Kim Yoon’s [Convolutional Neural Networks for Sentence Classification](http://arxiv.org/abs/1408.5882) and Denny Britz's [work](https://github.com/dennybritz/cnn-text-classification-tf). The model was published along the Dual-CNN model in the paper: [On Semantics and Deep Learning for Event Detection in Crisis Situations](http://oro.open.ac.uk/49639/).


If you use this code/model please cite the following publication:
- *[On Semantics and Deep Learning for Event Detection in Crisis Situations](http://oro.open.ac.uk/49639/)*
Burel, Grégoire; Saif, Hassan; Fernandez, Miriam and Alani, Harith (2017). On Semantics and Deep Learning for Event Detection in Crisis Situations. In: Workshop on Semantic Deep Learning (SemDeep), at ESWC 2017, 29 May 2017, Portoroz, Slovenia.

## Code
The CREES API code and models can be downloaded from [GitHub](https://github.com/evhart/crees). 

## Report an Issue
If you find any bug or have any issues with the API, you can add an isue to the (bug tracker)[https://github.com/evhart/crees/issues].


## References
- *[Semantic Wide and Deep Learning for Detecting Crisis-Information Categories on Social Media](http://oro.open.ac.uk/51726/)*
Burel, Grégoire; Saif, Hassan and Alani, Harith (2017). 
Semantic Wide and Deep Learning for Detecting Crisis-Information Categories on Social Media.  In: The Semantic Web – ISWC 2017. 2017, Vienna, Austria.
- *[On Semantics and Deep Learning for Event Detection in Crisis Situations](http://oro.open.ac.uk/49639/)*
Burel, Grégoire; Saif, Hassan; Fernandez, Miriam and Alani, Harith (2017). On Semantics and Deep Learning for Event Detection in Crisis Situations. In: Workshop on Semantic Deep Learning (SemDeep), at ESWC 2017, 29 May 2017, Portoroz, Slovenia.
- [COMRADES H2020 European Project](http://www.comrades-project.eu/)
- [CrisLex Datasets](http://crisislex.org/data-collections.html)
- [Convolutional Neural Networks for Sentence Classification](http://arxiv.org/abs/1408.5882)
- [Implementing a CNN for Text Classification in TensorFlow](http://www.wildml.com/2015/12/implementing-a-cnn-for-text-classification-in-tensorflow/)

## Acknowledgment
This work has received support from the European Union’s Horizon 2020 research and innovation programme under grant agreement [No 687847](http://cordis.europa.eu/project/rcn/198819_en.html) ([COMRADES](http://www.comrades-project.eu/)).
