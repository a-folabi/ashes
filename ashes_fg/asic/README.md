## Setup
External package dependencies. Run the following at a terminal

```
pip install python-gdsii numpy verilog-parser
```

## Clone
Clone with HTTPS
```
> https://github.com/GTIceLab/Analog-Synthesis.git
```
or

Clone with SSH key
```
> git clone git@github.com:GTIceLab/Analog-Synthesis.git
```


## Execute
```
> cd ./Analog-Synthesis/ASIC/py-to-gds
> python main.py
```

## Results
- Install [Klayout](https://www.klayout.de/build.html)


View Guide file
```
Open ./Analog-Synthesis/ASIC/py-to-gds/june_run/june_run_guide.def in klayout using `file>import>DEF/LEF`
```

View Placed (but not routed) `.gds`
```
Open ./Analog-Synthesis/ASIC/py-to-gds/june_run/june_run_placed.gds in klayout using 'file>open'
```