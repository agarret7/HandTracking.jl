import os, sys
import unittest


# env variables
TESTDIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(TESTDIR, ".."))

# import your test modules
import vis

# initialize the test suite
loader = unittest.TestLoader()
suite  = unittest.TestSuite()

# add tests to the test suite
suite.addTests(loader.loadTestsFromModule(vis))

# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
