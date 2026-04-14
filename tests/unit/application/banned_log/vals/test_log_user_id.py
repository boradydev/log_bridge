import pytest
from hypothesis import given, settings, strategies as st

from src.application.banned_log import excs
from src.application.banned_log.vals import UserIDLog


@pytest.mark.parametrize(
    "valid",
    [
        "test21356235-test22",
        "testtest",
        "---test---",
    ],
)
async def test_base_positive(valid: str) -> None:
    instance = UserIDLog(valid)
    assert str(instance) == valid


valid_identity_st = st.from_regex(r"^[a-z0-9-]{5,50}$", fullmatch=True)

invalid_identity_st = st.one_of(
    st.text(min_size=1, max_size=4),
    st.text(min_size=51),
    st.text().filter(lambda x: any(c in x for c in " @/!")),
)


@settings(max_examples=100)
@given(valid_identity_st)
async def test_positive(valid: str) -> None:
    instance = UserIDLog(valid)
    assert str(instance) == valid


@settings(max_examples=100)
@given(invalid_identity_st)
async def test_negative(invalid: str) -> None:
    with pytest.raises(excs.InvalidLogUserIDException):
        UserIDLog(invalid)
