---
name: test-generation
description: Generate comprehensive test suites for existing code. Use when asked to write tests, add test coverage, create unit tests, or build integration tests.
license: MIT
compatibility: Requires pytest (Python) or vitest/jest (Node.js)
---

## Process

1. **Read the source code.** Load every function and class under test. Do not write tests from a summary or description — you must see the implementation.

2. **Identify the test framework.** Check for:
   - `conftest.py` or `pytest.ini` → pytest
   - `vitest.config.*` → Vitest
   - `jest.config.*` → Jest
   If none are found, default to pytest for Python, Vitest for TypeScript/JavaScript.

3. **Categorize test types needed:**
   - **Happy path:** Normal inputs, expected outputs
   - **Edge cases:** Empty inputs, None/null, boundary values, maximum lengths
   - **Error cases:** Invalid inputs that should raise exceptions or return errors
   - **Integration:** Tests that verify multiple components work together

4. **Write tests following the AAA pattern:**
   ```python
   def test_descriptive_name():
       # Arrange — set up inputs and expected state
       user = create_test_user(name="Alice")
       
       # Act — call the function under test
       result = get_user_greeting(user)
       
       # Assert — verify the output
       assert result == "Hello, Alice!"
   ```

5. **Name tests descriptively.** The test name should describe the scenario and expected outcome:
   - ✅ `test_login_rejects_empty_password`
   - ❌ `test_login_2`

6. **Run the tests.** Execute the full test suite and confirm all tests pass. If any fail, fix the test (not the source code) unless you discover an actual bug.

## Rationalizations

| Excuse | Rebuttal |
|--------|----------|
| "I'll just write happy path tests" | Edge cases are where bugs live. Write at least one edge case per function. |
| "The function is too simple to test" | Simple functions get refactored. Tests protect against regressions during refactoring. |
| "I'll add tests later" | You won't. Write them now. |
| "Mocking everything is fine" | Over-mocking hides integration bugs. Mock external services, not your own code. |

## Verification

- [ ] Tests were executed (not just written)
- [ ] All tests pass
- [ ] At least one edge case test exists per function
- [ ] Test names describe the scenario, not just "test_1", "test_2"
