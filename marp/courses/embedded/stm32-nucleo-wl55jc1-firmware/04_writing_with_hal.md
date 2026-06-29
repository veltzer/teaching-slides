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
# Writing With The HAL

---

## Chapter Overview

1. What the HAL and LL libraries are
1. CubeMX-generated project structure
1. The same LED blink, the HAL way
1. HAL initialization patterns
1. When the HAL helps and when it hurts

---

## What Is The HAL?

1. **Hardware Abstraction Layer** — ST's official C driver library
1. Portable API across the whole STM32 range
1. Hides register bit-twiddling behind functions and handles
1. Ships with **STM32CubeWL** for this exact board
1. Comes with **CubeMX**, a graphical configurator

---

## HAL Versus LL

1. **HAL**: high-level, handle-based, lots of safety checks
1. **LL** (Low-Layer): thin inline wrappers over registers
1. HAL is easier; LL is faster and smaller
1. You can **mix** them in one project
1. Radio-timing-critical code often drops to LL

---

## The Abstraction Stack

![hal_abstraction_stack](svg/courses/embedded/stm32-nucleo-wl55jc1-firmware/04_writing_with_hal/hal_abstraction_stack.svg)

---

## A CubeMX Project Layout

```misc
Core/
  Inc/  main.h  stm32wlxx_hal_conf.h  stm32wlxx_it.h
  Src/  main.c  stm32wlxx_it.c  system_stm32wlxx.c
Drivers/
  STM32WLxx_HAL_Driver/   <- the HAL itself
  CMSIS/                  <- core + device headers
STM32WL55JCIX_FLASH.ld    <- generated linker script
```

CubeMX regenerates `main.c` — keep your code in the `USER CODE` blocks.

---

## HAL Startup Boilerplate

```c
int main(void) {
    HAL_Init();              // SysTick, NVIC priorities, flash latency
    SystemClock_Config();    // bring up the clock tree (incl. TCXO)
    MX_GPIO_Init();          // configure pins

    while (1) {
        // application code
    }
}
```

`HAL_Init()` and `SystemClock_Config()` replace pages of register writes.

---

## Blinking An LED — The HAL Way

```c
void MX_GPIO_Init(void) {
    __HAL_RCC_GPIOB_CLK_ENABLE();

    GPIO_InitTypeDef cfg = {0};
    cfg.Pin   = GPIO_PIN_15;
    cfg.Mode  = GPIO_MODE_OUTPUT_PP;
    cfg.Pull  = GPIO_NOPULL;
    cfg.Speed = GPIO_SPEED_FREQ_LOW;
    HAL_GPIO_Init(GPIOB, &cfg);
}

// In the main loop:
HAL_GPIO_TogglePin(GPIOB, GPIO_PIN_15);
HAL_Delay(500);   // milliseconds, driven by SysTick
```

---

## Compare The Two Styles

| Concern        | Bare metal           | HAL                       |
| -------------- | -------------------- | ------------------------- |
| Clock enable   | `RCC->AHB2ENR \|= …` | `__HAL_RCC_GPIOB_CLK_ENABLE()` |
| Pin config     | `MODER`, `PUPDR` …   | `HAL_GPIO_Init(&cfg)`     |
| Toggle         | `ODR ^= bit`         | `HAL_GPIO_TogglePin()`    |
| Delay          | busy loop            | `HAL_Delay(ms)`           |
| Portability    | none                 | whole STM32 family        |

---

## HAL Handles Carry State

```c
// A peripheral handle bundles config + runtime state
UART_HandleTypeDef huart2;

huart2.Instance        = USART2;
huart2.Init.BaudRate   = 115200;
huart2.Init.WordLength = UART_WORDLENGTH_8B;
huart2.Init.StopBits   = UART_STOPBITS_1;
huart2.Init.Parity     = UART_PARITY_NONE;
HAL_UART_Init(&huart2);

HAL_UART_Transmit(&huart2, (uint8_t*)"hi\r\n", 4, 100);
```

The handle is passed to every call — it is the object behind the API.

---

## HAL Callbacks Replace Raw ISRs

```c
// You no longer write USART2_IRQHandler yourself.
// The HAL's IRQ handler calls back into your code:
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart) {
    if (huart->Instance == USART2) {
        handle_received_byte(rx_byte);
        HAL_UART_Receive_IT(huart, &rx_byte, 1);  // re-arm
    }
}
```

Interrupt, DMA and polling variants share one tidy API.

---

## When The HAL Helps

1. Getting a new peripheral working **quickly**
1. Portable code across STM32 projects
1. Complex peripherals (USB, the radio middleware)
1. Built-in **error and timeout** handling
1. Generated init code you can trust

---

## When The HAL Hurts

1. **Code size** — it pulls in a lot
1. **Latency** — function-call and check overhead in ISRs
1. **Hidden behavior** — bugs are harder to localize
1. Tight **radio timing** may need LL or registers
1. CubeMX regeneration can **clobber** hand edits

---

## A Pragmatic Middle Ground

1. Use HAL for **bring-up** and slow peripherals
1. Drop to **LL** in hot interrupt paths
1. Keep radio-timing code **register-level** where needed
1. Never put logic **outside** the `USER CODE` markers
1. Profile before optimizing away the HAL

---

## Key Takeaways

1. HAL = **portable, handle-based** driver library
1. **LL** sits between HAL and raw registers
1. `HAL_Init` + `SystemClock_Config` replace startup boilerplate
1. Callbacks replace hand-written **ISRs**
1. Trade **convenience for size and latency** — choose per file
