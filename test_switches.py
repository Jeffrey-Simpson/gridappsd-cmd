import query_model_adms as query_model
import json
import argparse
from gridappsd import GOSS, DifferenceBuilder
from gridappsd.topics import simulation_input_topic, simulation_output_topic
goss_sim = "goss.gridappsd.process.request.simulation"
test_input = "/topic/goss.gridappsd.simulation.test.input."
import command_builder


if __name__ == '__main__':
    # python adms_cmd ieee9500 sw5 open
    # python adms_cmd ieee9500 vreg4_c 9 5
    # python adms_cmd ieee9500 diesel590 off

    # fid_select = '_67AB291F-DCCD-31B7-B499-338206B9828F'
    fid_select_123 = '_C1C3E687-6FFD-C753-582B-632A27E28507'
    fid_select_123_pv = '_E407CBB6-8C8D-9BC9-589C-AB83FBF0826D'  # Mine 123pv'
    # fid_select = '_C77C898B-788F-8442-5CEA-0D06ABA0693B'
    fid_select = '_EBDB5A4A-543C-9025-243E-8CAD24307380'
    # fid_select = '_4F76A5F9-271D-9EB8-5E31-AA362D86F2C3'
    # fid_select = '_C1C3E687-6FFD-C753-582B-632A27E28507'
    # fid_select = '_AAE94E4A-2465-6F5E-37B1-3E72183A4E44'
    simulation_id = 2110697140
    command_builder.init(fid_select, simulation_id)
    # test()

    msg = command_builder.switch_msg('ln2000901_sw', 1,0)
    msg = command_builder.switch_msg('ln2000701_sw', 1,0)
    msg = command_builder.switch_msg('ln2001301_sw', 1,0)
    msg = command_builder.switch_msg('sw5', 1,0)
    # send_command(simulation_id,msg)
    seconds = 1374510977
    seconds = 1374510720
    # seconds = 1374511022
    # msg = create_scheduled_message(msg,seconds+30, seconds+90)
    # print(json.dumps(msg, indent=2))
    command_builder.send_scheduled_command(msg,seconds+30, seconds+240)





