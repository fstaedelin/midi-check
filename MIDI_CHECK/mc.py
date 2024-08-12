##
# @package MIDI_CHECK
# @brief MIDI_CHECK is a logging package designed to help developers manage complex logging scenarios.
# It provides various utilities for logging messages at different levels, managing contexts,
# and testing functionality. This module defines the main MIDI_CHECK class, which integrates all
# the utility functions and logging capabilities into a single, easy-to-use interface.
# @ingroup MIDI_CHECK
#
# @{
##

from MIDI_CHECK.mc_utilities import MidiCheckUtilitiesMixin


##
# @class Main class for the MIDI_CHECK logging system.
#
# The MIDI_CHECK class extends MidiCheckUtilitiesMixin, incorporating a variety of logging and
# utility functions. This class provides methods for logging messages at different levels,
# navigating between contexts, adding and triggering tests, and generating callback messages.
# The class is designed to be the central point of interaction for the MIDI_CHECK logging system.
class MIDI_CHECK(MidiCheckUtilitiesMixin):
    ##
    # @brief Initializes the MIDI_CHECK logger with a default logging level.
    #
    # This constructor sets up the initial state of the MIDI_CHECK logger, including
    # the logging level, context hierarchy, and test management. It also initializes
    # internal variables that track indentation levels, logging contexts, and the log itself.
    #
    # @param level The default logging level (defaults to "WARNING").
    #
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

    ##
    # @brief Navigate to a different context within the logger.
    #
    # This method allows the user to move between different contexts within the
    # logging hierarchy. It can navigate to a child context or move up to the
    # parent context. If the destination context does not exist, it creates a new one.
    #
    # @param destination The context to navigate to (defaults to "children").
    #
    def Navigate(self, destination="children", logging=False):
        """
        Navigate to a different context.

        :param destination: The context to navigate to. Defaults to "children".
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
                    self.Warning("Destination does not exist, creating nested context: "+destination, True)
                self._set_new_context(destination)
            if not logging: 
                self.Debug("Moving to: " + destination, True)
            self.current_path.append(destination)  # Move to the new or existing context

    ##
    # @brief Print all the log entries stored in `msg_log`.
    #
    # This method iterates over all log entries stored in the `msg_log` list and
    # prints them. This provides a simple way to output the entire log to the console.
    #
    def WriteLog(self):
        """
        Print all the log entries stored in `msg_log`.
        """
        for entry in self.msg_log:
            print(entry)

    ##
    # @brief Log a message at a specified level.
    #
    # This method logs a message at the given level by navigating to the appropriate
    # context, formatting the message, and storing it in the current context. It also
    # returns the formatted message.
    #
    # @param message The message to log.
    # @param level The level at which to log the message.
    # @return The formatted message.
    #
    def Log(self, message, level, navigating = False):
        """
        Log a message at the given level.

        :param message: The message to log.
        :param level: The level at which to log the message.
        :return: The formatted message.
        """
#        if level not in self._get_current_context():
#            self._set_new_context(level)
        
        if not navigating:
            self.Navigate(level, True)  # Go to the desired level
            self.Navigate("parent", True)  # Return to the previous context

        msg_number = len(self._get_current_context())
        formatted_message = self._format_message(level, message)
        self._get_current_context()[msg_number] = formatted_message
        return formatted_message

    ##
    # @brief Log a debug message.
    #
    # This method logs a message at the "DEBUG" level, which is typically used
    # for detailed debugging information that may not be required during normal operation.
    #
    # @param message The debug message to log.
    #
    def Debug(self, message, navigating = False):
        """
        Log a debug message.

        :param message: The debug message to log.
        """
        self.Log(message, "DEBUG", navigating)

    ##
    # @brief Log a warning message.
    #
    # This method logs a message at the "WARNING" level, which is typically used
    # for logging potentially harmful situations or important notices that require
    # attention.
    #
    # @param message The warning message to log.
    #
    def Warning(self, message, navigating = False):
        """
        Log a warning message.

        :param message: The warning message to log.
        """
        self.Log(message, "WARNING", navigating)

    ##
    # @brief Log an error message.
    #
    # This method logs a message at the "ERROR" level, which is typically used
    # for logging serious issues that might cause the application to behave unexpectedly.
    #
    # @param message The error message to log.
    #
    def Error(self, message, navigating = False):
        """
        Log an error message.

        :param message: The error message to log.
        """
        self.Log(message, "ERROR", navigating)

    ##
    # @brief Add a new test to the current context.
    #
    # This method adds a new test to the current context within the logging hierarchy.
    # The test is defined by a test function, expected result, and optional callback
    # functions for handling success and failure. The test is automatically named to
    # avoid conflicts, and the method returns the test object.
    #
    # @param test_fn The test function to evaluate (defaults to a lambda returning False).
    # @param result_key Expected result key for the test (defaults to True).
    # @param callback_true Callback function if the test passes (defaults to a success message).
    # @param callback_false Callback function if the test fails (defaults to a failure message).
    # @param name Name of the test (defaults to "test").
    # @return The newly added test object.
    #
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
        self.Debug("Created test: "+name)
        return newTest  # Optionally return the test object if needed elsewhere

    ##
    # @brief Trigger a specific test.
    #
    # This method triggers a specific test by executing the test function with the
    # provided value. It then logs appropriate success or failure messages based
    # on the test result and updates the test's status.
    #
    # @param test The test object to trigger.
    # @param val The value to pass to the test function.
    # @return The test object after execution.
    #
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

    ##
    # @brief Generate a success callback message.
    #
    # This method generates a callback message indicating that a test has passed.
    # The message is formatted with a "SUCCESS" level by default.
    #
    # @param message The message to format.
    # @param level The logging level (defaults to "SUCCESS").
    # @return The formatted message.
    #
    def Cb_True(self, message, level="SUCCESS"):
        """
        Generate a success callback message.

        :param message: The message to format.
        :param level: The logging level, defaults to "SUCCESS".
        :return: The formatted message.
        """
        formatted_message = self._format_message(level, message, ignore=True)
        return formatted_message

    ##
    # @brief Generate a failure callback message.
    #
    # This method generates a callback message indicating that a test has failed.
    # The message is formatted with a "FAIL" level by default.
    #
    # @param message The message to format.
    # @param level The logging level (defaults to "FAIL").
    # @return The formatted message.
    #
    def Cb_False(self, message, level="FAIL"):
        """
        Generate a failure callback message.

        :param message: The message to format.
        :param level: The logging level, defaults to "FAIL".
        :return: The formatted message.
        """
        formatted_message = self._format_message(level, message, ignore=True)
        return formatted_message
##
# @}
##
