---
tags:
- concepts:virtualization
- concepts:linux-kernel
- concepts:io
level: advanced
category: operating-systems
audience:
- audiences:developers

---
# Understanding Linux Virtio and Queue Management
## Mark Veltzer
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)

---

## What is Virtio

![title](svg/lectures/operating_systems/virtio/title.svg)

---

## What is Virtio

- Standard for virtual device interfaces
- Efficient I/O virtualization
- Common framework for hypervisors
- Developed by Rusty Russell at IBM

---

## Key Components of Virtio

1. Frontend (Guest Driver)
1. Backend (Host Driver)
1. Transport Layer
1. Virtual Queues

---

## Virtio Device Types

- Network (virtio-net)
- Block (virtio-blk)
- Console (virtio-console)
- RNG (virtio-rng)
- GPU (virtio-gpu)
- Input (virtio-input)

---

## Basic Virtio Architecture

```c
struct virtio_device {
    struct device dev;
    struct virtio_config_ops *config;
    struct virtqueue *vqs;
    u64 features;
    void *priv;
};
```

---

## Virtqueues Overview

- Circular buffer for I/O requests
- Shared between guest and host
- Split virtqueue design
- Packed virtqueue design (newer)

---

## Split Virtqueue Structure

```c
struct virtqueue {
    struct virtio_device *vdev;
    unsigned int index;
    void (*callback)(struct virtqueue *vq);
    const char *name;
    struct virtring vring;
    void *priv;
};
```

---

## Virtring Components

```c
struct virtring {
    unsigned int num;
    struct vring_desc *desc;
    struct vring_avail *avail;
    struct vring_used *used;
};
```

---

## Descriptor Table Structure

```c
struct vring_desc {
    __le64 addr;     /* Buffer address */
    __le32 len;      /* Buffer length */
    __le16 flags;    /* Descriptor flags */
    __le16 next;     /* Next descriptor if flags & NEXT */
};
```

---

## Available Ring Structure

```c
struct vring_avail {
    __le16 flags;
    __le16 idx;
    __le16 ring[];
};
```

---

## Used Ring Structure

```c
struct vring_used {
    __le16 flags;
    __le16 idx;
    struct vring_used_elem ring[];
};
```

---

## Initializing a Virtqueue

```c
int virtqueue_add_sgs(struct virtqueue *vq,
                     struct scatterlist *sgs[],
                     unsigned int out_num,
                     unsigned int in_num,
                     void *data,
                     gfp_t gfp)
{
    unsigned int i, total_sg = out_num + in_num;
    struct scatterlist *sg;
    struct vring_desc *desc;

    /* Initialize descriptors */
    for (i = 0; i < total_sg; i++) {
        /* Setup descriptor chain */
    }

    return 0;
}
```

---

## Adding Buffers to Queue

```c
static inline void virtqueue_add_buff(struct virtqueue *vq,
                                    struct scatterlist *sg,
                                    unsigned int out,
                                    unsigned int in,
                                    void *data)
{
    /* Add buffer to virtqueue */
    vq->vq_ops->add_buf(vq, sg, out, in, data);
}
```

---

## Notifying the Host

```c
static inline void virtqueue_kick(struct virtqueue *vq)
{
    if (virtqueue_kick_prepare(vq))
        vq->vq_ops->kick(vq);
}
```

---

## Processing Used Buffers

```c
void vring_interrupt(int irq, void *_vq)
{
    struct virtqueue *vq = _vq;

    if (!vq->vq_ops->get_buf(vq, &len))
        return;

    /* Process completed buffer */
    vq->callback(vq);
}
```

---

## Packed Virtqueues

- Modern alternative to split virtqueues
- More efficient memory usage
- Better cache locality
- Introduced in virtio 1.1

---

## Packed Virtqueue Structure

```c
struct virtqueue_packed {
    struct virtqueue vq;
    struct packed_desc *desc;
    __le16 *driver_event;
    __le16 *device_event;
    unsigned int num_desc;
};
```

---

## Memory Barrier Usage

```c
/* Ensure descriptor updates are visible */
static inline void virtio_mb(struct virtio_device *vdev)
{
    mb();
}

/* Ensure availability ring update is visible */
static inline void virtio_wmb(struct virtio_device *vdev)
{
    wmb();
}
```

---

## Error Handling

```c
static int virtio_dev_probe(struct virtio_device *vdev)
{
    int err;

    err = setup_vqs(vdev);
    if (err)
        goto err_setup_vqs;

    return 0;

err_setup_vqs:
    cleanup_vqs(vdev);
    return err;
}
```

---

## DMA Mapping

```c
static int virtqueue_map_sg(struct virtqueue *vq,
                          struct scatterlist *sg,
                          unsigned int nents,
                          enum dma_data_direction direction)
{
    return dma_map_sg(vq->vdev->dev.parent, sg, nents, direction);
}
```

---

## Zero-Copy Operations

```c
static bool try_zero_copy_tx(struct virtnet_info *vi,
                           struct sk_buff *skb)
{
    struct page *page = virt_to_head_page(skb->data);
    return page_ref_count(page) == 1;
}
```

---

## Performance Optimization

- Batch operations when possible
- Use indirect descriptors for large transfers
- Implement proper memory barriers
- Monitor queue depth

---

## Debugging Tools

- virtio-trace
- ftrace events
- perf tools
- QEMU monitor

---

## Best Practices

1. Proper error handling
1. Memory barrier usage
1. Resource cleanup
1. Queue sizing
1. Buffer management

---

## Common Pitfalls

1. Missing memory barriers
1. Incorrect descriptor chaining
1. Buffer overflow
1. Resource leaks
1. Race conditions

---

## Future Developments

- Enhanced zero-copy support
- New device types
- Performance improvements
- Security features

---

## Resources

- Virtio Specification
- Linux Kernel Documentation
- QEMU Documentation
- KVM Documentation
