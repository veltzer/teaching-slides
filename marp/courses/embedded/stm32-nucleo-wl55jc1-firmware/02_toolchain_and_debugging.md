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

# Toolchain And Debugging

---

## Chapter Overview

1. Choosing a toolchain
1. Building from the command line
1. Flashing the board
1. Debugging with GDB and OpenOCD
1. Debugging a dual-core target

---

## Toolchain Options

1. **STM32CubeIDE** — Eclipse-based, all-in-one, GUI
1. **arm-none-eabi-gcc + Make/CMake** — scriptable, CI-friendly
1. **PlatformIO** — wraps the GCC toolchain
1. We focus on the **CLI** path: it teaches what is happening
1. CubeIDE is fine, but it hides the mechanics

---

## What You Need Installed

```bash
# The cross compiler
arm-none-eabi-gcc --version

# The on-chip debugger / flasher
openocd --version

# ST's command line flash tool (alternative to openocd)
STM32_Programmer_CLI --version
```

---

## Compiler Flags That Matter

```makefile
CPU    = -mcpu=cortex-m4
FPU    = -mfpu=fpv4-sp-d16 -mfloat-abi=hard
MCU    = $(CPU) -mthumb $(FPU)

CFLAGS = $(MCU) -DSTM32WL55xx -Os -g3 \
         -ffunction-sections -fdata-sections -Wall

LDFLAGS = $(MCU) -T STM32WL55JCIX_FLASH.ld \
          -Wl,--gc-sections -specs=nano.specs
```

Note: the **M0+ core** builds with `-mcpu=cortex-m0plus` and no FPU.

---

## The Linker Script Defines Memory

```ld
/* STM32WL55JCIX_FLASH.ld (CPU1 view) */
MEMORY
{
  FLASH (rx)  : ORIGIN = 0x08000000, LENGTH = 256K
  RAM1  (xrw) : ORIGIN = 0x20000000, LENGTH = 32K
  RAM2  (xrw) : ORIGIN = 0x20008000, LENGTH = 32K
}
```

The linker script is where **shared memory regions** are reserved later.

---

## Flashing The Board

```bash
# Using OpenOCD
openocd -f interface/stlink.cfg -f target/stm32wlx.cfg \
        -c "program build/app.elf verify reset exit"

# Using ST's CLI
STM32_Programmer_CLI -c port=SWD -w build/app.bin 0x08000000 -rst
```

The on-board **ST-LINK** appears as a USB device — no extra probe needed.

---

## Debugging With GDB

```bash
# Terminal 1: start the gdb server
openocd -f interface/stlink.cfg -f target/stm32wlx.cfg

# Terminal 2: connect gdb
arm-none-eabi-gdb build/app.elf
(gdb) target extended-remote localhost:3333
(gdb) load
(gdb) monitor reset halt
(gdb) break main
(gdb) continue
```

---

## Debug Workflow

![debug_workflow](svg/courses/embedded/stm32-nucleo-wl55jc1-firmware/02_toolchain_and_debugging/debug_workflow.svg)

---

## Debugging The Second Core

1. SWD on this board exposes **CPU1 (M4)** by default
1. **CPU2 (M0+)** debug must be enabled deliberately
1. Halting CPU1 does **not** auto-halt CPU2
1. Use ST-LINK GDB server with the **dual-core** option
1. Most teams debug CPU2 by **printf over IPCC** instead

---

## Printf Debugging Over The RF Console

1. The board has a UART wired to the ST-LINK **VCP**
1. Retarget `_write()` to that UART for `printf`
1. Appears as `/dev/ttyACM0` on the host
1. Cheap, always-available, non-intrusive
1. The first thing to bring up on any new board

---

## Retargeting printf

```c
// Send each character to USART2 (the ST-LINK VCP)
int _write(int fd, char *buf, int len) {
    (void)fd;
    for (int i = 0; i < len; i++) {
        while (!(USART2->ISR & USART_ISR_TXE_TXFNF)) { }
        USART2->TDR = (uint8_t)buf[i];
    }
    return len;
}
```

---

## Key Takeaways

1. CLI toolchain = **gcc + openocd + gdb**
1. The **linker script** owns the memory layout
1. Flash via the **on-board ST-LINK**, no extra hardware
1. Bring up a **UART console** before anything else
1. Debugging **CPU2** is harder — lean on `printf`
