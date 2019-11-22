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
from time import strptime, strftime, mktime, gmtime
from datetime import datetime, timedelta
from calendar import timegm


def combine_messages(msgs):
    msg1 = msgs[0]
    for msg in msgs[1:]:
        msg1['input']['message']['forward_differences'].append(msg['input']['message']['forward_differences'][0])
        msg1['input']['message']['reverse_differences'].append(msg['input']['message']['reverse_differences'][0])
    return msg1


if __name__ == '__main__':
    import pytz
    # viz move 6 hours forward to 1248199200
    tt = datetime.strptime('2009-07-21 12:00:00 GMT', '%Y-%m-%d %H:%M:%S %Z')
    tt = tt.replace(tzinfo=pytz.UTC)
    print(tt)
    print(tt.timestamp())
    # start_time = timegm(tt.timestamp())  # 2009-07-21 12:00:00
    # print(start_time)
    # exit(0)

    fid_select = '_AAE94E4A-2465-6F5E-37B1-3E72183A4E44' # test9500new

    simulation_id = 966953393
    command_builder.init(fid_select, simulation_id)

    #  LN5593236-6

    # Event 1
    # Open LN0895780_SW
    # 1 close
    # 0 open
    #  true is 1 and false is 0
    event1 = command_builder.switch_msg('LN0895780_SW'.lower(), 1, 0)
    print(event1)

    #Restore
    # Open LINE.V9111_48332_SW
    # Open LINE.LN0742811_SW
    # Close LINE.LN0653457_SW
    # Close LINE.TSW803273_SW
    restore_msg1 = command_builder.switch_msg('V9111_48332_SW'.lower(), 1, 0)
    print(restore_msg1)
    restore_msg2 = command_builder.switch_msg('LN0742811_SW'.lower(), 1, 0)
    print(restore_msg2)
    restore_msg3 = command_builder.switch_msg('LN0653457_SW'.lower(), 0, 1)
    print(restore_msg3)
    restore_msg4 = command_builder.switch_msg('TSW803273_SW'.lower(), 0, 1)
    print(restore_msg4)

    restore_msg1 = combine_messages([restore_msg1, restore_msg2, restore_msg3, restore_msg4])
    print(restore_msg1)

    start_time = timegm(strptime('2013-07-22 12:00:00 GMT', '%Y-%m-%d %H:%M:%S %Z')) #  2019-07-22 12:00:00 or for viz 2013-07-22 06:00:00

    event1_msg = command_builder.create_scheduled_file(event1, datetime.fromtimestamp(start_time + 1*60).strftime("%Y-%m-%d %H:%M:%S"),
                                                          datetime.fromtimestamp(start_time + 3*60).strftime("%Y-%m-%d %H:%M:%S"))
    print(event1_msg)
    with open('test_scheduled_event_1_fault.json', 'w') as outfile:
        json.dump(event1_msg, outfile, indent=2)

    cmd_msg = command_builder.create_scheduled_file(restore_msg1, datetime.fromtimestamp(start_time + 1.5*60).strftime("%Y-%m-%d %H:%M:%S"),
                                                          datetime.fromtimestamp(start_time + 3.5*60).strftime("%Y-%m-%d %H:%M:%S"))
    print(cmd_msg)

    with open('test_scheduled_event_1_restoration.json', 'w') as outfile:
        json.dump(cmd_msg, outfile, indent=2)
    exit(0)







