import os
import sys

import logging

from app import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
stdout_handler = logging.StreamHandler(sys.stdout)    
logger = logging.getLogger("ImagesLogger")
logger.setLevel(logging.INFO)
logger.addHandler(stdout_handler)


@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest        
    
    stdout_handler = logging.StreamHandler(sys.stdout)    
    logger = logging.getLogger("TestLog")
    logger.setLevel(logging.INFO)
    logger.addHandler(stdout_handler)

    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__=='__main__':
    app.run()