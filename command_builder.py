import query_model_adms as query_model
import json
import argparse
from gridappsd import GOSS, DifferenceBuilder
from gridappsd.topics import simulation_input_topic, simulation_output_topic
goss_sim = "goss.gridappsd.process.request.simulation"
test_input = "/topic/goss.gridappsd.simulation.test.input."

switch_name_map = {}
generator_name_map = {}
reg_name_map = {}
pv_name_map = {}
simulation_id = 1
# def create_message(object,attribute,forward_value,reverse_value):
#     m = {
#         "message": {
#             "forward_differences": [
#                 {
#                     "object": object,
#                     "attribute": attribute,
#                     "value": forward_value
#                 }
#             ],
#             "reverse_differences": [
#                 {
#                     "object": object,
#                     "attribute": attribute,
#                     "value": reverse_value
#                 }
#             ]
#         }
#     }
#     return m

def create_scheduled_message(msg,occuredDateTime,stopDateTime):
    m = {
        "message": {
            "forward_differences": [
            ],
            "reverse_differences": [
            ]
        },
        "event_type": "ScheduledCommandEvent",
        "occuredDateTime": occuredDateTime,
        "stopDateTime": stopDateTime
    }
    m['message']['forward_differences'] = msg['input']['message']['forward_differences']
    m['message']['reverse_differences'] = msg['input']['message']['reverse_differences']
    return m

def reg_msg(name,fv=1,rv=0):
    if name not in reg_name_map:
        print('No regulator named ' + name)
        return None
    _diff = DifferenceBuilder(simulation_id)
    _diff.add_difference(switch_name_map[name], "TapChanger.step", fv, rv)
    msg = _diff.get_message()
    return msg

def switch_msg(name,fv=1,rv=0):
    if name not in switch_name_map:
        print('No switch named ' + name)
        return None
    _diff = DifferenceBuilder(simulation_id)
    # _diff.add_difference(switch_name_map[name], "Switch.open", 1, 0)
    _diff.add_difference(switch_name_map[name], "Switch.open", fv, rv)
    msg = _diff.get_message()
    return msg

def genenrator_msg(name,fv_p=0,fv_q=0,rv_p=0,rv_q=0):
    if name not in generator_name_map:
        print('No generator named ' + name)
        return None
    # generators = query_model.get_generators(fid_select)
    # generator_name_map = {generator['name']: generator['id'] for generator in generators}
    # msg =create_message(generator_name_map[name], "SynchronousMachine.p", 0, 0)
    # msg2 = create_message(generator_name_map[name], "SynchronousMachine.q", 0, 0)
    # msg['message']['forward_differences'].append(msg2['message']['forward_differences'][0])
    # msg['message']['forward_differences'].append(msg2['message']['forward_differences'][0])
    _diff = DifferenceBuilder(simulation_id)
    # _diff.add_difference(generator_name_map[name], "SynchronousMachine.p", 0, 0)
    # _diff.add_difference(generator_name_map[name], "SynchronousMachine.q", 0, 0)
    _diff.add_difference(generator_name_map[name], "SynchronousMachine.p", fv_p, rv_p)
    _diff.add_difference(generator_name_map[name], "SynchronousMachine.q", fv_q, rv_q)
    msg = _diff.get_message()
    return msg

def pv_msg(name,fv_p=0,fv_q=0,rv_p=0,rv_q=0):
    if name not in pv_name_map:
        print('No pv named ' + name)
        return None
    # generators = query_model.get_generators(fid_select)
    # generator_name_map = {generator['name']: generator['id'] for generator in generators}
    # msg =create_message(generator_name_map[name], "SynchronousMachine.p", 0, 0)
    # msg2 = create_message(generator_name_map[name], "SynchronousMachine.q", 0, 0)
    # msg['message']['forward_differences'].append(msg2['message']['forward_differences'][0])
    # msg['message']['forward_differences'].append(msg2['message']['forward_differences'][0])
    _diff = DifferenceBuilder(simulation_id)
    _diff.add_difference(generator_name_map[name], "PowerElectronicsConnection.p", fv_p, rv_p)
    _diff.add_difference(generator_name_map[name], "PowerElectronicsConnection.q", fv_q, rv_q)
    msg = _diff.get_message()
    return msg


def send_command(msg):
    goss = GOSS()
    goss.connect()
    print(json.dumps(msg,indent=2))
    request = json.dumps(msg)
    status = goss.send(simulation_input_topic(simulation_id), request)
    print(status)


def send_scheduled_command(msg, occuredDateTime, stopDateTime):
    goss = GOSS()
    goss.connect()
    request_status = {
        "command": "new_events"  # new_events, update_events, query_events
    }
    msg = create_scheduled_message(msg, occuredDateTime, stopDateTime)
    request_status['events'] = [msg]
    print(json.dumps(request_status,indent=2))
    request = json.dumps(request_status)
    status = goss.get_response(test_input+str(simulation_id), request, timeout=120)
    print(status)


def init(fid_select, simulationID):
    generators = query_model.get_generators(fid_select)
    global generator_name_map
    global pv_name_map
    global reg_name_map
    global switch_name_map
    global simulation_id
    simulation_id = simulationID
    generator_name_map = {generator['name']: generator['id'] for generator in generators}
    pvs = query_model.get_solar(fid_select)
    pv_name_map = {pv['name']: pv['id'] for pv in pvs}
    regs = query_model.get_regulator(fid_select)
    reg_name_map = {reg['rname']: reg['id'] for reg in regs}
    switches = query_model.get_switches(fid_select)
    switch_name_map = {switch['name']: switch['id'] for switch in switches}


def test():   # fid name open
    query_model.get_feeder('')

    print(generator_name_map)
    msg = genenrator_msg('diesel590')
    print(json.dumps(msg, indent=2))
    print(pv_name_map)
    print(reg_name_map)

    print(switch_name_map)

    msg = switch_msg('2002200004641085_sw',1,0)
    print(json.dumps(msg, indent=2))

    import time
    seconds = time.time()

    msg = create_scheduled_message(msg,seconds+30, seconds+90)
    print(json.dumps(msg, indent=2))


if __name__ == '__main__':
    test()