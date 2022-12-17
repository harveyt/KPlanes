# Contract Pack: K-Planes

By: [610yeslovely][kspf:610yesnolovely]

The K-Planes contract pack adds various contracts to encourage and reward building of planes from
very early stages, through X-plane style rocket planes, to SSTO (single-stage to orbit) planes.

## Origins

This mod is inspired by and indeed uses some assets, configuration from the original [GAP][url:GAP]
mod, which is also a [MIT][url:MITLicense] license.

The original author of [GAP][url:GAP] [inigma][kspf:inigma] gave blanket permission to use anything
and everything from GAP [on the KSP Forums][kspf:inigmaPermission].

## Purpose

This pack is planet pack agnostic and tech tree agnostic, but the description assumes either Stock,
semi-Stock (2.5x or 2.7x scale like JNSQ or KSRSS), or Earth-scale planets (RSS/RO/RP-1). The pack
can also be used alongside [GAP][url:GAP] or deriviatives and does not need them for any shared
assets, though some of the early contracts are almost the same as the milestones from [GAP][url:GAP]
(because they were copied and made planet agnostic).

Initially you will find contracts to build your first powered aircraft, then several contracts which
increase the speed, height and/or distance that plane can travel. Bonus points are usually awarded
for landing back at the KSC Runway, but you can land anywhere that is safe.

After these the real K-Plane contracts arrive: building rocket powered air-launched X-1 style
aircraft, acheiving Mach 1, 2, 3, getting to the stratosphere (18km to 50km for Earth scale) for
sub-orbital flights.

Later contracts are more speculative and involve reaching Mach 4, Mach 5, to space (80km), and
orbital. Some contracts require SSTO (single-stage to orbit) and some let you use boosters, but
still require wings (think Space Shuttle), and some involve leaving satellites or cargo in space.

Far future contracts might include taking certain tonnage to other moons or planets and returning
the craft and landing back at Kerbin/Earth.

## Installation

I highly recommend installing mods using [CKAN][url:CKAN] as it will correctly add required
dependencies, however for those who like a more tedious life you can manually install them and
possibly get less of my attention if there are issues.

Required Dependencies:

* [ModuleManager][url:ModuleManager]
* [Contract Configurator][url:ContractConfiguratorGitHub], which has releases for the latest 1.12.x
  compatible RO fork, see the forums [Contract Configuration KSP Forums][url:ContractConfigurator])

Recommended Part Dependencies:

* [Firespitter][url:Firespitter] for very early airplane parts
* [KSPWheels][url:KSPWheels] and [Kerbal Foundries][url:KerbalFoundries] for better landing gear
(and rover wheels).
* [AirplanePlus][url:AirplanePlus] for airplane parts
* [Eskandare Aerospace][url:EskandareAero] for even more airplane parts
* [KAX][url:KAX] for more airplane parts
* [QuizTech Aero Pack][url:QuizTech] for advanced airplane parts
* [C.E.D.A. Aeronautics][url:CEDAAero] for moar airplane parts (you cannot have too many right?)
* [B9 Aerospace Parts][url:B9Aerospace] for advanced airplane, space plane parts
* [B9 Procedural Wings][url:B9ProcWings] for procedural wings of any size and shape
* [Mk2 Expansion][url:Mk2Expansion] for advanced airplane, space plane parts
* [Mk3 Expansion][url:Mk3Expansion] for larger space plane parts
* [OPT Spaceplane Continued][url:OPT] for high tech space plane parts

Recommended Helper Dependencies:

* [AtmosphereAutopilot][url:AA] for a very good aircraft autopilot and SAS replacement
* [NavUtils][url:NavUtils] for runway landing navigation
* [Waypoint Manager][url:WaypointManager] for managing waypoints
* [Contracts Window][url:ContractsWindow] for viewing contracts outside of Mission Control
* [CapCom][url:CapCom] for accepting contracts outside of Mission Control

Recommended IVA Dependencies, to fly inside the plane:

* [RasterPropMonitor][url:RasterPropMonitor] (or RPM) allows IVA to be interactive.
* [MOARdV's Avionics System][url:AvionicsSystems] (or MAS) the successor to RPM.
* [Reviva][url:Reviva] which is one of my other mods, allows much easier installing/switch IVA mods.

## Speeds

Speeds are measured in m/s and are always the same for any planet. Roughly speaking Mach numbers are
multiples of 343 m/s, though this will vary depending on pressure, temperature and altitude.

## Altitudes

Altitudes are scaled by the planets FlyingHigh, SpaceLow and SpaceHigh altitudes:

- TroposphereLow : ~15% from sea level to FlyingHigh.
- TroposphereHigh : ~30% from sea level to FlyingHigh.
- StratosphereLow : ~40% from sea level to FlyingHigh.
- StratosphereHigh : ~70% from sea level to FlyingHigh.
- MesosphereLow : always equals FlyingHigh.
- MesosphereHigh : ~20% from FlyingHigh to SpaceLow.
- ThermosphereLow : ~40% from FlyingHigh to SpaceLow.
- SpaceLow : is where space starts in KSP.
- SpaceLEO : is roughly how high ISS travels, or about 12% from SpaceLow to SpaceHigh.
- SpaceHigh : is taken to mean MKO / MEO (Mid-Kerbin or Mid-Earth Orbit).

The computations are algorithms which will work for any planet scale, but here are examples for
common scales:

For Stock (1x)

- TroposphereLow: 2.50 km
- TroposphereHigh: 5.00 km
- StratosphereLow: 7.00 km
- StratosphereHigh: 12.50 km
- MesosphereLow, FlyingHigh : 18.00 km
- MesosphereHigh: 30.00 km
- ThermosphereLow: 40.00 km
- SpaceLow : 70.00 km 

For KSRSS (2.7x)

- TroposphereLow: 2.50 km
- TroposphereHigh: 5.00 km
- StratosphereLow: 7.00 km
- StratosphereHigh: 12.50 km
- MesosphereLow, FlyingHigh : 18.00 km
- MesosphereHigh: 30.00 km
- ThermosphereLow: 40.00 km
- SpaceLow : 80.00 km 

For RSS (Earth):

- TroposphereLow: 5.00 km
- TroposphereHigh: 10.00 km
- StratosphereLow: 20.00 km
- StratosphereHigh: 45.00 km
- MesosphereLow, FlyingHigh : 50.00 km
- MesosphereHigh: 70.00 m
- ThermosphereLow: 85.00 km
- SpaceLow : 140.00 km 

## Distances

Distance contracts are scaled by the planets circumference, again using algorithms that work for any scale.

For Stock (1x):

- Shop Hop : 50.00 km
- Domestic : 100.00 km
- Continental : 250.00 km
- Intercontinental : 750.00 km
- Polar : ~1,885 km
- Equatorial : ~3,770 km

For KSRSS (2.7x):

- Shop Hop : 130.00 km
- Domestic : 250.00 km
- Continental : 700.00 km
- Intercontinental : 2,000.00 km
- Polar : ~5,000 km
- Equatorial : ~10,0000 km

For RSS (Earth):

- Shop Hop : 530.00 km
- Domestic : 1,000.00 km
- Continental : 2,700.00 km
- Intercontinental : 8,000.00 km
- Polar : ~20,000 km
- Equatorial : ~40,000 km

## Changes

### 0.1.0 Release - Basic contracts (1st Dec 2022)

- Not really functional, but general idea started.

## License

All content is [MIT][url:MITLicense] licensed.

* KASA logo derived from NASA svg downloaded from [Wikipedia](https://en.wikipedia.org/wiki/NASA_insignia#/media/File:NASA_logo.svg)
* KACA logo dervied from NACA svg downloaded from [Wikipedia](https://commons.wikimedia.org/wiki/File:US_NACA_logo.svg)

## Source

[Source][url:KPlanes] is available on GitHub.

[KSP Forum][url:KPlanesKSPF] is the home page for discussions.

[kspf:610yesnolovely]: https://forum.kerbalspaceprogram.com/index.php?/profile/211485-610yesnolovely/
[url:KPlanes]: https://github.com/harveyt/KPlanes
[url:KPlanesKSPF]: https://forum.kerbalspaceprogram.com/index.php?/topic/210897-112/
[url:MITLicense]: https://github.com/harveyt/KPlanes/blob/main/LICENSE
[url:GAP]: https://forum.kerbalspaceprogram.com/index.php?/topic/129208-contract-pack-giving-aircraft-a-purpose-gap-161-milestones-air-flights-coast-guard/
[url:CKAN]: https://forum.kerbalspaceprogram.com/index.php?/topic/154922-ckan-the-comprehensive-kerbal-archive-network-v1280-dyson/
[url:ModuleManager]: https://forum.kerbalspaceprogram.com/index.php?/topic/50533-18x-112x-module-manager-421-august-1st-2021-locked-inside-edition/
[url:ContractConfigurator]: https://forum.kerbalspaceprogram.com/index.php?/topic/91625-1101-contract-configurator-v1305-2020-10-05/
[url:ContractConfiguratorGitHub]: https://github.com/KSP-RO/ContractConfigurator/releases
[url:Firespitter]: https://github.com/snjo/Firespitter/releases
[url:KSPWheels]: https://forum.kerbalspaceprogram.com/index.php?/topic/152782-18x-kspwheel-physics-based-alternate-wheel-collider-api-only/
[url:KerbalFoundries]: https://forum.kerbalspaceprogram.com/index.php?/topic/155056-18x-kerbal-foundries-continued-tracks-wheels-and-gear/
[url:AirplanePlus]: https://forum.kerbalspaceprogram.com/index.php?/topic/140262-14x-18x-airplane-plus-r264-fixed-issuesgithub-is-up-to-date-dec-21-2019/
[url:EskandareAero]: https://forum.kerbalspaceprogram.com/index.php?/topic/187622-173-eskandare-aerospace-0051-beta/
[url:KAX]: https://forum.kerbalspaceprogram.com/index.php?/topic/180268-131/
[url:QuizTech]: https://forum.kerbalspaceprogram.com/index.php?/topic/145635-19x-quiztech-aero-pack-continued/
[url:CEDAAero]: https://forum.kerbalspaceprogram.com/index.php?/topic/188318-17x-ceda-aeronautics-division-airplane-parts-pack/
[url:B9Aerospace]: https://forum.kerbalspaceprogram.com/index.php?/topic/155491-18x-b9-aerospace-release-660-feb-5-2020/
[url:B9ProcWings]: https://forum.kerbalspaceprogram.com/index.php?/topic/203629-112-b9-procedural-wings-fork-modified/
[url:Mk2Expansion]: https://forum.kerbalspaceprogram.com/index.php?/topic/109145-112x-mk2-expansion-v191-update-10521/
[url:Mk3Expansion]: https://forum.kerbalspaceprogram.com/index.php?/topic/109401-mk3-expansion-ksp-112x-version-16-10521/
[url:Opt]: https://forum.kerbalspaceprogram.com/index.php?/topic/196187-191-opt-spaceplane-continued-311-mar-06-2021/
[url:AA]: https://forum.kerbalspaceprogram.com/index.php?/topic/124417-180-1123-atmosphereautopilot-160/
[url:NavUtils]: https://forum.kerbalspaceprogram.com/index.php?/topic/204929-112x-navutilities-continued-ft-hsi-instrument-landing-system/
[url:WaypointManager]: https://forum.kerbalspaceprogram.com/index.php?/topic/194876-112x-waypoint-manager-new-dependency-added/
[url:ContractsWindow]: https://forum.kerbalspaceprogram.com/index.php?/topic/82106-18x-contracts-window-v94-1112019/
[url:CapCom]: https://forum.kerbalspaceprogram.com/index.php?/topic/107789-18x-capcom-mission-control-on-the-go-v211-11-1-2019/
[kspf:inigma]: https://forum.kerbalspaceprogram.com/index.php?/profile/69310-inigma/
[kspf:inigmaPermission]: https://forum.kerbalspaceprogram.com/index.php?/topic/199185-112x-planes-with-purposes-pwp/&do=findComment&comment=3908846
[url:RasterPropMonitor]: https://forum.kerbalspaceprogram.com/index.php?/topic/190737-18x-112x-rasterpropmonitor-adopted/
[url:AvionicsSystems]: https://forum.kerbalspaceprogram.com/index.php?/topic/160856-wip-111x-moardvs-avionics-systems-mas-interactive-iva-v123-21-may-2021/
[url:Reviva]: https://forum.kerbalspaceprogram.com/index.php?/topic/206744-wip112x-reviva-the-iva-revival-and-editorflight-switcher-070-pre-release-3rd-feb-2022/
