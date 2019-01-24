#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask, url_for, render_template, redirect, json # request

from docs import run_sphinx
run_sphinx.run_sphinx()

app = Flask(__name__)
app.logger.setLevel(DEBUG)


### MEMORY #####################################################################

### ERRORS #####################################################################

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

### PAGES ######################################################################

@app.route('/home')
def page_home():
    return redirect(url_for('page_index'))

@app.route('/')
@app.route('/index')
def page_index():
    return render_template( 'index.html',
                            url = 'http://10.1.152.116/index',
                            title='Basic Template',
                            text='Basic Template')

### API ########################################################################

@app.route('/api/v1')
def api_explain_v1():
    return json.dumps(get_static_info('api_information'))

### Controller #################################################################


### ENTRY ######################################################################

if __name__ == '__main__':
    if os.__name__ == 'nt':
        app.run(debug=True, host='0.0.0.0')
    else:
        app.run(host='0.0.0.0')
        #app.run(host='10.1.152.116')
