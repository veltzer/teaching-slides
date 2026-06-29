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
# Core Peripherals

---

## Chapter Overview

1. GPIO: LEDs and the user buttons
1. UART: the debug console
1. SPI and the on-chip radio peripheral
1. Timers and PWM
1. DMA to offload the CPU

---

## What This Board Gives You

1. Three user LEDs (blue, green, red)
1. Three user buttons (B1, B2, B3)
1. UART wired to the ST-LINK virtual COM port
1. A **SUBGHZ** radio reachable over an internal SPI
1. Standard STM32 timers, ADC, I2C, SPI

---

## GPIO: LEDs And Buttons

```c
// LEDs: PB15 (blue), PB9 (green), PB11 (red)
// Buttons: PA0 (B1), PA1 (B2), PC6 (B3)

HAL_GPIO_WritePin(GPIOB, GPIO_PIN_15, GPIO_PIN_SET);

if (HAL_GPIO_ReadPin(GPIOA, GPIO_PIN_0) == GPIO_PIN_RESET) {
    // B1 pressed (active low with pull-up)
}
```

Always check the board user manual for the exact pin mapping.

---

## UART: The Console

```c
// Already configured as huart2 at 115200 8N1
char line[64];
int n = snprintf(line, sizeof line, "temp=%d\r\n", temp);
HAL_UART_Transmit(&huart2, (uint8_t*)line, n, HAL_MAX_DELAY);
```

1. Appears as `/dev/ttyACM0` over the ST-LINK
1. Your lifeline for logging and `printf`
1. Use **interrupt or DMA** mode to avoid blocking

---

## The SUBGHZ Radio Peripheral

1. The radio core is reached via a dedicated **SUBGHZSPI**
1. It is **not** an external SPI bus — it is internal
1. HAL provides `SUBGHZ_HandleTypeDef` and helpers
1. You write radio **commands and registers** over it
1. The LoRaWAN middleware wraps all of this for you

---

## Talking To The Radio

```c
SUBGHZ_HandleTypeDef hsubghz;
hsubghz.Init.BaudratePrescaler = SUBGHZSPI_BAUDRATEPRESCALER_4;
HAL_SUBGHZ_Init(&hsubghz);

// Put the radio in standby, then set frequency etc.
uint8_t standby = 0x00;   // STDBY_RC
HAL_SUBGHZ_ExecSetCmd(&hsubghz, RADIO_SET_STANDBY,
                      &standby, 1);
```

We treat the radio as a coprocessor with a command protocol.

---

## Peripheral Bus Layout

![peripheral_bus_layout](svg/courses/embedded/stm32-nucleo-wl55jc1-firmware/05_peripherals/peripheral_bus_layout.svg)

---

## Timers And PWM

```c
// htim2 configured for PWM on channel 1
HAL_TIM_PWM_Start(&htim2, TIM_CHANNEL_1);

// 0..1000 duty maps to the configured period
__HAL_TIM_SET_COMPARE(&htim2, TIM_CHANNEL_1, 250);  // 25%
```

1. Timers give precise periodic interrupts
1. PWM drives LEDs, motors, tones
1. A timer is also the base for **software time-bases**

---

## DMA: Move Data Without The CPU

1. **Direct Memory Access** copies between memory and peripherals
1. Frees the CPU during long UART/SPI transfers
1. Essential for **streaming** sensor or radio data
1. HAL exposes `_DMA` variants of transfer calls
1. Watch cache/coherency — here it is simple (no data cache)

---

## A DMA UART Transmit

```c
// Non-blocking: returns immediately, DMA does the work
HAL_UART_Transmit_DMA(&huart2, big_buffer, big_len);

// Notified when the transfer finishes
void HAL_UART_TxCpltCallback(UART_HandleTypeDef *huart) {
    tx_done = true;
}
```

The CPU is free to compute (or sleep) while the bytes go out.

---

## Key Takeaways

1. LEDs/buttons are plain **GPIO** — mind the pin map
1. The **UART console** is your primary debug tool
1. The radio is an internal **SUBGHZSPI** coprocessor
1. **Timers/PWM** give you precise timing and outputs
1. **DMA** offloads bulk transfers from the CPU
