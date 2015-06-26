[![Build Status](https://travis-ci.org/Harvard-ATG/canvas-syllabus-export.svg?branch=master)](https://travis-ci.org/Harvard-ATG/canvas-syllabus-export)

# Canvas Syllabus Export
Canvas LTI tool for exporting a customized course syllabus as a PDF 
# Installation Notes
1. You must configure a secure file containing an oauth authentication key for running the project locally
```sh
# secure.py

SECURE_SETTINGS = {'oauthtoken': "sampleoauthtoken"}
```
2. In order for the tool to work for any Canvas course, you must generate a master oauth token.
