#!/usr/bin/python3
#
# Parses ContractTable.csv and outputs actual contracts from snippets.
#
# WARNING: Edit this and ContractTable.csv, not the contracts!
#
import sys
import os
import csv
import re

ROOT = os.getenv('ROOT')
DEST = os.getenv('DEST')
DEBUG = True

# --------------------------------------------------------------------------------

def error(fmt, *a):
    sys.stderr.write("ContractGen.py: error: ")
    sys.stderr.write(fmt.format(*a))
    sys.stderr.write("\n")
    sys.exit(1)

def warning(fmt, *a):
    sys.stderr.write("ContractGen.py: warning: ")
    sys.stderr.write(fmt.format(*a))
    sys.stderr.write("\n")

def debug(fmt, *a):
    if not DEBUG:
        return
    sys.stderr.write("DEBUG: ")
    sys.stderr.write(fmt.format(*a))
    sys.stderr.write("\n")

def output(fmt, *a):
    sys.stdout.write(fmt.format(*a))
    sys.stdout.write("\n")
    
# --------------------------------------------------------------------------------

class ContractType:
    def __init__(self, group, counter, name, data):
        self.group = group
        self.counter = counter
        self.suffix = re.sub(r'[- ]', '', name)
        self.data = data
        self.name = "{}-{}-{}".format(self.group.title, self.counter, self.suffix)
        self.title = name
        self.output_path = "{}/{}/{}-{}.cfg".format(DEST, self.group.title, self.counter, self.suffix)
        self.out = sys.stdout
        self.agent = "KPlanes_{}".format(data[1])
        self.description = ""
        self.synopsis = ""
        self.notes = ""
        self.completedMessage = ""

    def write(self, fmt, *a):
        self.out.write(fmt.format(*a))

    def generate(self):
        if self.name != "Start-001-FirstFlight":
            return

        with open(self.output_path, "w") as self.out:
            self._gen_header()
            self._gen_begin()
            self._gen_requirements()
            self._gen_data()
            self._gen_description()
            self._gen_limits()
            self._gen_rewards()
            self._gen_behaviours()
            self._gen_parameters()
            self._gen_end()        

    def _gen_header(self):
        self.write('// -*- conf-javaprop -*-\n')
        self.write('//\n')
        self.write('// Copied and modified from GAP/Wright-FirstFlight.cfg\n')
        # self.write('// **** WARNING: DO NOT EDIT THIS FILE! Change ContractTable.csv and/or ContractGen.py ****\n')
        # self.write('//\n')
        self.write('\n')
        
    def _gen_begin(self):
        self.write('CONTRACT_TYPE\n')
        self.write('{{\n')
        self.write('\n')
        self.write('	sortKey = aa{:02d}\n', int(self.counter))
        self.write('\n')

    def _gen_requirements(self):
        self.write('//REQUIREMENTS FOR CONTRACT TO APPEAR\n')
        self.write('\n')
        self.write('	REQUIREMENT\n')
        self.write('	{{\n')
        self.write('		name = Any\n')
        self.write('		type = Any\n')
        self.write('\n')
        self.write('		REQUIREMENT\n')
        self.write('		{{\n')
        self.write('			name = PartModuleUnlocked\n')
        self.write('			type = PartModuleUnlocked\n')
        self.write('			\n')
        self.write('			partModule = ModuleControlSurface\n')
        self.write('\n')
        self.write('		}}\n')
        self.write('		\n')
        self.write('		REQUIREMENT:NEEDS[AtmosphereAutopilot]\n')
        self.write('		{{\n')
        self.write('			name = PartModuleUnlocked\n')
        self.write('			type = PartModuleUnlocked\n')
        self.write('			partModule = SyncModuleControlSurface\n')
        self.write('		}}\n')
        self.write('		\n')
        self.write('		REQUIREMENT:NEEDS[FerramAerospaceResearch]\n')
        self.write('		{{\n')
        self.write('			name = PartModuleUnlocked\n')
        self.write('			type = PartModuleUnlocked\n')
        self.write('			\n')
        self.write('			partModule = FARControllableSurface\n')
        self.write('\n')
        self.write('		}}\n')
        self.write('		\n')
        self.write('		REQUIREMENT:NEEDS[Firespitter]\n')
        self.write('		{{\n')
        self.write('			name = PartModuleUnlocked\n')
        self.write('			type = PartModuleUnlocked\n')
        self.write('			\n')
        self.write('			partModule = FSliftSurface\n')
        self.write('\n')
        self.write('		}}\n')
        self.write('		\n')
        self.write('		REQUIREMENT:NEEDS[Firespitter]\n')
        self.write('		{{\n')
        self.write('			name = PartModuleUnlocked\n')
        self.write('			type = PartModuleUnlocked\n')
        self.write('			\n')
        self.write('			partModule = FSwing\n')
        self.write('\n')
        self.write('		}}\n')
        self.write('\n')
        self.write('	}}\n')
        self.write('\n')
        self.write('	REQUIREMENT\n')
        self.write('	{{\n')
        self.write('		name = Any\n')
        self.write('		type = Any\n')
        self.write('		\n')
        self.write('		REQUIREMENT\n')
        self.write('		{{\n')
        self.write('			name = PartModuleUnlocked\n')
        self.write('			type = PartModuleUnlocked\n')
        self.write('			\n')
        self.write('			partModule = ModuleResourceIntake\n')
        self.write('		}}\n')
        self.write('		\n')
        self.write('		REQUIREMENT:NEEDS[AJE]\n')
        self.write('		{{\n')
        self.write('		    name = PartModuleUnlocked\n')
        self.write('		    type = PartModuleUnlocked\n')
        self.write('\n')
        self.write('		    partModule = AJEInlet\n')
        self.write('		}}\n')
        self.write('	}}\n')
        self.write('\n')

    def _gen_data(self):
        self.write('//DATA NODES TO PROCESS FOR CONTRACT USE\n')
        self.write('\n')
        self.write('//Contract Specific VesselParameterGroup Definition Key (to prevent conflict with other active contracts)\n')
        self.write('	DATA\n')
        self.write('	{{\n')
        self.write('		type = string\n')
        self.write('		\n')
        self.write('		craft = KPlanesCraftWrightFirstFlight\n')
        self.write('		\n')
        self.write('	}}\n')
        self.write('\n')

    def _gen_description(self):
        self.write('//CONTRACT DESCRIPTION\n')
        self.write('\n')
        self.write('	name = {}\n', self.name)
        self.write('	title = {}\n', self.title)        
        self.write('	group = {}\n', self.group.name)
        self.write('	agent = {}\n', self.agent)
        self.write('\n')
        self.write('	description = {}\n', self.description)
        self.write('	\n')
        self.write('	synopsis = {}\n', self.synopsis)
        self.write('\n')
        self.write('	notes = {}\n', self.notes)
        self.write('\n')
        self.write('	completedMessage = {}\n', self.completedMessage)
        self.write('	\n')
        
    def _gen_limits(self):
        self.write('//Contract Limits\n')
        self.write('   	maxCompletions = 1\n')
        self.write('   	maxSimultaneous = 1\n')
        self.write('//	weight = 100.0\n')
        self.write('	\n')
        self.write('	autoAccept = false\n')
        self.write('	declinable = true\n')
        self.write('	cancellable = true\n')
        self.write('	\n')
        self.write('	minExpiry = 7.0\n')
        self.write('	maxExpiry = 7.0\n')
        self.write('	deadline = 0\n')
        self.write('	\n')
        
    def _gen_rewards(self):
        self.write('//Contract Reward Modifiers\n')
        self.write('	prestige = Trivial\n')
        self.write('   	targetBody = HomeWorld()\n')
        self.write('	\n')
        self.write('//Contract Rewards\n')
        self.write('  	advanceFunds = 2000.0\n')
        self.write('  	rewardFunds = 10000.0\n')
        self.write('  	rewardReputation = 50.0\n')
        self.write(' 	rewardScience = 10.0\n')
        self.write('\n')
        self.write('//Contract Penalties\n')
        self.write('  	failureFunds = 4000.0\n')
        self.write(' 	failureReputation = 5.0\n')
        self.write('\n')

    def _gen_behaviours(self):
        self.write('	\n')
        self.write('//BEHAVIOURS TO DO WHEN CREATING CONTRACT\n')
        self.write('	BEHAVIOUR\n')
        self.write('	{{\n')
        self.write('		name = AwardExperience\n')
        self.write('		type = AwardExperience\n')
        self.write('		\n')
        self.write('		parameter = WrightLand\n')
        self.write('		experience = 1\n')
        self.write('		\n')
        self.write('	}}\n')
        self.write('\n')

    def _gen_parameters(self):
        self.write('\n')
        self.write('//PARAMETERS FOR CONTRACT COMPLETION\n')
        self.write('\n')
        self.write('//Craft definition\n')
        self.write('	PARAMETER\n')
        self.write('	{{\n')
        self.write('		name = VesselParameterGroup\n')
        self.write('		type = VesselParameterGroup\n')
        self.write('		title = Your flying machine must\n')
        self.write('		\n')
        self.write('		define = @/craft\n')
        self.write('		dissassociateVesselsOnContractCompletion = true\n')
        self.write('		\n')
        self.write('		PARAMETER\n')
        self.write('		{{\n')
        self.write('			name = HasCrew\n')
        self.write('			type = HasCrew\n')
        self.write('			title = have a volunteer\n')
        self.write('		\n')
        self.write('			minCrew = 1\n')
        self.write('		\n')
        self.write('			disableOnStateChange = false\n')
        self.write('			hideChildren = true\n')
        self.write('\n')
        self.write('		}}\n')
        self.write('\n')
        self.write('		PARAMETER\n')
        self.write('		{{\n')
        self.write('			name = PartValidation\n')
        self.write('			type = PartValidation\n')
        self.write('			title = have wings\n')
        self.write('			\n')
        self.write('			category = Aero\n')
        self.write('			\n')
        self.write('			disableOnStateChange = false\n')
        self.write('			hideChildren = true\n')
        self.write('\n')
        self.write('		}}\n')
        self.write('		\n')
        self.write('		PARAMETER\n')
        self.write('		{{\n')
        self.write('			name = All\n')
        self.write('			type = All\n')
        self.write('			title = have an air breathing engine only\n')
        self.write('			\n')
        self.write('			PARAMETER\n')
        self.write('			{{\n')
        self.write('				name = PartValidation\n')
        self.write('				type = PartValidation\n')
        self.write('				title = not have any solid rocket engines\n')
        self.write('\n')
        self.write('				NONE\n')
        self.write('				{{\n')
        self.write('					MODULE\n')
        self.write('					{{\n')
        self.write('						EngineType = SolidBooster\n')
        self.write('						\n')
        self.write('					}}\n')
        self.write('					\n')
        self.write('				}}\n')
        self.write('				\n')
        self.write('				disableOnStateChange = false\n')
        self.write('				hideChildren = true\n')
        self.write('			\n')
        self.write('			}}\n')
        self.write('			\n')
        self.write('			PARAMETER\n')
        self.write('			{{\n')
        self.write('				name = PartValidation\n')
        self.write('				type = PartValidation\n')
        self.write('				title = not have any liquid rocket engines\n')
        self.write('\n')
        self.write('				NONE\n')
        self.write('				{{\n')
        self.write('					MODULE\n')
        self.write('					{{\n')
        self.write('						EngineType = LiquidFuel\n')
        self.write('						\n')
        self.write('					}}\n')
        self.write('					\n')
        self.write('				}}\n')
        self.write('				\n')
        self.write('				disableOnStateChange = false\n')
        self.write('				hideChildren = true\n')
        self.write('			\n')
        self.write('			}}\n')
        self.write('			\n')
        self.write('\n')
        self.write('			PARAMETER\n')
        self.write('			{{\n')
        self.write('				name = HasResource\n')
        self.write('				type = HasResource\n')
        self.write('				title = not have any solid rocket fuel\n')
        self.write('				\n')
        self.write('				resource = SolidFuel				\n')
        self.write('				minQuantity = 0.0\n')
        self.write('				maxQuantity = 0.0\n')
        self.write('				\n')
        self.write('				disableOnStateChange = false\n')
        self.write('				hideChildren = true\n')
        self.write('		\n')
        self.write('			}}\n')
        self.write('			\n')
        self.write('			PARAMETER\n')
        self.write('			{{\n')
        self.write('				name = HasResource\n')
        self.write('				type = HasResource\n')
        self.write('				title = not have any oxidizer\n')
        self.write('				\n')
        self.write('				resource = Oxidizer				\n')
        self.write('				minQuantity = 0.0\n')
        self.write('				maxQuantity = 0.0\n')
        self.write('				\n')
        self.write('				disableOnStateChange = false\n')
        self.write('				hideChildren = true\n')
        self.write('		\n')
        self.write('			}}\n')
        self.write('			\n')
        self.write('			disableOnStateChange = false\n')
        self.write('		\n')
        self.write('		}}\n')
        self.write('		\n')
        self.write('		disableOnStateChange = false\n')
        self.write('\n')
        self.write('	}}\n')
        self.write('\n')
        self.write('//Contract Goals\n')
        self.write('	PARAMETER\n')
        self.write('	{{\n')
        self.write('		name = VesselParameterGroup\n')
        self.write('		type = VesselParameterGroup\n')
        self.write('		title = get airborne\n')
        self.write('		\n')
        self.write('		vessel = @/craft\n')
        self.write('		\n')
        self.write('		PARAMETER\n')
        self.write('		{{\n')
        self.write('			name = ReachState\n')
        self.write('			type = ReachState\n')
        self.write('\n')
        self.write('			targetBody = HomeWorld()		\n')
        self.write('			situation = FLYING\n')
        self.write('			minSpeed = 15\n')
        self.write('			\n')
        self.write('			completeInSequence = true\n')
        self.write('			disableOnStateChange = true\n')
        self.write('			hideChildren = true\n')
        self.write('\n')
        self.write('		}}\n')
        self.write('	\n')
        self.write('		completeInSequence = true\n')
        self.write('		hideChildren = true\n')
        self.write('	\n')
        self.write('	}}\n')
        self.write('\n')
        self.write('//Recovery Parameter - Landing\n')
        self.write('	PARAMETER\n')
        self.write('	{{\n')
        self.write('		name = WrightLand\n')
        self.write('		type = VesselParameterGroup\n')
        self.write('		title = and then land and stop anywhere\n')
        self.write('		\n')
        self.write('		vessel = @/craft\n')
        self.write('\n')
        self.write('		PARAMETER\n')
        self.write('		{{\n')
        self.write('			name = ReachState\n')
        self.write('			type = ReachState\n')
        self.write('			\n')
        self.write('			targetBody = HomeWorld()\n')
        self.write('			situation = LANDED\n')
        self.write('			maxSpeed = 0.0\n')
        self.write('			\n')
        self.write('			disableOnStateChange = false\n')
        self.write('			hideChildren = true\n')
        self.write('\n')
        self.write('		}}\n')
        self.write('	\n')
        self.write('		completeInSequence = true\n')
        self.write('		hideChildren = true\n')
        self.write('	\n')
        self.write('	}}\n')
        self.write('\n')
        self.write('//Recovery Parameter - Craft & Kerbal Safety Check\n')
        self.write('	PARAMETER\n')
        self.write('	{{\n')
        self.write('		name = All\n')
        self.write('		type = All\n')
        self.write('		title = safely\n')
        self.write('		\n')
        self.write('		PARAMETER\n')
        self.write('		{{\n')
        self.write('			name = VesselNotDestroyed\n')
        self.write('			type = VesselNotDestroyed\n')
        self.write('			title = without destroying your flying machine\n')
        self.write('			\n')
        self.write('			vessel = @/craft\n')
        self.write('\n')
        self.write('		}}\n')
        self.write('		\n')
        self.write('		PARAMETER\n')
        self.write('		{{\n')
        self.write('			name = KerbalDeaths\n')
        self.write('			type = KerbalDeaths\n')
        self.write('			title = or killing anyone\n')
        self.write('			\n')
        self.write('			vessel = @/craft\n')
        self.write('\n')
        self.write('		}}\n')
        self.write('		\n')
        self.write('		completeInSequence = true\n')
        self.write('		disableOnStateChange = true\n')
        self.write('		\n')
        self.write('	}}\n')
        self.write('	\n')
        
    def _gen_end(self):
        self.write('}}') # TODO: \n
        
class ContractGroup:
    def __init__(self, table, title):
        self.table = table
        self.title = title
        self.name = 'KPlanes_{}'.format(self.title)
        self.contract_types = []

    def add_type(self, counter, name, data):
        new_type = ContractType(self, counter, name, data)
        self.contract_types.append(new_type)

    def generate(self):
        for ct in self.contract_types:
            ct.generate()
        
class ContractTable:
    def __init__(self):
        self.contract_groups = {}
        self._read()

    def find_group(self, group_title):
        if group_title in self.contract_groups:
            return self.contract_groups[group_title]
        new_group = ContractGroup(self, group_title)
        self.contract_groups[group_title] = new_group
        return new_group

    def _read(self):
        with open("{}/ContractTable.csv".format(ROOT), newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            skip = True
            for row in reader:
                if skip:
                    skip = False
                    continue
                group_title = row[0]
                counter = row[2]
                name = row[3]
                group = self.find_group(group_title)
                group.add_type(counter, name, row)

    def generate(self):
        for group_title in self.contract_groups.keys():
            group = self.find_group(group_title)
            group.generate()

# --------------------------------------------------------------------------------

table = ContractTable()
table.generate()
