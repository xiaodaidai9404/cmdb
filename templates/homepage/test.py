result = 'date=2020-05-22 time=14:28:40 devname=FG3040B_591 devid=FG3K0B3I11700132 logid=0100044545 type=event subtype=system level=information vd="root" logdesc="Object configured" user="10000" ui="GUI(61.11.11.118)" action=Move cfgtid=3541788 cfgpath="router.policy" cfgobj="2->1" msg="Move router.policy 2->1"'
result.split()
a = {}
for item in result.split():
    print item