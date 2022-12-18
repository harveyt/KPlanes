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
DIST_TOLERANCE = 500.0 # 500m tolerance for distances, need to be at least X plus this distance for waypoint 
MOUNTAIN_BIOME = 'Mountains' # Blank if mountain biome not required
MISSING_LOC = False

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
        self.counter = int(counter)
        self.suffix = re.sub(r'[- ]', '', name)
        self.data = data
        self.name = "{}-{:03d}-{}".format(self.group.title, self.counter, self.suffix)
        self.title = name
        self.output_path = "{}/Groups/{}/{:03d}-{}.cfg".format(DEST, self.group.title, self.counter, self.suffix)
        self.out = sys.stdout
        self.indent = ''
        self.agent = self.agent_name_from_data(data[1])
        self.craft = "KPlanesCraft_{}_{:03d}".format(self.group.title, self.counter)
        self.description = ""
        self.synopsis = ""
        self.notes = ""
        self.completedMessage = ""
        self.gap_equiv = data[4]
        self.requires = self.requires_from_data(data[5])
        self.prestige = self.prestige_from_data(data[6])
        self.funds = data[7]
        self.rep = data[8]
        self.science = data[9]
        self.style = data[10]
        self.style_param = data[11]
        self.altMin = data[12]
        self.altMax = data[13]
        self.speed = data[14]
        self.distance = data[15]
        self.payload = data[16]
        self.jet = data[17]
        self.rocket = data[18]
        self.staging = data[19]
        self.airLaunch = data[20]
        self.landNearKSC = data[21]

    def agent_name_from_data(self, data):
        if data == "Wright":
            return "Wright Aeronautical"
        elif data == "SSI":
            return "SSI Aerospace"
        return data

    def requires_from_data(self, data):
        if data == '':
            return []
        requires_list = []
        requires_parts = data.split(',')
        debug("requires: data={} parts={}", data, requires_parts)
        for requires in requires_parts:
            requires_type = self.table.find_type(requires)
            requires_list.append(requires_type)
        return requires_list

    def prestige_from_data(self, data):
        prestige = "Trivial"
        prestige_stars = data
        if prestige_stars == "**":
            prestige = "Significant"
        elif prestige_stars == "***":
            prestige = "Exceptional"
        return prestige

    def write_indent(self, indent):
        self.indent = indent
        
    def write(self, fmt, *a):
        self.out.write(self.indent)
        self.out.write(fmt.format(*a))

    def localize(self, field):
        key = self.localization.make_key(self, field)
        if not self.localization.has(key):
            global MISSING_LOC            
            if not MISSING_LOC:
                sys.stdout.write('--------------------------------------------------------------------------------\n')
                sys.stdout.write('Missing localizations:\n')
                sys.stdout.write('\n')
                MISSING_LOC = True
            sys.stdout.write('		{} = XXX\n'.format(key))
        if REPLACE_AUTOLOC:
            value = self.localization.get(key)
        else:
            value = key
        return value

    def value_from_ident(self, ident, scale):
        if ident == '':
            return ''
        if ident.replace('.','',1).isdigit():
            value = ident
        else:
            value = "@KPlanes:{}".format(ident)
        return "Round({} * {})".format(value, scale)

    def desc_from_ident(self, ident):
        if ident == '':
            return ''
        if ident.replace('.','',1).isdigit():
            return ''
        # Alpha1Charlie -> ['Alpha', '1', 'Charlie'] -> 'Alpha 1 Charlie'
        desc = " ".join(re.findall(r'[A-Z0-9][a-z0-9]*', ident))
        return " ({})".format(desc)
        
    # Speed is in m/s
    def speed_value(self, ident):
        return self.value_from_ident(ident, "1.0")

    def speed_desc(self, ident):
        return self.desc_from_ident(ident)
    
    # Altitude is in km
    def altitude_value(self, ident):
        return self.value_from_ident(ident, "1000.0")

    def altitude_desc(self, ident):
        return self.desc_from_ident(ident)
    
    # Distance is in km
    def distance_value(self, ident):
        return self.value_from_ident(ident, "1000.0")

    def distance_desc(self, ident):
        return self.desc_from_ident(ident)
    
    def generate(self):
        if self.group.title != "Start" and self.group.title != "Early":
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
        if self.gap_equiv != "":
            self.write('// Copied and modified from GAP/{}.cfg\n', self.gap_equiv)
            self.write('//\n')
        self.write('// **** WARNING: DO NOT EDIT THIS FILE! Change ContractTable.csv and/or ContractGen.py ****\n')
        self.write('//\n')
        self.write('\n')
        
    def _gen_begin(self):
        self.write('CONTRACT_TYPE\n')
        self.write('{{\n')
        self.write('\n')
        self.write('	sortKey = a{:03d}\n', self.counter)
        self.write('\n')

    def _gen_requirements(self):
        self.write('//REQUIREMENTS FOR CONTRACT TO APPEAR\n')
        self.write('\n')
        self._gen_requirements_previous()
        if self.style == "Fly":
            self._gen_requirements_style_fly()
        self.write('\n')

    def _gen_requirements_previous(self):
        for req in self.requires:
            self.write('	REQUIREMENT\n')
            self.write('	{{\n')
            self.write('		name = CompleteContract\n')
            self.write('		type = CompleteContract\n')
            self.write('\n')
            self.write('		contractType = {}\n', req.name)
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
        if self.style == 'Altitude' or self.style == 'Speed' or self.style == 'Distance':
            self._gen_data_value('AltMin', self.altitude_desc(self.altMin), self.altitude_value(self.altMin), "#,#", 1000, "km", 'Minimum altitude')
            self._gen_data_value('AltMax', self.altitude_desc(self.altMax), self.altitude_value(self.altMax), "#,#", 1000, "km", 'Maximum altitude')
            self._gen_data_range('Alt', 'altitude', 'AltMin', self.altMin, 'AltMax', self.altMax)
        if self.style == 'Speed':
            self._gen_data_value('Speed', self.speed_desc(self.speed), self.speed_value(self.speed), "#,#", 1, "m/s", 'Speed')
            self._gen_data_range('Speed', 'speed', 'Speed', self.speed, '', '')
        if self.style == 'Distance':
            self._gen_data_value('Distance', self.distance_desc(self.distance), self.distance_value(self.distance), "#,#", 1000, "km", 'Distance')
            self._gen_data_range('Distance', 'distance', 'Distance', self.distance, '', '')
            if self.is_distance_marker():
                half_distance = '{} / 2.0'.format(self.distance_value(self.distance))
                self._gen_data_value('MarkerDistance', '', half_distance, "#,#", 1000, "km", 'Distance')
        if self.style == 'Land' and self.style_param == 'Mountain':
            self._gen_data_value('AltMin', self.altitude_desc(self.altMin), self.altitude_value(self.altMin), "#,#", 1000, "km", 'Minimum altitude')
            self._gen_data_range('Alt', 'altitude', 'AltMin', self.altMin, '', '')
        
    def _gen_data_value(self, name, desc, value, fmt, divisor, units, title):
        if value == '':
            return
        self.write('	DATA\n')
        self.write('	{{\n')
        self.write('		type = double\n')
        self.write('		{} = {}\n', name, value)
        self.write('		Scaled{} = Round(@/{} / {}.0)\n', name, name, divisor)
        self.write('		title = {}\n', title)
        self.write('	}}\n')
        self.write('\n')
        self.write('	DATA\n')
        self.write('	{{\n')
        self.write('		type = string\n')
        self.write('		Desc{} = "{}"\n', name, desc)
        self.write('		title = {}\n', title)
        self.write('	}}\n')
        self.write('\n')
        self.write('	DATA\n')
        self.write('	{{\n')
        self.write('		type = string\n')
        self.write('		Pretty{} = @/Scaled{}.ToString("{} {}")\n', name, name, fmt, units)
        self.write('		title = {}\n', title)        
        self.write('	}}\n')
        self.write('\n')

    def _gen_data_range(self, name, style, minName, minIdent, maxName, maxIdent):
        if minIdent == '' and maxIdent == '':
            return
        self.write('	DATA\n')
        self.write('	{{\n')
        self.write('		type = string\n')
        if minIdent != '' and maxIdent != '':
            self.write('		Pretty{}Range = {} between @/Pretty{}@/Desc{} and @/Pretty{}@/Desc{}\n', name, style, minName, minName, maxName, maxName)
        elif  minIdent != '' and maxIdent == '':
            self.write('		Pretty{}Range = {} of at least @/Pretty{}@/Desc{}\n', name, style, minName, minName)
        else:
            self.write('		Pretty{}Range = {} of at most @/Pretty{}@/Desc{}\n', name, style, maxName, maxName)
        self.write('		title = Range for {} \n', style)        
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
        self.write('	maxCompletions = 1\n')
        self.write('	maxSimultaneous = 1\n')
        self.write('//	weight = 100.0\n')
        self.write('\n')
        self.write('	autoAccept = false\n')
        self.write('	declinable = true\n')
        self.write('	cancellable = true\n')
        self.write('\n')
        # Never expire, and no deadline. What is the point of expiration and deadlines anyway?
        self.write('	minExpiry = 0.0\n')
        self.write('	maxExpiry = 0.0\n')
        self.write('	deadline = 0\n')
        self.write('\n')
        
    def _gen_rewards(self):
        self.write('//Contract Reward Modifiers\n')
        self.write('	prestige = {}\n', self.prestige)
        self.write('	targetBody = HomeWorld()\n')
        self.write('\n')
        self.write('//Contract Rewards\n')
        self.write('	advanceFunds = {} * @KPlanes:RewardAdvanceFunds\n', self.funds)
        self.write('	rewardFunds = {} * @KPlanes:RewardFunds\n', self.funds)
        self.write('	rewardReputation = {} * @KPlanes:RewardReputation\n', self.rep)
        self.write('	rewardScience = {} * @KPlanes:RewardScience\n', self.science)
        self.write('\n')
        self.write('//Contract Penalties\n')
        self.write('	failureFunds = {} * @KPlanes:FailureFunds\n', self.funds)
        self.write('	failureReputation = {} * @KPlanes:FailureReputation\n', self.rep)
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

    def is_distance_marker(self):
        if self.distance == 'Polar' or self.distance.startswith('Circum'):
            return False
        return True

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
        elif self.style == "Land" and self.style_param == "Splashed":
            self.write('		title = Your seaplane must\n')
        else:
            self.write('		title = Your aircraft must\n')
        self.write('\n')
        self.write('		define = @/craft\n')
        self.write('		dissassociateVesselsOnContractCompletion = true\n')
        self.write('\n')
        self._gen_parameters_have_crew()
        self._gen_parameters_have_wings()
        self._gen_parameters_land_reachstate()
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
        elif self.style == "Speed":
            self._gen_parameters_style_speed()
            self._gen_parameters_land_at_ksc()
        elif self.style == "Land":
            self._gen_parameters_style_land()
            if self.style_param == "Helipads":
                self._gen_parameters_land_at_ksc_helipads()
            else:
                self._gen_parameters_land_at_ksc()
        elif self.style == "Distance":
            self._gen_parameters_style_distance()
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
        self._gen_parameters_altitude_limits('true')
        pass

    def _gen_parameters_style_speed(self):
        self.write('//Contract Goals\n')
        self.write('	PARAMETER\n')
        self.write('	{{\n')
        self.write('		name = All\n')
        self.write('		type = All\n')
        self.write('		title = achieve a maximum airspeed of @/PrettySpeed\n')
        self.write('\n')
        self._gen_parameters_altitude_limits('false', '	')
        self._gen_parameters_speed_limits('	')
        self._gen_parameters_vert_speed_limits('	')
        self._gen_parameters_hold_duration('	')
        self.write('	\n')
        self.write('		completeInSequence = true\n')
        self.write('		disableOnStateChange = true\n')
        self.write('	\n')
        self.write('	}}\n')
        self.write('\n')

    def _gen_parameters_style_land(self):
        if self.style_param == 'Splashed':
            self.write('//Land on Water\n')
            self.write('	PARAMETER\n')
            self.write('	{{\n')
            self.write('		name = VesselParameterGroup\n')
            self.write('		type = VesselParameterGroup\n')
            self.write('		title = land on water\n')
            self.write('\n')
            self.write('		vessel = @/craft\n')
            self.write('\n')
            self.write('		PARAMETER\n')
            self.write('		{{\n')
            self.write('			name = ReachState\n')
            self.write('			type = ReachState\n')
            self.write('\n')
            self.write('			situation = SPLASHED\n')
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
            self.write('	PARAMETER\n')
            self.write('	{{\n')
            self.write('		name = VesselParameterGroup\n')
            self.write('		type = VesselParameterGroup\n')
            self.write('		title = and slow to 3.0 m/s or less\n')
            self.write('\n')
            self.write('		vessel = @/craft\n')
            self.write('\n')
            self.write('		PARAMETER\n')
            self.write('		{{\n')
            self.write('			name = ReachState\n')
            self.write('			type = ReachState\n')
            self.write('\n')
            self.write('			situation = SPLASHED\n')
            self.write('			maxSpeed = 3.0\n')
            self.write('\n')
            self.write('			completeInSequence = true\n')
            self.write('			disableOnStateChange = true\n')
            self.write('			hideChildren = true\n')
            self.write('			hidden = true\n')
            self.write('\n')
            self.write('		}}\n')
            self.write('\n')
            self.write('		completeInSequence = true\n')
            self.write('		hideChildren = true\n')
            self.write('\n')
            self.write('	}}\n')
            self.write('\n')
            self.write('//Take Off From Water\n')
            self.write('	PARAMETER\n')
            self.write('	{{\n')
            self.write('		name = VesselParameterGroup\n')
            self.write('		type = VesselParameterGroup\n')
            self.write('		title = and then go at least 20.0 m/s on water\n')
            self.write('\n')
            self.write('		vessel = @/craft\n')
            self.write('\n')
            self.write('		PARAMETER\n')
            self.write('		{{\n')
            self.write('			name = ReachState\n')
            self.write('			type = ReachState\n')
            self.write('\n')
            self.write('			situation = SPLASHED\n')
            self.write('			minSpeed = 20.0\n')
            self.write('\n')
            self.write('			completeInSequence = true\n')
            self.write('			disableOnStateChange = false\n')
            self.write('			hideChildren = true\n')
            self.write('			hidden = true\n')
            self.write('\n')
            self.write('		}}\n')
            self.write('\n')
            self.write('		completeInSequence = true\n')
            self.write('		disableOnStateChange = true\n')
            self.write('		hideChildren = true\n')
            self.write('\n')
            self.write('	}}\n')
            self.write('\n')
            self.write('	PARAMETER\n')
            self.write('	{{\n')
            self.write('		name = VesselParameterGroup\n')
            self.write('		type = VesselParameterGroup\n')
            self.write('		title = and then get airborne\n')
            self.write('\n')
            self.write('		vessel = @/craft\n')
            self.write('\n')
            self.write('		PARAMETER\n')
            self.write('		{{\n')
            self.write('			name = ReachState\n')
            self.write('			type = ReachState\n')
            self.write('\n')
            self.write('			situation = FLYING\n')
            self.write('\n')
            self.write('			completeInSequence = true\n')
            self.write('			disableOnStateChange = false\n')
            self.write('			hideChildren = true\n')
            self.write('			hidden = true\n')
            self.write('\n')
            self.write('		}}\n')
            self.write('\n')
            self.write('		completeInSequence = true\n')
            self.write('		disableOnStateChange = true\n')
            self.write('		hideChildren = true\n')
            self.write('\n')
            self.write('	}}\n')

    def _gen_parameters_style_distance(self):
        if self.is_distance_marker():
            self._gen_parameters_style_distance_marker()
        else:
            self._gen_parameters_style_distance_waypoints()
            
    def _gen_parameters_style_distance_marker(self):
        self.write('//Contract Behaviour (Distance Marker)\n')
        # Data for waypoints, depending on what style
        self.write('	DATA\n')
        self.write('	{{\n')
        self.write('		type = double\n')
        if self.distance == 'Polar':
            # Marker1 == Half-way
            marker1Lat = '(90.0 - KSC().Location().Latitude()) / 2.0 + KSC().Location().Latitude()'
            marker1Lon = 'KSC().Location().Longitude()'
            # Marker2 == North Pole (could choose South Pole randomly, but we do not)
            marker2Lat = '90.0'
            marker2Lon = 'KSC().Location().Longitude()'
            # Marker3 == same as Marker1, so come back the same way
            marker3Lat = '@/Marker1Lat'
            marker3Lon = '@/Marker1Lon'
        elif self.distance == 'CircumPolar':
            # Marker1 == North Pole (could choose South Pole randomly, but we do not)
            marker1Lat = '90.0'
            marker1Lon = 'KSC().Location().Longitude()'
            # Marker2 == Opposite side of world to KSC (so you have to go all the way round)
            marker2Lat = 'KSC().Location().Latitude()'
            marker2Lon = 'KSC().Location().Longitude() >= 0.0 ? KSC().Location().Longitude() - 180.0 : KSC().Location().Longitude() + 180.0'
            # Marker3 == South Pole
            marker3Lat = '-90.0'
            marker3Lon = 'KSC().Location().Longitude()'
        else:
            # Marker1 == -90 west of KSC on equator
            marker1Lat = '0.0'
            marker1Lon = 'KSC().Location().Longitude() >= 90.0 ? KSC().Location().Longitude() - 90.0 : KSC().Location().Longitude() + 90.0'
            # Marker2 == opposite side of world on equator
            marker2Lat = '0.0'
            marker2Lon = 'KSC().Location().Longitude() >= 0.0 ? KSC().Location().Longitude() - 180.0 : KSC().Location().Longitude() + 180.0'
            # Marker3 == +90 east of KSC
            marker3Lat = '0.0'
            marker3Lon = 'KSC().Location().Longitude() <= 90.0 ? KSC().Location().Longitude() + 90.0 : KSC().Location().Longitude() - 90.0'
        self.write('		Marker1Lat = {}\n', marker1Lat)
        self.write('		Marker1Lon = {}\n', marker1Lon)
        self.write('		Marker2Lat = {}\n', marker2Lat)
        self.write('		Marker2Lon = {}\n', marker2Lon)
        self.write('		Marker3Lat = {}\n', marker3Lat)
        self.write('		Marker3Lon = {}\n', marker3Lon)
        self.write('		title = Marker Locations\n')
        self.write('	}}\n')
        self.write('\n')
        # Waypoints and visiting each in order
        self.write('BEHAVIOUR\n')
        self.write('{{\n')
        self.write('    name = WaypointGenerator\n')
        self.write('    type = WaypointGenerator\n')
        self.write('\n')
        self.write('    PQS_CITY\n')
        self.write('    {{\n')
        self.write('        name = KSC\n')
        self.write('\n')
        self.write('        targetBody = HomeWorld()\n')
        self.write('        hidden = true\n')
        self.write('        icon = ksc\n')
        self.write('        pqsCity = KSC\n')
        self.write('    }}\n')
        self.write('\n')
        self.write('    RANDOM_WAYPOINT_NEAR\n')
        self.write('    {{\n')
        self.write('        name = Distance Marker\n')
        self.write('\n')
        self.write('        targetBody = HomeWorld()\n')
        self.write('        count = 1\n')
        self.write('        icon = custom\n')
        self.write('        altitude = 0.0\n')
        self.write('        waterAllowed = true\n')
        self.write('	    nearIndex = 0\n')
        self.write('        minDistance = @/MarkerDistance\n')
        self.write('        maxDistance = @/MarkerDistance\n')
        self.write('    }}\n')
        self.write('}}\n')
        self.write('\n')
        self.write('//Contract Goals\n')
        self._gen_parameters_altitude_limits('false', '	')
        self.write('	PARAMETER\n')
        self.write('	{{\n')
        self.write('		name = VesselParameterGroup\n')
        self.write('		type = VesselParameterGroup\n')
        self.write('		title = fly to waypoint "Distance Marker" which is @/PrettyMarkerDistance from KSC\n')
        self.write('\n')
        self.write('		vessel = @/craft\n')
        self.write('\n')
        self.write('		PARAMETER\n')
        self.write('		{{\n')
        self.write('			name = VisitWaypoint\n')
        self.write('			type = VisitWaypoint\n')
        self.write('\n')
        self.write('			index = 1\n')
        self.write('			horizontalDistance = {}\n', DIST_TOLERANCE)
        self.write('			hideOnCompletion = true\n')
        self.write('			showMessages = true\n')
        self.write('\n')
        self.write('			disableOnStateChange = true\n')
        self.write('			hideChildren = true\n')
        self.write('			hidden = true\n')
        self.write('\n')
        self.write('		}}\n')
        self.write('\n')
        self.write('		completeInSequence = true\n')
        self.write('		disableOnStateChange = true\n')
        self.write('		hideChildren = true\n')
        self.write('\n')
        self.write('	}}\n')
        self.write('\n')

    def _gen_parameters_style_distance_waypoints(self):
        self.write('//Contract Behaviour (Waypoints)\n')
        self.write('BEHAVIOUR\n')
        self.write('{{\n')
        self.write('    name = WaypointGenerator\n')
        self.write('    type = WaypointGenerator\n')
        self.write('\n')
        self.write('    PQS_CITY\n')
        self.write('    {{\n')
        self.write('        name = KSC\n')
        self.write('\n')
        self.write('        targetBody = HomeWorld()\n')
        self.write('        hidden = true\n')
        self.write('        icon = ksc\n')
        self.write('        pqsCity = KSC\n')
        self.write('    }}\n')
        self.write('\n')
        self.write('	WAYPOINT\n')
        self.write('	{{\n')
        self.write('		name = Marker 1\n')
        self.write('\n')
        self.write('		targetBody = HomeWorld()\n')
        self.write('		icon = custom\n')
        self.write('		altitude = 0.0\n')
        self.write('		latitude = @/Marker1Lat\n')
        self.write('		latitude = @/Marker1Lon\n')
        self.write('	}}\n')
        self.write('\n')
        self.write('	WAYPOINT\n')
        self.write('	{{\n')
        self.write('		name = Marker 2\n')
        self.write('		parameter = Marker1Reached\n')
        self.write('\n')
        self.write('		targetBody = HomeWorld()\n')
        self.write('		icon = custom\n')
        self.write('		altitude = 0.0\n')
        self.write('		latitude = @/Marker2Lat\n')
        self.write('		latitude = @/Marker2Lon\n')
        self.write('	}}\n')
        self.write('\n')
        self.write('	WAYPOINT\n')
        self.write('	{{\n')
        self.write('		name = Marker 3\n')
        self.write('		parameter = Marker2Reached\n')
        self.write('\n')
        self.write('		targetBody = HomeWorld()\n')
        self.write('		icon = custom\n')
        self.write('		altitude = 0.0\n')
        self.write('		latitude = @/Marker3Lat\n')
        self.write('		latitude = @/Marker3Lon\n')
        self.write('	}}\n')
        self.write('}}\n')
        self.write('\n')
        self.write('//Contract Goals\n')
        self._gen_parameters_altitude_limits('false', '	')
        self.write('	PARAMETER\n')
        self.write('	{{\n')
        self.write('		name = VesselParameterGroup\n')
        self.write('		type = VesselParameterGroup\n')
        self.write('		title = fly to Marker 1, 2 and 3 in sequence, then return to KSC\n')
        self.write('\n')
        self.write('		vessel = @/craft\n')
        self.write('\n')
        self.write('		PARAMETER\n')
        self.write('		{{\n')
        self.write('			name = Marker1Reached\n')
        self.write('			type = VisitWaypoint\n')
        self.write('\n')
        self.write('			index = 1\n')
        self.write('			horizontalDistance = {}\n', DIST_TOLERANCE)
        self.write('			hideOnCompletion = true\n')
        self.write('			showMessages = true\n')
        self.write('\n')
        self.write('			disableOnStateChange = true\n')
        self.write('			hideChildren = true\n')
        self.write('			hidden = true\n')
        self.write('\n')
        self.write('		}}\n')
        self.write('\n')
        self.write('		PARAMETER\n')
        self.write('		{{\n')
        self.write('			name = Marker2Reached\n')
        self.write('			type = VisitWaypoint\n')
        self.write('\n')
        self.write('			index = 2\n')
        self.write('			horizontalDistance = {}\n', DIST_TOLERANCE)
        self.write('			hideOnCompletion = true\n')
        self.write('			showMessages = true\n')
        self.write('\n')
        self.write('			disableOnStateChange = true\n')
        self.write('			hideChildren = true\n')
        self.write('			hidden = true\n')
        self.write('\n')
        self.write('		}}\n')
        self.write('\n')
        self.write('		PARAMETER\n')
        self.write('		{{\n')
        self.write('			name = Marker3Reached\n')
        self.write('			type = VisitWaypoint\n')
        self.write('\n')
        self.write('			index = 3\n')
        self.write('			horizontalDistance = {}\n', DIST_TOLERANCE)
        self.write('			hideOnCompletion = true\n')
        self.write('			showMessages = true\n')
        self.write('\n')
        self.write('			disableOnStateChange = true\n')
        self.write('			hideChildren = true\n')
        self.write('			hidden = true\n')
        self.write('\n')
        self.write('		}}\n')
        self.write('\n')
        self.write('		completeInSequence = true\n')
        self.write('		disableOnStateChange = true\n')
        self.write('		hideChildren = true\n')
        self.write('\n')
        self.write('	}}\n')
        self.write('\n')
        
    def _gen_parameters_altitude_limits(self, in_seq='true', indent=''):
        if self.altMin == '' and self.altMax == '':
            return
        self.write_indent(indent)
        self.write('	PARAMETER\n')
        self.write('	{{\n')
        self.write('		name = VesselParameterGroup\n')
        self.write('		type = VesselParameterGroup\n')
        self.write('		title = fly at an @/PrettyAltRange\n')
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
        if self.altMin != '':
            self.write('			minAltitude = @/AltMin\n')
        if self.altMax != '':
            self.write('			maxAltitude = @/AltMax\n')
        self.write('\n')
        self.write('			disableOnStateChange = {}\n', in_seq)
        self.write('			hideChildren = true\n')
        self.write('			hidden = true\n')
        self.write('\n')
        self.write('		}}\n')
        self.write('\n')
        self.write('		completeInSequence = {}\n', in_seq)
        self.write('		disableOnStateChange = {}\n', in_seq)
        self.write('		hideChildren = true\n')
        self.write('\n')
        self.write('	}}\n')
        self.write('\n')
        self.write_indent('')

    def _gen_parameters_speed_limits(self, indent=''):
        if self.speed == '':
            return
        self.write_indent(indent)
        self.write('	PARAMETER\n')
        self.write('	{{\n')
        self.write('		name = VesselParameterGroup\n')
        self.write('		type = VesselParameterGroup\n')
        self.write('		title = fly faster than @/PrettySpeed\n')
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
        self.write('			minSpeed = @/Speed\n')
        self.write('\n')
        self.write('			disableOnStateChange = false\n')
        self.write('			hideChildren = true\n')
        self.write('			hidden = true\n')
        self.write('\n')
        self.write('		}}\n')
        self.write('\n')
        self.write('		completeInSequence = false\n')
        self.write('		disableOnStateChange = false\n')
        self.write('		hideChildren = true\n')
        self.write('\n')
        self.write('	}}\n')
        self.write('\n')
        self.write_indent('')
        
    def _gen_parameters_vert_speed_limits(self, indent=''):
        self.write_indent(indent)
        self.write('	PARAMETER\n')
        self.write('	{{\n')
        self.write('		name = VesselParameterGroup\n')
        self.write('		type = VesselParameterGroup\n')
        self.write('		title = with less than 10 m/s of vertical speed\n')
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
        self.write('			minRateOfClimb = -10\n')
        self.write('			maxRateOfClimb = 10\n')
        self.write('\n')
        self.write('			disableOnStateChange = false\n')
        self.write('			hideChildren = true\n')
        self.write('			hidden = true\n')
        self.write('\n')
        self.write('		}}\n')
        self.write('\n')
        self.write('		completeInSequence = true\n')
        self.write('		disableOnStateChange = false\n')
        self.write('		hideChildren = true	\n')
        self.write('\n')
        self.write('	}}\n')
        self.write('\n')
        self.write_indent('')

    def _gen_parameters_hold_duration(self, indent=''):
        self.write_indent(indent)
        self.write('	PARAMETER\n')
        self.write('	{{\n')
        self.write('		name = Duration\n')
        self.write('		type = Duration\n')
        self.write('\n')
        self.write('		duration = 5s\n')
        self.write('		preWaitText = and hold for:\n')
        self.write('		waitingText = and hold for: \n')
        self.write('		completionText = You did it!\n')
        self.write('\n')
        self.write('		completeInSequence = true\n')
        self.write('		disableOnStateChange = false\n')
        self.write('\n')
        self.write('	}}\n')
        self.write('\n')
        self.write_indent('')

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

    def _gen_parameters_land_reachstate(self):
        if self.style != "Land":
            return
        if self.style_param == "Splashed":
            self.write('		PARAMETER\n')
            self.write('		{{\n')
            self.write('			name = ReachState\n')
            self.write('			type = ReachState\n')
            self.write('\n')
            self.write('			situation = SPLASHED\n')
            self.write('\n')
            self.write('			disableOnStateChange = true\n')
            self.write('			hideChildren = true\n')
            self.write('			hidden = true\n')
            self.write('\n')
            self.write('		}}\n')
            self.write('\n')
        elif self.style_param == "Mountain":
            self.write('		PARAMETER\n')
            self.write('		{{\n')
            self.write('			name = ReachState\n')
            self.write('			type = ReachState\n')
            self.write('\n')
            self.write('			targetBody = HomeWorld()\n')
            if MOUNTAIN_BIOME != '':
                self.write('			biome = {}\n', MOUNTAIN_BIOME)
            self.write('			minAltitude = @/AltMin\n')
            self.write('			situation = LANDED\n')
            self.write('			maxSpeed = 0.0\n')
            self.write('\n')
            self.write('			disableOnStateChange = true\n')
            self.write('			hideChildren = true\n')
            self.write('			hidden = true\n')
            self.write('\n')
            self.write('		}}\n')
            self.write('\n')

    def _gen_parameters_have_only_air_breathing(self):
        self.write('		PARAMETER\n')
        self.write('		{{\n')
        self.write('			name = All\n')
        self.write('			type = All\n')
        if self.rocket == 'N':
            self.write('			title = have air breathing engines only\n')
        else:
            self.write('			title = have air breathing engines and/or rockets\n')
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
        if self.rocket == 'N':
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
            self.write('				resource = SolidFuel\n')
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
            self.write('				resource = Oxidizer\n')
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
        self.write('					targetBody = HomeWorld()\n')
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
        self.write('					targetBody = HomeWorld()\n')
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
        
    def _gen_parameters_land_at_ksc_helipads(self):
        self.write('//Recovery Parameter - Landing\n')
        self.write('	PARAMETER\n')
        self.write('	{{\n')
        self.write('		name = GAPLand\n')
        self.write('		type = Any\n')
        self.write('		title = land on a helipad\n')
        self.write('\n')
        self.write('		PARAMETER\n')
        self.write('		{{\n')
        self.write('			name = Any\n')
        self.write('			type = Any\n')
        self.write('			title = at either\n')
        self.write('\n')
        self.write('			PARAMETER\n')
        self.write('			{{\n')
        self.write('				name = VesselParameterGroup\n')
        self.write('				type = VesselParameterGroup\n')
        self.write('				title = the Vehicle Assembly Building Helipad\n')
        self.write('\n')
        self.write('				vessel = @/craft\n')
        self.write('\n')
        self.write('			PARAMETER\n')
        self.write('				{{\n')
        self.write('					name = ReachState\n')
        self.write('					type = ReachState\n')
        self.write('\n')
        self.write('					targetBody = HomeWorld()\n')
        self.write('					biome = VAB Main Building\n')
        self.write('					situation = LANDED\n')
        self.write('					maxSpeed = 0.0\n')
        self.write('\n')
        self.write('					disableOnStateChange = false\n')
        self.write('					hideChildren = true\n')
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
        self.write('				name = VesselParameterGroup\n')
        self.write('				type = VesselParameterGroup\n')
        self.write('				title = or the Administration Building Helipad\n')
        self.write('\n')
        self.write('				vessel = @/craft\n')
        self.write('\n')
        self.write('				PARAMETER\n')
        self.write('				{{\n')
        self.write('					name = ReachState\n')
        self.write('					type = ReachState\n')
        self.write('\n')
        self.write('					targetBody = HomeWorld()\n')
        self.write('					biome = Administration\n')
        self.write('					situation = LANDED\n')
        self.write('					maxSpeed = 0.0\n')
        self.write('\n')
        self.write('					disableOnStateChange = false\n')
        self.write('					hideChildren = true\n')
        self.write('\n')
        self.write('				}}\n')
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

    def find_type(self, title, allow_none=False):
        for ct in self.contract_types:
            if ct.title == title:
                return ct
        if allow_none:
            return None
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

    def has(self, key):
        return key in self.entries
        
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

    def find_type(self, type_title):
        for group_title in self.contract_groups:
            group = self.find_group(group_title)
            ct = group.find_type(type_title, True)
            if ct is not None:
                return ct
        error("Cannot find contract {} in any groups", type_title)
        
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
                name = row[3]
                group = self.make_group(group_title)
                group.add_type(counter, name, row)

    def generate(self):
        for group_title in self.contract_groups.keys():
            group = self.find_group(group_title)
            group.generate()

# --------------------------------------------------------------------------------

table = ContractTable()
table.generate()
