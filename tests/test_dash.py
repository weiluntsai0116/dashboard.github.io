"""
test_dash.py
To test if the dash file runs without error.
"""

from dash.testing.application_runners import import_app
import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)


def test_bsly001_falsy_child(dash_duo, params):
    # get app name and define  app inside the test function
    print("test : ", params['app_name'])
    app_name = params['app_name']
    sys.path.insert(0, parentdir)
    app = import_app(app_name)

    # 4. host the app locally in a thread, all dash server configs could be
    # passed after the first app argument
    dash_duo.start_server(app)

    # 5. use wait_for_* if your target element is the result of a callback,
    # keep in mind even the initial rendering can trigger callbacks
    # dash_duo.wait_for_text_to_equal("#nully-wrapper", "0", timeout=4)

    # 6. use this form if its present is expected at the action point
    # assert dash_duo.find_element("#example1").text == "Hello dash"

    # 7. to make the checkpoint more readable, you can describe the
    # acceptance criterion as an assert message after the comma.
    assert dash_duo.get_logs() == [], "browser console should contain no error"

    # 8. visual testing with percy snapshot
    dash_duo.percy_snapshot("bsly001-layout")


def test_holder():
    assert 1 == 1

