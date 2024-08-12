## 
# @file Contains a test for all functionalities
from tests.test_helpers import *

# Create an event instance with an ID of 230 and mark it as not handled.
event1 = Event(230, False)

# Log a debug message indicating the start of initialization.
mc.Debug("GOING TO INITIALIZATION")

# Navigate to the "INIT" context.
mc.Navigate("INIT")

# Log a debug message within the "INIT" context.
mc.Debug("Initializing ...")

# Create a new event instance with an ID of 125 and mark it as not handled.
event1 = Event(125, False)

# Log a debug message indicating the start of adding and triggering handling tests.
mc.Debug("ADDING AND TRIGGERING HANDLING TESTS")

# Add a test to check if an event is handled. The test will return True if the event is handled.
test_handled = mc.AddTest(
    test_fn=lambda x: x,
    name="Event handled"
)

# Trigger the "Event handled" test with the `handled` status of `event1` (which is False).
mc.TriggerTest(test_handled, event1.handled)

# Navigate back to the parent context.
mc.Navigate("parent")

# Navigate to the "Processor" context.
mc.Navigate("Processor")

# Log a debug message indicating the start of adding ID tests.
mc.Debug("ADDING ID_TESTS")

# Add a test to check if the event ID is greater than 100.
ID_SUP_100 = mc.AddTest(
    test_fn=is_more_100["test_fn"],
    name="Event id >100"
)

# Add a test to check if the event ID is greater than 150.
ID_SUP_150 = mc.AddTest(
    test_fn=is_more_150["test_fn"],
    name="Event id >150"
)

# Log a debug message indicating the start of triggering ID tests.
mc.Debug("TRIGGERING ID_TESTS")

# Trigger the "Event id >100" test with the ID of `event1`.
mc.TriggerTest(ID_SUP_100, event1.id)

# Trigger the "Event id >150" test with the ID of `event1`.
mc.TriggerTest(ID_SUP_150, event1.id)

# Navigate back to the parent context.
mc.Navigate("Parent")

# Log a debug message indicating navigation to the "Processor" context.
mc.Debug("NAVIGATING TO PROCESSOR")

# Log a warning message indicating that the event has changed.
mc.Warning("event changed !!")

# Create a new event instance with an ID of 1110 and mark it as not handled.
event1 = Event(1110, False)

# Navigate back to the parent context.
mc.Navigate("parent")

# Log a debug message indicating the re-triggering of ID tests.
mc.Debug("TRIGGERING ID_TESTS again")

# Re-trigger the "Event id >100" test with the new ID of `event1`.
mc.TriggerTest(ID_SUP_100, event1.id)

# Re-trigger the "Event id >150" test with the new ID of `event1`.
mc.TriggerTest(ID_SUP_150, event1.id)

# Navigate to the "mapping" context.
mc.Navigate("mapping")

# Navigate to the "testing" context.
mc.Navigate("testing")

# Mark the event as handled.
event1.handled = True

# Navigate back to the parent context twice to return to the root context.
mc.Navigate("parent")
mc.Navigate("parent")

# Re-trigger the "Event handled" test with the updated `handled` status of `event1` (which is now True).
mc.TriggerTest(test_handled, event1.handled)

# Write the log, printing all logged messages.
mc.WriteLog()

