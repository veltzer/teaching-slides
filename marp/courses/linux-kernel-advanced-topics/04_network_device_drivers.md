# Network Device Drivers

---

## Network Stack Overview

<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">
<rect x="100" y="50" width="600" height="400" fill="#F0F0F0" stroke="black"/>
<text x="400" y="80" text-anchor="middle" font-weight="bold">Linux Network Stack</text>
<rect x="200" y="110" width="400" height="50" fill="#FFE6E6" stroke="black"/>
<text x="400" y="140" text-anchor="middle">Application Layer</text>
<rect x="200" y="170" width="400" height="50" fill="#E6F2FF" stroke="black"/>
<text x="400" y="200" text-anchor="middle">Socket Layer</text>
<rect x="200" y="230" width="400" height="50" fill="#E6FFE6" stroke="black"/>
<text x="400" y="260" text-anchor="middle">Protocol Layer (TCP/IP)</text>
<rect x="200" y="290" width="400" height="50" fill="#FFFFE6" stroke="black"/>
<text x="400" y="320" text-anchor="middle">Network Core</text>
<rect x="200" y="350" width="400" height="50" fill="#FFE6FF" stroke="black"/>
<text x="400" y="380" text-anchor="middle">Device Driver</text>
</svg>

---

## Network Device Structure

Core structure `net_device`:

```c
struct net_device {
    char name[IFNAMSIZ];
    unsigned int flags;
    unsigned int mtu;

    const struct net_device_ops *netdev_ops;
    const struct ethtool_ops *ethtool_ops;

    unsigned char *dev_addr;  /* MAC address */

    struct net_device_stats stats;

    void *priv;  /* Driver private data */
};
```

---

## Network Device Operations

```c
static const struct net_device_ops my_netdev_ops = {
    .ndo_open = my_net_open,
    .ndo_stop = my_net_close,
    .ndo_start_xmit = my_net_xmit,
    .ndo_set_rx_mode = my_net_set_rx_mode,
    .ndo_set_mac_address = my_net_set_mac,
    .ndo_validate_addr = eth_validate_addr,
    .ndo_do_ioctl = my_net_ioctl,
    .ndo_get_stats = my_net_get_stats,
};
```

---

## Driver Registration

```c
static int my_net_probe(struct platform_device *pdev)
{
    struct net_device *ndev;
    struct my_priv *priv;

    /* Allocate network device */
    ndev = alloc_etherdev(sizeof(struct my_priv));
    if (!ndev)
        return -ENOMEM;

    priv = netdev_priv(ndev);

    /* Setup device */
    ndev->netdev_ops = &my_netdev_ops;
    ndev->ethtool_ops = &my_ethtool_ops;

    /* Register device */
    ret = register_netdev(ndev);

    return ret;
}
```

---

## Socket Buffers (SKB)

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
<rect x="100" y="100" width="600" height="200" fill="#F0F0F0" stroke="black"/>
<text x="400" y="130" text-anchor="middle" font-weight="bold">sk_buff Structure</text>
<rect x="150" y="160" width="100" height="40" fill="#FFE6E6" stroke="black"/>
<text x="200" y="185" text-anchor="middle">head</text>
<rect x="250" y="160" width="100" height="40" fill="#E6F2FF" stroke="black"/>
<text x="300" y="185" text-anchor="middle">data</text>
<rect x="350" y="160" width="100" height="40" fill="#E6FFE6" stroke="black"/>
<text x="400" y="185" text-anchor="middle">payload</text>
<rect x="450" y="160" width="100" height="40" fill="#FFFFE6" stroke="black"/>
<text x="500" y="185" text-anchor="middle">tail</text>
<rect x="550" y="160" width="100" height="40" fill="#FFE6FF" stroke="black"/>
<text x="600" y="185" text-anchor="middle">end</text>
<line x1="200" y1="200" x2="200" y2="250" stroke="black"/>
<line x1="300" y1="200" x2="300" y2="250" stroke="black"/>
<line x1="500" y1="200" x2="500" y2="250" stroke="black"/>
<line x1="600" y1="200" x2="600" y2="250" stroke="black"/>
<text x="250" y="270">headroom</text>
<text x="400" y="270">data</text>
<text x="550" y="270">tailroom</text>
</svg>

---

## SKB Operations

```c
/* Allocate SKB */
skb = netdev_alloc_skb(ndev, size);

/* Reserve headroom */
skb_reserve(skb, NET_IP_ALIGN);

/* Add data */
memcpy(skb_put(skb, len), data, len);

/* Set protocol */
skb->protocol = eth_type_trans(skb, ndev);

/* Pass to network stack */
netif_rx(skb);  /* or netif_receive_skb(skb) */

/* Free SKB */
dev_kfree_skb(skb);
```

---

## Transmit Path

```c
static netdev_tx_t my_net_xmit(struct sk_buff *skb,
                               struct net_device *ndev)
{
    struct my_priv *priv = netdev_priv(ndev);

    /* Stop queue if full */
    if (tx_queue_full(priv)) {
        netif_stop_queue(ndev);
        return NETDEV_TX_BUSY;
    }

    /* Transmit packet */
    hw_transmit(priv, skb);

    /* Update stats */
    ndev->stats.tx_packets++;
    ndev->stats.tx_bytes += skb->len;

    /* Free SKB */
    dev_kfree_skb(skb);

    return NETDEV_TX_OK;
}
```

---

## Receive Path

```c
static irqreturn_t my_net_rx_interrupt(int irq, void *dev_id)
{
    struct net_device *ndev = dev_id;
    struct my_priv *priv = netdev_priv(ndev);
    struct sk_buff *skb;
    int len;

    while (hw_has_packet(priv)) {
        len = hw_get_packet_len(priv);
        skb = netdev_alloc_skb(ndev, len);

        if (!skb) {
            ndev->stats.rx_dropped++;
            continue;
        }

        hw_read_packet(priv, skb_put(skb, len));
        skb->protocol = eth_type_trans(skb, ndev);

        netif_rx(skb);

        ndev->stats.rx_packets++;
        ndev->stats.rx_bytes += len;
    }

    return IRQ_HANDLED;
}
```

---

## NAPI (New API)

Interrupt mitigation mechanism:

```c
static int my_napi_poll(struct napi_struct *napi, int budget)
{
    struct my_priv *priv = container_of(napi, struct my_priv, napi);
    int work_done = 0;

    while (work_done < budget && hw_has_packet(priv)) {
        /* Process packet */
        my_receive_packet(priv);
        work_done++;
    }

    if (work_done < budget) {
        napi_complete(napi);
        hw_enable_rx_interrupt(priv);
    }

    return work_done;
}
```

---

## NAPI Setup

```c
static int my_net_open(struct net_device *ndev)
{
    struct my_priv *priv = netdev_priv(ndev);

    /* Initialize NAPI */
    netif_napi_add(ndev, &priv->napi,
                   my_napi_poll, NAPI_POLL_WEIGHT);

    /* Enable NAPI */
    napi_enable(&priv->napi);

    /* Enable interrupts */
    request_irq(priv->irq, my_net_interrupt,
               0, ndev->name, ndev);

    /* Start queue */
    netif_start_queue(ndev);

    return 0;
}
```

---

## Interrupt Handler with NAPI

```c
static irqreturn_t my_net_interrupt(int irq, void *dev_id)
{
    struct net_device *ndev = dev_id;
    struct my_priv *priv = netdev_priv(ndev);

    /* Disable interrupts */
    hw_disable_rx_interrupt(priv);

    /* Schedule NAPI */
    if (napi_schedule_prep(&priv->napi))
        __napi_schedule(&priv->napi);

    return IRQ_HANDLED;
}
```

---

## PHY Management

Physical layer device handling:

```c
/* Connect to PHY */
phydev = phy_connect(ndev, phy_id,
                    &my_adjust_link,
                    PHY_INTERFACE_MODE_MII);

/* Configure PHY */
phydev->supported &= PHY_BASIC_FEATURES;
phydev->advertising = phydev->supported;

/* Start PHY */
phy_start(phydev);

/* Link change handler */
static void my_adjust_link(struct net_device *ndev)
{
    struct phy_device *phydev = ndev->phydev;

    if (phydev->link) {
        /* Link up */
        netif_carrier_on(ndev);
    } else {
        /* Link down */
        netif_carrier_off(ndev);
    }
}
```

---

## MDIO Bus

Management Data Input/Output:

```c
static struct mii_bus *mdio_bus_init(struct platform_device *pdev)
{
    struct mii_bus *bus;

    bus = mdiobus_alloc();
    bus->name = "my_mdio";
    bus->read = &my_mdio_read;
    bus->write = &my_mdio_write;
    bus->parent = &pdev->dev;

    /* Register MDIO bus */
    mdiobus_register(bus);

    return bus;
}

static int my_mdio_read(struct mii_bus *bus,
                        int phy_id, int reg)
{
    /* Implement MDIO read */
    return mdio_read_register(phy_id, reg);
}
```

---

## Ethtool Support

```c
static const struct ethtool_ops my_ethtool_ops = {
    .get_drvinfo = my_get_drvinfo,
    .get_link = ethtool_op_get_link,
    .get_ts_info = ethtool_op_get_ts_info,
    .get_ethtool_stats = my_get_ethtool_stats,
    .get_strings = my_get_strings,
    .get_sset_count = my_get_sset_count,
    .get_ringparam = my_get_ringparam,
    .set_ringparam = my_set_ringparam,
};

static void my_get_drvinfo(struct net_device *ndev,
                           struct ethtool_drvinfo *info)
{
    strlcpy(info->driver, DRIVER_NAME, sizeof(info->driver));
    strlcpy(info->version, DRIVER_VERSION, sizeof(info->version));
}
```

---

## Multicast and Promiscuous

```c
static void my_net_set_rx_mode(struct net_device *ndev)
{
    struct my_priv *priv = netdev_priv(ndev);

    if (ndev->flags & IFF_PROMISC) {
        /* Enable promiscuous mode */
        hw_set_promiscuous(priv, true);
    } else if (ndev->flags & IFF_ALLMULTI) {
        /* Accept all multicast */
        hw_set_allmulti(priv, true);
    } else {
        /* Setup multicast filter */
        struct netdev_hw_addr *ha;

        netdev_for_each_mc_addr(ha, ndev) {
            hw_add_multicast(priv, ha->addr);
        }
    }
}
```

---

## DMA for Network Drivers

```c
/* Allocate DMA buffers */
priv->rx_buf = dma_alloc_coherent(&pdev->dev,
                                  RX_BUF_SIZE,
                                  &priv->rx_dma,
                                  GFP_KERNEL);

/* Map SKB for DMA */
dma_addr = dma_map_single(&pdev->dev,
                          skb->data, skb->len,
                          DMA_TO_DEVICE);

/* Unmap after transmission */
dma_unmap_single(&pdev->dev, dma_addr,
                skb->len, DMA_TO_DEVICE);
```

---

## Ring Buffer Management

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
<ellipse cx="400" cy="200" rx="250" ry="120" fill="none" stroke="black" stroke-width="2"/>
<rect x="350" y="80" width="100" height="40" fill="#FFE6E6" stroke="black"/>
<rect x="500" y="100" width="100" height="40" fill="#E6F2FF" stroke="black"/>
<rect x="600" y="180" width="100" height="40" fill="#E6FFE6" stroke="black"/>
<rect x="550" y="280" width="100" height="40" fill="#FFFFE6" stroke="black"/>
<rect x="400" y="320" width="100" height="40" fill="#FFE6FF" stroke="black"/>
<rect x="250" y="280" width="100" height="40" fill="#E6E6E6" stroke="black"/>
<rect x="150" y="180" width="100" height="40" fill="#FFE6E6" stroke="black"/>
<rect x="200" y="100" width="100" height="40" fill="#E6F2FF" stroke="black"/>
<text x="400" y="30" text-anchor="middle" font-weight="bold">TX/RX Ring Buffer</text>
<line x1="300" y1="200" x2="350" y2="200" stroke="red" stroke-width="3" marker-end="url(#redarrow)"/>
<text x="280" y="195" fill="red">Head</text>
<line x1="500" y1="200" x2="550" y2="200" stroke="blue" stroke-width="3" marker-end="url(#bluearrow)"/>
<text x="520" y="195" fill="blue">Tail</text>
<defs>
<marker id="redarrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
<polygon points="0 0, 10 3, 0 6" fill="red"/>
</marker>
<marker id="bluearrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
<polygon points="0 0, 10 3, 0 6" fill="blue"/>
</marker>
</defs>
</svg>

---

## Ring Buffer Implementation

```c
struct tx_ring {
    struct tx_desc *desc;  /* Descriptor array */
    dma_addr_t dma;        /* DMA address */
    unsigned int head;     /* Producer index */
    unsigned int tail;     /* Consumer index */
    struct sk_buff **skbs; /* SKB array */
};

static int alloc_tx_ring(struct my_priv *priv)
{
    priv->tx_ring.desc = dma_alloc_coherent(
        priv->dev,
        TX_RING_SIZE * sizeof(struct tx_desc),
        &priv->tx_ring.dma,
        GFP_KERNEL);

    priv->tx_ring.skbs = kcalloc(TX_RING_SIZE,
                                 sizeof(struct sk_buff *),
                                 GFP_KERNEL);
    return 0;
}
```

---

## Hardware Offloading

Features to improve performance:

```c
/* Setup offload features */
ndev->features = NETIF_F_SG |           /* Scatter-gather */
                NETIF_F_IP_CSUM |       /* IPv4 checksum */
                NETIF_F_IPV6_CSUM |     /* IPv6 checksum */
                NETIF_F_TSO |           /* TCP segmentation */
                NETIF_F_GRO |           /* Generic receive offload */
                NETIF_F_RXCSUM;         /* RX checksum */

ndev->hw_features = ndev->features;
```

---

## Checksum Offload

```c
/* TX checksum offload */
if (skb->ip_summed == CHECKSUM_PARTIAL) {
    /* Hardware will calculate checksum */
    tx_desc->flags |= TX_CSUM_OFFLOAD;
}

/* RX checksum offload */
if (rx_status & RX_CSUM_DONE) {
    if (rx_status & RX_CSUM_OK)
        skb->ip_summed = CHECKSUM_UNNECESSARY;
    else
        skb->ip_summed = CHECKSUM_NONE;
}
```

---

## TSO (TCP Segmentation Offload)

```c
/* Enable TSO */
if (skb_is_gso(skb)) {
    tx_desc->mss = skb_shinfo(skb)->gso_size;
    tx_desc->flags |= TX_TSO_ENABLE;

    /* Setup headers */
    tx_desc->l3_offset = skb_network_offset(skb);
    tx_desc->l4_offset = skb_transport_offset(skb);
}
```

---

## Wireless Network Drivers

IEEE 802.11 stack integration:

```c
/* Allocate wireless device */
hw = ieee80211_alloc_hw(sizeof(struct my_priv),
                        &my_mac80211_ops);

/* Configure hardware */
hw->wiphy->interface_modes = BIT(NL80211_IFTYPE_STATION) |
                             BIT(NL80211_IFTYPE_AP);

/* Register with mac80211 */
ieee80211_register_hw(hw);
```

---

## MAC80211 Operations

```c
static const struct ieee80211_ops my_mac80211_ops = {
    .tx = my_mac80211_tx,
    .start = my_mac80211_start,
    .stop = my_mac80211_stop,
    .add_interface = my_mac80211_add_interface,
    .remove_interface = my_mac80211_remove_interface,
    .config = my_mac80211_config,
    .configure_filter = my_mac80211_configure_filter,
};
```

---

## Virtual Network Devices

Types of virtual devices:
- Bridge
- VLAN
- TUN/TAP
- Bonding
- VXLAN
- Macvlan

---

## TUN/TAP Driver

```c
/* TUN device operations */
static struct tun_struct {
    struct net_device *dev;
    struct file *file;
    struct fasync_struct *fasync;
};

/* Character device for userspace */
static const struct file_operations tun_fops = {
    .owner = THIS_MODULE,
    .read = tun_chr_read,
    .write = tun_chr_write,
    .poll = tun_chr_poll,
    .ioctl = tun_chr_ioctl,
    .open = tun_chr_open,
    .release = tun_chr_close,
};
```

---

## Network Statistics

```c
static struct net_device_stats *my_net_get_stats(
    struct net_device *ndev)
{
    struct my_priv *priv = netdev_priv(ndev);

    /* Update stats from hardware */
    ndev->stats.rx_errors = hw_read_rx_errors(priv);
    ndev->stats.tx_errors = hw_read_tx_errors(priv);
    ndev->stats.rx_dropped = hw_read_rx_dropped(priv);
    ndev->stats.tx_dropped = hw_read_tx_dropped(priv);

    return &ndev->stats;
}
```

---

## Debugging Network Drivers

Tools and techniques:

```bash
# Interface statistics
ip -s link show eth0
ifconfig eth0

# Ethtool diagnostics
ethtool -S eth0
ethtool -d eth0

# Kernel messages
dmesg | grep eth0

# Packet capture
tcpdump -i eth0
```

---

## Network Driver Tracing

```c
/* Add tracepoints */
#include <trace/events/net.h>

trace_net_dev_xmit(skb, rc, dev);
trace_netif_receive_skb(skb);

/* Custom tracepoints */
DEFINE_EVENT(net_dev_template, net_dev_queue,
    TP_PROTO(struct sk_buff *skb),
    TP_ARGS(skb));
```

---

## Performance Tuning

Optimization techniques:
1. Use NAPI for interrupt mitigation
1. Implement hardware offloading
1. Optimize ring buffer sizes
1. Use page pool API
1. CPU affinity for interrupts
1. RPS/RFS configuration

---

## Interrupt Coalescing

```c
/* Configure interrupt coalescing */
struct ethtool_coalesce {
    u32 rx_coalesce_usecs;    /* Delay in microseconds */
    u32 rx_max_coalesced_frames;  /* Frame count */
};

static int my_set_coalesce(struct net_device *ndev,
                           struct ethtool_coalesce *ec)
{
    struct my_priv *priv = netdev_priv(ndev);

    hw_set_coalesce(priv, ec->rx_coalesce_usecs,
                    ec->rx_max_coalesced_frames);

    return 0;
}
```

---

## Multi-Queue Support

```c
/* Allocate multi-queue device */
ndev = alloc_etherdev_mqs(sizeof(struct my_priv),
                          num_tx_queues,
                          num_rx_queues);

/* Select TX queue */
static u16 my_select_queue(struct net_device *ndev,
                           struct sk_buff *skb)
{
    /* Hash-based queue selection */
    u32 hash = skb_get_hash(skb);
    return hash % ndev->real_num_tx_queues;
}
```

---

## XDP (eXpress Data Path)

High-performance packet processing:

```c
static struct bpf_prog *xdp_prog;

static int my_xdp_handler(struct my_priv *priv,
                          struct xdp_buff *xdp)
{
    u32 act = bpf_prog_run_xdp(xdp_prog, xdp);

    switch (act) {
    case XDP_PASS:
        return my_receive_skb(priv, xdp);
    case XDP_DROP:
        return my_xdp_drop(priv, xdp);
    case XDP_TX:
        return my_xdp_xmit(priv, xdp);
    }
}
```

---

## Error Handling

```c
/* Handle TX timeout */
static void my_tx_timeout(struct net_device *ndev)
{
    struct my_priv *priv = netdev_priv(ndev);

    netdev_err(ndev, "TX timeout\n");

    /* Reset hardware */
    hw_reset(priv);

    /* Restart queue */
    netif_wake_queue(ndev);

    /* Update stats */
    ndev->stats.tx_errors++;
}
```

---

## Power Management

```c
static int my_net_suspend(struct device *dev)
{
    struct net_device *ndev = dev_get_drvdata(dev);

    if (netif_running(ndev)) {
        netif_device_detach(ndev);
        my_net_close(ndev);
    }

    return 0;
}

static int my_net_resume(struct device *dev)
{
    struct net_device *ndev = dev_get_drvdata(dev);

    if (netif_running(ndev)) {
        my_net_open(ndev);
        netif_device_attach(ndev);
    }

    return 0;
}
```

---

## Best Practices

1. Always use NAPI for receive path
1. Implement proper error handling
1. Support ethtool operations
1. Handle all SKB properly (no leaks)
1. Test with various packet sizes
1. Profile performance regularly
1. Document hardware quirks

---

## Summary

Network driver development requires:
- Understanding Linux network stack
- SKB management expertise
- Hardware knowledge
- Performance optimization skills

Key concepts:
- NAPI for interrupt mitigation
- Hardware offloading features
- Ring buffer management
- PHY and MDIO handling