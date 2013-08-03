import sys, os
package_dir = "packages"
package_dir_path = os.path.join(os.path.dirname(__file__), package_dir)
sys.path.insert(0, package_dir_path)

from google.appengine.ext.webapp.util import run_wsgi_app
from application import app

run_wsgi_app(app)
