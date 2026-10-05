---
tags:
  - networking:tcp-ip
  - networking:troubleshooting
  - architecture:load-balancing
  - practices:sysadmin
level: beginner
category: networking
audience:
  - audiences:network-engineers
  - audiences:sysadmins
  - audiences:devops

---

# Using `NAT`s and `SNAT`s

---

## What This Chapter Covers

- Address translation on the `BIG-IP` system
- Mapping one address to another with `NAT`s
- The return path problem and how `SNAT`s solve it
- `SNAT` auto map on a virtual server
- `SNAT` pools and standalone `SNAT` objects
- Keeping the client address visible to the servers
- Monitoring for and mitigating port exhaustion

---

## Address Translation on the BIG-IP System

- A full proxy rewrites addresses as a matter of course
- The virtual server translates the destination: `VS` address becomes a pool member address
- Source translation is optional and must be configured
- Three objects translate addresses outside a virtual server's pool choice:
    - `NAT`: one to one, both directions
    - `SNAT`: many to one (or to a few), source only
    - `SNAT` pool: the set of addresses a `SNAT` draws from
- Translation happens in `TMM`, on the data plane, at line rate

---

## What Each Object Translates

| Object | Translates | Direction | Load balances |
| --- | --- | --- | --- |
| Virtual server | Destination address and port | Client to server | Yes |
| `NAT` | Source outbound, destination inbound | Both | No |
| `SNAT` | Source address and maybe port | Initiator to responder | No |
| `SNAT` on a `VS` | Source address of server side flow | Client to server | Yes, via the pool |

---

## Addresses Before and After Translation

| Leg | Source | Destination |
| --- | --- | --- |
| Client to `BIG-IP` | `10.1.10.50:51000` | `10.1.10.100:80` |
| `BIG-IP` to server, no `SNAT` | `10.1.10.50:51000` | `10.1.20.11:80` |
| `BIG-IP` to server, `SNAT` auto map | `10.1.20.245:51000` | `10.1.20.11:80` |
| Server to `BIG-IP`, `SNAT` auto map | `10.1.20.11:80` | `10.1.20.245:51000` |
| `BIG-IP` to client | `10.1.10.100:80` | `10.1.10.50:51000` |

- The client always sees the virtual server address
- With `SNAT`, the server never sees the client address

---

## Mapping IP Addresses with NATs

- A `NAT` binds one origin address to one translation address
- Inbound: traffic to the translation address is sent to the origin address
- Outbound: traffic from the origin address leaves with the translation address
- No virtual server, no pool, no monitor, no profiles
- All ports and protocols pass through
- Classic use: give an internal host a public identity

---

## One to One, Both Directions

![nat_mapping](svg/courses/networking/f5-bigip-fundamentals/07_using_nats_and_snats/nat_mapping.svg)

---

## Creating a NAT

- GUI: Local Traffic > Address Translation > `NAT` List > Create
- Origin address is the internal host, translation address is the external identity
- Restrict the `VLAN`s it listens on

```bash
tmsh create ltm nat nat_admin_host \
    originating-address 10.1.20.50 \
    translation-address 10.1.10.50 \
    vlans add { external } vlans-enabled
tmsh list ltm nat nat_admin_host
tmsh show ltm nat nat_admin_host
```

---

## NAT Considerations

- `BIG-IP` answers `ARP` for the translation address (`arp enabled` by default)
- The origin host must route its outbound traffic through `BIG-IP`
- Every port of the origin host is exposed on the translation address
- No profiles means no `TCP` optimization, no `HTTP` processing, no `SSL` offload
- In an `HA` pair the `NAT` belongs to a traffic group and follows failover
- Prefer a virtual server when you only need one service published

---

## NAT or Virtual Server

| Need | Use |
| --- | --- |
| Publish one web service, load balanced | Virtual server with a pool |
| Give one host a full external identity | `NAT` |
| Remote administration of one backend box | `NAT`, restricted by `VLAN` and firewall |
| Outbound internet for many servers | `SNAT`, not `NAT` |
| Inspect or modify the traffic | Virtual server with profiles |

---

## The Return Path Problem

- The virtual server rewrote only the destination address
- The server sees the real client address as the source
- The server replies to its default gateway, not to `BIG-IP`
- The reply reaches the client with the server address as source
- The client has no connection with that address and drops or resets it
- Result: the `SYN` is forwarded, the handshake never completes

---

## Asymmetric Routing

![asymmetric_routing](svg/courses/networking/f5-bigip-fundamentals/07_using_nats_and_snats/asymmetric_routing.svg)

---

## Fixing the Return Path

| Fix | How | Trade-off |
| --- | --- | --- |
| Servers route through `BIG-IP` | Default gateway is the floating self `IP` | Client address preserved, all server traffic crosses `BIG-IP` |
| Policy routing on the router | Send replies from port 80 back to `BIG-IP` | Extra config outside `BIG-IP` |
| `SNAT` on the virtual server | Source becomes a `BIG-IP` address | Server loses the client address |

- `SNAT` is the most common fix: it needs no change outside `BIG-IP`
- It is mandatory in one arm deployments and when clients share the server subnet

---

## SNAT Fixes the Return Path

![snat_return_path](svg/courses/networking/f5-bigip-fundamentals/07_using_nats_and_snats/snat_return_path.svg)

---

## What a SNAT Changes

- Server side source address becomes a `BIG-IP` owned address
- Source port is preserved when possible (`source-port preserve` is the default)
- The server replies to `BIG-IP` regardless of its routing table
- Server access logs show the `SNAT` address for every client
- Server side access lists keyed on client address stop working
- Rate limits and geolocation must move to `BIG-IP` or use a header

---

## Keeping the Client Address Visible

- Insert `X-Forwarded-For` with the client address in an `HTTP` profile
- The server application or web server logs that header instead

```bash
tmsh create ltm profile http http_xff \
    defaults-from http insert-xforwarded-for enabled
tmsh modify ltm virtual vs_web profiles delete { http } \
    profiles add { http_xff }
```

```http
GET /index.html HTTP/1.1
Host: www.example.com
X-Forwarded-For: 10.1.10.50
```

---

## Configuring SNAT Auto Map on a Virtual Server

- GUI: Local Traffic > Virtual Servers > `vs_web` > Source Address Translation: Auto Map
- `BIG-IP` picks a self `IP` on the egress `VLAN` as the source
- No extra address to plan or allocate

```bash
tmsh modify ltm virtual vs_web source-address-translation { type automap }
tmsh list ltm virtual vs_web source-address-translation
```

```config
ltm virtual vs_web {
    source-address-translation {
        type automap
    }
}
```

---

## How Auto Map Picks an Address

![snat_auto_map_selection](svg/courses/networking/f5-bigip-fundamentals/07_using_nats_and_snats/snat_auto_map_selection.svg)

---

## Auto Map and High Availability

- In an `HA` pair, create a floating self `IP` on every server side `VLAN`
- Auto map prefers the floating address of the virtual server's traffic group
- After failover the floating address moves, so replies still reach the active unit
- Without a floating self `IP`, auto map uses the unit's own self `IP`
- Mirrored connections then break on failover: the address stayed behind

```bash
tmsh create net self 10.1.20.240/24 vlan internal \
    traffic-group traffic-group-1 allow-service none
```

---

## SNAT Pools

- A `SNAT` pool is a list of translation addresses
- Assigned to a virtual server or to a standalone `SNAT`
- `BIG-IP` spreads connections across the addresses
- Each member becomes a `snat-translation` object with its own settings
- Use when one address does not have enough ports
- Use when servers or firewalls expect a specific source address

---

## Configuring a SNAT Pool

```bash
tmsh create ltm snatpool snat_pool_web \
    members add { 10.1.20.61 10.1.20.62 10.1.20.63 10.1.20.64 }
tmsh modify ltm virtual vs_web \
    source-address-translation { type snat pool snat_pool_web }
tmsh list ltm snat-translation 10.1.20.61
tmsh show ltm snatpool snat_pool_web
```

- Put the addresses on a server side subnet so replies stay on link
- `BIG-IP` answers `ARP` for them automatically
- In an `HA` pair, set the translations to the right traffic group

---

## Standalone SNAT Objects

- A `SNAT` not attached to a virtual server matches by origin address
- Typical use: servers reaching the internet or update servers through `BIG-IP`
- Translation can be one address, auto map or a `SNAT` pool

```bash
tmsh create ltm snat snat_servers_out \
    origins add { 10.1.20.0/24 } \
    translation 10.1.10.60 \
    vlans add { internal } vlans-enabled
tmsh show ltm snat snat_servers_out
```

---

## Choosing the Right Translation

| Feature | `NAT` | `SNAT` auto map | `SNAT` pool | Standalone `SNAT` |
| --- | --- | --- | --- | --- |
| Mapping | One to one | Many to self `IP` | Many to a few | Many to one or a few |
| Direction | Both | Server side only | Server side only | Outbound only |
| Attached to | Nothing | Virtual server | Virtual server or `SNAT` | Origin addresses |
| Extra addresses | One per host | None | One per member | One or more |
| Port capacity | All ports | About 64,000 per self `IP` | About 64,000 per member | Depends on translation |

---

## Why Port Exhaustion Happens

- A server side connection is a 4-tuple: source `IP`, source port, destination `IP`, destination port
- With `SNAT` the source `IP` is fixed, so only the source port varies
- One translation address gives about 64,000 ports per destination `IP:port`
- Busy applications with one or two servers hit the limit first
- Long idle timeouts keep ports allocated after clients are gone
- Exhaustion is per translation address and per destination

---

## The Arithmetic of Ports

![port_exhaustion](svg/courses/networking/f5-bigip-fundamentals/07_using_nats_and_snats/port_exhaustion.svg)

---

## Signs of Port Exhaustion

| Symptom | Where you see it |
| --- | --- |
| `Inet port exhaustion` messages | `/var/log/ltm` |
| New connections reset, existing ones fine | Client errors, `tcpdump` on the client side |
| Server side connection count flat at a ceiling | `tmsh show ltm snat-translation` |
| Errors grow with load, vanish at night | Statistics graphs, `iHealth` |
| Only one pool member affected | That member has the most connections |

---

## Monitoring for Port Exhaustion

```bash
grep -i "port exhaustion" /var/log/ltm
tmsh show ltm snat-translation 10.1.20.61
tmsh show ltm snatpool snat_pool_web
tmsh show sys connection ss-client-addr 10.1.20.61 ss-server-addr 10.1.20.11
```

```output
Oct  5 10:42:17 bigip1 err tmm[12034]: 01010201:3: Inet port exhaustion
  on 10.1.20.245 to 10.1.20.11:80 (proto 6)
```

- Compare current connections per translation address with the 64,000 ceiling
- Alert on the log message, do not wait for user complaints

---

## Mitigating Port Exhaustion

| Mitigation | Effect |
| --- | --- |
| Replace auto map with a `SNAT` pool | Each added address adds about 64,000 ports |
| Add pool members | Each new destination `IP:port` has its own port range |
| Shorten idle timeouts on the `SNAT` translation or `TCP` profile | Ports return to the free list sooner |
| Enable `OneConnect` | Server side connections are reused across requests |
| Route servers through `BIG-IP` and drop `SNAT` | No source translation, no shared ports |

---

## Lab: Break and Fix the Return Path

1. Create `vs_web` on `10.1.10.100:80` with `web_pool` and no `SNAT`
1. Point the servers' default gateway at the lab router, not at `BIG-IP`
1. Run `curl -v http://10.1.10.100/` from the client and watch it hang
1. Capture on `BIG-IP`: `tcpdump -ni internal host 10.1.20.11`
1. Enable `SNAT` auto map on `vs_web` and repeat the request
1. Compare the two captures: which source address does the server see?

---

## Lab: SNAT Pool and Client Address

1. Create `snat_pool_web` with `10.1.20.61` to `10.1.20.64`
1. Attach it to `vs_web` and generate load with `ab -n 2000 -c 50`
1. Check `tmsh show ltm snatpool snat_pool_web` for the spread of connections
1. Create the `http_xff` profile and attach it to `vs_web`
1. Read the server access log and confirm the real client address appears
1. Create `nat_admin_host` and `ssh` to the server through its translation address

---

## Key Takeaways

- The virtual server always translates the destination; source translation is your choice
- `NAT` is one to one and bidirectional, with no profiles and every port exposed
- `SNAT` guarantees the return path at the cost of hiding the client address
- Use auto map with a floating self `IP` in `HA` pairs
- One translation address has about 64,000 ports per destination
- Watch `/var/log/ltm` for port exhaustion and add `SNAT` pool members before it bites
