from params.validate import validate_with
import unittest

class TestCase(unittest.TestCase):
    def test_all(self):
        with self.assertRaisesRegex(Exception, 'validate_with is called without spec in arguments'):
            validate_with(
                params = []
            )

        with self.assertRaisesRegex(Exception, 'validate_with is called without params in arguments'):
            validate_with(
                spec = []
            )

        with self.assertRaisesRegex(Exception, 'validate_with arguments has invalid keys: .unknown.'):
            validate_with(
                unknown = []
            )

        with self.assertRaisesRegex(Exception, 'validate_with allow_extra argument needs to be boolean'):
            validate_with(
                params = [],
                spec = [],
                allow_extra = 1,
            )

        with self.assertRaisesRegex(Exception, 'params need to be a dictionary but got: list'):
            validate_with(
                params = [],
                spec = [],
            )

        with self.assertRaisesRegex(Exception, 'spec need to be a dictionary but got: int'):
            validate_with(
                params = {},
                spec = 1,
            )

        with self.assertRaisesRegex(Exception, 'Empty specification provided'):
            validate_with(
                params = {},
                spec = {},
            )

        with self.assertRaisesRegex(Exception, 'spec for .first. is not a dictionary'):
            validate_with(
                params = {},
                spec = {
                    'first': []
                },
            )

        with self.assertRaisesRegex(Exception, 'Invalid spec keys found for .first.: .unknown.'):
            validate_with(
                params = {},
                spec = {
                    'first': {
                        'unknown': []
                    }
                },
            )

        with self.assertRaisesRegex(Exception, 'spec type .type. is not one of .int, float, bool, str, list, dict. for .first.'):
            validate_with(
                params = {},
                spec = {
                    'first': {
                        'type': 1
                    }
                },
            )

        with self.assertRaisesRegex(Exception, 'spec type .optional. is not a boolean for spec .first.'):
            validate_with(
                params = {},
                spec = {
                    'first': {
                        'optional': []
                    }
                },
            )

        with self.assertRaisesRegex(Exception, 'value of .default. for spec .first. is not of required type'):
            validate_with(
                params = {},
                spec = {
                    'first': {
                        'type': int,
                        'default': []
                    }
                },
            )

        with self.assertRaisesRegex(Exception, '.default. spec provided for non optional argument .first.'):
            validate_with(
                params = {},
                spec = {
                    'first': {
                        'optional': False,
                        'default': []
                    }
                },
            )

        with self.assertRaisesRegex(Exception, 'spec type .callbacks. is not of type dictionary for .first.'):
            validate_with(
                params = {},
                spec = {
                    'first': {
                        'callbacks': []
                    }
                },
            )

        with self.assertRaisesRegex(Exception, 'spec type .callbacks. is empty dictionary for .first.'):
            validate_with(
                params = {},
                spec = {
                    'first': {
                        'callbacks': {}
                    }
                },
            )

        with self.assertRaisesRegex(Exception, 'callback .check callback. is not callable for spec .first.'):
            validate_with(
                params = {},
                spec = {
                    'first': {
                        'callbacks': {
                            'check callback': 'foo'
                        }
                    }
                },
            )

        with self.assertRaisesRegex(Exception, 'Missing arguments .first.'):
            def sample_check(arg, value):
                pass

            validate_with(
                params = {},
                spec = {
                    'first': {
                        'callbacks': {
                            'check callback': sample_check
                        }
                    }
                },
            )

        with self.assertRaisesRegex(Exception, 'Missing arguments .first.'):
            validate_with(
                params = {},
                spec = {
                    'first': {
                    }
                },
            )

        with self.assertRaisesRegex(Exception, 'extra arguments found: .second,third.'):
            validate_with(
                params = {
                    'first': 1,
                    'second': 2,
                    'third': 3
                },
                spec = {
                    'first': {
                    }
                },
            )

        with self.assertRaisesRegex(Exception, 'Expecting value for argument .first. to be .list. but got: .int.'):
            validate_with(
                params = {
                    'first': 1,
                },
                spec = {
                    'first': {
                        'type': list
                    }
                },
            )

        with self.assertRaisesRegex(Exception, 'callback .is_list. does not return boolean for argument .first.'):
            def list_check(arg_name, arg_value):
                if isinstance(arg_value, list):
                    return 1
                else:
                    return 0

            validate_with(
                params = {
                    'first': 1,
                },
                spec = {
                    'first': {
                        'callbacks': {
                            'is_list': list_check
                        }
                    }
                },
            )

        with self.assertRaisesRegex(Exception, 'callback .is_list. failed for argument .first.'):
            def list_check(arg_name, arg_value):
                return False

            validate_with(
                params = {
                    'first': 1,
                },
                spec = {
                    'first': {
                        'callbacks': {
                            'is_list': list_check
                        }
                    }
                },
            )

        ret_val = validate_with(
            params = {
                'first': {'foo': 'bar'},
            },
            spec = {
                'first': {
                }
            },
        )

        self.assertEqual(ret_val, {'first': {'foo': 'bar'}})

        ret_val = validate_with(
            params = {
            },
            spec = {
                'first': {
                    'optional': True,
                    'default': 1
                }
            },
        )
        self.assertEqual(ret_val, {'first': 1})

        def int_check(arg_name, arg_value):
            return True

        ret_val = validate_with(
            params = {
                'first': 2
            },
            spec = {
                'first': {
                    'callbacks': {
                        'is_int': int_check
                    }
                }
            },
        )
        self.assertEqual(ret_val, {'first': 2})

        ret_val = validate_with(
            params = {},
            spec = {
                'first': {
                    'optional': True,
                    'default': False,
                }
            }
        )
        self.assertEqual(ret_val, {'first': False})

if __name__ == '__main__':
    unittest.main()