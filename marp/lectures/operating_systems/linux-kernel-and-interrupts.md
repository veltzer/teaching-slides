---
tags:
- concepts:linux-kernel
- concepts:interrupts
- concepts:drivers
level: advanced
category: operating-systems
audience:
- audiences:developers

---
# Linux Driver Interrupt Numbers
## Mark Veltzer
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)

---

## Overview

![title](svg/lectures/operating_systems/linux-kernel-and-interrupts/title.svg)

---

## Overview: Details

1. Types of interrupts on various systems
1. Linux virtual interrupt numbering
1. Methods to obtain interrupt numbers in drivers
1. Code examples for each method

---

## Types of Interrupts - x86 APIC

1. **Legacy PIC (8259A)**
   - IRQ 0-15
   - Fixed routing
   - Limited scalability

1. **IOAPIC (I/O APIC)**
   - 24+ interrupt lines
   - Programmable routing
   - Supports multiple CPUs

---

## Types of Interrupts - Triggering Modes

1. **Edge-triggered**
   - Fires on signal transition
   - Can be lost if not handled quickly
   - Common for legacy devices

1. **Level-triggered**
   - Active as long as signal asserted
   - More reliable
   - Standard for PCI devices

---

## MSI/MSI-X Interrupts

1. **MSI (Message Signaled Interrupts)**
   - Memory write transaction
   - No dedicated interrupt lines
   - Up to 32 vectors

1. **MSI-X**
   - Extended MSI
   - Up to 2048 vectors
   - Per-vector masking

---

## ARM Interrupt Controllers

1. **GIC (Generic Interrupt Controller)**
   - SGI: Software Generated (0-15)
   - PPI: Private Peripheral (16-31)
   - SPI: Shared Peripheral (32-1019)

1. **GICv3/GICv4**
   - LPI: Locality-specific Peripheral
   - Support for virtualization

---

## Why Linux Virtual IRQ Numbers?

![why_linux_virtual_irq_numbers](svg/lectures/operating_systems/linux-kernel-and-interrupts/why_linux_virtual_irq_numbers.svg)

---

## Virtual IRQ Benefits

1. **Hardware Independence**
   - Same driver works on different platforms
   - No hardcoded assumptions

1. **Dynamic Allocation**
   - IRQs allocated at runtime
   - Support for hotplug devices

1. **Namespace Management**
   - Avoid conflicts
   - Per-domain numbering

---

## IRQ Domains

```c
struct irq_domain {
    struct list_head link;
    const char *name;
    const struct irq_domain_ops *ops;
    void *host_data;
    unsigned int flags;
    /* ... */
};
```

Maps hardware interrupt numbers to Linux IRQ numbers

---

## Case 1: Hardcoded IRQ Number

The simplest but least portable method

```c
#define MY_DEVICE_IRQ 42

static int my_driver_probe(struct platform_device *pdev)
{
    int irq = MY_DEVICE_IRQ;
    int ret;

    ret = request_irq(irq, my_irq_handler,
                      IRQF_SHARED, "my_device", dev);
    if (ret) {
        dev_err(&pdev->dev, "Failed to request IRQ %d\n", irq);
        return ret;
    }

    return 0;
}
```

---

## Hardcoded IRQ - When to Use

1. **Legacy embedded systems**
   - Fixed hardware configuration
   - No device tree or ACPI

1. **Board-specific drivers**
   - Known, unchanging hardware
   - Quick prototyping

1. **NOT recommended for**
   - Upstream Linux drivers
   - Multi-platform support

---

## Case 2: Platform Device Resources

Plug and play approach using platform data

```c
static int my_driver_probe(struct platform_device *pdev)
{
    struct resource *res;
    int irq;

    res = platform_get_resource(pdev, IORESOURCE_IRQ, 0);
    if (!res) {
        dev_err(&pdev->dev, "No IRQ resource\n");
        return -ENODEV;
    }

    irq = res->start;

    /* Alternative method */
    irq = platform_get_irq(pdev, 0);
    if (irq < 0)
        return irq;

    return request_irq(irq, my_irq_handler, 0, "my_device", pdev);
}
```

---

## Platform Device Registration

```c
static struct resource my_device_resources[] = {
    {
        .start = 10,
        .end   = 10,
        .flags = IORESOURCE_IRQ,
    },
};

static struct platform_device my_device = {
    .name           = "my_device",
    .id             = -1,
    .num_resources  = ARRAY_SIZE(my_device_resources),
    .resource       = my_device_resources,
};

platform_device_register(&my_device);
```

---

## Platform IRQ Best Practices

1. **Always use platform_get_irq()**
   - Handles error cases
   - Supports IRQ domains
   - Future-proof

1. **Check return values**
   ```c
   irq = platform_get_irq(pdev, 0);
   if (irq < 0)
       return irq; /* Propagate error */
   ```

1. **Support multiple IRQs**
   ```c
   irq = platform_get_irq(pdev, index);
   ```

---

## Case 3: ACPI Systems (x86/x64)

![case_3_acpi_systems_x86_x64](svg/lectures/operating_systems/linux-kernel-and-interrupts/case_3_acpi_systems_x86_x64.svg)

---

## ACPI Device Definition

```asl
Device (MYD0) {
    Name (_HID, "ACPI0001")
    Name (_CRS, ResourceTemplate() {
        Interrupt(ResourceConsumer, Edge, ActiveHigh, Exclusive) {
            0x20
        }
        Memory32Fixed(ReadWrite, 0xFED40000, 0x1000)
    })
}
```

---

## ACPI IRQ Retrieval in Driver

```c
static int my_acpi_probe(struct platform_device *pdev)
{
    struct acpi_device *adev;
    int irq;

    adev = ACPI_COMPANION(&pdev->dev);
    if (!adev) {
        dev_err(&pdev->dev, "No ACPI companion\n");
        return -ENODEV;
    }

    /* Method 1: Using platform_get_irq */
    irq = platform_get_irq(pdev, 0);
    if (irq < 0)
        return irq;

    return request_irq(irq, my_irq_handler,
                      IRQF_TRIGGER_RISING | IRQF_ONESHOT,
                      "my_acpi_device", pdev);
}
```

---

## ACPI IRQ Resources - Direct Access

```c
static int get_acpi_irq_resources(struct acpi_device *adev)
{
    struct list_head resource_list;
    struct resource_entry *entry;
    int irq = -1;

    INIT_LIST_HEAD(&resource_list);

    acpi_dev_get_resources(adev, &resource_list, NULL, NULL);

    resource_list_for_each_entry(entry, &resource_list) {
        struct resource *res = entry->res;

        if (resource_type(res) == IORESOURCE_IRQ) {
            irq = res->start;
            break;
        }
    }

    acpi_dev_free_resource_list(&resource_list);
    return irq;
}
```

---

## ACPI Match Table

```c
static const struct acpi_device_id my_acpi_match[] = {
    { "ACPI0001", 0 },
    { "PNP0501", 0 },
    { }
};
MODULE_DEVICE_TABLE(acpi, my_acpi_match);

static struct platform_driver my_driver = {
    .probe = my_acpi_probe,
    .driver = {
        .name = "my_acpi_driver",
        .acpi_match_table = ACPI_PTR(my_acpi_match),
    },
};
```

---

## Case 4: Device Tree Systems (ARM/PowerPC)

![case_4_device_tree_systems_arm_powerpc](svg/lectures/operating_systems/linux-kernel-and-interrupts/case_4_device_tree_systems_arm_powerpc.svg)

---

## Device Tree Interrupt Specification

```dts
/* GIC-based system */
my_device@10000000 {
    compatible = "vendor,my-device";
    reg = <0x10000000 0x1000>;
    interrupts = <GIC_SPI 25 IRQ_TYPE_LEVEL_HIGH>;
    interrupt-parent = <&gic>;
};

/* Legacy interrupt controller */
my_device@20000000 {
    compatible = "vendor,my-device";
    reg = <0x20000000 0x1000>;
    interrupts = <14 IRQ_TYPE_EDGE_RISING>;
};
```

---

## Device Tree IRQ Retrieval

```c
static int my_dt_probe(struct platform_device *pdev)
{
    struct device_node *np = pdev->dev.of_node;
    int irq;

    /* Method 1: Using platform_get_irq (recommended) */
    irq = platform_get_irq(pdev, 0);
    if (irq < 0) {
        dev_err(&pdev->dev, "Failed to get IRQ\n");
        return irq;
    }

    /* Method 2: Direct OF functions */
    irq = of_irq_get(np, 0);
    if (irq < 0)
        return irq;

    return request_irq(irq, my_irq_handler, 0,
                      dev_name(&pdev->dev), pdev);
}
```

---

## Device Tree IRQ Parsing Details

```c
/* Getting interrupt with names */
irq = of_irq_get_byname(np, "tx_irq");

/* Parsing interrupt properties manually */
struct of_phandle_args irq_data;
int ret;

ret = of_irq_parse_one(np, index, &irq_data);
if (ret)
    return ret;

irq = irq_create_of_mapping(&irq_data);
```

---

## Device Tree Match Table

```c
static const struct of_device_id my_dt_match[] = {
    { .compatible = "vendor,my-device", },
    { .compatible = "vendor,my-device-v2", },
    { }
};
MODULE_DEVICE_TABLE(of, my_dt_match);

static struct platform_driver my_driver = {
    .probe = my_dt_probe,
    .driver = {
        .name = "my_dt_driver",
        .of_match_table = of_match_ptr(my_dt_match),
    },
};
```

---

## Multiple Interrupts in Device Tree

```dts
my_device@30000000 {
    compatible = "vendor,my-device";
    reg = <0x30000000 0x1000>;
    interrupts = <GIC_SPI 10 IRQ_TYPE_LEVEL_HIGH>,
                 <GIC_SPI 11 IRQ_TYPE_LEVEL_HIGH>,
                 <GIC_SPI 12 IRQ_TYPE_LEVEL_HIGH>;
    interrupt-names = "rx", "tx", "error";
};
```

```c
/* In driver */
irq_rx = platform_get_irq_byname(pdev, "rx");
irq_tx = platform_get_irq_byname(pdev, "tx");
irq_err = platform_get_irq_byname(pdev, "error");
```

---

## Case 5: PCI/PCIe Devices

PCI devices have special interrupt handling

```c
static int my_pci_probe(struct pci_dev *pdev,
                       const struct pci_device_id *id)
{
    int ret;

    ret = pci_enable_device(pdev);
    if (ret)
        return ret;

    /* Legacy INTx interrupt */
    ret = request_irq(pdev->irq, my_irq_handler,
                     IRQF_SHARED, "my_pci_device", pdev);
    if (ret) {
        dev_err(&pdev->dev, "Failed to request IRQ\n");
        goto err_disable;
    }

    return 0;

err_disable:
    pci_disable_device(pdev);
    return ret;
}
```

---

## PCI MSI/MSI-X Interrupts

```c
static int setup_msi_interrupts(struct pci_dev *pdev)
{
    int ret, i;
    int nvec = 4; /* Request 4 MSI vectors */

    /* Try MSI-X first */
    ret = pci_alloc_irq_vectors(pdev, 1, nvec, PCI_IRQ_MSIX);
    if (ret < 0) {
        /* Fall back to MSI */
        ret = pci_alloc_irq_vectors(pdev, 1, nvec, PCI_IRQ_MSI);
        if (ret < 0) {
            /* Fall back to legacy */
            ret = pci_alloc_irq_vectors(pdev, 1, 1, PCI_IRQ_LEGACY);
            if (ret < 0)
                return ret;
        }
    }

    /* Request IRQ for each vector */
    for (i = 0; i < ret; i++) {
        int irq = pci_irq_vector(pdev, i);
        request_irq(irq, my_msi_handler, 0, "my_msi", pdev);
    }

    return 0;
}
```

---

## USB Device Interrupts

```c
static int my_usb_probe(struct usb_interface *intf,
                       const struct usb_device_id *id)
{
    struct usb_endpoint_descriptor *int_endpoint;
    struct urb *int_urb;
    int pipe;

    /* Find interrupt endpoint */
    int_endpoint = &intf->cur_altsetting->endpoint[0].desc;
    if (!usb_endpoint_is_int_in(int_endpoint))
        return -ENODEV;

    /* Allocate interrupt URB */
    int_urb = usb_alloc_urb(0, GFP_KERNEL);
    if (!int_urb)
        return -ENOMEM;

    pipe = usb_rcvintpipe(usb_dev, int_endpoint->bEndpointAddress);

    usb_fill_int_urb(int_urb, usb_dev, pipe,
                     int_buffer, buffer_size,
                     my_usb_int_callback, context,
                     int_endpoint->bInterval);

    /* Submit URB - this starts interrupt transfers */
    return usb_submit_urb(int_urb, GFP_KERNEL);
}
```

---

## I2C Device Interrupts

```c
static int my_i2c_probe(struct i2c_client *client,
                       const struct i2c_device_id *id)
{
    int irq;

    /* Get IRQ from I2C client */
    irq = client->irq;
    if (irq <= 0) {
        dev_err(&client->dev, "No IRQ configured\n");
        return -EINVAL;
    }

    /* Request threaded IRQ for I2C devices */
    return devm_request_threaded_irq(&client->dev, irq,
                                    NULL, /* Hard IRQ handler */
                                    my_i2c_irq_thread, /* Thread fn */
                                    IRQF_TRIGGER_FALLING | IRQF_ONESHOT,
                                    "my_i2c_device", client);
}
```

---

## SPI Device Interrupts

```c
static int my_spi_probe(struct spi_device *spi)
{
    int irq;

    /* Get IRQ from SPI device */
    irq = spi->irq;
    if (irq <= 0) {
        /* Try to get from device tree */
        irq = of_irq_get(spi->dev.of_node, 0);
        if (irq <= 0) {
            dev_err(&spi->dev, "No IRQ available\n");
            return -EINVAL;
        }
    }

    return devm_request_irq(&spi->dev, irq,
                           my_spi_irq_handler,
                           IRQF_TRIGGER_RISING,
                           "my_spi_device", spi);
}
```

---

## GPIO Interrupts

```c
static int setup_gpio_interrupt(struct platform_device *pdev)
{
    struct gpio_desc *gpio;
    int irq;

    /* Get GPIO from device tree */
    gpio = devm_gpiod_get(&pdev->dev, "interrupt", GPIOD_IN);
    if (IS_ERR(gpio))
        return PTR_ERR(gpio);

    /* Convert GPIO to IRQ */
    irq = gpiod_to_irq(gpio);
    if (irq < 0) {
        dev_err(&pdev->dev, "Failed to get IRQ from GPIO\n");
        return irq;
    }

    /* Request the IRQ */
    return devm_request_irq(&pdev->dev, irq,
                           my_gpio_irq_handler,
                           IRQF_TRIGGER_RISING | IRQF_TRIGGER_FALLING,
                           "my_gpio_irq", pdev);
}
```

---

## Interrupt Flags and Types

```c
/* Common IRQ flags */
#define IRQF_TRIGGER_RISING   0x00000001
#define IRQF_TRIGGER_FALLING  0x00000002
#define IRQF_TRIGGER_HIGH     0x00000004
#define IRQF_TRIGGER_LOW      0x00000008
#define IRQF_ONESHOT          0x00002000
#define IRQF_SHARED           0x00000080
#define IRQF_NO_THREAD        0x00010000

/* Example usage */
ret = request_irq(irq, handler,
                 IRQF_TRIGGER_RISING | IRQF_ONESHOT,
                 "my_device", dev);
```

---

## Threaded IRQ Handlers

```c
/* Top half - runs in hard IRQ context */
static irqreturn_t my_irq_handler(int irq, void *data)
{
    /* Minimal work - just acknowledge interrupt */
    iowrite32(IRQ_STATUS_CLEAR, base + IRQ_STATUS_REG);

    return IRQ_WAKE_THREAD; /* Wake bottom half */
}

/* Bottom half - runs in thread context */
static irqreturn_t my_irq_thread(int irq, void *data)
{
    /* Do the actual work here */
    process_interrupt_data(data);

    return IRQ_HANDLED;
}

/* Registration */
ret = request_threaded_irq(irq, my_irq_handler, my_irq_thread,
                          IRQF_ONESHOT, "my_device", dev);
```

---

## Managing IRQs with devm

```c
static int my_probe(struct platform_device *pdev)
{
    int irq, ret;

    irq = platform_get_irq(pdev, 0);
    if (irq < 0)
        return irq;

    /* Automatically freed on driver removal */
    ret = devm_request_irq(&pdev->dev, irq,
                          my_irq_handler,
                          IRQF_SHARED,
                          dev_name(&pdev->dev),
                          pdev);
    if (ret) {
        dev_err(&pdev->dev, "Failed to request IRQ\n");
        return ret;
    }

    /* No need to free IRQ in remove() */
    return 0;
}
```

---

## IRQ Debugging - /proc/interrupts

```bash
$ cat /proc/interrupts
           CPU0       CPU1       CPU2       CPU3
  0:         19          0          0          0   IO-APIC   2-edge      timer
  1:          0          0          0          9   IO-APIC   1-edge      i8042
  8:          0          0          0          1   IO-APIC   8-edge      rtc0
  9:          0          0          0          0   IO-APIC   9-fasteoi   acpi
 16:          0          0         28          0   IO-APIC  16-fasteoi   ehci_hcd:usb1
 23:         35          0          0          0   IO-APIC  23-fasteoi   ahci[0000:00:1f.2]
 40:          0          0          0          0   PCI-MSI 327680-edge      xhci_hcd
 41:      12853          0          0          0   PCI-MSI 512000-edge      ahci[0000:00:1f.2]
 42:          0      14293          0          0   PCI-MSI 409600-edge      eth0
```

---

## IRQ Debugging - /sys/kernel/debug/irq

```bash
# List all IRQ descriptors
$ ls /sys/kernel/debug/irq/irqs/

# View specific IRQ details
$ cat /sys/kernel/debug/irq/irqs/42
handler:  handle_edge_irq
device:   0000:00:1c.0
status:   0x00000000
istate:   0x00000000
ddepth:   0
wdepth:   0
dstate:   0x01401200
            IRQD_ACTIVATED
            IRQD_IRQ_STARTED
            IRQD_SINGLE_TARGET
node:     0
affinity: 0-3
effectiv: 2
domain:  PCI-MSI-0000:00:1c.0
```

---

## Common IRQ Problems and Solutions

1. **IRQ not firing**
   - Check device tree/ACPI configuration
   - Verify interrupt controller setup
   - Check trigger type (edge vs level)

1. **Spurious interrupts**
   - Ensure proper acknowledgment
   - Check electrical noise
   - Verify sharing compatibility

1. **IRQ storms**
   - Implement proper masking
   - Use IRQF_ONESHOT for level interrupts
   - Check hardware configuration

---

## Best Practices Summary

1. **Always use platform_get_irq() when possible**
   - Works with DT, ACPI, and platform data
   - Handles error cases properly

1. **Use devm_* functions**
   - Automatic cleanup
   - Prevents resource leaks

1. **Choose appropriate IRQ flags**
   - IRQF_SHARED for PCI devices
   - IRQF_ONESHOT for threaded handlers
   - Correct trigger type

1. **Handle errors properly**
   - Check all return values
   - Clean up on failure

---

## Performance Considerations

1. **Hard vs Soft IRQ**
   - Keep hard IRQ handler minimal
   - Defer work to bottom halves

1. **IRQ Affinity**
   ```bash
   echo 2 > /proc/irq/42/smp_affinity_list
   ```

1. **NAPI for Network Drivers**
   - Polling under high load
   - Reduces interrupt overhead

1. **Coalescing**
   - Batch interrupts when possible
   - Balance latency vs throughput

---

## Modern IRQ APIs

```c
/* Generic IRQ chip */
struct irq_chip_generic *gc;
gc = irq_alloc_generic_chip("my_irq", 1, irq_base,
                           base, handle_level_irq);

/* IRQ domains for dynamic allocation */
struct irq_domain *domain;
domain = irq_domain_add_linear(node, nr_irqs,
                              &irq_domain_simple_ops, NULL);

/* Hierarchical domains */
domain = irq_domain_create_hierarchy(parent_domain, 0, nr_irqs,
                                   fwnode, &my_domain_ops, data);
```

---

## Summary

1. **Multiple methods to obtain IRQ numbers**
   - Hardcoded (avoid)
   - Platform resources
   - ACPI
   - Device Tree
   - Bus-specific methods

1. **Linux virtualizes IRQ numbers**
   - Hardware independence
   - Dynamic allocation
   - Better resource management

1. **Always use highest-level API available**
   - platform_get_irq() for most cases
   - Bus-specific helpers when needed
