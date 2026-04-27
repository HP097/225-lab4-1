import pytest

def test_basic_logic():
    # Verifies that the math works, proves the test runner is alive
    assert 1 + 1 == 2

def test_db_path():
    # Verifies that our app is still looking for the persistent NFS path
    from main import DATABASE
    assert '/nfs/' in DATABASE
