# `nbsearch`
Datasette based notebook search extension, originally inspired by Simon Willison's [Fast Autocomplete Search for Your Website](https://24ways.org/2018/fast-autocomplete-search-for-your-website/).


## Installation

`pip3 install --upgrade git+https://github.com/ouseful-testing/nbsearch.git`

## Usage

*This is still very much a work in progress.*

### From the command line

- create a database by passing a path to some notebook files, eg:
  - `nbsearch index -p "/Users/myuser/Documents/content/notebooks"`
- run the server, eg:
  -  `nbsearch serve`

  
`datasette` should start up and display a server port number.


## UI

![](.images/nbsearch.png)



## Know Issues

The links to notebooks may well be broken: I need to think about how to index and handle paths in links, particular in proxy server case.

Not tried: the `jupyter-server-proxy` version (bits of code are in place, but more fettling may still be required before it even runs, let alone works...)

The db should probably be placed somewhere out of the way; could we even keep it in the Python static file area?

MyBinder hates the repo for some reason? `Could not resolve ref for gh:ouseful-testing/nbsearch/master. Double check your URL.`

