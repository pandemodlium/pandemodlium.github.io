from flask import render_template, url_for
from . import main
from .. import pages, freezer
import os, yaml, pandas as pd, re

"""
@main.route('/')
def home():
    posts = [page for page in pages]
    # Sort pages by date
    sorted_posts = sorted(posts, reverse=True,
        key=lambda page: page.meta['date'])
    return render_template('index.html', pages=sorted_posts)
"""

@main.route('/<path:path>/')
def page(path):
    # 'path is the filename of a page, without the file extension'
    # e.g. "first-post"
    page = pages.get_or_404(path)
    return render_template('page.html', page=page)



basedir = os.path.abspath(os.path.dirname(__file__))
datadir = os.path.join(basedir, '../static/dat/')

class astr(str):
    """Class with additional function to make anchor-kosher text"""
    def anchor(self):
        return re.sub('[^A-Za-z0-9_-]', '', self.replace(' ','_'))

def get_papers():
    """Read in the data on papers and process a bit.
    1. Turn 'author' into a list where it is not one.
    2. fill NA with '' (0-length string)
    3. If there is a github site then add the tag 'github'
    """

    with open(os.path.join(datadir, 'papers.yml')) as f:
        papers = pd.DataFrame(yaml.load(f, Loader=yaml.BaseLoader)).fillna('')

    # Turn author into list where is a string
    a = papers['author']
    s = a.map(lambda x: isinstance(x, str)) # where is string
    a.loc[s] = a.loc[s].map(lambda x: [x])

    for i in papers[papers['github']!=''].index:
        papers.loc[i, 'tags'] = list(set(papers.loc[i, 'tags']).union({'github'}))

    # Convert tags to class astr so can use anchor function
    papers['tags'] = papers['tags'].map(lambda ts: [astr(t) for t in ts])

    return papers

@main.route("/")
@main.route('/index.html')
def home():
    return render_template('index.html')

@main.route("/papers.html")
def papers():
    # get the data
    return render_template('papers.html', papers=get_papers())


@main.route("/tags.html")
def tags():
    # get the data
    with open(os.path.join(datadir, 'papers.yml')) as f:
        papers = yaml.load(f, Loader=yaml.BaseLoader)
    p = get_papers()
    # Get pairs of (tag, papers)
    tags = set()
    for t in p['tags']:
        tags = tags.union(t)
    tags = sorted(tags, key=str.casefold)
    tagpapers = []
    for t in tags: # list of tuples: tag, and a dataframe
        tagpapers.append((t,  p[p['tags'].map(lambda z: t in z)]))
    return render_template('tags.html', tagpapers=tagpapers)
