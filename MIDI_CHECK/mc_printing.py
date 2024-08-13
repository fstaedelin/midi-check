class MidiCheckPrintingMixin:
    """Mixin class for printing MIDI check information.

    This class provides methods to print debug information related to MIDI checks, including 
    entering and exiting functions, printing context details, and formatting messages based on 
    their severity level.
    """
    
    def _printIn(self, fn_name):
        """Prints the entry of a function with an increasing indentation level.
        
        This method increments the print level and outputs the function name
        being entered, formatted with the current indentation level.

        Args:
            fn_name (str): The name of the function being entered.

        Returns:
            None
        """
        self.print_lvl += 1
        print(self.print_lvl * "  ", "In : ", fn_name)

    def _printOut(self, fn_name):
        """Prints the exit of a function with decreased indentation.

        This method outputs the function name being exited and decrements the print level to 
        reflect the exit from the function.

        Args:
            fn_name (str): The name of the function being exited.
            
        Returns:
            None
        """
        print(self.print_lvl * "  ", "Out: ", fn_name)
        self.print_lvl -= 1

    def _print(self, name, val=""):
        """Prints a name-value pair with the current context indentation.

        This method outputs a formatted string that includes the current context's indentation 
        along with the provided name and value, allowing for structured logging of information.

        Args:
            name (str): The name to print.
            val (str, optional): The value to print. Defaults to an empty string.

        Returns:
            None
        """

        print('|   ' * (len(self._get_current_context()) + 1), name, ":  ", val)

    def _print_contexts(self):
        """Prints the current contexts and path information.

        This method outputs a formatted display of the current contexts, the
        current path, and the context being accessed. It provides a clear
        visual separation of the information for better readability.

        Args:
            None

        Returns:
            None
        """

        self._print("----------------------------------------------------------")
        self._print("self.contexts              ", self.contexts)
        self._print("self.current_path          ", self.current_path)
        self._print("self.get_current_context   ", self._get_current_context())
        self._print("----------------------------------------------------------")

    def _format_message(self, level, message, name="", ignore=False):
        """Formats a message for output with a specified level and optional name.

        This method prepares a message for display, allowing for customization
        based on the provided level and name. It can also be configured to ignore
        certain conditions based on the ignore flag.

        Args:
            level (int): The severity level of the message.
            message (str): The message content to format.
            name (str, optional): An optional name to include in the message. Defaults to an empty string.
            ignore (bool, optional): A flag indicating whether to ignore the message. Defaults to False.

        Returns:
            str: The formatted message.
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
