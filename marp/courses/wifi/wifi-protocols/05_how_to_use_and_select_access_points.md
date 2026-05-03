---
tags:
  - networking:wifi
  - networking:access-points
level: intermediate
category: networking
audience:
  - audiences:developers
  - audiences:embedded-engineers

---
# How to Use and Select Access Points

---
## What This Chapter Covers

- The classes of AP products on the market
- Specifications that actually matter (and ones that don't)
- Coverage planning rules of thumb
- Mesh, controller-based, and standalone deployments
- A short procurement checklist

---
## Three Classes of AP

- **Consumer**: combined router/AP/switch, web UI, set-and-forget
- **SMB / prosumer**: separate AP, controller software, more knobs
- **Enterprise**: cloud or on-prem controllers, RF planning, rich telemetry
- The same chip may sit in all three; software and management differ
- Buy the class that matches the team, not the household-name brand

---
## Specs That Matter

- Supported 802.11 generations (Wi-Fi 6 minimum for new buys)
- Bands supported (2.4 / 5 / 6 GHz)
- Number of spatial streams per band
- Maximum channel width per band
- PoE power class (PoE+ usually required for Wi-Fi 6)

---
## Specs to Read Skeptically

- "AX5400" and other made-up totals: sum of theoretical peak rates per band
- A single client never reaches that number
- "Coverage area" claims assume open space and ignore walls
- "Up to 200 clients" — yes, if they barely talk
- Always look at independent reviews with throughput-under-load tests

---
## How Many APs Do I Need?

- Rule of thumb (offices): one AP per 1500 sq ft / 140 sq m of usable area
- Dense classrooms / conference halls: one per ~30 active clients
- Concrete or metal walls: assume an AP per room, not per floor
- Plan for *capacity*, not coverage — coverage is the easier problem
- Always do a survey for production deployments

---
## Where to Mount

- Ceiling, near the centre of the area to cover
- Avoid metal beams, HVAC ducts, and big mirrors directly below the antenna
- 3-4 metre ceilings are ideal; very high ceilings need directional antennas
- Wall-mount is a compromise — the antenna pattern leaks behind the wall
- Outdoor APs need outdoor enclosures; indoor APs do not survive rain

---
## Power and Cabling

- PoE (Power over Ethernet) feeds power and data on one cable
- PoE class 4 (~25 W) needed for many Wi-Fi 6 dual-band APs
- 802.3bt (PoE++) needed for Wi-Fi 6E and 7 with all radios at full power
- Underpowered APs silently disable a radio or drop spatial streams
- Cable: Cat5e is enough for 1 GbE; Cat6 if you want 2.5 GbE / 10 GbE uplink

---
## Standalone vs Controller

- Standalone: one AP, configured via its own UI
- Controller-based: many APs, central config, coordinated channel/power
- Cloud controller: vendor hosts the management plane (Meraki, Aruba Central)
- On-prem controller: physical or VM appliance, runs in your network
- Multi-AP without a controller is awkward — channels and roaming need coordination

---
## Mesh

- Each AP is also a *backhaul* node; one wired AP feeds wireless ones
- Easy retrofits where you can't run cable
- Each mesh hop roughly halves throughput (one radio talking on each side)
- Dedicated backhaul radios in tri-band mesh systems mitigate this
- Mesh is a workaround, not a substitute for a wired backbone

---
## Deployment Topologies

![deployment_topologies](svg/courses/wifi/wifi-protocols/05_how_to_use_and_select_access_points/deployment_topologies.svg)

---
## Architecture Comparison

![architecture_comparison](svg/courses/wifi/wifi-protocols/05_how_to_use_and_select_access_points/architecture_comparison.svg)

---
## SSID Strategy

- One SSID for staff (WPA2/3-Enterprise), one for guests (PSK), one for IoT
- Resist the urge to make many SSIDs — every one wastes airtime on beacons
- 3 SSIDs in 2.4 GHz already burns ~2-3% of airtime on management frames
- Use VLANs to segment, not separate radios
- Hide nothing: hidden SSIDs do not improve security and break some clients

---
## Channel Planning Cheat-Sheet

- 2.4 GHz: only 1, 6, 11. Always 20 MHz wide. Live with it.
- 5 GHz UNII-1 / UNII-3: easy, no DFS — start here
- 5 GHz UNII-2 / UNII-2e: DFS — radar can kick you off the channel
- 6 GHz: huge, clean. Wi-Fi 6E/7 only. 80 MHz is reasonable here.
- Auto-channel works for small deployments; survey for the rest

---
## Power Planning

- Resist the temptation to crank TX power to maximum
- The client transmits back at *its* power — usually much weaker than the AP
- Asymmetric power = the AP hears you weakly while you see "5 bars"
- Match AP TX power to the *weakest* client's TX power
- Many APs auto-tune; check it actually went down on quiet APs

---
## Roaming Behaviour

- Sticky clients hold a far AP and won't switch
- 802.11k: AP gives the client a list of neighbour APs
- 802.11v: AP can suggest "go talk to that other AP"
- 802.11r: fast BSS transition, sub-100ms re-auth
- Old clients ignore all of this; budget for them in AP density

---
## Procurement Checklist

- Wi-Fi 6 or newer; Wi-Fi 6E if you have 6 GHz allowed and dense clients
- 4x4 in 5 GHz at minimum for high-density rooms
- PoE++ supported on the switch port if buying Wi-Fi 6E/7
- Vendor's controller licensing and renewal model
- Vendor still publishing security firmware updates 5 years on?

---
## Common Mistakes

- Buying consumer routers for an office that has IT staff
- Spreading APs evenly without considering walls and people
- Mesh-everywhere instead of running one extra ethernet drop
- Maxing TX power then wondering why upload speeds are awful
- Trusting auto-everything without verifying with a survey
