from utility.import_utils import importTests
# Imports all files containing TEST in JARVIS/tests/
testLib = importTests()

# launches all tests
for _, test in testLib.items():
    test
