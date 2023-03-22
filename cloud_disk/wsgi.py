#!/usr/bin/env python

import sys
import site

site.addsitedir('/data/hitme/lib/python3.6/site-packages')

sys.path.insert(0, '/data/hitme')

from app import app as application
