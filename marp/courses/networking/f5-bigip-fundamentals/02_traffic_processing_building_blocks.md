---
tags:
  - architecture:load-balancing
  - networking:tcp-ip
  - networking:troubleshooting
  - practices:sysadmin
level: beginner
category: networking
audience:
  - audiences:network-engineers
  - audiences:sysadmins
  - audiences:devops

---

# Traffic Processing Building Blocks

---

## What This Chapter Covers

- The traffic processing objects: nodes, pool members, pools, virtual servers
- Building a virtual server and a pool, in the `GUI` and in `tmsh`
- Load balancing methods, static and dynamic
- Priority group activation
- Reading statistics and logs to verify traffic
- The Traffic Management Shell (`tmsh`) and its hierarchy
- Running versus stored configuration, load and save
- Shutting down, restarting, and archiving with `UCS` and `SCF`

---

## The Traffic Processing Objects

![object_model](svg/courses/networking/f5-bigip-fundamentals/02_traffic_processing_building_blocks/object_model.svg)

---

## Nodes

- A node is a backend server identified by its `IP` address only
- Created automatically when you add a pool member with a new address
- Can also be created explicitly, with a name and a description
- A node can carry its own monitor (e.g. `icmp`) and connection limit
- Disabling a node affects every pool member that uses that address

```bash
tmsh create ltm node web1 address 10.1.20.11
tmsh list ltm node web1
```

---

## Pool Members

- A pool member is a node plus a service port: `10.1.20.11:80`
- The same node can be a member of many pools, on different ports
- Each member has its own state, statistics, ratio and priority
- Member settings are per pool: `web1:80` in two pools are two members
- Members can be enabled, disabled, or forced offline individually

---

## Pools

- A pool is a named group of members that serve the same content
- The pool owns the load balancing method
- The pool owns the health monitor (applied to all members by default)
- A pool is not reachable by clients until a virtual server points at it
- One pool can be the default pool of several virtual servers

---

## Virtual Servers

- The listener that clients connect to: destination address, port, `VLAN`s
- Usually a public or client-side address, never the server's own
- Carries the profiles that decide how traffic is processed
- Points to a default pool, and optionally iRules and policies
- Also controls `SNAT`, persistence and connection limits

---

## How Traffic Flows Through a Virtual Server

![vs_traffic_flow](svg/courses/networking/f5-bigip-fundamentals/02_traffic_processing_building_blocks/vs_traffic_flow.svg)

---

## Destination Address Translation

- The client sends to the virtual address `10.1.10.100:80`
- `BIG-IP` picks a member and rewrites the destination to `10.1.20.12:80`
- The source address stays the client's address by default
- The server's reply must come back through `BIG-IP` to be translated back
- Usually solved by making `BIG-IP` the servers' default gateway, or with `SNAT` (covered later)

---

## Virtual Server Types

| Type | What it does | Typical use |
| --- | --- | --- |
| Standard | Full proxy, all profiles available | `HTTP`, `HTTPS`, most applications |
| Performance (Layer 4) | Fast path, `FastL4` profile, no `L7` | High throughput `TCP`/`UDP` |
| Performance (`HTTP`) | Fast `HTTP` profile, limited features | Simple, very high volume `HTTP` |
| Forwarding (`IP`) | Routes packets, no pool | Using `BIG-IP` as a router |
| Forwarding (Layer 2) | Bridges packets between `VLAN`s | Transparent deployments |
| Reject | Rejects matching traffic | Blocking a network or port |

---

## Virtual Server Matching Order

- A packet can match several virtual servers; the most specific wins
- Specific host address beats network address beats wildcard `0.0.0.0/0`
- A specific port beats the wildcard port `*` (any)
- A source address restriction makes a virtual server more specific
- Only enabled virtual servers on the ingress `VLAN` are candidates

| Destination | Port | Specificity |
| --- | --- | --- |
| `10.1.10.100/32` | `80` | Most specific |
| `10.1.10.100/32` | `*` | |
| `10.1.10.0/24` | `80` | |
| `0.0.0.0/0` | `*` | Least specific |

---

## Creating a Pool in the GUI

1. Go to Local Traffic > Pools > Pool List > Create
1. Name: `http_pool`
1. Health Monitors: move `http` to Active
1. Load Balancing Method: `Round Robin`
1. New Members: address `10.1.20.11`, port `80`, Add
1. Repeat for `10.1.20.12` and `10.1.20.13`
1. Finished

---

## Creating a Virtual Server in the GUI

1. Go to Local Traffic > Virtual Servers > Virtual Server List > Create
1. Name: `http_vs`, Type: `Standard`
1. Destination Address: `10.1.10.100`, Service Port: `80` (`HTTP`)
1. `HTTP` Profile (Client): `http`
1. Source Address Translation: `None` for now
1. Default Pool: `http_pool`
1. Finished

---

## The Same Thing in tmsh

```bash
tmsh create ltm pool http_pool \
    members add { 10.1.20.11:80 10.1.20.12:80 10.1.20.13:80 } \
    monitor http load-balancing-mode round-robin

tmsh create ltm virtual http_vs \
    destination 10.1.10.100:80 ip-protocol tcp \
    profiles add { tcp http } pool http_pool

tmsh save sys config
```

- Every `GUI` object is a `tmsh` object with the same properties
- Scripted creation is repeatable and easy to review

---

## Lab: Your First Application

1. Create `http_pool` with the three web servers on port `80`
1. Create `http_vs` on `10.1.10.100:80` with the `http` profile
1. Browse to `http://10.1.10.100` from the client and refresh several times
1. Note which server answered each time (the page shows its name)
1. Check pool member statistics: did each member get a share?

---

## Load Balancing Methods

![lb_methods](svg/courses/networking/f5-bigip-fundamentals/02_traffic_processing_building_blocks/lb_methods.svg)

---

## Static Versus Dynamic Methods

- Static methods ignore the current state of the servers
    - Decisions come from configuration only: order, ratio
    - Predictable, cheap, fair when servers and requests are similar
- Dynamic methods measure the servers while they work
    - Open connections, response time, measured capacity
    - Adapt to slow or busy servers, at the cost of some predictability
- Default for a new pool: `Round Robin`

---

## Load Balancing Methods Compared

| Method | Type | Decision based on |
| --- | --- | --- |
| `Round Robin` | Static | Next member in turn |
| `Ratio (member)` | Static | Configured ratio weights |
| `Least Connections (member)` | Dynamic | Fewest open connections |
| `Fastest (application)` | Dynamic | Fewest outstanding `L7` requests |
| `Observed (member)` | Dynamic | Connection count trend over time |
| `Predictive (member)` | Dynamic | Improving connection trend |
| `Weighted Least Connections` | Dynamic | Connections relative to a limit |
| `Least Sessions` | Dynamic | Fewest persistence records |

---

## Member Versus Node Methods

- Most methods come in two flavors: `(member)` and `(node)`
- `(member)` counts only this pool's connections to that member
- `(node)` counts all connections to the server `IP`, across all pools
- Use `(node)` when one server hosts several pools or ports
- Example: `Least Connections (node)` balances whole servers, not services

---

## Ratio Load Balancing

- Each member gets a ratio, default `1`
- A member with ratio `3` receives three connections for every one of a ratio `1` member
- Use it when servers have different capacity
- Combined with dynamic data in `Ratio Least Connections`

```bash
tmsh modify ltm pool http_pool load-balancing-mode ratio-member \
    members modify { 10.1.20.11:80 { ratio 3 } 10.1.20.12:80 { ratio 2 } }
```

---

## Least Connections

- New connection goes to the member with the fewest current connections
- Self-correcting: a slow server holds connections longer and gets fewer new ones
- Good default for long lived or uneven connections
- Watch out with `OneConnect` and persistence: counts may not reflect load
- A newly added member gets a burst of connections until it catches up

```bash
tmsh modify ltm pool http_pool load-balancing-mode least-connections-member
```

---

## Priority Group Activation

![priority_groups](svg/courses/networking/f5-bigip-fundamentals/02_traffic_processing_building_blocks/priority_groups.svg)

---

## Configuring Priority Groups

- Enable on the pool: Priority Group Activation, `Less than N` available members
- Give each member a priority group number; higher numbers are preferred
- Traffic goes only to the highest group while it has at least `N` members up
- Below `N`, the next lower group is added to the rotation
- Load balancing still applies within the active members

```bash
tmsh modify ltm pool http_pool min-active-members 2 \
    members modify { 10.1.20.11:80 { priority-group 10 } \
                     10.1.20.12:80 { priority-group 10 } \
                     10.1.20.13:80 { priority-group 5 } }
```

---

## Member States

| State | New connections | Existing connections | Typical reason |
| --- | --- | --- | --- |
| Enabled, up | Yes | Yes | Normal |
| Disabled | Persistent only | Yes | Graceful maintenance |
| Forced offline | No | Yes, until they close | Draining a server |
| Down (monitor) | No | Depends on pool action | Server failed health check |

- Use disable or force offline before patching a server
- Watch current connections drop to zero before taking it down

---

## Lab: Methods and Priority Groups

1. Switch `http_pool` to `Ratio (member)` with ratios `3:2:1`
1. Send 60 requests with `curl` in a loop and compare member statistics
1. Switch to `Least Connections (member)`
1. Put `.11` and `.12` in priority group 10 and `.13` in group 5, minimum 2
1. Disable `.11` and confirm that `.13` starts receiving traffic

```bash
for i in $(seq 60); do curl -s http://10.1.10.100/ | grep server; done | sort | uniq -c
```

---

## Viewing Statistics

- Statistics > Module Statistics > Local Traffic
- Choose the object type: Virtual Servers, Pools, Pool Members, Nodes
- Counters: bits and packets in and out, current, maximum and total connections
- Reset counters before a test to read clean numbers
- Network Map (Local Traffic > Network Map) shows status of all objects

---

## Statistics in tmsh

```bash
tmsh show ltm virtual http_vs
tmsh show ltm pool http_pool members
tmsh show ltm pool http_pool members field-fmt
tmsh reset-stats ltm pool http_pool
tmsh show sys connection cs-server-addr 10.1.10.100
```

- `show` reads statistics and status; `list` reads configuration
- `field-fmt` gives one value per line, easy to grep
- `show sys connection` lists the live connection table

---

## Reading the Pool Statistics

```output
Ltm::Pool Member: http_pool 10.1.20.11:80
  Status
    Availability : available
    State        : enabled
    Reason       : Pool member is available
  Traffic          ServerSide
    Bits In              1.2M
    Bits Out            18.4M
    Current Connections     4
    Maximum Connections    12
    Total Connections     210
```

---

## Logs

| File | Contents |
| --- | --- |
| `/var/log/ltm` | Local traffic: monitors, pool status, iRule log output |
| `/var/log/gtm` | `DNS` (`GTM`) module events |
| `/var/log/audit` | Configuration changes: who changed what and when |
| `/var/log/secure` | Logins and authentication |
| `/var/log/messages` | Linux host messages |
| `/var/log/daemon.log` | System daemons |

- In the `GUI`: System > Logs
- Follow live: `tail -f /var/log/ltm`

---

## The Traffic Management Shell

- `tmsh` is the command line for all of `BIG-IP` configuration and status
- Run it from `bash` with `tmsh`, or set it as the user's default shell
- One-shot mode: `tmsh show ltm pool` from `bash` runs one command and exits
- Tab completion and `?` help at every level
- Everything the `GUI` does goes through the same configuration daemon (`mcpd`)

---

## The tmsh Hierarchy

![tmsh_hierarchy](svg/courses/networking/f5-bigip-fundamentals/02_traffic_processing_building_blocks/tmsh_hierarchy.svg)

---

## Modules, Components and Objects

- Modules are the top level: `ltm`, `net`, `sys`, `cm`, `auth`, `gtm`
- Components live inside modules: `ltm pool`, `net vlan`, `sys ntp`
- Some components have sub components: `ltm profile http`, `ltm monitor http`
- Objects are your named instances: `ltm pool http_pool`
- A full command: verb, then the path, then the object, then properties

```bash
tmsh create ltm profile http my_http defaults-from http
```

---

## Navigating the Hierarchy

```console
root@(bigip1)(cfg-sync Standalone)(Active)(/Common)(tmos)# cd ltm
root@(bigip1)(cfg-sync Standalone)(Active)(/Common)(tmos.ltm)# list pool
root@(bigip1)(cfg-sync Standalone)(Active)(/Common)(tmos.ltm)# cd pool
root@(bigip1)(cfg-sync Standalone)(Active)(/Common)(tmos.ltm.pool)# show
root@(bigip1)(cfg-sync Standalone)(Active)(/Common)(tmos.ltm.pool)# cd /
```

- The prompt shows sync state, failover state, partition and position
- `cd ..` goes up one level, `cd /` returns to the top
- `quit` leaves `tmsh`; `run util bash` drops to `bash` without leaving

---

## Common tmsh Verbs

| Verb | Purpose | Example |
| --- | --- | --- |
| `list` | Show configuration | `list ltm pool http_pool` |
| `show` | Show status and statistics | `show ltm virtual http_vs` |
| `create` | Create a new object | `create ltm node web4 address 10.1.20.14` |
| `modify` | Change properties | `modify ltm pool http_pool monitor tcp` |
| `delete` | Remove an object | `delete ltm node web4` |
| `save` / `load` | Save or load configuration | `save sys config` |
| `run` | Run a utility | `run util ping 10.1.20.11` |

---

## tmsh Productivity

- `list ltm pool http_pool all-properties` shows defaults too
- `list ltm pool one-line` prints one object per line
- `list ltm virtual http_vs pool` prints a single property
- `help` and `?` at any point; `edit ltm pool http_pool` opens an editor
- `show running-config` shows everything; pipe to `grep`

```bash
tmsh list ltm pool one-line | grep 10.1.20.13
tmsh list ltm virtual http_vs destination pool profiles
```

---

## Partitions and Folders

- Every object lives in an administrative partition, by default `/Common`
- Full object names include the path: `/Common/http_pool`
- Partitions let different teams own different objects
- `tmsh cd /Common` or `cd /Tenant_A` changes partition
- In the `GUI`, the partition selector is at the top right

---

## Lab: Working in tmsh

1. `SSH` to `bigip1` as `root` and run `tmsh`
1. Navigate to `ltm pool` and list your pool
1. Create a second pool `http_pool2` with only `.13:80`
1. Point `http_vs` at the new pool, test, then point it back
1. Compare `list` and `show` output for the same pool

---

## Configuration State

![config_state](svg/courses/networking/f5-bigip-fundamentals/02_traffic_processing_building_blocks/config_state.svg)

---

## Running and Stored Configuration

- Running configuration: held in memory by `mcpd`, used by `TMM` right now
- Stored configuration: text files under `/config`, loaded at boot
- `GUI` and `tmsh` changes take effect immediately in the running configuration
- The `GUI` saves automatically; `tmsh` does not
- Forgetting `save sys config` after `tmsh` work loses it at the next reboot

---

## Configuration Files

| File | Contents |
| --- | --- |
| `/config/bigip.conf` | Local traffic objects: virtual servers, pools, profiles |
| `/config/bigip_base.conf` | Network and system: `VLAN`s, self `IP`s, device settings |
| `/config/bigip_user.conf` | User accounts and roles |
| `/config/BigDB.dat` | System database variables (`db` keys) |
| `/config/bigip_script.conf` | iRules and scripts |
| `/config/partitions/<name>/` | Objects in non-Common partitions |

---

## Loading and Saving

```bash
tmsh save sys config                 # write running config to /config
tmsh save sys config partitions all  # include every partition
tmsh load sys config                 # replace running config from /config
tmsh load sys config verify          # syntax-check without applying
tmsh load sys config default         # reset to factory defaults (keeps mgmt and license)
```

- `load` discards unsaved running changes: save first or know why you do not
- `verify` catches a hand-edited file error before it takes the box down

---

## Shutting Down and Restarting

| Action | Command | Effect |
| --- | --- | --- |
| Restart services | `tmsh restart sys service tmm` | Data plane restart, traffic interrupted |
| Reboot | `tmsh reboot` | Full system reboot |
| Shut down | `tmsh stop sys service all` then `shutdown -h now` | Power off safely |
| Reload config | `tmsh load sys config` | No restart, config replaced |

- On a standalone system every option interrupts traffic
- In a high availability pair, fail over first, then reboot the standby

---

## Saving and Replicating Configuration Data

- `UCS` (user configuration set): full archive of the system
    - Configuration, certificates, keys, licenses, users, `db` variables
    - Restore on the same box or a replacement of the same platform
- `SCF` (single configuration file): one flat text file of the configuration
    - No keys, no license
    - Used to replicate a configuration onto another system

---

## `UCS` and `SCF` Compared

| Property | `UCS` | `SCF` |
| --- | --- | --- |
| Format | Compressed archive | Plain text |
| Includes keys and certificates | Yes (optionally encrypted) | No |
| Includes license | Yes | No |
| Typical use | Backup and disaster recovery | Templating, cloning, diff |
| Location | `/var/local/ucs/` | `/var/local/scf/` |
| Restore | `load sys ucs` | `load sys config file` |

---

## `UCS` and `SCF` Commands

```bash
tmsh save sys ucs /var/local/ucs/before_change.ucs
tmsh save sys ucs before_change passphrase MyArchivePass
tmsh load sys ucs before_change.ucs

tmsh save sys config file /var/local/scf/lab.scf no-passphrase
tmsh load sys config file /var/local/scf/lab.scf
```

- Copy archives off the box: a backup on the failed device is no backup
- Take a `UCS` before every upgrade and every large change

---

## Lab: Save, Break and Restore

1. Run `tmsh save sys ucs lab_baseline.ucs`
1. Delete `http_vs` in `tmsh`, without saving
1. Run `tmsh load sys config` and confirm `http_vs` is back
1. Delete `http_vs` again and save
1. Restore with `tmsh load sys ucs lab_baseline.ucs` and test the application

---

## Key Takeaways

- Node = address, member = address and port, pool = members plus method
- Virtual server = listener plus profiles plus default pool
- Pick a load balancing method by how similar your servers and requests are
- Priority groups give you a preferred set with automatic backup
- `show` for status, `list` for configuration, and always `save sys config`
- Archive with `UCS` for recovery, `SCF` for readable replication
