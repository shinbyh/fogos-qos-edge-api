import csv
import traceback

supported_svc_types = {}
default_qosreq_dict = {}
requirement_rules = {}
units = {}

def get_network_req(str):
    name,operator,value,unit = str.split()
    req = {}
    req['metricName'] = name
    req['metricValue'] = float(value)
    req['metricUnit'] = unit

    # handle operator
    op_str = ''
    if(operator == '<'):
        op_str = 'lt'
    elif(operator == '<='):
        op_str = 'le'
    elif(operator == '>'):
        op_str = 'gt'
    elif(operator == '>='):
        op_str = 'ge'
    elif(operator == '=='):
        op_str = 'eq'
    elif(operator == '!='):
        op_str = 'ne'
    else:
        op_str = 'none'
    req['metricOperator'] = op_str

    return req

def load_deafult_qosreq():
    with open('default_qos.csv', newline='') as csvfile:
        rows = csv.reader(csvfile)
        for row in rows:
            svc_type = row[0]
            default_qosreq_dict[svc_type] = []
            for item in row[1:len(row)]:
                requirement = get_network_req(item)
                default_qosreq_dict[svc_type].append(requirement)
                #print('adding ', requirement, ' to ', svc_type)

def load_supported_svctypes():
    with open('supported_svc_type.csv', newline='') as csvfile:
        rows = csv.reader(csvfile)
        for row in rows:
            basic_name = row[0]
            supported_svc_types[basic_name] = [basic_name]
            for item in row[1:len(row)]:
                supported_svc_types[basic_name].append(item)
                #print('[default svc type] add ',item,' to ',basic_name)

def load_requirement_rules():
    with open('requirement_rules.csv', newline='') as csvfile:
        rows = csv.reader(csvfile)
        for row in rows:
            if(len(row) < 8):
                continue

            req_category = row[0]
            if(req_category not in requirement_rules.keys()):
                requirement_rules[req_category] = {}

            req_type = row[1]
            if(req_type not in requirement_rules[req_category].keys()):
                requirement_rules[req_category][req_type] = {}

            req_value = row[2]
            req_qos_param = row[3]
            req_qos_unit = row[4]
            req_qos_op = row[5]
            req_qos_min = row[6]
            req_qos_max = row[7]
            requirement_rules[req_category][req_type][req_value] = {
                'qos_param':req_qos_param,
                'qos_unit':req_qos_unit,
                'qos_op':req_qos_op,
                'qos_min':req_qos_min,
                'qos_max':req_qos_max
            }

def load_units():
    with open('units.csv', newline='') as csvfile:
        rows = csv.reader(csvfile)
        for row in rows:
            units[row[0]] = float(row[1])

def get_basic_svctype_name(svc_type_str):
    for supported_svc_type in supported_svc_types.keys():
        if(svc_type_str.lower() in supported_svc_types[supported_svc_type]):
            return supported_svc_type
    return None

def make_error_msg(type, msg):
    error_msg = {}
    error_msg['type'] = type;
    error_msg['msg'] = msg;
    return error_msg

def apply_unit_diff(base_unit, apply_unit):
    if(apply_unit == 'any'):
        return 1.0
    else:
        return units[apply_unit.lower()]/units[base_unit.lower()]

def process_requirements(qosreq, requirements):
    for requirement in requirements:
        req_category = requirement['category']
        req_value = requirement['value']
        req_type = requirement['type']
        print('## category:', req_category, ', type:', req_type, ', value:', req_value)
        #print(req_category)
        #print(req_type)
        #print(req_value)

        if(req_value in requirement_rules[req_category][req_type].keys()):
            rule = requirement_rules[req_category][req_type][req_value]
        elif('any' in requirement_rules[req_category][req_type].keys()):
            rule = requirement_rules[req_category][req_type]['any']
        else:
            print('[Error] Unsupported requirement value: ', req_value)
            continue

        print('  @@ Applying rule:', rule)
        if(qosreq[rule['qos_param']] is not None):
            print('  @@ Target: ', qosreq[rule['qos_param']])

            value_to_apply = 0.0
            if(rule['qos_max'] == 'value'):
                value_to_apply  = float(req_value)
            else:
                value_to_apply = float(rule['qos_max'])

            if(rule['qos_op'] == 'add'):
                qosreq[rule['qos_param']]['metricValue'] += value_to_apply*apply_unit_diff(qosreq[rule['qos_param']]['metricUnit'], rule['qos_unit'])
            elif(rule['qos_op'] == 'multiply'):
                qosreq[rule['qos_param']]['metricValue'] *= value_to_apply*apply_unit_diff(qosreq[rule['qos_param']]['metricUnit'], rule['qos_unit'])
            elif(rule['qos_op'] == 'subtract'):
                qosreq[rule['qos_param']]['metricValue'] -= value_to_apply*apply_unit_diff(qosreq[rule['qos_param']]['metricUnit'], rule['qos_unit'])
            elif(rule['qos_op'] == 'min'):
                qosreq[rule['qos_param']]['metricValue'] = min([qosreq[rule['qos_param']]['metricValue'], value_to_apply*apply_unit_diff(qosreq[rule['qos_param']]['metricUnit'], rule['qos_unit'])])
            elif(rule['qos_op'] == 'max'):
                qosreq[rule['qos_param']]['metricValue'] = max([qosreq[rule['qos_param']]['metricValue'], value_to_apply*apply_unit_diff(qosreq[rule['qos_param']]['metricUnit'], rule['qos_unit'])])
    return qosreq

def interpret(svc_desc):
    try:
        # Check if service type is valid. otherwise, return error.
        svc_type = get_basic_svctype_name(svc_desc['service_type'])
        if(svc_type is None):
            return make_error_msg('unsupported_svc_type',
                    'The service type {} is not supported.'.format(svc_desc['service_type']))

        # Load default based on service type (copy from default)
        #qosreq = list(default_qosreq_dict[svc_type])
        qosreq = {}
        for item in default_qosreq_dict[svc_type]:
            qosreq[item['metricName']] = item

        # Apply service-specific requirements
        process_requirements(qosreq, svc_desc['requirements'])

        # Apply user preferences

        # Return network requirements
        qosreq['service_name'] = svc_desc['service_name']
        return qosreq
    except:
        traceback.print_exc()
        return make_error_msg('internal_error', 'Internal server error.')

if __name__ == '__main__':
    load_supported_svctypes()
    load_deafult_qosreq()
    load_requirement_rules()
    load_units()

    svc_desc = {
        'service_type':'videostreaming',
        'service_name':'Pyongchang Olymphic Speed Skating Highlight #2',
        'requirements':[
            {
                'category':'screen',
                'type':'resolution',
                'unit':'pixels',
                'value':'720p'
            },
            {
                'category':'screen',
                'type':'frame_rate',
                'unit':'fps',
                'value':'60fps'
            },
            {
                'category':'sound',
                'type':'bit_rate',
                'unit':'kbps',
                'value':'128'
            }
        ]
    }
    qosreq = interpret(svc_desc)
    print(qosreq)
