from .mc_printing import MidiCheckPrintingMixin

class MidiCheckUtilitiesMixin(MidiCheckPrintingMixin):
    """Mixin class providing utilities for managing MIDI check contexts.

    This class facilitates the creation and management of context structures
    for MIDI checks, allowing for dynamic naming and retrieval of contexts
    based on the current path.

    Args:
        name (str): The name of the new context to be created. Defaults to "children".
        parent (str): The parent context name. Defaults to None.

    Raises:
        ValueError: If the context structure is improperly accessed.

    Examples:
        # Example usage of the context management methods
        mixin = MidiCheckUtilitiesMixin()
        mixin._set_new_context("test_context")
        current_context = mixin._get_current_context()
    """


    def _set_new_context(self, name="children", parent=None):
        """Sets a new context in the current context structure.

        This method creates a new context based on the provided name and parent,
        ensuring that the context structure is properly initialized and navigated
        according to the current path.

        Args:
            name (str): The name of the new context to be created. Defaults to "children".
            parent (str): The parent context name. Defaults to None.

        Returns:
            None
        """

        name = self._autoname(name, parent)
        parent = self._autoname(parent)

        context_ref = self.contexts
        for part in self.current_path:
            context_ref = context_ref.setdefault(part, {})

        context_ref.setdefault(name, {})


    def _get_current_context(self):
        """Retrieves the current context based on the current path.

        This method navigates through the context structure using the current path
        and returns the corresponding context. If the path does not exist, it returns
        the original context.

        Args:
            None

        Returns:
            dict: The current context corresponding to the current path.
        """

        context = self.contexts.copy()
        for part in self.current_path:
            context = context.get(part, context)
        return context

    def _autoname(self, name="children", parent=""):
        """Generates a unique name for a context based on the current context.

        This method creates a new name by appending a number to the provided name
        if it already exists within the specified parent context. It ensures that
        names remain unique within the context structure.

        Args:
            name (str): The base name to be used for the context. Defaults to "children".
            parent (str): The parent context name to check against. Defaults to an empty string.

        Returns:
            str: A unique name for the context.
        """

        if name:
            context = self._get_current_context()
            if parent in context:
                context = context[parent]
                name = f"{name}_{len(context[name]) + 1}"
            elif name in context:
                name = f"{name}_{len(context[name])}"
        return name

    def _autonameTests(self, name="test", parent="TESTS"):
        """Generates a unique name for a test context based on the current context.

        This method creates a new name for a test by appending a number to the
        provided name if it already exists within the specified parent context. 
        It ensures that test names remain unique within the context structure.

        Args:
            name (str): The base name to be used for the test context. Defaults to "test".
            parent (str): The parent context name to check against. Defaults to "TESTS".

        Returns:
            str: A unique name for the test context.
        """

        context = self._get_current_context()
        if parent in context:
            context = context[parent]
        if name in context:
            name = f"{name}_{self.unnamed_tests + 1}"
            self.unnamed_tests += 1
        return name

    def _trigger_messages(self, result, test):
        """Logs messages based on the result of a test.

        This method updates the message log with the status of a test based on its
        result and whether it was previously triggered. It also updates the test's
        passed status accordingly.

        Args:
            result (bool): The result of the test, indicating success or failure.
            test (dict): A dictionary containing test information, including its name,
                        triggered status, passed status, and callback messages.

        Returns:
            None
        """

        status = "SUCCESS" if result else "FAIL"
        if test["triggered"]:
            if test["passed"] != result:
                self.msg_log.append(self._format_message(status, f"{test['name']} was {'Passed' if result else 'Failed'}, now is:", ignore=True))
            else:
                self.msg_log.append(self._format_message(status, f"{test['name']} was {'Passed' if result else 'Failed'}, still is:", ignore=True))

        self.msg_log.append(test["callback_true"] if result else test["callback_false"])
        test["passed"] = result