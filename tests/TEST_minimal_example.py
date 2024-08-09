from tests.test_helpers import *

event1 = Event(230, False)

jarvis.Debug("GOING TO INITIALIZATION")
jarvis.Navigate("INIT")
jarvis.Debug("Initializing ...")
#logger._print_contexts()
event1 = Event(125, False)
jarvis.Debug("ADDING AND TRIGGERING HANDLING TESTS")
test_handled = jarvis.AddTest(
    test_fn=lambda x: x,
    name = "Event handled"
)

jarvis.TriggerTest(test_handled, event1.handled)

jarvis.Navigate("parent")

jarvis.Navigate("Processor")
jarvis.Debug("ADDING ID_TESTS")
## Need to initiate and TriggerTest tests in same context for now

ID_SUP_100 = jarvis.AddTest(
    test_fn=is_more_100["test_fn"],
    name = "Event id >100"
)
ID_SUP_150 = jarvis.AddTest(
    test_fn=is_more_150["test_fn"],
    name = "Event id >150"    
)

jarvis.Debug("TRIGGERING ID_TESTS")
jarvis.TriggerTest(ID_SUP_100, event1.id)
jarvis.TriggerTest(ID_SUP_150, event1.id)


jarvis.Navigate("Parent")

jarvis.Debug("NAVIGATING TO PROCESSOR")

jarvis.Warning("event changed !!")

event1 = Event(1110, False)


jarvis.Navigate("parent")

### Debug
jarvis.Debug("TRIGGERING ID_TESTS again")
jarvis.TriggerTest(ID_SUP_100, event1.id)
jarvis.TriggerTest(ID_SUP_150, event1.id)


jarvis.Navigate("mapping")
jarvis.Navigate("testing")
event1.handled = True

jarvis.Navigate("parent")
jarvis.Navigate("parent")

jarvis.TriggerTest(test_handled, event1.handled)



jarvis.WriteLog()