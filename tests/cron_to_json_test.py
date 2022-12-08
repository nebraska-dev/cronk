from cronk.cron_to_json import Json, Routine, cron_to_json


def test_cron_to_json_handles_happy_path():
    with open("tests/cron_to_json_test_happy.cron") as fp:
        text = fp.read()

    assert cron_to_json(text) == Json(
        intro=["# Intro comment"],
        routines=[
            Routine(
                comments=["# First action comment"],
                command="0 * * * * echo 'hello world'",
            ),
            Routine(
                comments=["# Second action", "# comment"],
                command="1 * * * * echo 'farewell'",
            ),
        ],
        outro=["# Outro"],
    )


# TODO: Test sad path
