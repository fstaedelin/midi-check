Python Logger Utility

A flexible and customizable logging utility for Python applications. This logger allows you to log messages at different levels, navigate contexts, manage tests, and format log messages with different styles.
Features

    Contextual Logging: Navigate between different contexts and manage hierarchical logging.
    Customizable Levels: Support for various log levels like DEBUG, WARNING, ERROR, and SUCCESS.
    Message Formatting: Different formatting styles for log messages based on their levels.
    Testing Framework: Add and trigger tests with automatic callbacks for success and failure scenarios.
    Log Management: Store and manage log messages and test results.

Installation

To use the Logger utility, you need Python 3.6 or later. You can include this project as a dependency in your own Python projects. If you have a Git repository, you can clone it and use it directly.
Clone the Repository

bash

git clone https://gitlab.com/your-username/your-repository.git

Install Dependencies

Navigate to the project directory and install any required dependencies (if specified in a requirements.txt file).

bash

cd your-repository
pip install -r requirements.txt

Usage

Here’s a brief guide on how to use the Logger utility:
Basic Example

python

from your_module import Logger

# Create a Logger instance
logger = Logger(level="DEBUG")

# Log messages at different levels
logger.Debug("This is a debug message")
logger.Warning("This is a warning message")
logger.Error("This is an error message")

# Navigate to a new context and log messages
logger.Navigate("my_context")
logger.Log("This is a message in my_context", level="INFO")

# Add and trigger tests
def sample_test_fn(val):
    return val > 0

test = logger.AddTest(test_fn=sample_test_fn, result_key=True, name="positive_test")
logger.TriggerTest(test, 10)  # Test should pass

# Print all log messages
logger.WriteLog()

Advanced Usage
Navigating Contexts

You can navigate through different contexts using the Navigate method. This helps in managing logs and tests within specific contexts.

python

logger.Navigate("context1")
logger.Log("Message in context1", level="INFO")
logger.Navigate("parent")  # Return to the previous context

Adding Tests

Add tests to your logger with automatic naming and callback functions for success and failure scenarios.

python

def success_callback():
    return "Test passed!"

def failure_callback():
    return "Test failed!"

test = logger.AddTest(
    test_fn=lambda x: x == 10,
    callback_true=success_callback,
    callback_false=failure_callback,
    name="equality_test"
)

Project Structure

    logger.py: Contains the Logger class and its related methods.
    utils.py: Contains utility classes and functions used by the Logger.
    tests/: Directory containing unit tests for the Logger.
    requirements.txt: File listing the dependencies required for the project.

Contributing

We welcome contributions to the project. If you want to contribute:

    Fork the repository.
    Create a feature branch (git checkout -b feature-branch).
    Commit your changes (git commit -am 'Add new feature').
    Push to the branch (git push origin feature-branch).
    Create a new Pull Request on GitLab.

Please make sure to update tests and documentation as appropriate.
License

This project is licensed under the MIT License - see the LICENSE file for details.
Contact

For any questions or issues, please contact your-email@example.com.