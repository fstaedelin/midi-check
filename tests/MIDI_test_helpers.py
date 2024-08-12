##
# @file Contains utils for MIDI-related tests
from MIDI_CHECK.mc import MIDI_CHECK

# Initialize the MIDI_CHECK logger with an "INFO" level.
mc = MIDI_CHECK("INFO")


##
# @class Represents a MIDI event.
#
# The Event class encapsulates data related to MIDI events. This includes
# the event ID, whether the event has been handled, and potentially other
# MIDI-specific information such as the type of event (e.g., Note On, Note Off),
# the channel number, and additional data bytes (e.g., note number, velocity).
class Event:
    ##
    # @brief Initializes a new instance of the Event class.
    #
    # The constructor initializes the event with an ID and a handled status.
    # The handled attribute is set to False by default, indicating that the
    # event has not yet been processed.
    #
    # @param event_id The unique identifier for the event.
    # @param handled A boolean indicating whether the event has been handled (default is False).
    #
    def __init__(self, event_id, handled=False):
        self.id = event_id  # The unique identifier for the event.
        self.handled = handled  # Whether the event has been handled or not.

        # Additional attributes for MIDI event details could include:
        self.type = None  # MIDI event type (e.g., Note On, Note Off, Control Change).
        self.channel = None  # MIDI channel (0-15).
        self.data = []  # Data bytes associated with the MIDI event.

    ##
    # @brief Set the MIDI event details.
    #
    # This method allows setting the type, channel, and data bytes of the MIDI event.
    #
    # @param event_type The type of MIDI event (e.g., "Note On", "Control Change").
    # @param channel The MIDI channel number (0-15).
    # @param data A list of data bytes associated with the event.
    #
    def set_event_details(self, event_type, channel, data):
        self.type = event_type
        self.channel = channel
        self.data = data

    ##
    # @brief Marks the event as handled.
    #
    # This method updates the handled attribute to True, indicating that the event
    # has been processed.
    #
    def mark_handled(self):
        self.handled = True


# Add a test to check if a given value is greater than 100.
# This test returns True if the value exceeds 100, otherwise False.
is_more_100 = mc.AddTest(
    test_fn=lambda x: x > 100,
    name=">100"
)

# Add a test to check if a given value is greater than 150.
# This test returns True if the value exceeds 150, otherwise False.
is_more_150 = mc.AddTest(
    test_fn=lambda x: x > 150,
    name=">150"
)