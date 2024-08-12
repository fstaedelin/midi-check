##
# @package MIDI_CHECK
# @ingroup MIDI_CHECK
# @{
##

##
# @class MidiCheckPrintingMixin
# A mixer class to handle functions helpful to print messages
class MidiCheckPrintingMixin:
    ##
    # @brief Increases indentation level and prints entering/exiting messages.
    #
    # This method increments the indentation level and prints a message indicating
    # the entry into a specific function. This is useful for tracking the flow of
    # execution and understanding the nested structure of function calls.
    #
    # @param fn_name The name of the function being entered.
    # @return None
    #
    def _printIn(self, fn_name):
        """
        Increase indentation level and print entering message.

        :param fn_name: The name of the function being entered.
        """
        self.print_lvl += 1
        print(self.print_lvl * "  ", "In : ", fn_name)

    ##
    # @brief Decreases indentation level and prints an exiting message.
    #
    # This method decreases the indentation level and prints a message indicating
    # the exit from a specific function. This helps in tracking when functions are
    # completed and the flow of control is returning to a higher level.
    #
    # @param fn_name The name of the function being exited.
    # @return None
    #
    def _printOut(self, fn_name):
        """
        Decrease indentation level and print exiting message.

        :param fn_name: The name of the function being exited.
        """
        print(self.print_lvl * "  ", "Out: ", fn_name)
        self.print_lvl -= 1

    ##
    # @brief Prints a debug message with the current indentation level.
    #
    # This method outputs a debug message that is formatted according to the current
    # level of indentation. It is useful for providing contextual information during
    # the execution of the program.
    #
    # @param name The name of the debug message.
    # @param val The value or content of the debug message.
    # @return None
    #
    def _print(self, name, val=""):
        """
        Print a debug message with the current indentation.

        :param name: The name of the debug message.
        :param val: The value or content of the debug message.
        """
        print('|   ' * (len(self._get_current_context()) + 1), name, ":  ", val)

    ##
    # @brief Prints the current state of contexts for debugging purposes.
    #
    # This method outputs the current state of various contexts, which can be
    # helpful for understanding the internal state of the program at a particular
    # point in time.
    #
    # @return None
    #
    def _print_contexts(self):
        """
        Print the current state of contexts for debugging.
        """
        self._print("----------------------------------------------------------")
        self._print("self.contexts              ", self.contexts)
        self._print("self.current_path          ", self.current_path)
        self._print("self.get_current_context   ", self._get_current_context())
        self._print("----------------------------------------------------------")

    ##
    # @brief Formats a log message based on its level and other parameters.
    #
    # This method creates a formatted log message that includes information such as
    # the logging level, an optional name, and the message content. It can also decide
    # whether to append the message to the log based on the ignore parameter.
    #
    # @param level The logging level (e.g., SUCCESS, DEBUG, ERROR).
    # @param message The message to format.
    # @param name Optional name to include in the message.
    # @param ignore Whether to ignore adding the message to the log.
    # @return The formatted message.
    #
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

##
# @}
##