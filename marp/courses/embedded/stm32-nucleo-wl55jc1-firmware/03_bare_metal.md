---
tags:
  - hardware-and-embedded:embedded
  - hardware-and-embedded:hardware-programming
level: advanced
category: embedded
audience:
  - audiences:embedded-engineers
  - audiences:developers

---

# Writing Bare Metal

---

## Chapter Overview

1. What "bare metal" really means
1. The startup code and vector table
1. Talking to peripherals through registers
1. Blinking an LED with zero libraries
1. Reading a button and using interrupts

---

## What Is Bare Metal?

1. No operating system, no HAL, no RTOS
1. Your `main()` runs directly on the hardware
1. You write to **memory-mapped registers** yourself
1. You provide the **startup code** and **vector table**
1. Maximum control, minimum abstraction

---

## Why Learn It On This Board?

1. The HAL is built **on top of** these registers
1. Debugging the HAL requires register-level understanding
1. Radio timing is unforgiving — abstractions can cost you
1. Smallest possible firmware footprint
1. You will appreciate the HAL much more afterwards

---

## The Boot Sequence In Code

![bare_metal_boot](svg/courses/embedded/stm32-nucleo-wl55jc1-firmware/03_bare_metal/bare_metal_boot.svg)

---

## The Vector Table

```c
extern uint32_t _estack;
void Reset_Handler(void);
void Default_Handler(void);

__attribute__((section(".isr_vector")))
void (* const vector_table[])(void) = {
    (void (*)(void))&_estack,   // Initial stack pointer
    Reset_Handler,              // Reset
    Default_Handler,            // NMI
    Default_Handler,            // HardFault
    /* ... core exceptions ... */
    SysTick_Handler,            // SysTick
    /* ... STM32WL peripheral IRQs follow ... */
};
```

---

## The Reset Handler

```c
extern uint32_t _sdata, _edata, _sidata, _sbss, _ebss;

void Reset_Handler(void) {
    // Copy .data from flash to RAM
    uint32_t *src = &_sidata, *dst = &_sdata;
    while (dst < &_edata) *dst++ = *src++;

    // Zero .bss
    for (dst = &_sbss; dst < &_ebss; ) *dst++ = 0;

    main();          // Off we go
    while (1) { }    // main() must never return
}
```

---

## Peripherals Are Just Memory

```c
// A register block is a struct overlaid on an address
#define PERIPH_BASE      0x40000000UL
#define AHB2_BASE        (PERIPH_BASE + 0x08000000UL)
#define GPIOB_BASE       (AHB2_BASE + 0x0400UL)

#define RCC_BASE         (AHB2_BASE + 0x21000UL)

#define GPIOB            ((GPIO_TypeDef *) GPIOB_BASE)
#define RCC              ((RCC_TypeDef  *) RCC_BASE)
```

Every peripheral is a `volatile` struct at a fixed address.

---

## Blinking An LED — The Whole Program

```c
int main(void) {
    // 1. Enable the clock to GPIO port B
    RCC->AHB2ENR |= RCC_AHB2ENR_GPIOBEN;

    // 2. Set PB15 (LED) as a push-pull output
    GPIOB->MODER &= ~(3U << (15 * 2));
    GPIOB->MODER |=  (1U << (15 * 2));   // 01 = output

    // 3. Toggle forever
    while (1) {
        GPIOB->ODR ^= (1U << 15);
        for (volatile int i = 0; i < 200000; i++) { }
    }
}
```

---

## Why `volatile` Is Not Optional

1. Registers can change **outside** the program's control
1. Without `volatile`, the compiler may **cache** a read
1. Or **delete** a write it thinks is dead
1. Peripheral structs are always declared `volatile`
1. The busy-wait counter is `volatile` so it is not optimized away

---

## Reading The User Button

```c
// PA0 is the B1 user button on this board
RCC->AHB2ENR |= RCC_AHB2ENR_GPIOAEN;
GPIOA->MODER &= ~(3U << (0 * 2));        // 00 = input
GPIOA->PUPDR |=  (2U << (0 * 2));        // 10 = pull-down

while (1) {
    if (GPIOA->IDR & (1U << 0)) {
        GPIOB->ODR |= (1U << 15);        // pressed -> LED on
    } else {
        GPIOB->ODR &= ~(1U << 15);
    }
}
```

---

## Polling Versus Interrupts

1. The loop above **polls** — it burns CPU spinning
1. Better: let the hardware **interrupt** you on a change
1. Configure **EXTI** to fire on the button edge
1. The CPU can `WFI` (sleep) until something happens
1. Essential for a **battery-powered RF node**

---

## A Bare-Metal EXTI Handler

```c
// Enable EXTI line 0, rising edge, in the NVIC
EXTI->RTSR1 |= EXTI_RTSR1_RT0;
EXTI->IMR1  |= EXTI_IMR1_IM0;
NVIC_EnableIRQ(EXTI0_IRQn);

void EXTI0_IRQHandler(void) {
    if (EXTI->PR1 & EXTI_PR1_PIF0) {
        EXTI->PR1 = EXTI_PR1_PIF0;   // write-1-to-clear
        GPIOB->ODR ^= (1U << 15);
    }
}
```

---

## The Cost Of Bare Metal

1. You must read the **reference manual** constantly
1. No portability between MCU families
1. Easy to forget a clock-enable and chase a dead peripheral
1. Every bit field is yours to get right
1. This is exactly what the **HAL** automates next

---

## Key Takeaways

1. Bare metal = **registers + startup code**, nothing else
1. You provide the **vector table** and **Reset_Handler**
1. Peripherals are `volatile` **memory-mapped structs**
1. Always **enable the clock** before touching a peripheral
1. Prefer **interrupts over polling** for low power
