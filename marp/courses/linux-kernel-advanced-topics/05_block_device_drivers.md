# Block Device Drivers

---

## Block Layer Architecture

<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">
<rect x="100" y="50" width="600" height="420" fill="#F0F0F0" stroke="black"/>
<text x="400" y="80" text-anchor="middle" font-weight="bold">Linux Block Layer</text>
<rect x="200" y="110" width="400" height="50" fill="#FFE6E6" stroke="black"/>
<text x="400" y="140" text-anchor="middle">Filesystem (ext4, xfs, btrfs)</text>
<rect x="200" y="170" width="400" height="50" fill="#E6F2FF" stroke="black"/>
<text x="400" y="200" text-anchor="middle">VFS Layer</text>
<rect x="200" y="230" width="400" height="50" fill="#E6FFE6" stroke="black"/>
<text x="400" y="260" text-anchor="middle">Block Layer Core</text>
<rect x="200" y="290" width="195" height="50" fill="#FFFFE6" stroke="black"/>
<text x="297" y="320" text-anchor="middle">I/O Scheduler</text>
<rect x="405" y="290" width="195" height="50" fill="#FFE6FF" stroke="black"/>
<text x="502" y="320" text-anchor="middle">Device Mapper</text>
<rect x="200" y="350" width="400" height="50" fill="#E6E6E6" stroke="black"/>
<text x="400" y="380" text-anchor="middle">Block Device Driver</text>
<rect x="200" y="410" width="400" height="50" fill="#D0D0D0" stroke="black"/>
<text x="400" y="440" text-anchor="middle">Hardware (HDD, SSD, NVMe)</text>
</svg>

---

## Block Device Operations

```c
static const struct block_device_operations my_blk_ops = {
    .owner = THIS_MODULE,
    .open = my_blk_open,
    .release = my_blk_release,
    .ioctl = my_blk_ioctl,
    .getgeo = my_blk_getgeo,
    .media_changed = my_blk_media_changed,
    .revalidate_disk = my_blk_revalidate,
};
```

---

## Basic Block Driver

```c
static int __init my_blk_init(void)
{
    /* Register block device */
    major = register_blkdev(0, "myblk");

    /* Allocate gendisk */
    disk = alloc_disk(1);
    disk->major = major;
    disk->first_minor = 0;
    disk->fops = &my_blk_ops;
    strcpy(disk->disk_name, "myblk");

    /* Setup queue */
    queue = blk_init_queue(my_blk_request, &lock);
    disk->queue = queue;

    /* Set capacity */
    set_capacity(disk, nsectors);

    /* Add disk */
    add_disk(disk);

    return 0;
}
```

---

## Request Queue

Central structure for I/O management:

```c
struct request_queue {
    struct request *last_merge;
    struct elevator_queue *elevator;

    struct blk_queue_stats *stats;
    struct rq_qos *rq_qos;

    make_request_fn *make_request_fn;
    dma_drain_needed_fn *dma_drain_needed;

    const struct blk_mq_ops *mq_ops;

    /* Queue limits */
    struct queue_limits limits;
};
```

---

## Request Structure

```c
struct request {
    struct request_queue *q;
    struct bio *bio;
    struct bio *biotail;

    unsigned int cmd_flags;
    req_flags_t rq_flags;

    sector_t __sector;
    unsigned int __data_len;

    void *special;
    int errors;
};
```

---

## Bio Structure

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
<rect x="100" y="50" width="200" height="300" fill="#FFE6E6" stroke="black"/>
<text x="200" y="80" text-anchor="middle" font-weight="bold">bio</text>
<text x="200" y="110" text-anchor="middle">sector</text>
<text x="200" y="130" text-anchor="middle">size</text>
<text x="200" y="150" text-anchor="middle">bi_vcnt</text>
<text x="200" y="170" text-anchor="middle">bi_io_vec</text>
<line x1="300" y1="160" x2="350" y2="160" stroke="black" marker-end="url(#arrow)"/>
<rect x="350" y="100" width="150" height="50" fill="#E6F2FF" stroke="black"/>
<text x="425" y="130" text-anchor="middle">bio_vec[0]</text>
<rect x="350" y="160" width="150" height="50" fill="#E6FFE6" stroke="black"/>
<text x="425" y="190" text-anchor="middle">bio_vec[1]</text>
<rect x="350" y="220" width="150" height="50" fill="#FFFFE6" stroke="black"/>
<text x="425" y="250" text-anchor="middle">bio_vec[2]</text>
<line x1="500" y1="125" x2="550" y2="125" stroke="black" marker-end="url(#arrow)"/>
<rect x="550" y="100" width="150" height="50" fill="#FFE6FF" stroke="black"/>
<text x="625" y="130" text-anchor="middle">Page</text>
<defs>
<marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
<polygon points="0 0, 10 3, 0 6"/>
</marker>
</defs>
</svg>

---

## Bio Operations

```c
/* Iterate over bio segments */
struct bio_vec bvec;
struct bvec_iter iter;

bio_for_each_segment(bvec, bio, iter) {
    void *buffer = page_address(bvec.bv_page) + bvec.bv_offset;
    unsigned int len = bvec.bv_len;

    /* Process buffer */
    if (bio_data_dir(bio) == WRITE)
        device_write(buffer, len, iter.bi_sector);
    else
        device_read(buffer, len, iter.bi_sector);
}
```

---

## Request Processing

```c
static void my_blk_request(struct request_queue *q)
{
    struct request *req;

    while ((req = blk_fetch_request(q)) != NULL) {
        if (req->cmd_type != REQ_TYPE_FS) {
            __blk_end_request_all(req, -EIO);
            continue;
        }

        /* Process request */
        my_transfer_request(req);

        /* Complete request */
        __blk_end_request_all(req, 0);
    }
}
```

---

## Block Multi-Queue (blk-mq)

Modern high-performance framework:

```c
static struct blk_mq_ops my_mq_ops = {
    .queue_rq = my_queue_rq,
    .init_hctx = my_init_hctx,
    .complete = my_complete_rq,
    .init_request = my_init_request,
    .timeout = my_timeout_rq,
};

static int my_queue_rq(struct blk_mq_hw_ctx *hctx,
                       const struct blk_mq_queue_data *bd)
{
    struct request *req = bd->rq;

    blk_mq_start_request(req);

    /* Submit to hardware */
    my_submit_request(req);

    return BLK_MQ_RQ_QUEUE_OK;
}
```

---

## Multi-Queue Setup

```c
static int my_blk_mq_init(void)
{
    struct blk_mq_tag_set *set;

    set = &my_tag_set;
    set->ops = &my_mq_ops;
    set->nr_hw_queues = num_online_cpus();
    set->queue_depth = 128;
    set->numa_node = NUMA_NO_NODE;
    set->cmd_size = sizeof(struct my_cmd);
    set->flags = BLK_MQ_F_SHOULD_MERGE;
    set->driver_data = my_dev;

    if (blk_mq_alloc_tag_set(set))
        return -ENOMEM;

    disk->queue = blk_mq_init_queue(set);

    return 0;
}
```

---

## I/O Schedulers

Available schedulers:
- `noop` - Simple FIFO
- `deadline` - Latency guarantees
- `cfq` - Completely Fair Queuing
- `bfq` - Budget Fair Queuing
- `kyber` - Multi-queue scheduler
- `mq-deadline` - MQ deadline

---

## Scheduler Selection

```bash
# View current scheduler
cat /sys/block/sda/queue/scheduler

# Change scheduler
echo deadline > /sys/block/sda/queue/scheduler

# Set default scheduler
elevator=deadline  # kernel parameter
```

---

## Custom I/O Scheduler

```c
static struct elevator_type my_elevator = {
    .ops.sq = {
        .elevator_merge_fn = my_merge,
        .elevator_merged_fn = my_merged,
        .elevator_merge_req_fn = my_merge_requests,
        .elevator_dispatch_fn = my_dispatch,
        .elevator_add_req_fn = my_add_request,
        .elevator_init_fn = my_init_queue,
        .elevator_exit_fn = my_exit_queue,
    },
    .elevator_name = "my_scheduler",
    .elevator_owner = THIS_MODULE,
};

static int __init my_sched_init(void)
{
    return elv_register(&my_elevator);
}
```

---

## Partition Handling

```c
static int my_blk_getgeo(struct block_device *bdev,
                        struct hd_geometry *geo)
{
    geo->heads = 4;
    geo->sectors = 16;
    geo->cylinders = get_capacity(bdev->bd_disk) /
                     (geo->heads * geo->sectors);
    return 0;
}

/* Partition detection */
static int my_revalidate_disk(struct gendisk *disk)
{
    /* Update capacity */
    set_capacity(disk, new_size);

    /* Rescan partitions */
    return blk_revalidate_disk(disk, true);
}
```

---

## SCSI Subsystem

SCSI driver integration:

```c
static struct scsi_host_template my_scsi_template = {
    .name = "My SCSI HBA",
    .queuecommand = my_queuecommand,
    .eh_abort_handler = my_abort,
    .eh_device_reset_handler = my_device_reset,
    .eh_host_reset_handler = my_host_reset,
    .can_queue = 256,
    .this_id = -1,
    .sg_tablesize = SG_ALL,
    .cmd_per_lun = 1,
    .use_clustering = ENABLE_CLUSTERING,
};
```

---

## SCSI Command Processing

```c
static int my_queuecommand(struct Scsi_Host *host,
                           struct scsi_cmnd *cmd)
{
    struct my_dev *dev = shost_priv(host);

    /* Setup command */
    switch (cmd->cmnd[0]) {
    case READ_10:
    case WRITE_10:
        return my_rw_command(dev, cmd);
    case TEST_UNIT_READY:
        cmd->result = DID_OK << 16;
        cmd->scsi_done(cmd);
        return 0;
    }

    return SCSI_MLQUEUE_HOST_BUSY;
}
```

---

## MMC/SD Card Drivers

```c
static const struct mmc_host_ops my_mmc_ops = {
    .request = my_mmc_request,
    .set_ios = my_mmc_set_ios,
    .get_ro = my_mmc_get_ro,
    .get_cd = my_mmc_get_cd,
    .enable_sdio_irq = my_mmc_enable_sdio_irq,
};

static int my_mmc_probe(struct platform_device *pdev)
{
    struct mmc_host *mmc;

    mmc = mmc_alloc_host(sizeof(struct my_host), &pdev->dev);
    mmc->ops = &my_mmc_ops;
    mmc->f_min = 400000;
    mmc->f_max = 50000000;
    mmc->caps = MMC_CAP_4_BIT_DATA | MMC_CAP_SD_HIGHSPEED;

    mmc_add_host(mmc);
    return 0;
}
```

---

## NVMe Driver Structure

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
<rect x="200" y="50" width="400" height="60" fill="#FFE6E6" stroke="black"/>
<text x="400" y="85" text-anchor="middle">NVMe Driver</text>
<rect x="150" y="150" width="150" height="60" fill="#E6F2FF" stroke="black"/>
<text x="225" y="185" text-anchor="middle">Admin Queue</text>
<rect x="325" y="150" width="150" height="60" fill="#E6FFE6" stroke="black"/>
<text x="400" y="185" text-anchor="middle">I/O Queue 0</text>
<rect x="500" y="150" width="150" height="60" fill="#FFFFE6" stroke="black"/>
<text x="575" y="185" text-anchor="middle">I/O Queue N</text>
<rect x="200" y="250" width="400" height="60" fill="#D0D0D0" stroke="black"/>
<text x="400" y="285" text-anchor="middle">NVMe Controller</text>
<line x1="225" y1="210" x2="225" y2="250" stroke="black" marker-end="url(#arrowhead)"/>
<line x1="400" y1="210" x2="400" y2="250" stroke="black" marker-end="url(#arrowhead)"/>
<line x1="575" y1="210" x2="575" y2="250" stroke="black" marker-end="url(#arrowhead)"/>
<defs>
<marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
<polygon points="0 0, 10 3, 0 6"/>
</marker>
</defs>
</svg>

---

## NVMe Queue Pairs

```c
struct nvme_queue {
    struct nvme_dev *dev;
    spinlock_t sq_lock;
    struct nvme_command *sq_cmds;
    struct nvme_completion *cqes;
    dma_addr_t sq_dma_addr;
    dma_addr_t cq_dma_addr;
    u32 __iomem *q_db;
    u16 q_depth;
    u16 sq_tail;
    u16 cq_head;
    u16 qid;
    u8 cq_phase;
};
```

---

## Block Layer Caching

```c
/* Setup write cache */
blk_queue_write_cache(q, true, false);

/* Flush support */
blk_queue_flag_set(QUEUE_FLAG_WC, q);

/* FUA (Force Unit Access) support */
blk_queue_flag_set(QUEUE_FLAG_FUA, q);

/* Handle flush requests */
if (req_op(req) == REQ_OP_FLUSH) {
    my_device_flush_cache();
    blk_mq_end_request(req, BLK_STS_OK);
}
```

---

## DMA Mapping for Block I/O

```c
static int my_map_sg(struct request *req)
{
    struct scatterlist *sg;
    int count;

    count = blk_rq_map_sg(req->q, req, my_sg_list);

    count = dma_map_sg(&pdev->dev, my_sg_list,
                      count, rq_data_dir(req));

    for_each_sg(my_sg_list, sg, count, i) {
        dma_addr_t addr = sg_dma_address(sg);
        unsigned int len = sg_dma_len(sg);
        /* Program DMA controller */
    }

    return count;
}
```

---

## Block Device Polling

```c
/* Setup polling */
static blk_qc_t my_make_request(struct request_queue *q,
                                struct bio *bio)
{
    /* Submit I/O */
    cookie = my_submit_bio(bio);

    /* Return cookie for polling */
    return cookie;
}

static int my_poll(struct blk_mq_hw_ctx *hctx,
                  blk_qc_t cookie)
{
    /* Check completion */
    if (my_check_completion(cookie)) {
        my_complete_request(cookie);
        return 1;
    }
    return 0;
}
```

---

## Discard/TRIM Support

```c
/* Enable discard */
blk_queue_flag_set(QUEUE_FLAG_DISCARD, q);
queue->limits.discard_granularity = 512;
queue->limits.max_discard_sectors = UINT_MAX;

/* Handle discard requests */
if (req_op(req) == REQ_OP_DISCARD) {
    sector_t sector = blk_rq_pos(req);
    unsigned int nr_sectors = blk_rq_sectors(req);

    my_device_trim(sector, nr_sectors);
    blk_mq_end_request(req, BLK_STS_OK);
}
```

---

## Zoned Block Devices

```c
/* Zone operations */
static int my_report_zones(struct gendisk *disk,
                           sector_t sector,
                           unsigned int nr_zones,
                           report_zones_cb cb,
                           void *data)
{
    struct blk_zone zone;

    zone.start = sector;
    zone.len = zone_size;
    zone.wp = sector;
    zone.type = BLK_ZONE_TYPE_SEQWRITE_REQ;
    zone.cond = BLK_ZONE_COND_EMPTY;

    return cb(&zone, idx, data);
}

disk->fops->report_zones = my_report_zones;
```

---

## Error Handling

```c
static void my_handle_error(struct request *req)
{
    switch (error_code) {
    case MEDIA_ERROR:
        blk_mq_end_request(req, BLK_STS_MEDIUM);
        break;
    case TIMEOUT:
        blk_mq_end_request(req, BLK_STS_TIMEOUT);
        break;
    case DEVICE_BUSY:
        blk_mq_requeue_request(req, true);
        break;
    default:
        blk_mq_end_request(req, BLK_STS_IOERR);
    }
}
```

---

## Block Layer Tracing

```bash
# Enable block tracing
echo 1 > /sys/block/sda/trace/enable

# blktrace
blktrace -d /dev/sda -o trace
blkparse -i trace

# BPF tracing
bpftrace -e 'kprobe:blk_mq_submit_bio { printf("%s\n", comm); }'
```

---

## Performance Metrics

```c
/* I/O statistics */
struct disk_stats {
    u64 ios[2];        /* Read/write I/Os */
    u64 merges[2];     /* Read/write merges */
    u64 sectors[2];    /* Sectors read/written */
    u64 ticks[2];      /* Time in queue */
    u64 io_ticks;      /* Time doing I/O */
    u64 time_in_queue; /* Weighted time */
};

/* Update stats */
part_stat_inc(&disk->part0, ios[rw]);
part_stat_add(&disk->part0, sectors[rw], nr_sectors);
```

---

## Queue Limits

```c
/* Set queue limits */
blk_queue_logical_block_size(q, 512);
blk_queue_physical_block_size(q, 4096);
blk_queue_max_hw_sectors(q, 2048);
blk_queue_max_segments(q, 128);
blk_queue_max_segment_size(q, 65536);
blk_queue_io_min(q, 512);
blk_queue_io_opt(q, 4096);

/* Alignment */
blk_queue_alignment_offset(q, 0);
blk_queue_update_dma_alignment(q, 511);
```

---

## Hot Add/Remove

```c
/* Hot add */
static int my_blk_hotplug(void)
{
    disk = alloc_disk(1);
    /* Setup disk */
    add_disk(disk);

    /* Notify udev */
    kobject_uevent(&disk_to_dev(disk)->kobj, KOBJ_ADD);
    return 0;
}

/* Hot remove */
static void my_blk_remove(void)
{
    del_gendisk(disk);
    blk_cleanup_queue(disk->queue);
    put_disk(disk);
}
```

---

## Device Mapper Target

```c
static struct target_type my_target = {
    .name = "my_target",
    .version = {1, 0, 0},
    .module = THIS_MODULE,
    .ctr = my_ctr,
    .dtr = my_dtr,
    .map = my_map,
    .status = my_status,
};

static int my_map(struct dm_target *ti, struct bio *bio)
{
    struct my_target_data *data = ti->private;

    /* Remap bio */
    bio_set_dev(bio, data->dev->bdev);
    bio->bi_iter.bi_sector += data->start;

    return DM_MAPIO_REMAPPED;
}
```

---

## Block Crypto

```c
/* Inline encryption */
struct blk_crypto_key {
    struct blk_crypto_config crypto_cfg;
    unsigned int data_unit_size_bits;
    unsigned int size;
    u8 raw[BLK_CRYPTO_MAX_KEY_SIZE];
};

/* Setup encryption */
bio_crypt_set_ctx(bio, &key, dun, GFP_KERNEL);

/* Hardware crypto support */
blk_queue_flag_set(QUEUE_FLAG_INLINE_ENCRYPTION, q);
```

---

## Testing Block Drivers

```bash
# Create test device
dd if=/dev/zero of=disk.img bs=1M count=100
losetup /dev/loop0 disk.img

# Performance testing
fio --name=test --filename=/dev/myblk \
    --ioengine=libaio --direct=1 \
    --rw=randrw --bs=4k --runtime=60

# Verify data integrity
badblocks -w /dev/myblk
```

---

## Debugging Techniques

```c
/* Debug prints */
#define blk_dbg(fmt, ...) \
    pr_debug("myblk: " fmt, ##__VA_ARGS__)

/* Dump request */
static void dump_request(struct request *req)
{
    blk_dbg("req: op=%d sector=%llu len=%u\n",
            req_op(req),
            blk_rq_pos(req),
            blk_rq_bytes(req));
}

/* Tracepoints */
trace_block_rq_issue(req);
trace_block_rq_complete(req, error);
```

---

## Best Practices

1. Use blk-mq for new drivers
1. Implement proper error handling
1. Support discard operations
1. Handle flush/FUA correctly
1. Test with various I/O patterns
1. Profile with blktrace
1. Document hardware limitations

---

## Summary

Block driver development involves:
- Understanding block layer architecture
- Request queue management
- Bio/request handling
- I/O scheduling integration

Key concepts:
- Multi-queue for scalability
- DMA for efficient transfers
- Proper cache handling
- Performance optimization techniques