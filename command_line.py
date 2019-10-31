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

import json
import argparse
import time
import command_builder


if __name__ == '__main__':
    example1 = '''# List switches\npython command_line.py  -f _AAE94E4A-2465-6F5E-37B1-3E72183A4E44 -l switch\n'''
    example2 = '''# Open switch ln2000901_sw for two minutes 
python command_line.py -i 1752306429 -f _EBDB5A4A-543C-9025-243E-8CAD24307380 -s ln2000901_sw -fv 1 -rv 0 -od 1374510840 -sd 1374510960'''
    parser = argparse.ArgumentParser(description='Command line utility to create and send events to the'
                                                 'GridAPPS-D platform', usage='python %(prog)s [options] \nExamples:\n' + example1
                                                                              + example2)
    parser.add_argument("-i", "--id", type=int, help="simulation id", required=False)
    parser.add_argument("-f", "--feeder_id", type=str, help="feeder id", default='_AAE94E4A-2465-6F5E-37B1-3E72183A4E44', required=False)
    parser.add_argument("-l", "--list", type=str, help="followed by equipment name or first letter of equipment,"
                                                       " -l switch or -l regulator", default=None, required=False)
    parser.add_argument("-s", "--switch", type=str, help="switch name", default=None, required=False)
    parser.add_argument("-p", "--pv", type=str, help="pv name", default=None, required=False)
    parser.add_argument("-r", "--regulator", type=str, help="regulator name", default=None, required=False)
    parser.add_argument("-g", "--generator", type=str, help="generator name", default=None, required=False)
    parser.add_argument("-fv", "--forward_values", nargs='+', type=float, help="forward values", default=0, required=False)
    parser.add_argument("-rv", "--reverse_values", nargs='+', type=float, help="reverse values", default=0, required=False)
    parser.add_argument("-od", "--occured_date_time", type=int, help="occured date time", default=None, required=False)
    parser.add_argument("-sd", "--stop_date_time", type=int, help="stop date time", default=None, required=False)

    args = parser.parse_args()
    print(int(time.time()))

    # fid_select = '_67AB291F-DCCD-31B7-B499-338206B9828F'
    fid_select_123 = '_C1C3E687-6FFD-C753-582B-632A27E28507'
    fid_select_123_pv = '_E407CBB6-8C8D-9BC9-589C-AB83FBF0826D'  # Mine 123-spv'
    # fid_select = '_C77C898B-788F-8442-5CEA-0D06ABA0693B'
    fid_select = '_EBDB5A4A-543C-9025-243E-8CAD24307380'
    # fid_select = '_4F76A5F9-271D-9EB8-5E31-AA362D86F2C3'
    # fid_select = '_C1C3E687-6FFD-C753-582B-632A27E28507'
    # fid_select = '_AAE94E4A-2465-6F5E-37B1-3E72183A4E44'
    simulation_id = args.id
    fid_select = args.feeder_id
    command_builder.init(fid_select, simulation_id)
    # test()
    if args.list:
        if args.list[0].lower() == 'f':
            for f in command_builder.feeder_name_list:
                print(f['feeder_name'] + " " + f["fdrid"])
            # print(json.dumps(command_builder.feeder_name_list,indent=2))
        elif args.list[0].lower() == 's':
            print(json.dumps(command_builder.switch_name_map,indent=2))
        elif args.list[0].lower() == 'l':
            print(json.dumps(command_builder.line_name_map,indent=2))
        elif args.list[0].lower() == 'p':
            print(json.dumps(command_builder.pv_name_map,indent=2))
        elif args.list[0].lower() == 'g':
            print(json.dumps(command_builder.generator_name_map,indent=2))
        elif args.list[0].lower() == 'r':
            print(json.dumps(command_builder.reg_name_map,indent=2))
        else:
            print('Unknown type ' + args.list)
        exit(0)

    msg = ''
    if args.regulator:
        msg = command_builder.reg_msg(args.regulator, int(args.forward_values[0]), int(args.reverse_values[0]))
    elif args.switch:
        msg = command_builder.switch_msg(args.switch, int(args.forward_values[0]), int(args.reverse_values[0]))
    elif args.pv:
        msg = command_builder.pv_msg(args.pv, args.forward_values[0], args.forward_values[1],
                                     args.reverse_values[0], args.reverse_values[1])
    elif args.genenrator:
        msg = command_builder.genenrator_msg(args.genenrator,args.forward_values[0], args.forward_values[1],
                                     args.reverse_values[0], args.reverse_values[1])


    current_seconds = time.time()
    occured_date_time, stop_date_time = args.occured_date_time, args.stop_date_time
    if occured_date_time is not None and occured_date_time <= 0:
        occured_date_time = current_seconds
        stop_date_time = current_seconds + stop_date_time

    # seconds=1374510977
    # msg = create_scheduled_message(msg,seconds+30, seconds+90)
    # print(json.dumps(msg, indent=2))
    if occured_date_time is None:
        command_builder.send_command(msg)
    else:
        command_builder.send_scheduled_command(msg, occured_date_time, stop_date_time)

usage = '''
 ## Open switch sw5 at time 1374510977 and close at 1374510997
python command_line.py -i 1083048786 -f _EBDB5A4A-543C-9025-243E-8CAD24307380 -s sw5 -fv 1 -rv 0 -od 1374510937 -sd 1374510997

# List switch names
python command_line.py  -f _AAE94E4A-2465-6F5E-37B1-3E72183A4E44 -l switch
# Open switch ln2000901_sw for two minutes 
python command_line.py -i 1752306429 -f _EBDB5A4A-543C-9025-243E-8CAD24307380 -s ln2000901_sw -fv 1 -rv 0 -od 1374510840 -sd 1374510960

 
python command_line.py  -f _C1C3E687-6FFD-C753-582B-632A27E28507 -l r

'''

