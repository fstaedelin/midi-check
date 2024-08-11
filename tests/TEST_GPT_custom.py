from tests.test_helpers import *

# Initialize the MIDI event with some initial values
event1 = Event(230, False)
event2 = Event(50, True)  # Another event for more comprehensive testing

# Start testing with JARVIS logger
jarvis.Debug("GOING TO INITIALIZATION")
jarvis.Navigate("INIT")
jarvis.Debug("Initializing MIDI Script ...")

# Add tests for MIDI events
jarvis.Debug("ADDING MIDI EVENT TESTS")
test_event_handled = jarvis.AddTest(
    test_fn=lambda event: event.handled,
    name="Event handled"
)

test_event_id_gt_100 = jarvis.AddTest(
    test_fn=lambda event: event.id > 100,
    name="Event ID > 100"
)

test_event_id_lt_100 = jarvis.AddTest(
    test_fn=lambda event: event.id < 100,
    name="Event ID < 100"
)

# Trigger tests with the initial event
jarvis.Debug("TRIGGERING MIDI EVENT TESTS")
jarvis.TriggerTest(test_event_handled, event1.handled)
jarvis.TriggerTest(test_event_id_gt_100, event1.id)
jarvis.TriggerTest(test_event_id_lt_100, event1.id)

# Navigate to the "Processor" context for further tests
jarvis.Navigate("parent")
jarvis.Navigate("Processor")
jarvis.Debug("ADDING PROCESSOR TESTS")

# Add additional tests specific to the "Processor" context
test_event_id_gt_150 = jarvis.AddTest(
    test_fn=lambda event: event.id > 150,
    name="Event ID > 150"
)

jarvis.Debug("TRIGGERING PROCESSOR TESTS")
jarvis.TriggerTest(test_event_id_gt_150, event1.id)

# Simulate a change in event and log it
jarvis.Navigate("parent")
jarvis.Debug("MIDI EVENT CHANGED")
event1 = Event(1110, False)  # New event with updated values

# Trigger the tests again with the updated event
jarvis.Debug("TRIGGERING TESTS WITH UPDATED EVENT")
jarvis.TriggerTest(test_event_handled, event1.handled)
jarvis.TriggerTest(test_event_id_gt_100, event1.id)
jarvis.TriggerTest(test_event_id_lt_100, event1.id)
jarvis.TriggerTest(test_event_id_gt_150, event1.id)

# Navigate to a final context for additional checks
jarvis.Navigate("mapping")
jarvis.Navigate("testing")
jarvis.Debug("FINAL TESTS")

# Update event handled status
event1.handled = True

# Trigger final tests
jarvis.Debug("TRIGGERING FINAL TESTS")
jarvis.TriggerTest(test_event_handled, event1.handled)

# Write out the log to review the test results
jarvis.WriteLog()
