# -*- coding: utf-8 -*-

import re

ARRAY_SYMBOL = '$'
IS_OPTIONAL = '$isOptional'

patten_email = "^(?:[a-z\d]+[_\-\+\.]?)*[a-z\d]+@(?:([a-z\d]+\-?)*[a-z\d]+\.)+([a-z]{2,})+$"
re_email = re.compile(patten_email, re.I)

# Checker function creators
def __create_is_type_func(value_type):
    def checker(v, flg):
        return (isinstance(v, value_type) == flg)

    return checker

def __create_is_type_with_condition_func(value_type, contiditon):
    def checker(v, flg):
        if not isinstance(v, value_type):
            return False
        else:
            return (contiditon(v) == flg)

    return checker

def __create_as_type_func(value_type):
    def checker(v, flg):
        target_type_v = value_type(v)
        return (isinstance(target_type_v, value_type) == flg)

    return checker

def __create_as_type_with_condition_func(value_type, contiditon):
    def checker(v, flg):
        target_type_v = value_type(v)
        return (contiditon(target_type_v) == flg)

    return checker

def __create_not_empty_string_func(value_type):
    def checker(v, flg):
        if (not isinstance(v, value_type)) or (len(v) == 0):
            return False
        else:
            return True

    return checker

# Checkers
def _assert_true(v, func):
    return (func(v) == True)

def _assert_false(v, func):
    return (func(v) == False)

def _min_value(v, opt):
    return (v >= opt)

def _max_value(v, opt):
    return (v <= opt)

def _is_value(v, opt):
    return (type(v) == type(opt) and (v == opt))

def _isnt_value(v, opt):
    return not _is_value(v, opt)

def _as_value(v, opt):
    as_result = False
    args = [v, opt]

    if any([isinstance(x, (int, float)) for x in args]):
        try:
            as_result = (float(v) == float(opt))
        except:
            pass
        else:
            if as_result == True:
                return True

    if any([isinstance(x, (str, unicode)) for x in args]):
        try:
            def convert(v):
                ret = v
                if isinstance(v, str):
                    ret = v.decode('utf8')
                elif isinstance(v, unicode):
                    pass
                else:
                    ret = str(v).decode('utf8')

                return ret

            converted_values = map(convert, [v, opt])
            as_result = converted_values[0] == converted_values[1]

        except:
            pass
        else:
            if as_result == True:
                return True

    return as_result

def _not_as_value(v, opt):
    return not _as_value(v, opt)

def _in(v, opt):
    return (v in opt)

def _not_in(v, opt):
    return not _in(v, opt)

def _min_length(v, opt):
    return (len(value_length) >= opt)

def _max_length(v, opt):
    return (len(value_length) <= opt)

def _is_length(v, opt):
    return (len(value_length) == opt)

def _is_email(v, opt):
    return ((re_email.match(email) != None) == opt)

def _match_reg(v, opt):
    return ((re.match(opt, v) != None) == True)

def _not_match_reg(v, opt):
    return not _match_reg(v, opt)

checkers = {
    '$assertTrue': _assert_true,
    '$assertFalse': _assert_false,

    '$notEmptyString': __create_not_empty_string_func((str, unicode)),
    '$notEmptyStr': __create_not_empty_string_func(str),
    '$notEmptyUnicode': __create_not_empty_string_func(unicode),

    '$isInteger': __create_is_type_func(int),
    '$isPositiveInteger': __create_is_type_with_condition_func(int, lambda x: x > 0),
    '$isNegativeInteger': __create_is_type_with_condition_func(int,  lambda x: x < 0),
    '$isPositiveIntegerOrZero': __create_is_type_with_condition_func(int, lambda x: x >= 0),
    '$isNegativeIntegerOrZero': __create_is_type_with_condition_func(int,  lambda x: x <= 0),

    '$isFloat': __create_is_type_func(float),
    '$isPositiveFloat': __create_is_type_with_condition_func(float, lambda x: x > 0),
    '$isNegativeFloat': __create_is_type_with_condition_func(float,  lambda x: x < 0),
    '$isPositiveFloatOrZero': __create_is_type_with_condition_func(float, lambda x: x >= 0),
    '$isNegativeFloatOrZero': __create_is_type_with_condition_func(float,  lambda x: x <= 0),

    '$isNumber': __create_is_type_func((int, float)),
    '$isPositiveNumber': __create_is_type_with_condition_func((int, float), lambda x: x > 0),
    '$isNegativeNumber': __create_is_type_with_condition_func((int, float),  lambda x: x < 0),
    '$isPositiveNumberOrZero': __create_is_type_with_condition_func((int, float), lambda x: x >= 0),
    '$isNegativeNumberOrZero': __create_is_type_with_condition_func((int, float),  lambda x: x <= 0),

    '$asInteger': __create_as_type_func(int),
    '$asPositiveInteger': __create_as_type_with_condition_func(int, lambda x: x > 0),
    '$asNegativeInteger': __create_as_type_with_condition_func(int,  lambda x: x < 0),
    '$asPositiveIntegerOrZero': __create_as_type_with_condition_func(int, lambda x: x >= 0),
    '$asNegativeIntegerOrZero': __create_as_type_with_condition_func(int,  lambda x: x <= 0),

    '$asFloat': __create_as_type_func(float),
    '$asPositiveFloat': __create_as_type_with_condition_func(float, lambda x: x > 0),
    '$asNegativeFloat': __create_as_type_with_condition_func(float,  lambda x: x < 0),
    '$asPositiveFloatOrZero': __create_as_type_with_condition_func(float, lambda x: x >= 0),
    '$asNegativeFloatOrZero': __create_as_type_with_condition_func(float,  lambda x: x <= 0),

    '$asNumber': __create_as_type_func((int, float)),
    '$asPositiveNumber': __create_as_type_with_condition_func((int, float), lambda x: x > 0),
    '$asNegativeNumber': __create_as_type_with_condition_func((int, float),  lambda x: x < 0),
    '$asPositiveNumberOrZero': __create_as_type_with_condition_func((int, float), lambda x: x >= 0),
    '$asNegativeNumberOrZero': __create_as_type_with_condition_func((int, float),  lambda x: x <= 0),

    '$minValue': _min_value,
    '$maxValue': _max_value,
    '$isValue': _is_value,
    '$asValue': _as_value,
    '$isntValue': _isnt_value,
    '$notAsValue': _not_as_value,

    '$in': _in,
    '$notIn': _not_in,

    '$minLength': _min_length,
    '$maxLength': _max_length,
    '$isLength': _is_length,

    '$isEmail': _is_email,
    '$matchRegExp': _match_reg,
    '$notMatchRegExp': _not_match_reg,
}

def _execute(obj_name, obj, options, ignore_unexpected_keys=False):
    # For unexpected keys
    if not ignore_unexpected_keys:
        for k in obj.keys():
            if (k not in checkers) and (k not in options):
                raise Exception('Found unexpected key `{0}.{1}`'.format(obj_name, k))

    # Check object by options
    for (opt_name, opt_value) in options.items():
        # For Checker
        if opt_name in checkers:
            check_result = None
            try:
                check_result = checkers[opt_name](obj, opt_value)
            except Exception as e:
                print e
                check_result = False
            finally:
                if check_result == False:
                    raise Exception("`{0}`'s value does not match rule {1}:{2}".format(
                            obj_name,
                            opt_name,
                            opt_value))

        # For list symbol
        elif opt_name == ARRAY_SYMBOL:
            for i in range(len(obj)):
                _execute(
                        '{0}[{1}]'.format(obj_name, i),
                        obj[i],
                        opt_value,
                        ignore_unexpected_keys)

        # For sub-object
        else:
            if opt_name in obj:
                _execute(
                        '{0}.{1}'.format(obj_name, opt_name),
                        obj[opt_name],
                        opt_value,
                        ignore_unexpected_keys)

            elif (IS_OPTIONAL in options) and (options[IS_OPTIONAL] == True):
                # skip optional key if not exist
                pass

            else:
                raise Exception('Cannot find `{0}.{1}`'.format(obj_name, opt_name))

def execute(obj, options, ignore_unexpected_keys=False):
    _execute('OBJECT', obj, options, ignore_unexpected_keys)

def is_valid(obj, options, ignore_unexpected_keys=False):
    try:
        _execute('OBJECT', obj, options, ignore_unexpected_keys)
    except Exception as e:
        print e
        return False
    else:
        return True