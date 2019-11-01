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

import command_builder
import json
import time

outage_event = {
    "allOutputOutage": False,
    "allInputOutage": False,
    "inputOutageList": [],
    "outputOutageList": [],
    "event_type": "CommOutage",
    "occuredDateTime": 1374510900,  # 35
    "stopDateTime": 1374511080  # 38
}

outage_event_file = {
    "allOutputOutage": False,
    "allInputOutage": False,
    "tag": "mc45mjk2",
    "inputList": [],
    "outputList": [],
    "event_type": "CommOutage",
    "startDateTime": "2019-07-22 12:01:00",  # 35
    "stopDateTime": "2019-07-22 12:01:00",  # 38
}

def create_pv_outage(pv_name_map, pvs):

    for pv in pvs:
        obj_template = {"objectMRID": pv_name_map[pv]["id"],
                        "attribute": "PowerElectronicsConnection.p"}
        outage_event["inputOutageList"].append(obj_template)
        obj_template = {"objectMRID": pv_name_map[pv]["id"],
                        "attribute": "PowerElectronicsConnection.q"}
        outage_event["inputOutageList"].append(obj_template)
        outage_event["outputOutageList"].append(pv_name_map[pv]["power measurement"])

    return outage_event

def create_reg_outage(reg_name_map, regs):
    for reg in regs:
        obj_template = {"objectMRID": reg_name_map[reg]["id"],
                        "attribute": "TapChanger.step"}
        outage_event["inputOutageList"].append(obj_template)
        outage_event["outputOutageList"].append(reg_name_map[reg]["pos measurement"])

    return outage_event


def create_reg_outage_file(reg_name_map, regs, startDateTime=1374510900,stopDateTime=1374511080):
    for reg in regs:
        obj_template = {"name":reg,
                        "type":"Regulator",
                        "mRID": [reg_name_map[reg]["id"]],
                        "attribute": "TapChanger.step",
                        "phases":
                        [{
                            "phaseLabel": reg_name_map[reg]['phases'][count],
                            "phaseIndex": count
                        } for count, phase_name in enumerate(reg_name_map[reg]['phases'])]
                    }
        output_template = {
                    "name": reg,
                    "type": "Regulator",
                    "mRID": [reg_name_map[reg]["pos measurement"]],  # measurement
                    "phases": [phase_name for phase_name in reg_name_map[reg]['phases'] ],
                    "measurementTypes": ["POS" for phase_name in reg_name_map[reg]['phases'] ]
                }
        outage_event_file["inputList"].append(obj_template)
        # outage_event_file["outputList"].append(output_template) # TODO regulator in output not working yet
        outage_event_file["startDateTime"] = startDateTime
        outage_event_file["stopDateTime"] = stopDateTime

    return outage_event_file

def test_9500():
    fid_select = '_EBDB5A4A-543C-9025-243E-8CAD24307380'
    fid_select = '_AAE94E4A-2465-6F5E-37B1-3E72183A4E44'  # test9500new

    simulation_id = 1747300482
    command_builder.init(fid_select, simulation_id)

    pvs = ['pv_163', 'pv_164', 'pv_155', 'pv_156', 'pv_161', 'pv_162', 'pv_153', 'pv_154', 'pv_167', 'pv_168', 'pv_141',
           'pv_142', 'pv_165', 'pv_166', 'pv_145', 'pv_146', 'pv_143', 'pv_144', 'pv_159', 'pv_160', 'pv_151', 'pv_152',
           'pv_147', 'pv_148', 'pv_157', 'pv_158', 'pv_149', 'pv_150']
    pv_name_map = command_builder.pv_name_map
    pv_event = create_pv_outage(pv_name_map, pvs)
    msg = json.dumps(pv_event, indent=2)
    print(msg)
    with open('test_comm_outage_9500.json', 'w') as outfile:
        json.dump(pv_event, outfile, indent=2)

    # command_builder.send_scheduled_command(msg,seconds+30, seconds+240)


def test_123_pv():
    fid_select = '_EBDB5A4A-543C-9025-243E-8CAD24307380'

    simulation_id = 1747300482
    command_builder.init(fid_select, simulation_id)

    pvs = ['dg_84', 'dg_90']

    pv_name_map = command_builder.pv_name_map
    pv_event = create_pv_outage(pv_name_map, pvs)
    msg = json.dumps(pv_event, indent=2)
    print(msg)
    with open('test_comm_outage_123_pv.json', 'w') as outfile:
        json.dump(pv_event, outfile, indent=2)


def test_123_reg():
    fid_select = '_EBDB5A4A-543C-9025-243E-8CAD24307380'
    simulation_id = 1747300482
    command_builder.init(fid_select, simulation_id)

    regs = ['creg4a', 'creg4b', 'creg4c']

    pv_name_map = command_builder.reg_name_map
    pv_event = create_reg_outage(pv_name_map, regs)
    msg = json.dumps(pv_event, indent=2)
    print(msg)
    with open('test_comm_outage_123.json', 'w') as outfile:
        json.dump(pv_event, outfile, indent=2)

def test_123_reg_schedule():
    fid_select = '_C1C3E687-6FFD-C753-582B-632A27E28507'
    simulation_id = 474305352
    command_builder.init(fid_select, simulation_id)

    regs = ['creg4a', 'creg4b', 'creg4c']

    pv_event = create_reg_outage(command_builder.reg_name_map, regs)

    print(json.dumps(pv_event, indent=2))
    with open('test_comm_outage_123_reg.json', 'w') as outfile:
        json.dump(pv_event, outfile, indent=2)

    seconds = int(time.time())
    command_builder.send_comm_outage(pv_event, seconds+30,seconds+120)


if __name__ == '__main__':
    # test_9500()
    # test_123_reg_schedule()
    pass





