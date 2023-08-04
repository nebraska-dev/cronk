import sys
from json import dumps, load

import atheris
from hypothesis import given
from hypothesis import strategies as st

from cronk.cron_to_json import cron_to_json
from cronk.json_to_cron import json_to_cron

JSON_ATOMS = st.one_of(
    st.none(),
    st.booleans(),
    st.integers(min_value=-(2**63), max_value=2**63 - 1),
    st.floats(allow_nan=False, allow_infinity=False),
    st.text(),
)
JSON_OBJECTS = st.recursive(
    base=JSON_ATOMS,
    extend=lambda inner: st.lists(inner) | st.dictionaries(st.text(), inner),
)


@atheris.instrument_func
@given(json=JSON_OBJECTS)
def test_json_to_cron_to_json_roundtrip(json: dict) -> None:
    print(json)
    txt = json
    if json is not None:
        txt = dumps(json, default=lambda o: o.__dict__, indent=4)

    try:
        cron_text = "\n".join(json_to_cron(text=txt))
        output = cron_to_json(text=cron_text)
    except TypeError as err:
        assert str(err) == "Must be str type"
        return
    except ValueError as err:
        assert "schema.json" in str(err)
        return

    assert json == output.__dict__


if __name__ == "__main__":
    # Running this function will replay, deduplicate, and minimize any failures
    # discovered by earlier runs, or briefly search for new failures if none are known.
    atheris.Setup(
        sys.argv,
        atheris.instrument_func(
            test_json_to_cron_to_json_roundtrip.hypothesis.fuzz_one_input
        ),
    )
    atheris.Fuzz()
