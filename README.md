# object-checker-py

A tool for checking dict-list-based object.

|     API     |                      Description                      |
|-------------|-------------------------------------------------------|
| `verify()`  | Check the object and throw Exceptions when invalid    |
| `check()`   | Check the object and return check result.             |
| `isValid()` | Check the object and return `true`/`false` for result |

### Quick Example:

```python
from objectchecker import ObjectChecker

obj = {
    "users": [
        {
            "name": "a@a.com",
            "additional": {
                "age"   : 20,
                "height": 180,
                "score" : [80, 90, 100]
            }
        },
        {
            "name": "123@b.com"
        },
        {
            "name": "123@a.com",
            "additional": {
                "age"   : 100,
                "height": 200,
                "score" : [60, 70, 80, 90]
            }
        }
    ]
}

opt = {
    "users": {
        "$maxLength": 5,
        "$": {
            "name": {
                "$isEmail": True,
                "$minLength": 6,
                "$maxLength": 10
            },
            "additional": {
                "$isOptional": True,
                "age": {
                    "$minValue": 20,
                    "$maxValue": 100
                },
                "height": {
                    "$minValue": 100,
                    "$maxValue": 200
                },
                "score": {
                    "$minLength": 3,
                    "$": {
                        "$minValue": 60,
                        "$maxValue": 100
                    }
                }
            }
        }
    }
}

if (not ObjectChecker.is_valid(obj, opt)):
    print 'Error'
```

### Option list

- $type:
  - Assert the type of value.
- $skip:
  - Do not check this field.
- $:
  - Iterate all elements in array.
- $isOptional: true
  - Can be `undefined`. (When `defaultRequired` === true)
- $optional: true
  - Alias to `$isOptional`
- $isRequired: true
  - Can be `undefined`. (When `defaultRequired` === true)
- $required: true
  - Alias to `$isRequired`
- $allowNull: true
  - Can be `null`.
- $assertTrue: `assertFunction`
  - `assertFunction(value)` should return `true`.
- $assertFalse: `assertFunction`
  - `assertFunction(value)` should return `false`.
- $notEmptyString: true
  - Should be `''`.
- $isInteger: ture
  - Should be an integer.
- $isPositiveZeroInteger: Renamed to `$isPositiveIntegerOrZero`
- $isPositiveIntegerOrZero: true
  - Should be an positive integer or `0`.
- $isPositiveInteger: ture
  - Should be an positive integer.
- $isNegativeZeroInteger: Renamed to `$isNegativeIntegerOrZero`
- $isNegativeIntegerOrZero: ture
  - Should be an negative integer or `0`.
- $isNegativeInteger: true
  - Should be an negative integer.
- $minValue: `option`
  - Min value should be `option`.
- $maxValue: `option`
  - Max value should be `option`.
- $isValue: `option`
  - Should be `option`
- $in: [`option1`, `option2`, ...]
  - Value should be in the array.
- $notIn: [`option1`, `option2`, ...]
  - Value should not be in the array.
- $minLength
  - Min length of value should be `option`.
- $maxLength
  - Max length of value should be `option`.
- $isLength: `option`
  - Length of value should be `option`.
- $isEmail: true
  - Should be email.
- $matchRegExp: `RegExp`.
  - Should match `RegExp`.
- $notMatchRegExp: `RegExp`.
  - Should not match `RegExp`.

### Test:

```shell
python test/test.py
```

### License

[MIT](LICENSE)
