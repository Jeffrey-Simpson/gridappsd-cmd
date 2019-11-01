# Copyright (c) 2019 Alliance for Sustainable Energy, LLC
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import query_model_adms as query_model
import json
from gridappsd import GOSS, DifferenceBuilder
from gridappsd.topics import simulation_input_topic, simulation_output_topic
goss_sim = "goss.gridappsd.process.request.simulation"
test_input = "/topic/goss.gridappsd.simulation.test.input."

feeder_name_list = []
line_name_map = {}
switch_name_map = {}
generator_name_map = {}
reg_name_map = {}
pv_name_map = {}
simulation_id = 1

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

def create_fault(mrid,phase,occuredDateTime,stopDateTime):
    event = {"PhaseConnectedFaultKind": "lineToGround",
             "FaultImpedance": {
                 "rGround": 0.001,
                 "xGround": 0.001
             },
             "ObjectMRID": [mrid],
             "phases": phase,
             "event_type": "Fault",
             "occuredDateTime": occuredDateTime,
             "stopDateTime": stopDateTime
             }

def reg_msg(name,fv=1,rv=0):
    if name not in reg_name_map:
        print('No regulator named ' + name)
        return None
    _diff = DifferenceBuilder(simulation_id)
    _diff.add_difference(reg_name_map[name]['id'], "TapChanger.step", fv, rv)
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
    # print(json.dumps(msg,indent=2))
    request = json.dumps(msg)
    status = goss.send(simulation_input_topic(simulation_id), request)
    print(status)


def send_comm_outage(msg, occuredDateTime, stopDateTime):
    goss = GOSS()
    goss.connect()
    request_status = {
        "command": "new_events"  # new_events, update_events, query_events
    }
    msg['occuredDateTime'] = occuredDateTime
    msg['stopDateTime'] = stopDateTime
    request_status['events'] = [msg]
    # print(json.dumps(request_status, indent=2))
    request = json.dumps(request_status)
    status = goss.get_response(test_input+str(simulation_id), request, timeout=120)
    print(status)


def send_scheduled_command(msg, occuredDateTime, stopDateTime):
    goss = GOSS()
    goss.connect()
    request_status = create_scheduled_command(msg, occuredDateTime, stopDateTime)
    # print(json.dumps(request_status, indent=2))
    request = json.dumps(request_status)
    status = goss.get_response(test_input+str(simulation_id), request, timeout=120)
    print(status)


def create_scheduled_command(msg, occuredDateTime, stopDateTime):
    request_status = {
        "command": "new_events"  # new_events, update_events, query_events
    }
    msg = create_scheduled_message(msg, occuredDateTime, stopDateTime)
    request_status['events'] = [msg]

    return request_status

def create_scheduled_file(msg, occuredDateTime, stopDateTime):
    msg = create_scheduled_message(msg, occuredDateTime, stopDateTime)
    return {'commandEvents': [msg]}



def init(fid_select, simulationID):

    global feeder_name_list
    global generator_name_map
    global pv_name_map
    global reg_name_map
    global switch_name_map
    global simulation_id
    global line_name_map
    simulation_id = simulationID

    result, name_map, node_name_map_va_power, node_name_map_pnv_voltage, \
    pec_map, load_power_map, line_map, trans_map, cap_pos, tap_pos, \
    load_voltage_map, line_voltage_map, trans_voltage_map = query_model.lookup_meas(fid_select)
    # print(repr(pec_map))
    feeder_name_list = query_model.get_feeder()
    generators = query_model.get_generators(fid_select)
    generator_name_map = {generator['name']: generator['id'] for generator in generators}
    pvs = query_model.get_solar(fid_select)
    # print(cap_pos)
    pv_name_map = {pv['name']: pv['id'] for pv in pvs}
    pv_name_map = {pv['name']:{'id':pv['id'], 'power measurement': pec_map[pv['busname'].upper()+'.'+pv['busphase'][0]]} for pv in pvs}
    regs = query_model.get_regulator(fid_select)
    # reg_name_map = {reg['rname']: reg['id'] for reg in regs}
    reg_name_map = {reg['rname']: {'id':reg['id'],
                                   'pos measurement': tap_pos[reg['bus'].upper()+'.'+query_model.lookup[reg['phs'][0]]],
                                   'phases': [phase for phase in reg['phs']],
                                   'phase_indexes': [str(int(query_model.lookup[phase])-1) for phase in reg['phs']]
                                   }
                                    for reg in regs}
    switches = query_model.get_switches(fid_select)
    switch_name_map = {switch['name']: switch['id'] for switch in switches}
    lines = query_model.get_line_segements(fid_select)
    line_name_map = {line['name']: line['eqid'] for line in lines}


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