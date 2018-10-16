---
title: "Influences on Bike Rentals"
subtitle: "What are the influening factors and <br>how well can they predict the number of rented bikes?"
author: "Ingo Nader"
date: "Oct 2018"
#output: html_document
output: 
  ioslides_presentation:
    css: styles-edx.css
    #logo: img/logo-um-154x127.png
    widescreen: true
    keep_md: true
    #smaller: true  ## only works without "---" slide breaks (use ##)
    slide_level: 2
## Comments and Instructions
##
## ## ------------------------------------------- ##
## ## Controlling presentation (best use chrome):
## ## ------------------------------------------- ##
    # 'f' enable fullscreen mode
    # 'w' toggle widescreen mode
    # 'o' enable overview mode
    # 'h' enable code highlight mode
    # 'p' show presenter notes
##
## ## ------------------------------------------- ##
## ## Images
## ## ------------------------------------------- ##
##
## Replace markdown images "![]()" with R's include_graphics()
## (in order for them to scale to slide width properly):
## Search:
## !\[\]\((.*)\)
## Replace with:
## ```{r, eval = TRUE, echo = FALSE, out.width = "100%", fig.align = "left"}\nknitr::include_graphics("\1")\n```
##
##
## ## ------------------------------------------- ##
## ## Font size in slides, and other layout stuff
## ## ------------------------------------------- ##
##
## use {.smaller} after title for single slides
## use {.flexbox .vcenter} for centering of text
## 
## ## ------------------------------------------- ##
## ## color:
## ## ------------------------------------------- ##
##
##   <div class="red2"></div>
## or:
##   <font color="red"> </font>
##
## ## ------------------------------------------- ##
## ## two-column layout:
## ## ------------------------------------------- ##
## 
## <div></div>                            <!-- needed, but don't put anything here -->
## <div style="float: left; width: 50%;"> <!-- start of first column               -->
## Put col 1 markdown here
## </div>                                 <!-- end of first column                 -->
## <div style="float: left; width: 50%;"> <!-- start of second column              --> 
## Put col 2 markdown here
## </div>                                 <!-- end of second column                -->
## 
## other possibilities (not as good):
## * In slide title line, use:
##   ## title {.columns-2}
## * put md into this div:
##   <div class="columns-2">  </div>
##
---
[//]: # (
http://www.w3schools.com/css/css_font.asp
http://www.cssfontstack.com/Helvetica
)

<style>
/* gdbar size (that contains logo) on title page */
/* needs to have greater height than logo image, other stuff is irrelevant */
.gdbar {
  position:absolute !important;
  top: 50px !important; left: auto; right: 0px !important; width: 0px !important;
  height: 500px !important;  /* modify if logo is larger than this in height */
}

/* logo size on title page */
.gdbar img {
  position: absolute; 
  top: 0px;
  left: 50px;
  width: 154px !important;
  height: 127px !important;
}

/* logo size on slides */
slides > slide:not(.nobackground):before {
  width: 77px; height: 64px; /* modify width and height (twice) */
  background-size: 77px 64px;
  position: absolute; left: auto;
  right: -30px;  /* modify position */
  top: 10px;
}


/*slides > slide.backdrop {   */
/*  background-color:#ffaaaa;   */
/*  background:#ffaaaa;   */
/*}   */
</style>



## Abstract

Summarize your questions and findings in 1 brief paragraph (4-6 sentences max). Your abstract needs to include: what dataset, what question, what method was used, and findings.
 
## Motivation
Describe the problem you want to solve with the data. It may relate closely with your research question, but your goal here is to make your audience care about the project/problem you are trying to solve. You need to articulate the problem you are exploring and why (and for whom) insight would be valuable.
 
## Dataset(s)
Describe your dataset(s) here. You should say what data is in the dataset, how much data, and where you found the dataset (if applicable).
 
## Data Preparation and Cleaning
At a high-level, what did you need to do to prepare the data for analysis? Describe what problems, if any, did you encounter with the dataset?
 
## Research Question(s)
What is your research question you aim to answer using the dataset? Be sure the research question is well defined (see project description for details).
 
## Methods
What methods did you use to analyze the data and why are they appropriate? Be sure to adequately, but briefly, describe your methods.
 
## Findings
Feel free to replicate this slide to show multiple findings

Present your findings. Include at least one visualization in your presentation (feel free to include more). The visualization should be honest, accessible, and elegant for a general audience.
You need not come to a definitive conclusion, but you need to say how your findings relate back to your research question.
 
## Limitations
If applicable, describe limitations to your findings. For example, you might note that these results were true for British Premier league players but may not be applicable to other leagues because of differences in league structures.
Or you may note that your data has inherent limitations. For example, you may not have access to the number of Twitter followers per users so you assumed all users are equally influential. If you had the number of followers, you could weight the impact of their tweet’s sentiment by their influence (# of followers).

Brainstorming: 

* Results only valid for cities with roughly the same climate.
* Bike rides might be influenced by weather *predictions* for a given day, not only by the actual weather.
* Precipitation (rain, snow) might also be a very good predictor; unfortunately, this was not easily available for the given weather station.
 
## Conclusions
Report your overall conclusions, preferably a conclusion per research question
 
## Acknowledgements
Where did you get your data? Did you use other informal analysis to inform your work? Did you get feedback on your work by friends or colleagues? Etc. If you had no one give you feedback and you collected the data yourself, say so.
 
## References
If applicable, report any references you used in your work. For example, you may have used a research paper from X to help guide your analysis. You should cite that work here. If you did all the work on your own, please state this.
 