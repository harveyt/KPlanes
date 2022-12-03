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
DEBUG = False
REPLACE_AUTOLOC = False

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
        self.table = self.group.table
        self.localization = self.table.localization
        self.counter = counter
        self.suffix = re.sub(r'[- ]', '', name)
        self.data = data
        self.name = "{}-{}-{}".format(self.group.title, self.counter, self.suffix)
        self.title = name
        self.output_path = "{}/{}/{}-{}.cfg".format(DEST, self.group.title, self.counter, self.suffix)
        self.out = sys.stdout
        self.agent = "KPlanes_{}".format(data[1])
        self.craft = "KPlanesCraft_{}_{}".format(self.group.title, self.counter)
        self.description = ""
        self.synopsis = ""
        self.notes = ""
        self.completedMessage = ""
        # Requires
        if data[3] != "":
            requires_parts = data[3].split('_')
            if len(requires_parts) == 1:
                requires_group = self.group
                requires_counter = requires_parts[0]
            else:
                requires_group = self.table.find_group(requires_parts[0])
                requires_counter = requires_parts[1]
            self.requires = requires_group.find_type(requires_counter)
        else:
            self.requires = None
        # Prestige
        self.prestige = "Trivial"
        prestige_stars = data[5]
        if prestige_stars == "**":
            self.prestige = "Significant"
        elif prestige_stars == "***":
            self.prestige = "Exceptional"
        # Other data
        self.rewardScale = data[6]
        self.style = data[7]
        self.altMin = data[8]
        self.altMax = data[9]
        self.speedMach = data[10]
        self.distanceKM = data[11]
        self.midState = data[12]
        self.payload = data[13]
        self.jet = data[14]
        self.rocket = data[15]
        self.staging = data[16]
        self.airLaunch = data[17]
        self.landNearKSC = data[18]

    def write(self, fmt, *a):
        self.out.write(fmt.format(*a))

    def localize(self, field):
        key = self.localization.make_key(self, field)
        if REPLACE_AUTOLOC:
            value = self.localization.get(key)
        else:
            value = key
        return value

    def from_number(self, value, scale):
        if not value.replace('.','',1).isdigit(): # not float or int, must be keyword
            value = "@KPlanes:{}".format(value)
        return "Round({} * {})".format(value, scale)

    # Speed is in Mach
    def speed(self, value):
        return self.from_number(value, "@KPlanes:Mach")

    # Altitude is in km
    def altitude(self, value):
        return self.from_number(value, "1000.0")

    # Distance is in km
    def distance(self, value):
        return self.from_number(value, "1000.0")
    
    def generate(self):
        if self.group.title != "Start":
            return
        if int(self.counter) > 2:
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
        self.write('	sortKey = a{}\n', self.counter)
        self.write('\n')

    def _gen_requirements(self):
        self.write('//REQUIREMENTS FOR CONTRACT TO APPEAR\n')
        self.write('\n')
        self._gen_requirements_previous()
        if self.style == "Fly":
            self._gen_requirements_style_fly()
        self.write('\n')

    def _gen_requirements_previous(self):
        if self.requires is None:
            return
        self.write('	REQUIREMENT\n')
        self.write('	{{\n')
        self.write('		name = CompleteContract\n')
        self.write('		type = CompleteContract\n')
        self.write('\n')
        self.write('		contractType = {}\n', self.requires.name)
        self.write('		minCount = 1\n')
        self.write('\n')
        self.write('	}}\n')
        self.write('\n')

    def _gen_requirements_style_fly(self):
        self.write('	REQUIREMENT\n')
        self.write('	{{\n')
        self.write('		name = Any\n')
        self.write('		type = Any\n')
        self.write('\n')
        self.write('		REQUIREMENT\n')
        self.write('		{{\n')
        self.write('			name = PartModuleUnlocked\n')
        self.write('			type = PartModuleUnlocked\n')
        self.write('\n')
        self.write('			partModule = ModuleControlSurface\n')
        self.write('\n')
        self.write('		}}\n')
        self.write('\n')
        self.write('		REQUIREMENT:NEEDS[AtmosphereAutopilot]\n')
        self.write('		{{\n')
        self.write('			name = PartModuleUnlocked\n')
        self.write('			type = PartModuleUnlocked\n')
        self.write('			partModule = SyncModuleControlSurface\n')
        self.write('		}}\n')
        self.write('\n')
        self.write('		REQUIREMENT:NEEDS[FerramAerospaceResearch]\n')
        self.write('		{{\n')
        self.write('			name = PartModuleUnlocked\n')
        self.write('			type = PartModuleUnlocked\n')
        self.write('\n')
        self.write('			partModule = FARControllableSurface\n')
        self.write('\n')
        self.write('		}}\n')
        self.write('\n')
        self.write('		REQUIREMENT:NEEDS[Firespitter]\n')
        self.write('		{{\n')
        self.write('			name = PartModuleUnlocked\n')
        self.write('			type = PartModuleUnlocked\n')
        self.write('\n')
        self.write('			partModule = FSliftSurface\n')
        self.write('\n')
        self.write('		}}\n')
        self.write('\n')
        self.write('		REQUIREMENT:NEEDS[Firespitter]\n')
        self.write('		{{\n')
        self.write('			name = PartModuleUnlocked\n')
        self.write('			type = PartModuleUnlocked\n')
        self.write('\n')
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
        self.write('\n')
        self.write('		REQUIREMENT\n')
        self.write('		{{\n')
        self.write('			name = PartModuleUnlocked\n')
        self.write('			type = PartModuleUnlocked\n')
        self.write('\n')
        self.write('			partModule = ModuleResourceIntake\n')
        self.write('		}}\n')
        self.write('\n')
        self.write('		REQUIREMENT:NEEDS[AJE]\n')
        self.write('		{{\n')
        self.write('		    name = PartModuleUnlocked\n')
        self.write('		    type = PartModuleUnlocked\n')
        self.write('\n')
        self.write('		    partModule = AJEInlet\n')
        self.write('		}}\n')
        self.write('	}}\n')

    def _gen_data(self):
        self.write('//DATA NODES TO PROCESS FOR CONTRACT USE\n')
        self.write('\n')
        self.write('//Contract Specific VesselParameterGroup Definition Key (to prevent conflict with other active contracts)\n')
        self.write('	DATA\n')
        self.write('	{{\n')
        self.write('		type = string\n')
        self.write('\n')
        self.write('		craft = {}\n', self.craft)
        self.write('\n')
        self.write('	}}\n')
        self.write('\n')
        self._gen_data_alt('AltMin', self.altMin)
        self._gen_data_alt('AltMax', self.altMax)

    def _gen_data_alt(self, prefix, altValue):
        if altValue == '':
            return
        self.write('	DATA\n')
        self.write('	{{\n')
        self.write('		type = string\n')
        expr = self.altitude(altValue)
        debug('prefix={} altValue={} expr={}', prefix, altValue, expr)
        self.write('		{} = {}\n', prefix, expr)
        self.write('		Pretty{} = @{}.Print()m\n', prefix, prefix, self.altitude(altValue))
        self.write('	}}\n')
        self.write('\n')
        
    def _gen_description(self):
        self.write('//CONTRACT DESCRIPTION\n')
        self.write('\n')
        self.write('	name = {}\n', self.name)
        self.write('	title = {}\n', self.localize('title'))
        self.write('	group = {}\n', self.group.name)
        self.write('	agent = {}\n', self.agent)
        self.write('\n')
        self.write('	description = {}\n', self.localize('description'))
        self.write('\n')
        self.write('	synopsis = {}\n', self.localize('synopsis'))
        self.write('\n')
        self.write('	notes = {}\n', self.localize('notes'))
        self.write('\n')
        self.write('	completedMessage = {}\n', self.localize('completedMessage'))
        self.write('\n')
        
    def _gen_limits(self):
        self.write('//Contract Limits\n')
        self.write('   	maxCompletions = 1\n')
        self.write('   	maxSimultaneous = 1\n')
        self.write('//	weight = 100.0\n')
        self.write('\n')
        self.write('	autoAccept = false\n')
        self.write('	declinable = true\n')
        self.write('	cancellable = true\n')
        self.write('\n')
        self.write('	minExpiry = 7.0\n')
        self.write('	maxExpiry = 7.0\n')
        self.write('	deadline = 0\n')
        self.write('\n')
        
    def _gen_rewards(self):
        self.write('//Contract Reward Modifiers\n')
        self.write('	prestige = {}\n', self.prestige)
        self.write('   	targetBody = HomeWorld()\n')
        self.write('\n')
        self.write('//Contract Rewards\n')
        self.write('  	advanceFunds = {} * @KPlanes:RewardAdvanceFunds\n', self.rewardScale)
        self.write('  	rewardFunds = {} * @KPlanes:RewardFunds\n', self.rewardScale)
        self.write('  	rewardReputation = {} * @KPlanes:RewardReputation\n', self.rewardScale)
        self.write(' 	rewardScience = {} * @KPlanes:RewardScience\n', self.rewardScale)
        self.write('\n')
        self.write('//Contract Penalties\n')
        self.write('  	failureFunds = {} * @KPlanes:FailureFunds\n', self.rewardScale)
        self.write(' 	failureReputation = {} * @KPlanes:FailureReputation\n', self.rewardScale)
        self.write('\n')

    def _gen_behaviours(self):
        if self.style == "Fly":
            self._gen_behaviours_style_fly()
            
    def _gen_behaviours_style_fly(self):
        self.write('\n')
        self.write('//BEHAVIOURS TO DO WHEN CREATING CONTRACT\n')
        self.write('	BEHAVIOUR\n')
        self.write('	{{\n')
        self.write('		name = AwardExperience\n')
        self.write('		type = AwardExperience\n')
        self.write('\n')
        self.write('		parameter = WrightLand\n')
        self.write('		experience = 1\n')
        self.write('\n')
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
        if self.style == "Fly":
            self.write('		title = Your flying machine must\n')
        else:
            self.write('		title = Your aircraft must\n')
        self.write('\n')
        self.write('		define = @/craft\n')
        self.write('		dissassociateVesselsOnContractCompletion = true\n')
        self.write('\n')
        self._gen_parameters_have_crew()
        self._gen_parameters_have_wings()
        self._gen_parameters_have_only_air_breathing()
        self.write('		disableOnStateChange = false\n')
        self.write('\n')
        self.write('	}}\n')
        self.write('\n')
        if self.style == "Fly":
            self._gen_parameters_style_fly()
            self._gen_parameters_land_anywhere()
        elif self.style == "Altitude":
            self._gen_parameters_style_altitude()
            self._gen_parameters_land_at_ksc()
        self._gen_parameters_safety_check()

    def _gen_parameters_style_fly(self):
        self.write('//Contract Goals\n')
        self.write('	PARAMETER\n')
        self.write('	{{\n')
        self.write('		name = VesselParameterGroup\n')
        self.write('		type = VesselParameterGroup\n')
        self.write('		title = get airborne\n')
        self.write('\n')
        self.write('		vessel = @/craft\n')
        self.write('\n')
        self.write('		PARAMETER\n')
        self.write('		{{\n')
        self.write('			name = ReachState\n')
        self.write('			type = ReachState\n')
        self.write('\n')
        self.write('			targetBody = HomeWorld()\n')
        self.write('			situation = FLYING\n')
        self.write('			minSpeed = 15\n')
        self.write('\n')
        self.write('			completeInSequence = true\n')
        self.write('			disableOnStateChange = true\n')
        self.write('			hideChildren = true\n')
        self.write('\n')
        self.write('		}}\n')
        self.write('\n')
        self.write('		completeInSequence = true\n')
        self.write('		hideChildren = true\n')
        self.write('\n')
        self.write('	}}\n')
        self.write('\n')

    def _gen_parameters_style_altitude(self):
        self.write('//Contract Goals\n')
        self._gen_parameters_altitude_limits()
        pass

    def _gen_parameters_altitude_limits(self):
        if self.altMin == '' and self.altMax == '':
            return
        self.write('	PARAMETER\n')
        self.write('	{{\n')
        self.write('		name = VesselParameterGroup\n')
        self.write('		type = VesselParameterGroup\n')
        if self.altMin != '' and self.altMax != '':
             self.write('		title = fly between @/PrettyAltMin and @/PrettyAltMax\n')
        elif self.altMin != '':
             self.write('		title = fly up to @/PrettyAltMin\n')
        else:
             self.write('		title = fly no higher than @/PrettyAltMax\n')
        self.write('\n')
        self.write('		vessel = @/craft\n')
        self.write('\n')
        self.write('		PARAMETER\n')
        self.write('		{{\n')
        self.write('			name = ReachState\n')
        self.write('			type = ReachState\n')
        self.write('\n')
        self.write('			targetBody = Kerbin\n')
        self.write('			situation = FLYING\n')
        if self.altMin != '':
            self.write('			minAltitude = @/AltMin\n')
        if self.altMax != '':
            self.write('			maxAltitude = @/AltMax\n')
        self.write('\n')
        self.write('			disableOnStateChange = true\n')
        self.write('			hideChildren = true\n')
        self.write('			hidden = true\n')
        self.write('\n')
        self.write('		}}\n')
        self.write('\n')
        self.write('		completeInSequence = true\n')
        self.write('		disableOnStateChange = true\n')
        self.write('		hideChildren = true	\n')
        self.write('\n')
        self.write('	}}\n')
        self.write('\n')

    def _gen_parameters_have_crew(self):
        self.write('		PARAMETER\n')
        self.write('		{{\n')
        self.write('			name = HasCrew\n')
        self.write('			type = HasCrew\n')
        if self.style == "Fly":
            self.write('			title = have a volunteer\n')
            self.write('\n')            
        else:    
            self.write('			title = have a certified pilot\n')
            self.write('\n')            
            self.write('			trait = Pilot\n')            
        self.write('			minCrew = 1\n')
        self.write('\n')
        self.write('			disableOnStateChange = false\n')
        self.write('			hideChildren = true\n')
        self.write('\n')
        self.write('		}}\n')
        self.write('\n')

    def _gen_parameters_have_wings(self):
        self.write('		PARAMETER\n')
        self.write('		{{\n')
        self.write('			name = PartValidation\n')
        self.write('			type = PartValidation\n')
        self.write('			title = have wings\n')
        self.write('\n')
        self.write('			category = Aero\n')
        self.write('\n')
        self.write('			disableOnStateChange = false\n')
        self.write('			hideChildren = true\n')
        self.write('\n')
        self.write('		}}\n')
        self.write('\n')

    def _gen_parameters_have_only_air_breathing(self):
        self.write('		PARAMETER\n')
        self.write('		{{\n')
        self.write('			name = All\n')
        self.write('			type = All\n')
        self.write('			title = have an air breathing engine only\n')
        self.write('\n')
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
        self.write('\n')
        self.write('					}}\n')
        self.write('\n')
        self.write('				}}\n')
        self.write('\n')
        self.write('				disableOnStateChange = false\n')
        self.write('				hideChildren = true\n')
        self.write('\n')
        self.write('			}}\n')
        self.write('\n')
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
        self.write('\n')
        self.write('					}}\n')
        self.write('\n')
        self.write('				}}\n')
        self.write('\n')
        self.write('				disableOnStateChange = false\n')
        self.write('				hideChildren = true\n')
        self.write('\n')
        self.write('			}}\n')
        self.write('\n')
        self.write('\n')
        self.write('			PARAMETER\n')
        self.write('			{{\n')
        self.write('				name = HasResource\n')
        self.write('				type = HasResource\n')
        self.write('				title = not have any solid rocket fuel\n')
        self.write('\n')
        self.write('				resource = SolidFuel				\n')
        self.write('				minQuantity = 0.0\n')
        self.write('				maxQuantity = 0.0\n')
        self.write('\n')
        self.write('				disableOnStateChange = false\n')
        self.write('				hideChildren = true\n')
        self.write('\n')
        self.write('			}}\n')
        self.write('\n')
        self.write('			PARAMETER\n')
        self.write('			{{\n')
        self.write('				name = HasResource\n')
        self.write('				type = HasResource\n')
        self.write('				title = not have any oxidizer\n')
        self.write('\n')
        self.write('				resource = Oxidizer				\n')
        self.write('				minQuantity = 0.0\n')
        self.write('				maxQuantity = 0.0\n')
        self.write('\n')
        self.write('				disableOnStateChange = false\n')
        self.write('				hideChildren = true\n')
        self.write('\n')
        self.write('			}}\n')
        self.write('\n')
        self.write('			disableOnStateChange = false\n')
        self.write('\n')
        self.write('		}}\n')
        self.write('\n')

    def _gen_parameters_land_anywhere(self):
        self.write('//Recovery Parameter - Landing\n')
        self.write('	PARAMETER\n')
        self.write('	{{\n')
        self.write('		name = WrightLand\n')
        self.write('		type = VesselParameterGroup\n')
        self.write('		title = and then land and stop anywhere\n')
        self.write('\n')
        self.write('		vessel = @/craft\n')
        self.write('\n')
        self.write('		PARAMETER\n')
        self.write('		{{\n')
        self.write('			name = ReachState\n')
        self.write('			type = ReachState\n')
        self.write('\n')
        self.write('			targetBody = HomeWorld()\n')
        self.write('			situation = LANDED\n')
        self.write('			maxSpeed = 0.0\n')
        self.write('\n')
        self.write('			disableOnStateChange = false\n')
        self.write('			hideChildren = true\n')
        self.write('\n')
        self.write('		}}\n')
        self.write('\n')
        self.write('		completeInSequence = true\n')
        self.write('		hideChildren = true\n')
        self.write('\n')
        self.write('	}}\n')
        self.write('\n')

    def _gen_parameters_land_at_ksc(self):
        self.write('//Recovery Parameter - Landing\n')
        self.write('	PARAMETER\n')
        self.write('	{{\n')
        self.write('		name = Any\n')
        self.write('		type = Any\n')
        self.write('		title = and then land and stop\n')
        self.write('\n')
        self.write('		PARAMETER\n')
        self.write('		{{\n')
        self.write('			name = Any\n')
        self.write('			type = Any\n')
        self.write('			title = at one of the following recovery areas\n')
        self.write('\n')
        self.write('			PARAMETER\n')
        self.write('			{{\n')
        self.write('				name = VesselParameterGroup\n')
        self.write('				type = VesselParameterGroup\n')
        self.write('				title = the KSC Runway\n')
        self.write('\n')
        self.write('				vessel = @/craft\n')
        self.write('\n')
        self.write('			PARAMETER\n')
        self.write('				{{\n')
        self.write('					name = ReachState\n')
        self.write('					type = ReachState\n')
        self.write('\n')
        self.write('					targetBody = Kerbin\n')
        self.write('					biome = Runway\n')
        self.write('					situation = LANDED\n')
        self.write('					maxSpeed = 0.0\n')
        self.write('\n')
        self.write('					disableOnStateChange = false\n')
        self.write('					hideChildren = true\n')
        self.write('\n')
        self.write('				}}\n')
        self.write('\n')
        self.write('				disableOnStateChange = false\n')
        self.write('				hideChildren = true		\n')
        self.write('\n')
        self.write('			}}\n')
        self.write('\n')
        self.write('			PARAMETER\n')
        self.write('			{{\n')
        self.write('				name = VesselParameterGroup\n')
        self.write('				type = VesselParameterGroup\n')
        self.write('				title = or the Spaceplane Hangar Air Terminal\n')
        self.write('\n')
        self.write('				vessel = @/craft\n')
        self.write('\n')
        self.write('			PARAMETER\n')
        self.write('				{{\n')
        self.write('					name = ReachState\n')
        self.write('					type = ReachState\n')
        self.write('\n')
        self.write('					targetBody = Kerbin\n')
        self.write('					biome = SPH\n')
        self.write('					situation = LANDED\n')
        self.write('					maxSpeed = 0.0\n')
        self.write('\n')
        self.write('					disableOnStateChange = false\n')
        self.write('					hideChildren = true\n')
        self.write('\n')
        self.write('				}}\n')
        self.write('\n')
        self.write('				disableOnStateChange = false\n')
        self.write('				hideChildren = true		\n')
        self.write('\n')
        self.write('			}}\n')
        self.write('\n')
        self.write('			disableOnStateChange = false\n')
        self.write('\n')
        self.write('		}}\n')
        self.write('\n')
        self.write('		completeInSequence = true\n')
        self.write('		disableOnStateChange = false\n')
        self.write('\n')
        self.write('	}}\n')
        self.write('\n')        

    def _gen_parameters_safety_check(self):
        self.write('//Recovery Parameter - Craft & Kerbal Safety Check\n')
        self.write('	PARAMETER\n')
        self.write('	{{\n')
        self.write('		name = All\n')
        self.write('		type = All\n')
        self.write('		title = safely\n')
        self.write('\n')
        self.write('		PARAMETER\n')
        self.write('		{{\n')
        self.write('			name = VesselNotDestroyed\n')
        self.write('			type = VesselNotDestroyed\n')
        if self.style == 'Fly':
            self.write('			title = without destroying your flying machine\n')
        else:
            self.write('			title = without destroying your aircraft\n')
        self.write('\n')
        self.write('			vessel = @/craft\n')
        self.write('\n')
        self.write('		}}\n')
        self.write('\n')
        self.write('		PARAMETER\n')
        self.write('		{{\n')
        self.write('			name = KerbalDeaths\n')
        self.write('			type = KerbalDeaths\n')
        self.write('			title = or killing anyone\n')
        self.write('\n')
        self.write('			vessel = @/craft\n')
        self.write('\n')
        self.write('		}}\n')
        self.write('\n')
        self.write('		completeInSequence = true\n')
        self.write('		disableOnStateChange = true\n')
        self.write('\n')
        self.write('	}}\n')
        self.write('\n')
        
    def _gen_end(self):
        self.write('}}\n')
        
class ContractGroup:
    def __init__(self, table, title):
        self.table = table
        self.title = title
        self.name = 'KPlanes_{}'.format(self.title)
        self.contract_types = []

    def add_type(self, counter, name, data):
        new_type = ContractType(self, counter, name, data)
        self.contract_types.append(new_type)

    def find_type(self, counter):
        for ct in self.contract_types:
            if int(ct.counter) == int(counter):
                return ct
        error("Cannot find contract {} in group {}", counter, self.title)

    def generate(self):
        for ct in self.contract_types:
            ct.generate()

class Localization:
    def __init__(self):
        self.entries = {}
        self.read()

    def make_key(self, ct, field):
        prefix = ct.name.replace('-', '_')
        return "#autoLOC_KPlanes_{}_{}".format(prefix, field)

    def add(self, key, value):
        self.entries[key] = value
        
    def get(self, key):
        if key not in self.entries:
            error("No localization key {}", key)
        return self.entries[key]
    
    def read(self):
        with open("{}/Localization/en-us.cfg".format(DEST)) as locfile:
            for line in locfile.readlines():
                m = re.search(r'(#autoLOC_KPlanes_[a-zA-Z0-9_]*)\s*=\s*(.*)$', line)
                if not m:
                    continue
                key = m.group(1)
                value = m.group(2)
                self.add(key, value)
        for key in self.entries.keys():
            debug('Loc: {} = {}', key, self.get(key))
    
class ContractTable:
    def __init__(self):
        self.contract_groups = {}
        self.localization = Localization()
        self.read()
        self.localization.read()

    def find_group(self, group_title):
        if not group_title in self.contract_groups:
            error("Cannot find group {}", group_title)
        return self.contract_groups[group_title]
        
    def make_group(self, group_title):
        if group_title in self.contract_groups:
            return self.contract_groups[group_title]
        new_group = ContractGroup(self, group_title)
        self.contract_groups[group_title] = new_group
        return new_group

    def read(self):
        with open("{}/ContractTable.csv".format(ROOT), newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            skip = True
            for row in reader:
                if skip:
                    skip = False
                    continue
                group_title = row[0]
                counter = row[2]
                name = row[4]
                group = self.make_group(group_title)
                group.add_type(counter, name, row)

    def generate(self):
        for group_title in self.contract_groups.keys():
            group = self.find_group(group_title)
            group.generate()

# --------------------------------------------------------------------------------

table = ContractTable()
table.generate()
