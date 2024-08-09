from test_helpers import *

event1 = Event(230, False)

logger.Debug("GOING TO INITIALIZATION")
logger.Navigate("INIT")
logger.Debug("Initializing ...")
#logger._print_contexts()
event1 = Event(125, False)
logger.Debug("ADDING AND TRIGGERING HANDLING TESTS")
test_handled = logger.AddTest(
    test_fn=lambda x: x,
    name = "Event handled"
)

logger.TriggerTest(test_handled, event1.handled)

logger.Navigate("parent")

logger.Navigate("Processor")
logger.Debug("ADDING ID_TESTS")
## Need to initiate and TriggerTest tests in same context for now

ID_SUP_100 = logger.AddTest(
    test_fn=is_more_100["test_fn"],
    name = "Event id >100"
)
ID_SUP_150 = logger.AddTest(
    test_fn=is_more_150["test_fn"],
    name = "Event id >150"    
)

logger.Debug("TRIGGERING ID_TESTS")
logger.TriggerTest(ID_SUP_100, event1.id)
logger.TriggerTest(ID_SUP_150, event1.id)


logger.Navigate("Parent")

logger.Debug("NAVIGATING TO PROCESSOR")

logger.Warning("event changed !!")

event1 = Event(1110, False)


logger.Navigate("parent")

### Debug
logger.Debug("TRIGGERING ID_TESTS again")
logger.TriggerTest(ID_SUP_100, event1.id)
logger.TriggerTest(ID_SUP_150, event1.id)


logger.Navigate("mapping")
logger.Navigate("testing")
event1.handled = True

logger.Navigate("parent")
logger.Navigate("parent")

logger.TriggerTest(test_handled, event1.handled)



logger.WriteLog()