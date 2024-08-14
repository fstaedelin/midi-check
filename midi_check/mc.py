from .mc_utilities import MidiCheckUtilitiesMixin


class MIDI_CHECK(MidiCheckUtilitiesMixin):
    """Class for managing MIDI checks and logging.

    This class provides functionality to create and manage tests, log messages,
    and navigate through context structures for MIDI checks. It allows for
    dynamic logging at various levels and facilitates the addition and triggering
    of tests.

    Attributes:
        print_lvl (int): Tracks indentation in print statements.
        level (str): The current logging level.
        tests (list): A list to store all tests.
        levels (dict): A dictionary defining logging levels with priorities.
        msg_log (list): A log to store all messages.
        contexts (dict): A dictionary to initialize the root context.
        unnamed_tests (int): A counter for unnamed tests.
        current_path (list): A list representing the path to the current context.

    Examples:
        midi_check = MIDI_CHECK()
        midi_check.AddTest(lambda: True, name="Sample Test")
        midi_check.TriggerTest(midi_check.tests[0], "test value")
    """


    def __init__(self, level="WARNING"):
        """Initializes the MIDI_CHECK class with default settings.

        This constructor sets up the initial state of the MIDI_CHECK instance,
        including the logging level, message log, and context management. It
        prepares the instance to manage tests and log messages at various levels.

        Args:
            level (str): The default logging level. Defaults to "WARNING".
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


    def Navigate(self, destination="children", logging=False):
        """Navigates to a specified context within the MIDI check structure.

        This method allows moving to a new context or back to the parent context,
        creating a new context if it does not already exist. It also provides an
        option to log the navigation actions.

        Args:
            destination (str): The name of the context to navigate to. Defaults to "children".
            logging (bool): A flag indicating whether to log the navigation actions. Defaults to False.

        Returns:
            None
        """

        if destination == "parent":
            if len(self.current_path) > 0:  # Move to the parent context
                if not logging: 
                    self.Debug("Moving to parent folder", True)
                self.current_path.pop()
            else:
                print("Cannot Navigate to parent, root has no parents")
        else:
            # Create a new context if the destination doesn't exist
            if destination not in self._get_current_context():
                if not logging: 
                    self.Warning(f"Destination does not exist, creating nested context: {destination}", True)
                self._set_new_context(destination)
            if not logging: 
                self.Debug(f"Moving to: {destination}", True)
            self.current_path.append(destination)  # Move to the new or existing context

    def WriteLog(self):
        """Prints all log entries stored in the message log.

        This method iterates through the message log and outputs each entry to
        the console, allowing users to review all logged messages.

        Args:
            None

        Returns:
            None
        """
        """
        Print all the log entries stored in `msg_log`.
        """
        for entry in self.msg_log:
            print(entry)

    def Log(self, message, level, navigating=False):
        """Logs a message at a specified logging level.

        This method navigates to the appropriate context level, formats the message,
        and stores it in the current context. It also allows for navigation to be
        skipped if already in the desired context.

        Args:
            message (str): The message to be logged.
            level (str): The logging level at which to log the message.
            navigating (bool): A flag indicating whether to navigate to the desired level. Defaults to False.

        Returns:
            str: The formatted message that was logged.
        """

        if not navigating:
            self.Navigate(level, True)  # Go to the desired level
            self.Navigate("parent", True)  # Return to the previous context

        msg_number = len(self._get_current_context())
        formatted_message = self._format_message(level, message)
        self._get_current_context()[msg_number] = formatted_message
        return formatted_message

    def Debug(self, message, navigating=False):
        """Logs a debug message at the DEBUG logging level.

        This method formats and logs a debug message, optionally navigating to the
        desired context level before logging. It serves as a convenience method for
        logging messages specifically at the DEBUG level.

        Args:
            message (str): The debug message to be logged.
            navigating (bool): A flag indicating whether to navigate to the desired level. Defaults to False.

        Returns:
            str: The formatted debug message that was logged.
        """

        self.Log(message, "DEBUG", navigating)

    def Warning(self, message, navigating=False):
        """Logs a warning message at the WARNING logging level.

        This method formats and logs a warning message, optionally navigating to the
        desired context level before logging. It serves as a convenience method for
        logging messages specifically at the WARNING level.

        Args:
            message (str): The warning message to be logged.
            navigating (bool): A flag indicating whether to navigate to the desired level. Defaults to False.

        Returns:
            str: The formatted warning message that was logged.
        """

        self.Log(message, "WARNING", navigating)

    def Error(self, message, navigating=False):
        """Logs an error message at the ERROR logging level.

        This method formats and logs an error message, optionally navigating to the
        desired context level before logging. It serves as a convenience method for
        logging messages specifically at the ERROR level.

        Args:
            message (str): The error message to be logged.
            navigating (bool): A flag indicating whether to navigate to the desired level. Defaults to False.

        Returns:
            str: The formatted error message that was logged.
        """

        self.Log(message, "ERROR", navigating)

    def AddTest(self,
                test_fn=lambda: False,
                result_key=True,
                callback_true=None,
                callback_false=None,
                name="test"):
        """Adds a new test to the MIDI check context.

        This method allows for the registration of a test function along with its
        associated callbacks and name. It ensures that the test is properly named
        and added to the current context for later execution.

        Args:
            test_fn (function): The function to be executed as the test. Defaults to a function that returns False.
            result_key (bool): A key indicating the expected result of the test. Defaults to True.
            callback_true (function): A callback function to be executed if the test passes. Defaults to None.
            callback_false (function): A callback function to be executed if the test fails. Defaults to None.
            name (str): The name of the test. Defaults to "test".

        Returns:
            dict: The newly created test object containing its details.
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
        self.Debug(f"Created test: {name}")
        return newTest  # Optionally return the test object if needed elsewhere

    def TriggerTest(self, test, val):
        """Triggers the execution of a specified test with a given value.

        This method executes the test function associated with the provided test
        object, using the specified value as input. It updates the test's status
        based on the result of the execution and logs the appropriate messages.

        Args:
            test (dict): The test object containing the test function and its details.
            val: The value to be passed to the test function during execution.

        Returns:
            dict: The updated test object after execution.
        """

        if ("TESTS" not in self._get_current_context()) or test["name"] not in self._get_current_context()["TESTS"]:
            print("Not in the correct context to trigger the test")

        # Execute the test function with the given value
        result = test["test_fn"](val) and test["result_key"]
        self._trigger_messages(result, test)
        test["triggered"] = True
        return test

    def Cb_True(self, message, level="SUCCESS"):
        """Formats a success callback message.

        This method creates a formatted message indicating a successful outcome,
        using the specified level for logging. It is intended to be used as a
        callback when a test passes.

        Args:
            message (str): The message to be formatted for the success callback.
            level (str): The logging level for the message. Defaults to "SUCCESS".

        Returns:
            str: The formatted success message.
        """

        return self._format_message(level, message, ignore=True)

    def Cb_False(self, message, level="FAIL"):
        """Formats a failure callback message.

        This method creates a formatted message indicating a failure outcome,
        using the specified level for logging. It is intended to be used as a
        callback when a test fails.

        Args:
            message (str): The message to be formatted for the failure callback.
            level (str): The logging level for the message. Defaults to "FAIL".

        Returns:
            str: The formatted failure message.
        """
        return self._format_message(level, message, ignore=True)
