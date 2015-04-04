# beautify-dpxdt
Create html-files from the results of running dpxdt locally.

## Why

If you use dpxdt locally, as described [here](https://github.com/bslatkin/dpxdt/wiki/Local-dpxdt), you get only some log-output which tests failed.

This small python-script will scan the tmp-folder for files created by dpxdt and create an index.html and for every test another html-file referencing the base-, the diff- and the current screenshot. Now you can open one of the generated html-files in your browser and inspect the test-results.

## Install

Pull this repository, cd into it and run `pip install -r requirements.txt`

## Run

* Run dpxdt in test-mode: e.g. `dpxdt test <path-to-your-tests>`
* Run `python beautify-dpxdt-results.py <path-to-tmp>`
* Inspect your `<path-to-tmp>`-folder and open the `index.html`-file in your browser.

## Future

This script will be part of the [dpxdt-docker-file](https://github.com/factorial-io/dpxdt-docker) to beautify the output. The dockerfile includes a fully running dpxdt-installation with phantom-js etc.

## Todo

* Better styling of the html-files.
