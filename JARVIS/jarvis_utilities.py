##
# @package JARVIS
# JARVIS is a logging package designed to aid in debugging, formatting output, 
# and managing complex logging contexts. This module introduces the 
# JarvisUtilitiesMixin class, which provides various utility functions to manage 
# and manipulate logging contexts, handle naming conventions, and trigger 
# appropriate log messages based on test results.

from jarvis_printing import JarvisPrintingMixin

##
# @brief Mixin class providing utility functions for the Logger class.
#
# The JarvisUtilitiesMixin class extends the JarvisPrintingMixin class and includes
# several utility functions that manage logging contexts, handle automatic naming
# of contexts and tests, and trigger messages based on the outcomes of tests.
# These utilities are designed to work seamlessly with the logging system in JARVIS.
class JarvisUtilitiesMixin(JarvisPrintingMixin):
    """
    Mixin class for various utility functions used by the Logger class.
    """

    ##
    # @brief Sets a new context in the logger's hierarchy.
    #
    # This method creates and sets a new context within the logging hierarchy. 
    # It can either initialize a root context if none exists, or it navigates 
    # the existing hierarchy to add a new sub-context. The new context is named 
    # either as specified or automatically to avoid conflicts.
    #
    # @param name The name of the new context (defaults to "children").
    # @param parent The parent context in which to create the new context (defaults to None).
    # @return None
    #
    def _set_new_context(self, name="children", parent=None):
        """
        Set a new context in the logger's hierarchy.

        :param name: The name of the new context.
        :param parent: The parent context, defaults to None.
        """
        name = self._autoname(name, parent)
        parent = self._autoname(parent)
        
        if not self.current_path:  # If no current path, initialize the root context
            if name not in self.contexts:
                self.contexts[name] = {}

        else:  # Navigate to the current context and add the new context
            context_ref = self.contexts
            for part in self.current_path:
                if part not in context_ref:
                    context_ref[part] = {}
                context_ref = context_ref[part]
            
            if name not in context_ref:
                context_ref[name] = {}

    ##
    # @brief Retrieves the current context based on the current path.
    #
    # This method navigates the hierarchy of contexts according to the current path
    # and returns the dictionary representing the current context. It allows for easy
    # access to the current working context within the logger.
    #
    # @return The current context dictionary.
    #
    def _get_current_context(self):
        """
        Get the current context based on the current path.

        :return: The current context dictionary.
        """
        context = self.contexts.copy()
        for part in self.current_path:
            context = context.get(part, context)
        return context

    ##
    # @brief Automatically generates a name for a new context to avoid conflicts.
    #
    # This method generates a name for a new context, ensuring that it does not
    # overwrite existing contexts with the same name. It appends a number to the 
    # name if a conflict is detected, making it unique within the parent context.
    #
    # @param name The desired context name (defaults to "children").
    # @param parent The parent context name (defaults to an empty string).
    # @return The auto-generated name.
    #
    def _autoname(self, name="children", parent=""):
        """
        Automatically name the context to avoid overwriting existing contexts.

        :param name: The desired context name.
        :param parent: The parent context name, defaults to an empty string.
        :return: The auto-generated name.
        """
        if name:
            context = self._get_current_context()
            if parent in context:
                context = context[parent]
                name = f"{name}_{len(context[name]) + 1}"
            elif name in context:
                name = f"{name}_{len(context[name])}"
        return name
    
    ##
    # @brief Automatically generates a unique name for a new test.
    #
    # This method automatically names a new test within a specific parent context
    # (by default, the "TESTS" context). It ensures that the test name is unique by 
    # appending a number if necessary, which prevents overwriting existing tests.
    #
    # @param name The desired test name (defaults to "test").
    # @param parent The parent context name (defaults to "TESTS").
    # @return The auto-generated test name.
    #
    def _autonameTests(self, name="test", parent="TESTS"):
        """
        Automatically name the test to avoid overwriting existing tests.

        :param name: The desired test name.
        :param parent: The parent context name, defaults to "TESTS".
        :return: The auto-generated test name.
        """
        context = self._get_current_context()
        if parent in context:
            context = context[parent]
        if name in context:
            name = f"{name}_{self.unnamed_tests + 1}"
            self.unnamed_tests += 1
        return name
    
    ##
    # @brief Triggers success or failure messages based on the result of a test.
    #
    # This method appends appropriate success or failure messages to the log, depending
    # on the outcome of a test. It also handles the callback functions associated with
    # the test, which are triggered when a test passes or fails. The method ensures that
    # the correct sequence of messages is logged, providing clear feedback on the test's
    # status.
    #
    # @param result The result of the test (True for success, False for failure).
    # @param test The test object containing information about the test and callbacks.
    # @return None
    #
    def _trigger_messages(self, result, test):
        """
        Trigger success or failure messages based on the test result.

        :param result: The result of the test (True/False).
        :param test: The test object.
        """
        if result:
            self.msg_log.append(self._format_message("SUCCESS", "----------------", ignore=True))
            if test["triggered"] and not test["passed"]:
                self.msg_log.append(test["callback_false"])
            elif test["triggered"]:
                self.msg_log.append(test["callback_true"])
            
            self.msg_log.append(test["callback_true"])
            self.msg_log.append(self._format_message("SUCCESS", "----------------", ignore=True))
            test["passed"] = True
        else:
            self.msg_log.append(self._format_message("FAIL", "----------------"))
            if test["triggered"] and not test["passed"]:
                self.msg_log.append(test["callback_false"])
            elif test["triggered"]:
                self.msg_log.append(test["callback_true"])
            
            self.msg_log.append(test["callback_false"])
            self.msg_log.append(self._format_message("FAIL", "----------------", ignore=True))
            test["passed"] = False

