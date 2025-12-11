# Direct Memory Access (DMA)

---

## DMA Overview

Direct Memory Access enables:
- Hardware to access memory without CPU
- High-speed data transfers
- Reduced CPU overhead
- Parallel I/O operations

Key benefit: CPU can perform other tasks during transfers

---

## DMA vs PIO

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
<text x="400" y="30" text-anchor="middle" font-weight="bold">PIO vs DMA Transfer</text>
<g id="pio">
<text x="200" y="70">PIO:</text>
<rect x="100" y="90" width="80" height="60" fill="#FFE6E6" stroke="black"/>
<text x="140" y="125" text-anchor="middle">CPU</text>
<rect x="100" y="200" width="80" height="60" fill="#E6F2FF" stroke="black"/>
<text x="140" y="235" text-anchor="middle">Memory</text>
<rect x="250" y="200" width="80" height="60" fill="#E6FFE6" stroke="black"/>
<text x="290" y="235" text-anchor="middle">Device</text>
<line x1="140" y1="150" x2="140" y2="200" stroke="red" stroke-width="2" marker-end="url(#redarrow)"/>
<line x1="140" y1="150" x2="290" y2="200" stroke="red" stroke-width="2" marker-end="url(#redarrow)"/>
</g>
<g id="dma">
<text x="500" y="70">DMA:</text>
<rect x="450" y="90" width="80" height="60" fill="#FFE6E6" stroke="black"/>
<text x="490" y="125" text-anchor="middle">CPU</text>
<rect x="400" y="200" width="80" height="60" fill="#E6F2FF" stroke="black"/>
<text x="440" y="235" text-anchor="middle">Memory</text>
<rect x="550" y="200" width="80" height="60" fill="#E6FFE6" stroke="black"/>
<text x="590" y="235" text-anchor="middle">Device</text>
<line x1="480" y1="230" x2="550" y2="230" stroke="green" stroke-width="3" marker-end="url(#greenarrow)"/>
<text x="490" y="170" fill="gray">CPU Idle</text>
</g>
<defs>
<marker id="redarrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
<polygon points="0 0, 10 3, 0 6" fill="red"/>
</marker>
<marker id="greenarrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
<polygon points="0 0, 10 3, 0 6" fill="green"/>
</marker>
</defs>
</svg>

---

## DMA Types

Two main categories:

**Coherent DMA** (Consistent)
- CPU and device see same data
- No cache management needed
- Higher overhead allocation

**Streaming DMA**
- Requires explicit synchronization
- Better performance
- Cache management required

---

## DMA Mapping API

```c
#include <linux/dma-mapping.h>

/* Set DMA mask */
if (dma_set_mask_and_coherent(&pdev->dev, DMA_BIT_MASK(32))) {
    dev_err(&pdev->dev, "No suitable DMA mask\n");
    return -EINVAL;
}
```

---

## Coherent DMA Allocation

```c
/* Allocate coherent DMA buffer */
void *cpu_addr;
dma_addr_t dma_handle;

cpu_addr = dma_alloc_coherent(&pdev->dev,
                              size,
                              &dma_handle,
                              GFP_KERNEL);
if (!cpu_addr)
    return -ENOMEM;

/* Use buffer */
memset(cpu_addr, 0, size);

/* Program device with dma_handle */
writel(dma_handle, dev->dma_addr_reg);

/* Free when done */
dma_free_coherent(&pdev->dev, size,
                 cpu_addr, dma_handle);
```

---

## Streaming DMA Mapping

```c
/* Map single buffer */
dma_addr_t dma_addr;

dma_addr = dma_map_single(&pdev->dev,
                         buffer,
                         size,
                         DMA_TO_DEVICE);

if (dma_mapping_error(&pdev->dev, dma_addr))
    return -ENOMEM;

/* Start DMA transfer */
start_dma_transfer(dma_addr, size);

/* Unmap after transfer */
dma_unmap_single(&pdev->dev,
                dma_addr,
                size,
                DMA_TO_DEVICE);
```

---

## DMA Direction

```c
enum dma_data_direction {
    DMA_BIDIRECTIONAL = 0,  /* Both directions */
    DMA_TO_DEVICE = 1,      /* Memory to device */
    DMA_FROM_DEVICE = 2,    /* Device to memory */
    DMA_NONE = 3,           /* Debug only */
};
```

---

## Scatter-Gather DMA

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
<text x="400" y="30" text-anchor="middle" font-weight="bold">Scatter-Gather DMA</text>
<rect x="100" y="80" width="100" height="40" fill="#FFE6E6" stroke="black"/>
<text x="150" y="105" text-anchor="middle">Buffer 1</text>
<rect x="100" y="140" width="150" height="40" fill="#E6F2FF" stroke="black"/>
<text x="175" y="165" text-anchor="middle">Buffer 2</text>
<rect x="100" y="200" width="80" height="40" fill="#E6FFE6" stroke="black"/>
<text x="140" y="225" text-anchor="middle">Buffer 3</text>
<rect x="100" y="260" width="120" height="40" fill="#FFFFE6" stroke="black"/>
<text x="160" y="285" text-anchor="middle">Buffer 4</text>
<rect x="450" y="140" width="250" height="100" fill="#FFE6FF" stroke="black"/>
<text x="575" y="195" text-anchor="middle">DMA Controller</text>
<line x1="200" y1="100" x2="450" y2="165" stroke="black" marker-end="url(#arrow)"/>
<line x1="250" y1="160" x2="450" y2="180" stroke="black" marker-end="url(#arrow)"/>
<line x1="180" y1="220" x2="450" y2="195" stroke="black" marker-end="url(#arrow)"/>
<line x1="220" y1="280" x2="450" y2="215" stroke="black" marker-end="url(#arrow)"/>
<defs>
<marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
<polygon points="0 0, 10 3, 0 6"/>
</marker>
</defs>
</svg>

---

## Scatter-Gather Mapping

```c
/* Map scatter-gather list */
struct scatterlist *sg;
int i, count;

count = dma_map_sg(&pdev->dev,
                  sg_list,
                  nents,
                  DMA_TO_DEVICE);

if (!count)
    return -ENOMEM;

/* Iterate mapped entries */
for_each_sg(sg_list, sg, count, i) {
    dma_addr_t addr = sg_dma_address(sg);
    unsigned int len = sg_dma_len(sg);

    /* Program DMA controller */
    setup_dma_descriptor(addr, len);
}

/* Unmap after transfer */
dma_unmap_sg(&pdev->dev, sg_list,
            nents, DMA_TO_DEVICE);
```

---

## DMA Engine Framework

```c
#include <linux/dmaengine.h>

/* Request DMA channel */
struct dma_chan *chan;

chan = dma_request_chan(&pdev->dev, "tx");
if (IS_ERR(chan))
    return PTR_ERR(chan);

/* Prepare transfer */
struct dma_async_tx_descriptor *desc;

desc = dmaengine_prep_slave_single(chan,
                                   dma_addr,
                                   size,
                                   DMA_MEM_TO_DEV,
                                   flags);

/* Submit transfer */
dmaengine_submit(desc);
dma_async_issue_pending(chan);
```

---

## DMA Slave Configuration

```c
struct dma_slave_config config = {
    .direction = DMA_MEM_TO_DEV,
    .src_addr_width = DMA_SLAVE_BUSWIDTH_4_BYTES,
    .dst_addr_width = DMA_SLAVE_BUSWIDTH_4_BYTES,
    .src_maxburst = 16,
    .dst_maxburst = 16,
    .dst_addr = dev->fifo_addr,
};

dmaengine_slave_config(chan, &config);
```

---

## DMA Callbacks

```c
static void dma_complete(void *param)
{
    struct my_device *dev = param;

    /* Handle completion */
    dev->dma_done = true;
    wake_up(&dev->wait_queue);
}

/* Setup callback */
desc->callback = dma_complete;
desc->callback_param = dev;

/* Submit and wait */
dmaengine_submit(desc);
dma_async_issue_pending(chan);
wait_event(dev->wait_queue, dev->dma_done);
```

---

## Cyclic DMA

For continuous transfers (audio, video):

```c
/* Prepare cyclic transfer */
desc = dmaengine_prep_dma_cyclic(chan,
                                 dma_addr,
                                 buf_len,
                                 period_len,
                                 DMA_MEM_TO_DEV,
                                 DMA_PREP_INTERRUPT);

/* Callback called for each period */
desc->callback = audio_dma_callback;
desc->callback_param = audio_dev;

dmaengine_submit(desc);
dma_async_issue_pending(chan);
```

---

## DMA Synchronization

```c
/* Sync for CPU access */
dma_sync_single_for_cpu(&pdev->dev,
                       dma_addr,
                       size,
                       DMA_FROM_DEVICE);

/* Access buffer */
process_data(buffer);

/* Sync for device access */
dma_sync_single_for_device(&pdev->dev,
                           dma_addr,
                           size,
                           DMA_FROM_DEVICE);
```

---

## DMA Pools

For small, frequent allocations:

```c
/* Create DMA pool */
struct dma_pool *pool;

pool = dma_pool_create("my_pool",
                      &pdev->dev,
                      size,
                      align,
                      boundary);

/* Allocate from pool */
void *vaddr = dma_pool_alloc(pool,
                            GFP_KERNEL,
                            &dma_addr);

/* Free to pool */
dma_pool_free(pool, vaddr, dma_addr);

/* Destroy pool */
dma_pool_destroy(pool);
```

---

## IOMMU Integration

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
<rect x="100" y="100" width="150" height="80" fill="#FFE6E6" stroke="black"/>
<text x="175" y="145" text-anchor="middle">Device</text>
<rect x="350" y="100" width="150" height="80" fill="#E6F2FF" stroke="black"/>
<text x="425" y="145" text-anchor="middle">IOMMU</text>
<rect x="600" y="100" width="150" height="80" fill="#E6FFE6" stroke="black"/>
<text x="675" y="145" text-anchor="middle">Memory</text>
<line x1="250" y1="140" x2="350" y2="140" stroke="black" stroke-width="2" marker-end="url(#arrowhead)"/>
<line x1="500" y1="140" x2="600" y2="140" stroke="black" stroke-width="2" marker-end="url(#arrowhead)"/>
<text x="175" y="220">Virtual Address</text>
<text x="425" y="220">Translation</text>
<text x="675" y="220">Physical Address</text>
<defs>
<marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
<polygon points="0 0, 10 3, 0 6"/>
</marker>
</defs>
</svg>

---

## IOMMU Benefits

- Memory protection
- Virtual addressing for devices
- Scatter-gather without hardware support
- Address space isolation
- 32-bit devices accessing >4GB memory

---

## DMA Attributes

```c
/* Special DMA attributes */
unsigned long attrs = 0;

/* Skip CPU cache sync */
attrs |= DMA_ATTR_SKIP_CPU_SYNC;

/* Weak ordering */
attrs |= DMA_ATTR_WEAK_ORDERING;

/* No kernel mapping */
attrs |= DMA_ATTR_NO_KERNEL_MAPPING;

/* Allocate with attributes */
cpu_addr = dma_alloc_attrs(&pdev->dev,
                          size,
                          &dma_handle,
                          GFP_KERNEL,
                          attrs);
```

---

## Bounce Buffers

For devices with limited DMA capability:

```c
/* System automatically uses bounce buffers
   when needed based on DMA mask */

/* Set 32-bit DMA mask */
dma_set_mask(&pdev->dev, DMA_BIT_MASK(32));

/* Kernel handles bouncing for memory > 4GB */
```

---

## DMA Debugging

Enable DMA-API debugging:

```bash
# Kernel config
CONFIG_DMA_API_DEBUG=y

# Boot parameter
dma_debug=on

# Runtime control
echo 1 > /sys/kernel/debug/dma-api/disabled
```

---

## Common DMA Errors

```c
/* Check for mapping errors */
dma_addr = dma_map_single(&pdev->dev,
                         buf, size,
                         DMA_TO_DEVICE);

if (dma_mapping_error(&pdev->dev, dma_addr)) {
    dev_err(&pdev->dev, "DMA mapping failed\n");
    return -ENOMEM;
}

/* Always unmap */
dma_unmap_single(&pdev->dev,
                dma_addr, size,
                DMA_TO_DEVICE);
```

---

## DMA Constraints

Platform-specific limitations:

```c
/* Check DMA constraints */
struct device *dev = &pdev->dev;

dev_info(dev, "DMA mask: %llx\n",
         dma_get_mask(dev));

dev_info(dev, "Coherent mask: %llx\n",
         dev->coherent_dma_mask);

dev_info(dev, "Max segment size: %u\n",
         dma_get_max_seg_size(dev));
```

---

## Page-based DMA

```c
/* Map pages for DMA */
struct page *page = virt_to_page(buffer);
dma_addr_t dma_addr;

dma_addr = dma_map_page(&pdev->dev,
                       page,
                       offset,
                       size,
                       DMA_TO_DEVICE);

/* Unmap page */
dma_unmap_page(&pdev->dev,
              dma_addr,
              size,
              DMA_TO_DEVICE);
```

---

## DMA Controller Driver

```c
static int my_dma_probe(struct platform_device *pdev)
{
    struct dma_device *dma_dev;

    dma_dev = devm_kzalloc(&pdev->dev,
                          sizeof(*dma_dev),
                          GFP_KERNEL);

    /* Setup capabilities */
    dma_cap_set(DMA_MEMCPY, dma_dev->cap_mask);
    dma_cap_set(DMA_SLAVE, dma_dev->cap_mask);

    /* Setup operations */
    dma_dev->device_prep_dma_memcpy = my_prep_memcpy;
    dma_dev->device_prep_slave_sg = my_prep_slave_sg;
    dma_dev->device_issue_pending = my_issue_pending;
    dma_dev->device_tx_status = my_tx_status;

    /* Register controller */
    dma_async_device_register(dma_dev);

    return 0;
}
```

---

## Descriptor Management

```c
struct my_dma_desc {
    struct dma_async_tx_descriptor async;
    struct list_head node;

    /* Hardware descriptor */
    dma_addr_t src;
    dma_addr_t dst;
    u32 len;
    u32 control;
};

static struct dma_async_tx_descriptor *
my_prep_memcpy(struct dma_chan *chan,
              dma_addr_t dst, dma_addr_t src,
              size_t len, unsigned long flags)
{
    struct my_dma_desc *desc;

    desc = my_alloc_desc();
    desc->src = src;
    desc->dst = dst;
    desc->len = len;

    return &desc->async;
}
```

---

## DMA Performance Tips

1. Use appropriate DMA type
    - Coherent for control structures
    - Streaming for data buffers
1. Minimize synchronization points
1. Use scatter-gather when possible
1. Align buffers to cache lines
1. Batch DMA operations

---

## Cache Coherency

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
<text x="400" y="30" text-anchor="middle" font-weight="bold">Cache Coherency Issues</text>
<rect x="150" y="80" width="120" height="60" fill="#FFE6E6" stroke="black"/>
<text x="210" y="115" text-anchor="middle">CPU Cache</text>
<rect x="530" y="80" width="120" height="60" fill="#E6F2FF" stroke="black"/>
<text x="590" y="115" text-anchor="middle">Device</text>
<rect x="340" y="200" width="120" height="60" fill="#E6FFE6" stroke="black"/>
<text x="400" y="235" text-anchor="middle">Memory</text>
<line x1="210" y1="140" x2="400" y2="200" stroke="red" stroke-width="2"/>
<line x1="590" y1="140" x2="400" y2="200" stroke="blue" stroke-width="2"/>
<text x="120" y="180" fill="red">Cached data</text>
<text x="520" y="180" fill="blue">Direct access</text>
<text x="400" y="300">Potential data inconsistency!</text>
</svg>

---

## Memory Barriers

```c
/* DMA memory barriers */

/* Ensure writes complete before DMA */
wmb();
start_dma_transfer();

/* Ensure DMA completes before reading */
wait_for_dma_complete();
rmb();
read_dma_buffer();

/* Full barrier */
mb();
```

---

## Device Tree DMA

```dts
dma-controller@40000000 {
    compatible = "vendor,dma";
    reg = <0x40000000 0x1000>;
    interrupts = <17>;
    #dma-cells = <1>;
    dma-channels = <8>;
};

device@50000000 {
    compatible = "vendor,device";
    dmas = <&dma 2>, <&dma 3>;
    dma-names = "tx", "rx";
};
```

---

## DMA Channel Allocation

```c
/* Get DMA channel from DT */
struct dma_chan *chan;

chan = dma_request_chan(&pdev->dev, "tx");
if (IS_ERR(chan)) {
    /* Fallback to manual allocation */
    dma_cap_mask_t mask;
    dma_cap_zero(mask);
    dma_cap_set(DMA_SLAVE, mask);

    chan = dma_request_channel(mask,
                              filter_fn,
                              filter_param);
}
```

---

## DMA Test Module

```c
static int dma_test_init(void)
{
    void *src, *dst;
    dma_addr_t src_dma, dst_dma;

    /* Allocate test buffers */
    src = dma_alloc_coherent(dev, PAGE_SIZE,
                            &src_dma, GFP_KERNEL);
    dst = dma_alloc_coherent(dev, PAGE_SIZE,
                            &dst_dma, GFP_KERNEL);

    /* Fill source */
    memset(src, 0xAA, PAGE_SIZE);

    /* Perform DMA */
    desc = dmaengine_prep_dma_memcpy(chan,
                                    dst_dma,
                                    src_dma,
                                    PAGE_SIZE,
                                    0);
    dmaengine_submit(desc);
    dma_async_issue_pending(chan);

    /* Verify */
    if (memcmp(src, dst, PAGE_SIZE) == 0)
        pr_info("DMA test passed\n");

    return 0;
}
```

---

## Profiling DMA

```bash
# Monitor DMA usage
cat /sys/kernel/debug/dmaengine/summary

# Per-channel statistics
cat /sys/class/dma/dma0chan0/in_use
cat /sys/class/dma/dma0chan0/bytes_transferred

# Trace DMA operations
echo 1 > /sys/kernel/debug/tracing/events/dmaengine/enable
cat /sys/kernel/debug/tracing/trace
```

---

## DMA vs CPU Performance

When to use DMA:
- Large transfers (> 1KB typically)
- CPU needs to do other work
- Hardware supports it efficiently

When to avoid:
- Small transfers (overhead > benefit)
- Infrequent transfers
- Complex setup requirements

---

## Security Considerations

DMA security issues:
1. DMA attacks (DMA from untrusted devices)
1. Memory isolation violations
1. Information leakage

Mitigations:
- IOMMU usage
- DMA restricted zones
- Proper unmapping

---

## Best Practices

1. Always check for errors
1. Properly unmap all mappings
1. Use correct DMA direction
1. Handle DMA mask properly
1. Test on various platforms
1. Profile actual performance
1. Document hardware requirements

---

## Summary

DMA is essential for:
- High-performance I/O
- Reduced CPU overhead
- Power efficiency
- Real-time requirements

Key concepts:
- Coherent vs streaming DMA
- DMA engine framework
- IOMMU benefits
- Proper synchronization