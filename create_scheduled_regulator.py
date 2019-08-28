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

if __name__ == '__main__':
    fid_select = '_EBDB5A4A-543C-9025-243E-8CAD24307380'
    fid_select = '_AAE94E4A-2465-6F5E-37B1-3E72183A4E44'  # test9500new
    fid_select = '_C1C3E687-6FFD-C753-582B-632A27E28507'  # ieee123

    simulation_id = 1547704875
    command_builder.init(fid_select, simulation_id)

    msg = command_builder.reg_msg('creg4a', 5, 10)

    seconds = int(time.time())
    # seconds = 1374510720 # Monday, July 22, 2013 4:32:00 PM
    # 2013-07-22 16:32:00
    # Monday, July 22, 2013 10:32:00 AM
    # 2013-07-22 10:32:00

    cmd_msg = command_builder.create_scheduled_command(msg, seconds + 30, seconds + 120)
    with open('test_scheduled_regulator.json', 'w') as outfile:
        json.dump(cmd_msg, outfile, indent=2)

    command_builder.send_scheduled_command(msg,seconds+30, seconds+240)

    request_status = {"command": "new_events"}

    request_status['events'] = [msg]
    print(json.dumps(request_status,indent=2))






