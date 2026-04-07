# Power Management

---

## Power Management Overview

Linux power management aims to:
- Reduce power consumption
- Extend battery life
- Manage thermal constraints
- Meet performance requirements

Key challenge: Balance power savings with system responsiveness

---

## Power Management Framework

![power_management_framework](/svg/courses/operating_systems/linux-kernel-advanced-topics/04_power_management/power_management_framework.svg)

---

## Power States

System power states (`/sys/power/state`):
- `freeze` - Suspend to idle
- `standby` - Power-on suspend
- `mem` - Suspend to RAM
- `disk` - Suspend to disk (hibernation)

---

## CPU Frequency Scaling

Dynamic frequency adjustment based on load

Key components:
- Governors - Policy algorithms
- Drivers - Hardware control
- Core - Framework infrastructure

---

## CPUFreq Governors

Available governors:
- `performance` - Maximum frequency
- `powersave` - Minimum frequency
- `ondemand` - Dynamic scaling
- `conservative` - Gradual scaling
- `schedutil` - Scheduler-based
- `userspace` - Manual control

---

## CPUFreq Configuration

```bash
# View current governor
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor

# Set governor
echo ondemand > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor

# View available frequencies
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_available_frequencies

# Set frequency limits
echo 1000000 > /sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq
```

---

## CPUFreq Driver Implementation

```c
static struct cpufreq_driver my_cpufreq_driver = {
    .name = "my-cpufreq",
    .init = my_cpufreq_init,
    .verify = cpufreq_generic_frequency_table_verify,
    .target_index = my_cpufreq_target,
    .get = my_cpufreq_get,
    .attr = cpufreq_generic_attr,
};

static int __init my_cpufreq_module_init(void)
{
    return cpufreq_register_driver(&my_cpufreq_driver);
}
```

---

## CPU Idle States

C-States for idle CPU management:
- `C0` - Active state
- `C1` - Halt
- `C2` - Stop clock
- `C3` - Deep sleep
- Higher states - Deeper sleep

---

## CPUIdle Framework

![cpuidle_framework](/svg/courses/operating_systems/linux-kernel-advanced-topics/04_power_management/cpuidle_framework.svg)

---

## CPUIdle Driver

```c
static struct cpuidle_driver my_idle_driver = {
    .name = "my_idle",
    .owner = THIS_MODULE,
    .states = {
        [0] = {
            .name = "WFI",
            .desc = "ARM WFI",
            .exit_latency = 1,
            .target_residency = 1,
            .enter = my_enter_idle,
        },
        [1] = {
            .name = "DEEP",
            .desc = "Deep Sleep",
            .exit_latency = 100,
            .target_residency = 1000,
            .enter = my_enter_deep_idle,
        },
    },
    .state_count = 2,
};
```

---

## Runtime PM

Device-level power management

Key concepts:
- Automatic suspend/resume
- Reference counting
- Parent-child relationships
- Async operations

---

## Runtime PM API

```c
/* Driver runtime PM setup */
pm_runtime_enable(&pdev->dev);
pm_runtime_set_autosuspend_delay(&pdev->dev, 1000);
pm_runtime_use_autosuspend(&pdev->dev);

/* Get/Put operations */
pm_runtime_get_sync(&pdev->dev);
/* Use device */
pm_runtime_put_autosuspend(&pdev->dev);

/* Callbacks */
static const struct dev_pm_ops my_pm_ops = {
    SET_RUNTIME_PM_OPS(my_runtime_suspend,
                       my_runtime_resume,
                       NULL)
};
```

---

## Runtime PM States

![runtime_pm_states](/svg/courses/operating_systems/linux-kernel-advanced-topics/04_power_management/runtime_pm_states.svg)

---

## System Suspend

Suspend entire system to save power

Phases:
1. Prepare - Prevent new operations
1. Suspend - Save state and power down
1. Suspend_late - Final operations
1. Suspend_noirq - IRQs disabled

---

## Suspend/Resume Callbacks

```c
static int my_suspend(struct device *dev)
{
    struct my_device *mydev = dev_get_drvdata(dev);
    /* Save device state */
    mydev->saved_reg = readl(mydev->base + REG_OFFSET);
    /* Power down */
    return 0;
}

static int my_resume(struct device *dev)
{
    struct my_device *mydev = dev_get_drvdata(dev);
    /* Restore state */
    writel(mydev->saved_reg, mydev->base + REG_OFFSET);
    return 0;
}

static SIMPLE_DEV_PM_OPS(my_pm_ops, my_suspend, my_resume);
```

---

## Wakeup Sources

Configure wake events:

```c
/* Enable device as wakeup source */
device_init_wakeup(&pdev->dev, true);

/* In suspend handler */
if (device_may_wakeup(dev))
    enable_irq_wake(mydev->irq);

/* Report wakeup event */
pm_wakeup_event(dev, 0);
```

---

## Power Domains

Group related devices for power control

```c
static struct generic_pm_domain my_power_domain = {
    .name = "my-pd",
    .power_on = my_pd_power_on,
    .power_off = my_pd_power_off,
};

/* Add device to domain */
of_genpd_add_device(&my_power_domain.pd, dev);
```

---

## Voltage Scaling

Adjust voltage with frequency:

```c
/* OPP (Operating Performance Points) */
struct dev_pm_opp *opp;
unsigned long freq = 1000000000; /* 1GHz */
int volt;

opp = dev_pm_opp_find_freq_exact(dev, freq, true);
volt = dev_pm_opp_get_voltage(opp);
dev_pm_opp_put(opp);

/* Set voltage */
regulator_set_voltage(cpu_reg, volt, volt);
```

---

## Clock Management

Power-aware clock control:

```c
/* Get clock */
clk = devm_clk_get(&pdev->dev, "core");

/* Enable when needed */
clk_prepare_enable(clk);

/* Disable when idle */
clk_disable_unprepare(clk);

/* Runtime PM integration */
pm_runtime_get_sync(dev);  /* Clocks enabled */
pm_runtime_put(dev);        /* Clocks disabled */
```

---

## Thermal Management

Temperature monitoring and control

Components:
- Thermal zones
- Cooling devices
- Governors
- Trip points

---

## Thermal Framework

![thermal_framework](/svg/courses/operating_systems/linux-kernel-advanced-topics/04_power_management/thermal_framework.svg)

---

## Thermal Driver

```c
static struct thermal_zone_device_ops tz_ops = {
    .get_temp = my_get_temp,
    .get_trip_type = my_get_trip_type,
    .get_trip_temp = my_get_trip_temp,
};

/* Register thermal zone */
tz = thermal_zone_device_register("cpu-thermal",
                                  trips, 0, devdata,
                                  &tz_ops, NULL, 0, 0);

/* Cooling device */
cdev = thermal_cooling_device_register("cpu-freq",
                                       NULL,
                                       &cooling_ops);
```

---

## Battery Management

Power supply class:

```c
static enum power_supply_property battery_props[] = {
    POWER_SUPPLY_PROP_STATUS,
    POWER_SUPPLY_PROP_CAPACITY,
    POWER_SUPPLY_PROP_VOLTAGE_NOW,
    POWER_SUPPLY_PROP_CURRENT_NOW,
    POWER_SUPPLY_PROP_TEMP,
};

static const struct power_supply_desc battery_desc = {
    .name = "battery",
    .type = POWER_SUPPLY_TYPE_BATTERY,
    .properties = battery_props,
    .num_properties = ARRAY_SIZE(battery_props),
    .get_property = battery_get_property,
};
```

---

## Power Debugging

Tools and techniques:

```bash
# PowerTOP - Power analysis
powertop

# Monitor CPU frequency
watch -n 1 cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_cur_freq

# Trace PM events
echo 1 > /sys/kernel/debug/tracing/events/power/enable
cat /sys/kernel/debug/tracing/trace
```

---

## PM Statistics

```bash
# Suspend stats
cat /sys/kernel/debug/suspend_stats

# Runtime PM stats
cat /sys/devices/.../power/runtime_status
cat /sys/devices/.../power/runtime_active_time
cat /sys/devices/.../power/runtime_suspended_time

# CPUIdle stats
cat /sys/devices/system/cpu/cpu0/cpuidle/state*/time
cat /sys/devices/system/cpu/cpu0/cpuidle/state*/usage
```

---

## Wake Lock (Android)

Prevent system suspend:

```c
/* Kernel wake lock */
struct wake_lock my_wake_lock;
wake_lock_init(&my_wake_lock, WAKE_LOCK_SUSPEND, "my_lock");

/* Acquire */
wake_lock(&my_wake_lock);

/* Release */
wake_unlock(&my_wake_lock);
```

---

## PM QoS

Quality of Service constraints:

```c
/* Add latency constraint */
struct dev_pm_qos_request qos_req;
dev_pm_qos_add_request(dev, &qos_req,
                       DEV_PM_QOS_RESUME_LATENCY,
                       100); /* 100us max */

/* Update constraint */
dev_pm_qos_update_request(&qos_req, 50);

/* Remove constraint */
dev_pm_qos_remove_request(&qos_req);
```

---

## Dynamic Power Management

Strategies:
1. Clock gating
1. Power gating
1. Voltage scaling
1. Frequency scaling
1. Core parking

---

## Power Profiling

Measurement techniques:

```bash
# Current measurement
cat /sys/class/power_supply/battery/current_now

# Energy monitoring
perf stat -e power/energy-pkg/ command

# Kernel tracepoints
trace-cmd record -e power:* command
trace-cmd report
```

---

## Device Tree PM Properties

```dts
device@0 {
    compatible = "vendor,device";
    /* Power domain */
    power-domains = <&pd_domain>;

    /* Operating points */
    operating-points-v2 = <&cpu_opp_table>;

    /* Clocks */
    clocks = <&clk_controller CLK_ID>;
    clock-names = "core";

    /* Wake capable */
    wakeup-source;
};
```

---

## PM Constraints

Define system constraints:

```c
/* Latency constraint */
static struct pm_qos_request cpu_dma_lat_req;
pm_qos_add_request(&cpu_dma_lat_req,
                   PM_QOS_CPU_DMA_LATENCY,
                   100);

/* Network throughput */
pm_qos_add_request(&net_req,
                   PM_QOS_NETWORK_THROUGHPUT,
                   1000);
```

---

## Suspend Freezer

Process freezing during suspend:

```c
/* Freezable kernel thread */
set_freezable();
while (!kthread_should_stop()) {
    try_to_freeze();
    /* Do work */
}

/* Freezable workqueue */
queue_work(system_freezable_wq, &work);
```

---

## Hibernation

Suspend to disk implementation:

```bash
# Configure swap for hibernation
mkswap /dev/sda2
swapon /dev/sda2

# Hibernate
echo disk > /sys/power/state

# Resume kernel parameter
resume=/dev/sda2
```

---

## Platform PM Ops

```c
static const struct platform_suspend_ops my_suspend_ops = {
    .valid = my_suspend_valid,
    .begin = my_suspend_begin,
    .prepare = my_suspend_prepare,
    .prepare_late = my_suspend_prepare_late,
    .enter = my_suspend_enter,
    .wake = my_suspend_wake,
    .finish = my_suspend_finish,
    .end = my_suspend_end,
};

suspend_set_ops(&my_suspend_ops);
```

---

## Regulator Framework

Voltage/current control:

```c
/* Get regulator */
reg = devm_regulator_get(dev, "vdd");

/* Enable/disable */
regulator_enable(reg);
regulator_disable(reg);

/* Set voltage */
regulator_set_voltage(reg, 1800000, 1800000);

/* Query state */
if (regulator_is_enabled(reg))
    volt = regulator_get_voltage(reg);
```

---

## CPU Hotplug

Dynamic CPU on/off:

```bash
# Offline CPU
echo 0 > /sys/devices/system/cpu/cpu1/online

# Online CPU
echo 1 > /sys/devices/system/cpu/cpu1/online

# Hotplug governor
echo 2 > /sys/devices/system/cpu/kernel_max
```

---

## ACPI Power Management

ACPI states mapping:
- `S0` - Working
- `S1` - Power on suspend
- `S3` - Suspend to RAM
- `S4` - Suspend to disk
- `S5` - Soft off

---

## Power Management Policies

System-wide policies:

```bash
# Set PM profile
echo low-power > /sys/firmware/acpi/pm_profile

# Laptop mode
echo 5 > /proc/sys/vm/laptop_mode

# Aggressive power saving
echo 1 > /sys/module/pcie_aspm/parameters/policy
```

---

## Best Practices

1. Use runtime PM for all drivers
1. Implement proper suspend/resume
1. Test all power transitions
1. Profile power consumption
1. Handle wake events correctly
1. Document power states
1. Consider thermal constraints

---

## Summary

Power management involves:
- Multiple frameworks working together
- Hardware and software coordination
- Trade-offs between power and performance
- Comprehensive testing needed

Key takeaways:
- Runtime PM for devices
- CPUFreq/CPUIdle for processors
- Thermal management critical
- Measurement drives optimization
