# Network Device Overview
## Chapter 6: Device Drivers and Network Stack Integration

---

## Chapter Overview

- Socket Buffer Management (`sk_buff`)
- Network Device Structure
- Driver Registration
- Private Data Handling
- Device Operations
- Interrupt Management
- Memory Mapping

---
## Socket Buffer (`sk_buff`)

```c
struct sk_buff {
    struct sk_buff      *next;
    struct sk_buff      *prev;
    struct sock         *sk;
    struct net_device   *dev;
    unsigned int         len;
    unsigned char       *data;
    unsigned char       *head;
    unsigned char       *tail;
    unsigned char       *end;
    // ... more fields
};
```

---

## SK Buffer Layout

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_05_network_devices)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_05_network_devices)"/>
  <defs>
    <marker id="arrowd0_05_network_devices" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## SK Buffer Management Functions

```c
// Allocation
struct sk_buff *skb = alloc_skb(len, GFP_KERNEL);

// Reserve space
skb_reserve(skb, header_len);

// Add data at tail
unsigned char *data = skb_put(skb, len);

// Add data at head
unsigned char *data = skb_push(skb, len);

// Remove data from head
unsigned char *data = skb_pull(skb, len);
```

---

## The net_device Structure

```c
struct net_device {
    char                name[IFNAMSIZ];
    unsigned long       state;
    struct net_device_stats stats;
    const struct net_device_ops *netdev_ops;
    const struct ethtool_ops   *ethtool_ops;
    unsigned int        flags;
    unsigned int        features;
    unsigned int        mtu;
    unsigned char       addr_len;
    unsigned char       *dev_addr;
    void               *priv;
};
```

---

## Network Device States

```c
// Device states
#define __LINK_STATE_START       0
#define __LINK_STATE_PRESENT    1
#define __LINK_STATE_NOCARRIER  2
#define __LINK_STATE_LINKWATCH_PENDING 3
#define __LINK_STATE_DORMANT    4
```

---

## Device Operations Structure

```c
const struct net_device_ops my_netdev_ops = {
    .ndo_open            = my_open,
    .ndo_stop           = my_stop,
    .ndo_start_xmit     = my_start_xmit,
    .ndo_get_stats      = my_get_stats,
    .ndo_set_mac_address = my_set_mac,
    .ndo_do_ioctl       = my_ioctl,
};
```

---

## Registering Network Driver

```c
static int my_init(void)
{
    struct net_device *dev;

    dev = alloc_etherdev(sizeof(struct my_priv));
    if (!dev)
        return -ENOMEM;

    dev->netdev_ops = &my_netdev_ops;
    dev->ethtool_ops = &my_ethtool_ops;

    return register_netdev(dev);
}
```

---

## Private Data Management

```c
struct my_priv {
    void __iomem *base_addr;
    spinlock_t lock;
    int status;
    struct napi_struct napi;
    // ... device specific data
};

// Get private data
struct my_priv *priv = netdev_priv(dev);
```

---

## Open Operation

```c
static int my_open(struct net_device *dev)
{
    struct my_priv *priv = netdev_priv(dev);

    // Initialize hardware
    if (init_hardware(priv) < 0)
        return -EIO;

    // Start tx queue
    netif_start_queue(dev);

    // Enable interrupts
    enable_irq(dev->irq);

    return 0;
}
```

---

## Stop Operation

```c
static int my_stop(struct net_device *dev)
{
    struct my_priv *priv = netdev_priv(dev);

    // Disable interrupts
    disable_irq(dev->irq);

    // Stop tx queue
    netif_stop_queue(dev);

    // Cleanup hardware
    cleanup_hardware(priv);

    return 0;
}
```

---

## Transmission Function

```c
static netdev_tx_t my_start_xmit(struct sk_buff *skb,
                                struct net_device *dev)
{
    struct my_priv *priv = netdev_priv(dev);

    // Check if queue is full
    if (tx_ring_full(priv)) {
        netif_stop_queue(dev);
        return NETDEV_TX_BUSY;
    }

    // Copy data to tx ring
    copy_to_tx_ring(priv, skb);

    // Free skb
    dev_kfree_skb(skb);

    return NETDEV_TX_OK;
}
```

---

## Interrupt Handling

```c
static irqreturn_t my_interrupt(int irq, void *dev_id)
{
    struct net_device *dev = dev_id;
    struct my_priv *priv = netdev_priv(dev);

    // Disable device interrupts
    disable_device_interrupts(priv);

    // Schedule NAPI poll
    napi_schedule(&priv->napi);

    return IRQ_HANDLED;
}
```

---

## NAPI Implementation

```c
static int my_poll(struct napi_struct *napi, int budget)
{
    struct my_priv *priv = container_of(napi,
                                      struct my_priv, napi);
    int work_done = 0;

    while (work_done < budget) {
        // Process received packets
        if (!process_rx(priv))
            break;
        work_done++;
    }

    // If all work done, exit polling
    if (work_done < budget) {
        napi_complete(napi);
        enable_device_interrupts(priv);
    }

    return work_done;
}
```

---

## Interrupt Mitigation

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_05_network_devices)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_05_network_devices)"/>
  <defs>
    <marker id="arrowd1_05_network_devices" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Memory Mapping

```c
struct my_priv {
    void __iomem *base_addr;
    // ... other fields
};

static int my_probe(struct pci_dev *pdev)
{
    struct my_priv *priv;

    // Map device memory
    priv->base_addr = ioremap(pci_resource_start(pdev, 0),
                             pci_resource_len(pdev, 0));
    if (!priv->base_addr)
        return -ENOMEM;
}
```

---

## DMA Operations

```c
// Allocate DMA buffer
dma_addr_t dma_handle;
void *buffer = dma_alloc_coherent(&pdev->dev,
                                 size,
                                 &dma_handle,
                                 GFP_KERNEL);

// Free DMA buffer
dma_free_coherent(&pdev->dev, size,
                  buffer, dma_handle);
```

---

## Statistics Handling

```c
static struct net_device_stats *my_get_stats(struct net_device *dev)
{
    struct my_priv *priv = netdev_priv(dev);

    // Update statistics from hardware
    update_statistics(priv);

    return &dev->stats;
}
```

---

## Ethtool Operations

```c
static const struct ethtool_ops my_ethtool_ops = {
    .get_drvinfo = my_get_drvinfo,
    .get_link = ethtool_op_get_link,
    .get_ringparam = my_get_ringparam,
    .set_ringparam = my_set_ringparam,
    .get_strings = my_get_strings,
    .get_ethtool_stats = my_get_ethtool_stats,
};
```

---

## Best Practices

1. Proper error handling
1. Resource cleanup
1. Interrupt management
1. Memory management
1. Performance optimization
1. Statistics maintenance
1. Documentation

---

## Common Pitfalls

1. Memory leaks
1. Race conditions
1. Interrupt handling issues
1. DMA errors
1. Resource cleanup
1. Buffer management
1. Performance issues

---

## Summary

- Socket buffer management
- Device initialization
- Data transmission
- Interrupt handling
- Memory operations
- Statistics tracking
