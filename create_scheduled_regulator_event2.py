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
from time import strptime, strftime, mktime, gmtime
from datetime import datetime, timedelta
from calendar import timegm
import create_comm_outage

if __name__ == '__main__':
    start_time = timegm(strptime('2013-07-22 12:00:00 GMT', '%Y-%m-%d %H:%M:%S %Z')) #  2019-07-22 12:00:00 or for viz 2019-07-22 06:00:00
    start_time_local = timegm(strptime('2013-07-22 18:01:00 GMT', '%Y-%m-%d %H:%M:%S %Z'))

    print(timegm(strptime('2013-07-22 18:01:00 GMT', '%Y-%m-%d %H:%M:%S %Z')))
    print(timegm(strptime('2013-07-22 12:01:00 GMT', '%Y-%m-%d %H:%M:%S %Z')))
    print(timegm(strptime('2013-07-22 12:01:00 GMT', '%Y-%m-%d %H:%M:%S %Z')))
    print(mktime(strptime('2013-07-22 06:01:00 MST', '%Y-%m-%d %H:%M:%S %Z')))

    print(start_time)
    print(start_time_local )

    print(datetime.utcfromtimestamp(mktime(strptime('2013-07-22 06:01:00', '%Y-%m-%d %H:%M:%S')) + 1 * 60).strftime("%Y-%m-%d %H:%M:%S"))

    # start_time = timegm(strptime('2019-07-22 12:00:00 GMT', '%Y-%m-%d %H:%M:%S %Z')) #  2019-07-22 12:00:00 or for viz 2019-07-22 06:00:00
    # back_to_  =  datetime.utcfromtimestamp(start_time + 60)
    #
    # print(datetime.utcfromtimestamp(start_time + 60).strftime("%Y-%m-%d %H:%M:%S"))
    # exit(0)

    fid_select = '_DA00D94F-4683-FD19-15D9-8FF002220115'
    fid_select = '_C1C3E687-6FFD-C753-582B-632A27E28507'
    # fid_select = '_AAE94E4A-2465-6F5E-37B1-3E72183A4E44'  # test9500new

    simulation_id = 1264612599
    command_builder.init(fid_select, simulation_id)

    # seconds = 1374510720 # Monday, July 22, 2013 4:32:00 PM
    # 2013-07-22 16:32:00
    # Monday, July 22, 2013 10:32:00 AM
    # 2013-07-22 10:32:00

    reg = 'vreg3_a'
    reg = 'creg2a'

    start_time = timegm(strptime('2013-07-22 12:00:00 GMT', '%Y-%m-%d %H:%M:%S %Z')) #  2019-07-22 12:00:00 or for viz 2013-07-22 06:00:00
    # start_time_local = timegm(strptime('2013-07-22 12:00:00 GMT', '%Y-%m-%d %H:%M:%S %Z'))
    # start_time_local = timegm(strptime('2013-07-22 18:00:00 GMT', '%Y-%m-%d %H:%M:%S %Z'))
    # 1374516240
    # Transformer.VREG3_A
    msg = command_builder.reg_msg(reg, 10, 5)

    tap_event = create_comm_outage.create_reg_outage_file(command_builder.reg_name_map, [reg],
                                                          datetime.fromtimestamp(start_time + 1*60).strftime("%Y-%m-%d %H:%M:%S"),
                                                          datetime.fromtimestamp(start_time + 4*60).strftime("%Y-%m-%d %H:%M:%S"))
    # "2019-07-22 12:01:00"
    print(json.dumps(tap_event, indent=2))
    with open('test_comm_outage_event_2_fault.json', 'w') as outfile:
        json.dump(tap_event, outfile, indent=2)

    event1_msg = command_builder.create_scheduled_file(msg, start_time + 1*60, start_time + 4*60)
    event1_msg['outageEvents'] = [tap_event]
    print(event1_msg)
    with open('test_scheduled_event_2_fault.json', 'w') as outfile:
        json.dump(event1_msg, outfile, indent=2)

