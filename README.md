## Testing

Easiest way is to run the tests in the test directory. All test so far have mocked the 
API responses.

You can add new TEST_RECORD_SETs in the test file to try out different test cases.
Each entry in the record set represents one response from an API. If you want to add 
APIs just add them to the API_LIST in the config file.

## Modules

- models.py contains all dataclasses
- config.py contains the API definitions
- coalesce/main.py contains all functions
