import os

import logging

from app import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest    
    import sys
    
    stdout_handler = logging.StreamHandler(sys.stdout)    
    logger = logging.getLogger("TestLog")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(stdout_handler)

    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
