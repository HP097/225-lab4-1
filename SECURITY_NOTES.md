Security & Testing Research:

Bandit: I am using Bandit to perform static security analysis. It scans the Python source code for common vulnerabilities like insecure function calls and hardcoded configurations.

Pytest: I am using Pytest to automate unit testing. This will make sure that the core logic of the application is verified before deployment.

Input Sanitization: I have modified the Flask application to use `.strip()` on all form inputs. This will prevent trailing whitespace errors and provide a basic layer of data cleaning before database insertion.
