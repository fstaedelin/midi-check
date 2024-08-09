from LoggerUtilities import LoggerUtilitiesMixin

class Logger(LoggerUtilitiesMixin):
    def __init__(self, level="WARNING"):
        """
        Initialize the Logger with a default logging level.

        :param level: Default logging level, defaults to "WARNING".
        """
        self.print_lvl = -1  # Used for tracking indentation in print statements
        self.level = level  # Set the default logging level
        self.tests = []  # List to store all tests
        self.levels = {
            "INFO": 0,
            "DEBUG": 10,
            "FAIL": 15,
            "SUCCESS": 15,
            "WARNING": 20,
            "ERROR": 30
        }  # Define logging levels with priorities
        self.msg_log = []  # Log to store all messages
        self.contexts = {}  # Initialize the root context
        self.unnamed_tests = 0  # Counter for unnamed tests
        self.current_path = []  # Path to the current context
        
    def Navigate(self, destination="children"):
        """
        Navigate to a different context.

        :param destination: The context to navigate to. Defaults to "children".
        """
        if destination == "parent":
            if len(self.current_path) > 0:  # Move to the parent context
                self.current_path.pop()
            else:
                print("Cannot Navigate to parent, root has no parents")
        else:
            # Create a new context if the destination doesn't exist
            if destination not in self._get_current_context():
                self._set_new_context(destination)
            self.current_path.append(destination)  # Move to the new or existing context

    def WriteLog(self):
        """
        Print all the log entries stored in `msg_log`.
        """
        for entry in self.msg_log:
            print(entry)
            
    def Log(self, message, level):
        """
        Log a message at the given level.

        :param message: The message to log.
        :param level: The level at which to log the message.
        :return: The formatted message.
        """
        if level not in self._get_current_context():
            self._set_new_context(level)

        self.Navigate(level)  # Go to the desired level
        msg_number = len(self._get_current_context())
        formatted_message = self._format_message(level, message)
        self._get_current_context()[msg_number] = formatted_message
        self.Navigate("parent")  # Return to the previous context

        return formatted_message

    def Debug(self, message):
        """
        Log a debug message.

        :param message: The debug message to log.
        """
        self.Log(message, "DEBUG")

    def Warning(self, message):
        """
        Log a warning message.

        :param message: The warning message to log.
        """
        self.Log(message, "WARNING")

    def Error(self, message):
        """
        Log an error message.

        :param message: The error message to log.
        """
        self.Log(message, "ERROR")

    def AddTest(self, 
            test_fn=lambda: False,
            result_key=True, 
            callback_true=None,
            callback_false=None, 
            name="test"):
        """
        Add a new test to the current context.

        :param test_fn: The test function to evaluate.
        :param result_key: Expected result key for the test.
        :param callback_true: Callback function if the test passes.
        :param callback_false: Callback function if the test fails.
        :param name: Name of the test.
        :return: The newly added test object.
        """
        if "TESTS" not in self._get_current_context():
            self._set_new_context("TESTS")
        self.Navigate("TESTS")
        
        # Set automatic callbacks if not provided
        if callback_false is None:
            callback_false = self.Cb_False(f"Test {name} failed!")
        if callback_true is None:
            callback_true = self.Cb_True(f"Test {name} passed :D")

        # Automatically name the test if not provided
        name = self._autonameTests(name)
        
        # Define new test and assign it in the context
        newTest = {
            "name": name,
            "test_fn": test_fn,
            "result_key": result_key,
            "callback_true": callback_true,
            "callback_false": callback_false,
            "passed": False,
            "triggered": False,
            "output": {}
        }
        
        self._get_current_context()[name] = newTest
        self.tests.append(newTest)
        self.Navigate("parent")  # Return to the previous context

        return newTest  # Optionally return the test object if needed elsewhere

    def TriggerTest(self, test, val):
        """
        Trigger a specific test.

        :param test: The test object to trigger.
        :param val: The value to pass to the test function.
        :return: The test object after execution.
        """
        if ("TESTS" not in self._get_current_context()) or test["name"] not in self._get_current_context()["TESTS"]:
            print("Not in the correct context to trigger the test")

        # Execute the test function with the given value
        result = test["test_fn"](val) and test["result_key"]
        self._trigger_messages(result, test)
        test["triggered"] = True
        return test

    def Cb_True(self, message, level="SUCCESS"):
        """
        Generate a success callback message.

        :param message: The message to format.
        :param level: The logging level, defaults to "SUCCESS".
        :return: The formatted message.
        """
        formatted_message = self._format_message(level, message, ignore=True)
        return formatted_message
    
    def Cb_False(self, message, level="FAIL"):
        """
        Generate a failure callback message.

        :param message: The message to format.
        :param level: The logging level, defaults to "FAIL".
        :return: The formatted message.
        """
        formatted_message = self._format_message(level, message, ignore=True)
        return formatted_message
