class LoggerPrintingMixin:
    def _printIn(self, fn_name):
        """
        Increase indentation level and print entering message.

        :param fn_name: The name of the function being entered.
        """
        self.print_lvl += 1
        print(self.print_lvl * "  ", "In : ", fn_name)
    
    def _printOut(self, fn_name):
        """
        Decrease indentation level and print exiting message.

        :param fn_name: The name of the function being exited.
        """
        print(self.print_lvl * "  ", "Out: ", fn_name)
        self.print_lvl -= 1
    
    def _print(self, name, val=""):
        """
        Print a debug message with the current indentation.

        :param name: The name of the debug message.
        :param val: The value or content of the debug message.
        """
        print('|   ' * (len(self._get_current_context()) + 1), name, ":  ", val)
    
    def _print_contexts(self):
        """
        Print the current state of contexts for debugging.
        """
        self._print("----------------------------------------------------------")
        self._print("self.contexts              ", self.contexts)
        self._print("self.current_path          ", self.current_path)
        self._print("self.get_current_context   ", self._get_current_context())
        self._print("----------------------------------------------------------")

    def _format_message(self, level, message, name="", ignore=False):
        """
        Format the log message based on its level.

        :param level: The logging level.
        :param message: The message to format.
        :param name: Optional name to include in the message.
        :param ignore: Whether to ignore adding the message to the log.
        :return: The formatted message.
        """
        if level == "SUCCESS":
            indent = '====' * (len(self.current_path))
        elif level == "FAIL":
            indent = '|XXX' + '|   ' * (len(self.current_path) - 1)
        else:    
            indent = '|   ' * (len(self.current_path))
            
        flag = {
            "SUCCESS": '===3',
            "DEBUG": '|-->',
            "ERROR": "|/!\\",
            "WARNING": "|/!\\",
            "FAIL": "|/X\\"
        }.get(level, '')
        lvl = {
            "SUCCESS": 'C===',
            "DEBUG": "DBG|",
            "ERROR": "|/!\\",
            "WARNING": "WNG!",
            "FAIL": "|/X\\",
        }.get(level, '')
        if name:
            formatted_message = f"{lvl}{indent}{flag}|{name}:{message}"
        else:
            formatted_message = f"{lvl}{indent}{flag}|{message}"
        
        if not ignore:
            self.msg_log.append(formatted_message)
        
        return formatted_message
