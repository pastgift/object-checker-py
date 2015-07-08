# -*- coding: utf-8 -*-

import objectchecker

obj = {
    'name': 'Tomaa',
    'age': 1,
    'scores': [
        {
            'name': 'math',
            'score': 90,
        }
    ],
    'gender': 'M',
}
opt = {
    'name': {
        '$minLength': 5,
    },
    'age': {
        '$isInteger': True,
    },
    'scores': {
        '$minLength': 1,
        '$': {
            'name': {
                '$minLength': 5,
            },
            'score': {
                '$isInteger': True,
            },
        },
    },
}
print objectchecker.is_valid(obj, opt)
objectchecker.execute(obj, opt)