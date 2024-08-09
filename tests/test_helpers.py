from JARVIS.jarvis import JARVIS
global logger
jarvis = JARVIS("INFO")

class Event:
    def __init__(self, event_id, handled):
        self.id = event_id
        self.handled = False

is_more_100 = jarvis.AddTest(
    test_fn=lambda x: True if x > 100 else False,
    name = ">100")

#logger._print_contexts()
is_more_150 = jarvis.AddTest(
    test_fn=lambda x: True if x > 150 else False,
    name = ">150"
)