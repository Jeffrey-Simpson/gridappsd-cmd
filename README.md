# gridappsd-cmd

Examples using gridappsd-cmd.

## Install first time only

Create an enviroment with `conda` or `virtualenv`.  If you are using conda, you can 
simply type:

        conda env create -f environment.yml
        
## 
Alternately you can install gridappsd-python and that should be the only dependency  
pip install git+git://github.com/GRIDAPPSD/gridappsd-python/tree/app-in-container.git


## Example commands
        
### Feeder IDs
```bash
ieee123 _C1C3E687-6FFD-C753-582B-632A27E28507
ieee123pv _E407CBB6-8C8D-9BC9-589C-AB83FBF0826D
ieee13nodeckt _49AD8E07-3BF9-A4E2-CB8F-C3722F837B62
ieee13nodecktassets _5B816B93-7A5F-B64C-8460-47C17D6E4B0F
ieee37 _49003F52-A359-C2EA-10C4-F4ED3FD368CC
ieee8500 _4F76A5F9-271D-9EB8-5E31-AA362D86F2C3
j1 _67AB291F-DCCD-31B7-B499-338206B9828F
test9500new _AAE94E4A-2465-6F5E-37B1-3E72183A4E44
acep_psil _77966920-E1EC-EE8A-23EE-4EFD23B205BD
sourceckt _9CE150A8-8CC5-A0F9-B67E-BBD8C79D3095
```

## Test Scripts
There are test scripts that generate commands JSON events for demonstrations purposes.

```bash
python create_scheduled_regulator.py
python create_scheduled_switch.py
python create_comm_outage.py
```

## Things to check if there are problems

- [ ] Make sure the simulaiton id is set correctly
- [ ] Make sure that the times of the events are correct
- [ ] Make sure the feeder id is correct
- [ ] Make sure the name of the object is correct

```bash
docker ps
docker exec -it <CONTAINER ID> bash
```

```sql
mysql -u gridappsd -pgridappsd1234
use gridappsd;
select * from log where source = 'ProcessEvents';
select * from log where source = 'fncs_goss_bridge.py' and log_message LIKE '%phase_%';
```
        
### List all switches for a feeder 
```bash
python command_line.py  -f _AAE94E4A-2465-6F5E-37B1-3E72183A4E44 -l swi
```

### Open switch ln2000901_sw for two minutes
```bash
python command_line.py -i 1752306429 -f _AAE94E4A-2465-6F5E-37B1-3E72183A4E44 -s ln2000901_sw -fv 1 -rv 0 -od 1374510840 -sd 1374510960
```

## List all regulators
```bash
python command_line.py  -f _C1C3E687-6FFD-C753-582B-632A27E28507 -l r
```

### Open change tap 
```bash
python command_line.py -i 1276630028 -f _C1C3E687-6FFD-C753-582B-632A27E28507 -r creg4a -fv 5 -rv 10 -od 1567025394 -sd 1567025574
```