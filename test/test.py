# -*- coding: utf-8 -*-

import unittest

from objectchecker import ObjectChecker

# Config
options = {
    'messageTemplate': {
        'invalid'   : "Value of Field `{{fieldName}}` is not valid. Got `{{fieldValue}}`, but require {{checkerName}} = {{checkerOption}}",
        'missing'   : "Missing {{fieldName}}",
        'unexpected': "Not support {{fieldName}}"
    }
}

checker = ObjectChecker()

# Complicated objects
complicated_valid_obj = {
    "users": [
        {
            "id"  : 1,
            "name": "a@a.com",
            "additional": {
                "age"   : 20,
                "height": 180,
                "score" : [80, 90, 100]
            }
        },
        {
            "id"  : 2,
            "name": "123@b.com"
        },
        {
            "id"  : 3,
            "name": "123@a.com",
            "additional": {
                "age"   : 100,
                "height": 200,
                "score" : [60, 70, 80, 90]
            }
        }
    ]
}

complicated_invalid_obj = {
    "users": [
        {
            "id"  : "a1",
            "name": "a@a.com",
            "additional": {
                "age"   : 20,
                "height": 180,
                "score" : [80, 90, 100]
            }
        },
        {
            "id"  : 2,
            "name": "123@b.com"
        },
        {
            "id"  : 3,
            "name": "123@a.com",
            "additional": {
                "age"   : 500,
                "height": 300,
                "score" : [30]
            }
        }
    ]
}

complicated_options = {
    "users": {
        "$maxLength": 5,
        "$": {
            "id": {
                "$matchRegExp": "^\\d$"
            },
            "name": {
                "$isEmail"  : True,
                "$minLength": 6,
                "$maxLength": 10
            },
            "additional": {
                "$isOptional": True,
                "$type": "json",
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
                    "$type"     : "array",
                    "$": {
                        "$minValue": 60,
                        "$maxValue": 100
                    }
                }
            }
        }
    }
}

# Simple objects
obj = None
opt = {
    "username": {
        "$minLength": 6,
        "$maxLength": 10
    },
    "age": {
        "$minValue": 1,
        "$maxValue": 100
    },
    "email": {
        "$isEmail"   : True,
        "$isOptional": True
    },
    "score1": {
        "$isInteger": True
    },
    "score2": {
        "$isPositiveZeroInteger": True
    },
    "score3": {
        "$isPositiveInteger": True
    },
    "score4": {
        "$isNegativeZeroInteger": True
    },
    "score5": {
        "$isNegativeInteger": True
    },
    "fix1": {
        "$isValue": 12345
    },
    "fix2": {
        "$isLength": 5
    },
    "range1": {
        "$in": [1, 2, 3]
    },
    "range2": {
        "$notIn": [1, 2, 3]
    }
}

class TestObjectChecker(unittest.TestCase):
    def test_complicated_object_valid_object(self):
        self.assertEqual(True, checker.is_valid(complicated_valid_obj, complicated_options))

    def test_complicated_object_invalid_object(self):
        self.assertEqual(False, checker.is_valid(complicated_invalid_obj, complicated_options))

    # Valid objects
    def test_valid_object_1(self):
        obj = {
          'username': 'abcdef',
          'age'     : 1,
          'email'   : 'a@e.com',
          'score1'  : 1,
          'score2'  : 0,
          'score3'  : 1,
          'score4'  : 0,
          'score5'  : -1,
          'fix1'    : 12345,
          'fix2'    : '11111',
          'range1'  : 1,
          'range2'  : 0
        };
        self.assertEqual(True,  checker.is_valid(obj, opt))

    def test_valid_object_2(self):
        obj = {
          'username': 'abcdef1234',
          'age'     : 100,
          'score1'  : 100,
          'score2'  : 1,
          'score3'  : 1,
          'score4'  : -1,
          'score5'  : -1,
          'fix1'    : 12345,
          'fix2'    : '12345',
          'range1'  : 2,
          'range2'  : 4
        };
        self.assertEqual(True,  checker.is_valid(obj, opt))

    # Invalid objects
    def test_invalid_object_1(self):
        opt = {
          'foo': {
            '$minLength': 3
          }
        };
        obj = {
          'foo': 'ab'
        };
        self.assertEqual(False,  checker.is_valid(obj, opt))

    def test_invalid_object_2(self):
        opt = {
          'foo': {
            '$maxLength': 3
          }
        };
        obj = {
          'foo': 'abcd'
        };
        self.assertEqual(False,  checker.is_valid(obj, opt))

    def test_invalid_object_3(self):
        opt = {
          'foo': {
            '$minValue': 3
          }
        };
        obj = {
          'foo': 2
        };
        self.assertEqual(False,  checker.is_valid(obj, opt))

    def test_invalid_object_4(self):
        opt = {
          'foo': {
            '$maxValue': 3
          }
        };
        obj = {
          'foo': 4
        };
        self.assertEqual(False,  checker.is_valid(obj, opt))

    def test_invalid_object_5(self):
        opt = {
          'foo': {
            '$isEmail': True
          }
        };
        obj = {
          'foo': 'a@@.com'
        };
        self.assertEqual(False,  checker.is_valid(obj, opt))

    def test_invalid_object_6(self):
        opt = {
          'foo': {
            '$in': [1,2]
          }
        };
        obj = {
          'foo': 0
        };
        self.assertEqual(False,  checker.is_valid(obj, opt))

    def test_invalid_object_7(self):
        opt = {
          'foo': {
            '$notIn': [1, 2]
          }
        };
        obj = {
          'foo': 1
        };
        self.assertEqual(False,  checker.is_valid(obj, opt))

    def test_invalid_object_8(self):
        opt = {
          'foo': {
            '$isValue': 9
          }
        };
        obj = {
          'foo': 8
        };
        self.assertEqual(False,  checker.is_valid(obj, opt))

    def test_invalid_object_9(self):
        opt = {
          'foo': {
            '$isInteger': True
          }
        };
        obj = {
          'foo': 'a'
        };
        self.assertEqual(False,  checker.is_valid(obj, opt))

    def test_invalid_object_10(self):
        vopt = {
          'foo': {
            '$isPositiveZeroInteger': True
          }
        };
        obj = {
          'foo': -1
        };
        self.assertEqual(False,  checker.is_valid(obj, opt))

    def test_invalid_object_11(self):
        opt = {
          'foo': {
            '$isPositiveInteger': True
          }
        };
        obj = {
          'foo': 0
        };
        self.assertEqual(False,  checker.is_valid(obj, opt))

    def test_invalid_object_12(self):
        opt = {
          'foo': {
            '$isNegativeZeroInteger': True
          }
        };
        obj = {
          'foo': 1
        };
        self.assertEqual(False,  checker.is_valid(obj, opt))

    def test_invalid_object_13(self):
        opt = {
          'foo': {
            '$isNegativeInteger': True
          }
        };
        obj = {
          'foo': 0
        };
        self.assertEqual(False,  checker.is_valid(obj, opt))

    def test_invalid_object_14(self):
        opt = {
          'foo': {
            '$notEmptyString': True
          }
        };
        obj = {
          'foo': ''
        };
        self.assertEqual(False,  checker.is_valid(obj, opt))

    def test_invalid_object_15(self):
        opt = {
          'foo': {
            '$assertTrue': lambda v: v == 'assertTrue'
          }
        };
        obj = {
          'foo': 'xxx'
        };
        self.assertEqual(False,  checker.is_valid(obj, opt))

    def test_invalid_object_16(self):
        opt = {
          'foo': {
            '$assertFalse': lambda v: v == 'xxx'
          }
        };
        obj = {
          'foo': 'xxx'
        };
        self.assertEqual(False,  checker.is_valid(obj, opt))

    def test_invalid_object_17(self):
        opt = {
          'foo': {
            '$matchRegExp': '^[12]$'
          }
        };
        obj = {
          'foo': '3'
        };
        self.assertEqual(False,  checker.is_valid(obj, opt))

    def test_invalid_object_18(self):
        opt = {
          'foo': {
            '$notMatchRegExp': '^[12]$'
          }
        };
        obj = {
          'foo': '1'
        };
        self.assertEqual(False,  checker.is_valid(obj, opt))

    def test_invalid_object_19(self):
        opt = {
          'foo': {
            '$isInteger': True
          }
        };
        obj = {
          'bar': 2
        };
        self.assertEqual(False,  checker.is_valid(obj, opt))

    def test_null_field_1(self):
        opt = {
          'foo': {
            '$allowNull': True,
            '$isInteger': True
          }
        };
        obj = {
          'foo': 2
        };
        self.assertEqual(True,  checker.is_valid(obj, opt))

    def test_null_field_2(self):
        opt = {
          'foo': {
            '$allowNull': True,
            '$isInteger': True
          }
        };
        obj = {
          'foo': None
        };
        self.assertEqual(True,  checker.is_valid(obj, opt))

    def test_null_field_3(self):
        opt = {
          'foo': {
            '$allowNull': True,
            '$isInteger': True
          }
        };
        obj = {
          'foo': 'abc'
        };
        self.assertEqual(False,  checker.is_valid(obj, opt))

    def test_skip_option(self):
        opt = {
          'foo': {
            '$skip': True
          }
        };
        obj = {
          'foo': {
            'bar': [1, 2, 3, 4, 5]
          }
        };
        self.assertEqual(True,  checker.is_valid(obj, opt))

    def test_regext_in_string_1(self):
        opt = {
          'foo': {
            '$matchRegExp': 'A[A-Z][0-9]'
          }
        };
        obj = {
          'foo': 'AB3'
        };
        self.assertEqual(True,  checker.is_valid(obj, opt))

    def test_regext_in_string_2(self):
        opt = {
          'foo': {
            '$matchRegExp': 'A[A-Z][0-9]'
          }
        };
        obj = {
          'foo': '123'
        };
        self.assertEqual(False,  checker.is_valid(obj, opt))

    def test_type_string_1(self):
        opt = {
          'foo': {
            '$type': 'string'
          }
        };
        obj = {
          'foo': 123
        };
        self.assertEqual(False,  checker.is_valid(obj, opt))

    def test_type_string_2(self):
        opt = {
          'foo': {
            '$type': 'string'
          }
        };
        obj = {
          'foo': '123'
        };
        self.assertEqual(True,  checker.is_valid(obj, opt))

    def test_type_number_1(self):
        opt = {
          'foo': {
            '$type': 'number'
          }
        };
        obj = {
          'foo': 123
        };
        self.assertEqual(True,  checker.is_valid(obj, opt))

    def test_type_number_2(self):
        opt = {
          'foo': {
            '$type': 'number'
          }
        };
        obj = {
          'foo': '123'
        };
        self.assertEqual(False,  checker.is_valid(obj, opt))

    def test_type_int_1(self):
        opt = {
          'foo': {
            '$type': 'int'
          }
        };
        obj = {
          'foo': 123
        };
        self.assertEqual(True,  checker.is_valid(obj, opt))

    def test_type_int_2(self):
        opt = {
          'foo': {
            '$type': 'int'
          }
        };
        obj = {
          'foo': '123'
        };
        self.assertEqual(False,  checker.is_valid(obj, opt))

    def test_type_array_1(self):
        opt = {
          'foo': {
            '$type': 'array',
            '$': {
              '$type': 'int',
            }
          }
        };
        obj = {
          'foo': [1, 2, 3]
        };
        self.assertEqual(True,  checker.is_valid(obj, opt))

    def test_type_array_2(self):
        opt = {
          'foo': {
            '$type': 'array',
            '$': {
              '$type': 'int',
            }
          }
        };
        obj = {
          'foo': '123'
        };
        self.assertEqual(False,  checker.is_valid(obj, opt))

    def test_default_required_is_false_1(self):
        _checker = ObjectChecker(False);

        opt = {
          'foo': {
            '$required': True,
            '$minValue': 0,
          }
        };
        obj = {
          'foo': 123
        };
        self.assertEqual(True, _checker.is_valid(obj, opt))

    def test_default_required_is_false_2(self):
        _checker = ObjectChecker(False);

        opt = {
          'foo': {
            '$isRequired': True,
            '$minValue'  : 0,
          }
        };
        obj = {
          'foo': 123
        };
        self.assertEqual(True, _checker.is_valid(obj, opt))

    def test_default_required_is_false_3(self):
        _checker = ObjectChecker(False);

        opt = {
          'foo': {
            '$minValue': 0,
          }
        };
        obj = {
        };
        self.assertEqual(True, _checker.is_valid(obj, opt))

    def test_default_required_is_false_4(self):
        _checker = ObjectChecker(False);

        opt = {
          'foo': {
            '$minValue': 0,
          }
        };
        obj = {
          'foo': 0
        };
        self.assertEqual(True, _checker.is_valid(obj, opt))

    def test_default_required_is_false_5(self):
        _checker = ObjectChecker(False);

        opt = {
          'foo': {
            '$minValue': 0,
          }
        };
        obj = {
          'foo': -1
        };
        self.assertEqual(False, _checker.is_valid(obj, opt))

    def test_type_any(self):
        _checker = ObjectChecker(False);

        opt = {
          'foo': {
            '$type'      : 'any',
            '$isRequired': True
          }
        };
        obj = {
          'foo': -1
        };
        self.assertEqual(True, _checker.is_valid(obj, opt))

    def test_type_any_or_not_existed(self):
        _checker = ObjectChecker(False);

        opt = {
          'foo': {
            '$type'      : 'any',
            '$isRequired': True
          }
        };
        obj = {
        };
        self.assertEqual(False, _checker.is_valid(obj, opt))

if __name__ == '__main__':
    unittest.main()