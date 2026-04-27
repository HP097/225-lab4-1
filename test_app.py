import pytest
import os

def test_logic():
    # Simple logic test to make sure the test runner is working
    assert 1 + 1 == 2

def test_database_config():
    # Verifies that the application is using the correct persistent storage path
    from main import DATABASE
    assert '/nfs/' in DATABASE
