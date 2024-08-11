import os
import glob
import importlib.util

def importTests():
    # Import all test modules from the 'tests' folder that start with 'TEST_'.
    #
    # @return A dictionary where keys are module names and values are the imported modules.
    return _importHelp("tests")

def _importHelp(folder):
    # Helper function to import all modules from a specific folder whose names contain 'TEST'.
    #
    # @param folder The folder containing the modules you want to import.
    # @return A dictionary where keys are module names and values are the imported modules.
    
    # Ensure the folder path is absolute
    folder_path = os.path.abspath(folder)
    
    # Find all .py files in the folder that which name starts with 'TEST_'
    pattern = os.path.join(folder_path, 'TEST_.py')
    module_files = glob.glob(pattern)
    
    imported_modules = {}
    
    # Print the absolute path of the folder for debugging purposes
    print(folder_path)
    
    for file_path in module_files:
        # Print the file path for each test module found
        print(file_path)
        
        # Extract the module name from the file name (remove the '.py' extension)
        module_name = os.path.basename(file_path)[:-3]
        
        # Load the module from its file path
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Store the imported module in the dictionary
        imported_modules[module_name] = module
    
    return imported_modules

# Imports all files containing 'TEST' in the 'tests' folder
testLib = importTests()

# Launches all tests by simply referencing them
for _, test in testLib.items():
    test

