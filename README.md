# Logger Library

## Overview

This repository contains a Python-based logging library designed to manage complex hierarchical logging and testing within a software application. The library provides utility functions to manage contexts, create automated logs, and handle test cases with customizable callback messages.

## Features

- **Context Management**: Navigate through different logging contexts and maintain a structured log hierarchy.
- **Automated Test Logging**: Add tests with expected results and automatically log success or failure messages.
- **Customizable Log Levels**: Support for multiple log levels such as DEBUG, INFO, WARNING, ERROR, SUCCESS, and FAIL.
- **Callback Functions**: Define custom callback messages for test success or failure.

## Installation

Clone this repository to your local machine using:

```bash
git clone <your-git-url>

## Usage

### Logger Class

The Logger class provides the core functionality to create and manage logs.

Initialization

python

logger = Logger(level="WARNING")

Logging Messages

python

logger.Debug("This is a debug message.")
logger.Warning("This is a warning message.")
logger.Error("This is an error message.")

Context Navigation

python

logger.Navigate("new_context")

Writing Logs

python

logger.WriteLog()

Adding and Triggering Tests

Adding Tests

python

logger.AddTest(
    test_fn=lambda: True,
    result_key=True,
    callback_true="Test passed!",
    callback_false="Test failed!",
    name="test_name"
)

Triggering Tests

python

test = logger.TriggerTest(test, val)

LoggerUtilitiesMixin Class

The LoggerUtilitiesMixin class provides utility functions that are inherited by the Logger class. These include functions for context management, automatic naming of tests and contexts, and triggering test messages.

LoggerPrintingMixin Class

The LoggerPrintingMixin class provides utility functions specifically for printing and formatting log messages. These include functions for indenting messages, printing contexts, and managing print levels.

Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss your ideas.

License

This project is licensed under the MIT License. See the LICENSE file for more details.