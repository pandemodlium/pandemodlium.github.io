This is a static site blog like Jekyll for Github pages, but it uses python and flask instead of ruby to generate the static pages.

It generates

[https://pandemodlium.github.io/](https://pandemodlium.github.io/)

## Updating information
* update any yml files in app/main/static/dat/\
    * papers.yml: see its header for more, is the main one
    * *not* static/dat/papers.yml, which is used for display and produced in publication
* run ```python manage.py publish 'Your commit message here'```
* to test before uploading: ```python manage.py freeze && python -m http.server```

## Notes

* see flask-jekyll for more info
* This repo is used for the convenience functions from flask-jekyll 
* flask-jekyll is really for blog posts but it has nice convenience commands I'm cannibalizing.
* flask-jekyll convenience commands:
    * to publish your blog pages: `python manage.py publish`.  This command will create a bunch of new directories in your root directory.  Those are the html files that are going to be served on github pages.  You will be prompted for whether to push your changes.
