from objectchecker import ObjectChecker

checker = ObjectChecker()

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


print checker.check(obj, opt)
