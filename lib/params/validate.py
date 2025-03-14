import copy

def _validate_spec(name, spec):
    if not isinstance(spec, dict):
        raise Exception(f'spec for [{name}] is not a dictionary')

    invalid_spec_keys = []
    for spec_key in sorted(list(spec.keys())):
        if spec_key not in ['type', 'optional', 'default', 'callbacks']:
            invalid_spec_keys.append(spec_key)

    if len(invalid_spec_keys) > 0:
        raise Exception(f'Invalid spec keys found for [{name}]: [' + ','.join(invalid_spec_keys) + ']')

    # ----------------------------------------------------
    # check for spec_type type
    # ----------------------------------------------------
    if 'type' in spec and spec['type'] not in [int, float, bool, str, list, dict]:
        raise Exception(f'spec type [type] is not one of [int, float, bool, str, list, dict] for [{name}]')

    # ----------------------------------------------------
    # check for spec_type optional
    # ----------------------------------------------------
    if 'optional' in spec and not isinstance(spec['optional'], bool):
        raise Exception(f'spec type [optional] is not a boolean for spec [{name}]')

    # ----------------------------------------------------
    # check for spec_type default
    # ----------------------------------------------------
    if 'default' in spec and 'type' in spec and not isinstance(spec['default'], spec['type']):
        raise Exception(f'value of [default] for spec [{name}] is not of required type')

    if 'default' in spec and ('optional' not in spec or not spec['optional']):
        raise Exception(f'[default] spec provided for non optional argument [{name}]')

    # ----------------------------------------------------
    # check for spec_type callbacks
    # ----------------------------------------------------
    if 'callbacks' in spec:
        if not isinstance(spec['callbacks'], dict):
            raise Exception(f'spec type [callbacks] is not of type dictionary for [{name}]')

        if len(spec['callbacks'].keys()) == 0:
            raise Exception(f'spec type [callbacks] is empty dictionary for [{name}]')

        for callback in spec['callbacks']:
            if not callable(spec['callbacks'][callback]):
                raise Exception(f'callback [{callback}] is not callable for spec [{name}]')

    return

def _validate_param_with_spec(param_name, param_value, param_spec):
    # ----------------------------------------------------
    # validate the type of the value
    # ----------------------------------------------------
    if 'type' in param_spec and not isinstance(param_value, param_spec['type']):
        raise ValueError(f'Expecting value for argument [{param_name}] to be [' + param_spec['type'].__name__ + '] but got: [' + type(param_value).__name__ + ']')

    ret_value = None
    if type(param_value) in [list, dict]:
        ret_value = copy.deepcopy(param_value)
    else:
        ret_value = param_value

    if 'callbacks' in param_spec:
        for callback in param_spec['callbacks']:
            callback_return = param_spec['callbacks'][callback](param_name, ret_value)
            if not isinstance(callback_return, bool):
                raise Exception(f'callback [{callback}] does not return boolean for argument [{param_name}]')
            if not callback_return:
                raise ValueError(f'callback [{callback}] failed for argument [{param_name}]')

    return ret_value

def validate_with(**args):
    invalidate_validate_with_args = []
    for arg_key in sorted(list(args.keys())):
        if arg_key not in ['params', 'spec', 'allow_extra']:
            invalidate_validate_with_args.append(arg_key)
    if len(invalidate_validate_with_args) > 0:
        raise Exception('validate_with arguments has invalid keys: [' + ','.join(invalidate_validate_with_args) + ']')

    if 'params' not in args:
        raise Exception('validate_with is called without params in arguments')

    if 'spec' not in args:
        raise Exception('validate_with is called without spec in arguments')

    if 'allow_extra' in args and not isinstance(args['allow_extra'], bool):
        raise Exception('validate_with allow_extra argument needs to be boolean')

    params      = args['params']
    spec        = args['spec']
    allow_extra = False
    if 'allow_extra' in args:
        allow_extra = args['allow_extra']

    if not isinstance(params, dict):
        raise ValueError('params need to be a dictionary but got: ' + type(params).__name__)
    if not isinstance(spec, dict):
        raise Exception('spec need to be a dictionary but got: ' + type(spec).__name__)

    if len(spec.keys()) == 0:
        raise Exception('Empty specification provided')

    for spec_name in sorted(list(spec.keys())):
        _validate_spec(spec_name, spec[spec_name])

    missing_params = []
    for param in spec:
        if param not in params and ('optional' not in spec[param] or not spec[param]['optional']):
            missing_params.append(param)

    if len(missing_params) > 0:
        raise ValueError('Missing arguments [' + ','.join(missing_params) + ']')

    if not allow_extra:
        extra_params = []
        for param in sorted(list(params.keys())):
            if param not in spec:
                extra_params.append(param)

        if len(extra_params) > 0:
            raise ValueError('extra arguments found: [' + ','.join(extra_params) + ']')

    ret_params = {}
    for param in sorted(list(params.keys())):
        if param in spec:
            ret_params[param] = _validate_param_with_spec(param, params[param], spec[param])
        else:
            if type(params[param]) in [list, dict]:
                ret_params[param] = copy.deepcopy(params[param])
            else:
                ret_params[param] = params[param]

    for param in spec:
        if param not in ret_params and 'default' in spec[param]:
            ret_params[param] = spec[param]['default']

    return ret_params