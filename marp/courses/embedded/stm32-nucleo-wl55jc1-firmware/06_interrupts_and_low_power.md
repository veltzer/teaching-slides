---
tags:
  - hardware-and-embedded:embedded
  - hardware-and-embedded:hardware-programming
  - infrastructure:real-time
level: advanced
category: embedded
audience:
  - audiences:embedded-engineers
  - audiences:developers

---

# Interrupts And Low Power

---

## Chapter Overview

1. The NVIC and interrupt priorities
1. EXTI: interrupts from pins
1. Writing safe interrupt handlers
1. Low-power modes on an RF node
1. Waking up: which sources work in which mode

---

## The NVIC

1. **Nested Vectored Interrupt Controller** — part of the core
1. Each interrupt has a **priority**; higher preempts lower
1. Lower number = higher priority (0 is most urgent)
1. Each core (M4, M0+) has **its own** NVIC
1. The radio stack on CPU2 needs **top priority** for its IRQs

---

## Configuring An Interrupt

```c
// Priority grouping done once by HAL_Init()
HAL_NVIC_SetPriority(EXTI0_IRQn, 5, 0);  // preempt, sub
HAL_NVIC_EnableIRQ(EXTI0_IRQn);
```

1. Set the priority **before** enabling
1. Keep real-time / radio IRQs numerically **low**
1. Keep slow background IRQs numerically **high**

---

## EXTI: Pin Change Interrupts

```c
// A button configured as GPIO_MODE_IT_FALLING fires EXTI
void HAL_GPIO_EXTI_Callback(uint16_t pin) {
    if (pin == GPIO_PIN_0) {
        button_pressed = true;   // keep it short!
    }
}
```

1. Each pin number maps to an EXTI line
1. The HAL dispatches the line to your callback
1. Do the **minimum** in the handler

---

## Rules For Interrupt Handlers

1. Keep them **short** — defer work to the main loop
1. Never block, never `HAL_Delay`, never `malloc`
1. Touch shared data only through a **safe pattern**
1. Mark shared flags `volatile`
1. Re-arm / clear the source before returning

---

## Interrupt-To-Task Handoff

![interrupt_to_task_handoff](svg/courses/embedded/stm32-nucleo-wl55jc1-firmware/06_interrupts_and_low_power/interrupt_to_task_handoff.svg)

---

## Why Low Power Matters Here

1. WL55 nodes are often **battery** or energy-harvested
1. The radio sleeps between transmissions for **seconds**
1. The CPU should sleep too, not spin
1. Sleep current can be **microamps** if done right
1. Power discipline decides battery life, not clever code

---

## The Low-Power Modes

| Mode      | CPU   | RAM kept   | Wake latency | Typical use        |
| --------- | ----- | ---------- | ------------ | ------------------ |
| Run       | on    | all        | —            | active work        |
| Sleep     | clock off | all    | instant      | idle between IRQs  |
| Stop2     | off   | retained   | microseconds | between RF frames  |
| Standby   | off   | mostly lost| milliseconds | long deep sleep    |
| Shutdown  | off   | lost       | reset-like   | shelf / ship mode  |

---

## Entering A Low-Power Mode

```c
// Idle until the next interrupt — cheapest sleep
__WFI();

// Deeper: Stop 2 keeps RAM, wakes fast enough for RF
HAL_PWREx_EnterSTOP2Mode(PWR_STOPENTRY_WFI);

// On wake from Stop, the clock tree must be re-configured!
SystemClock_Config();
```

---

## Choosing A Wake Source

1. **EXTI** lines (buttons, sensor IRQ) wake from Stop
1. **RTC** alarm wakes for periodic duty cycling
1. **LPTIM** runs in low power for timeouts
1. The **radio IRQ** wakes the node when a packet arrives
1. Standby loses most state — wake means **re-init**

---

## A Duty-Cycled Main Loop

```c
while (1) {
    do_measurement();
    radio_transmit(payload, len);

    schedule_rtc_wakeup_seconds(60);
    HAL_PWREx_EnterSTOP2Mode(PWR_STOPENTRY_WFI);
    SystemClock_Config();   // restore clocks after wake
}
```

Sleep is the default state; wake, work briefly, sleep again.

---

## Dual-Core And Low Power

1. The system enters Stop only when **both cores** agree
1. CPU2 (radio) may hold the system awake mid-frame
1. Use the **PWR** low-power request bits per core
1. A core stuck awake **kills** your power budget
1. Coordinate sleep through **IPCC**, never guess

---

## Key Takeaways

1. The **NVIC** ranks and nests interrupts; each core has one
1. Handlers stay **short**; defer work to the main loop
1. **Sleep aggressively** — it is where battery life is won
1. **Stop2** balances RAM retention with fast wake
1. Both cores must **agree** before the system sleeps
