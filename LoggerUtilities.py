from Logger_printing import LoggerPrintingMixin

class LoggerUtilitiesMixin(LoggerPrintingMixin):
    """
    Mixin class for various utility functions used by the Logger class.
    """

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

    def _get_current_context(self):
        """
        Get the current context based on the current path.

        :return: The current context dictionary.
        """
        context = self.contexts.copy()
        for part in self.current_path:
            context = context.get(part, context)
        return context

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
