class Error:
    errors = {
        'not_gt_size': {'detail': [{'loc': ['query', 'page[size]'], 'msg': 'ensure this value is greater than 0',
                                    'type': 'value_error.number.not_gt', 'ctx': {'limit_value': 0}}]},
        'not_gt_number': {'detail': [{'loc': ['query', 'page[number]'], 'msg': 'ensure this value is greater than 0',
                                      'type': 'value_error.number.not_gt', 'ctx': {'limit_value': 0}}]},
        'int_number': {'detail': [{'loc': ['query', 'page[number]'], 'msg': 'value is not a valid integer',
                                   'type': 'type_error.integer'}]},
        'int_size': {'detail': [{'loc': ['query', 'page[size]'], 'msg': 'value is not a valid integer',
                                 'type': 'type_error.integer'}]}
    }
