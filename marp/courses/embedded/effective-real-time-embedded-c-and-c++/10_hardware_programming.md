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
# Hardware Programming Model

---

## Chapter Overview

1. Interrupt handling architecture
1. Hardware vs software interrupts
1. Interrupt dispatchers and handlers
1. Context switching mechanisms
1. Real-world interrupt patterns

---

## Interrupt System Architecture

![interrupt_system_architecture](svg/courses/embedded/effective-real-time-embedded-c-and-c++/10_hardware_programming/interrupt_system_architecture.svg)

---

## Interrupt Vector Table

```c
// ARM Cortex-M vector table
typedef void (*vector_handler_t)(void);

__attribute__((section(".vectors")))
const vector_handler_t vector_table[] = {
    (vector_handler_t)&_estack,    // Initial stack pointer
    Reset_Handler,                 // Reset handler
    NMI_Handler,                  // NMI handler
    HardFault_Handler,            // Hard fault
    MemManage_Handler,            // Memory management fault
    BusFault_Handler,             // Bus fault
    UsageFault_Handler,           // Usage fault
    0, 0, 0, 0,                   // Reserved
    SVC_Handler,                  // SVCall
    DebugMon_Handler,             // Debug monitor
    0,                            // Reserved
    PendSV_Handler,               // PendSV
    SysTick_Handler,              // SysTick
    // External interrupts
    UART1_IRQHandler,             // IRQ0
    SPI1_IRQHandler,              // IRQ1
    // ... more IRQs
};
```

---

## Interrupt Priority Levels

```c
// Configure interrupt priorities
void configure_interrupts(void) {
    // Set priority grouping (3 bits preemption, 1 bit sub)
    NVIC_SetPriorityGrouping(3);

    // Critical interrupts - highest priority
    NVIC_SetPriority(UsageFault_IRQn, 0);
    NVIC_SetPriority(BusFault_IRQn, 0);

    // High priority - real-time
    NVIC_SetPriority(TIM2_IRQn, 1);
    NVIC_SetPriority(DMA1_Channel1_IRQn, 2);

    // Medium priority - communication
    NVIC_SetPriority(USART1_IRQn, 8);
    NVIC_SetPriority(SPI1_IRQn, 9);

    // Low priority - background
    NVIC_SetPriority(ADC1_IRQn, 12);

    // Enable interrupts
    NVIC_EnableIRQ(TIM2_IRQn);
    NVIC_EnableIRQ(USART1_IRQn);
}
```

---

## Interrupt Handler Structure

```c
// Basic interrupt handler
void TIM2_IRQHandler(void) {
    // 1. Save context (done by hardware)

    // 2. Check interrupt source
    if (TIM2->SR & TIM_SR_UIF) {
        // 3. Clear interrupt flag
        TIM2->SR &= ~TIM_SR_UIF;

        // 4. Handle interrupt
        timer_callback();

        // 5. Trigger any deferred processing
        trigger_software_interrupt();
    }

    // 6. Restore context and return (hardware)
}
```

---

## Nested Interrupts

![nested_interrupts](svg/courses/embedded/effective-real-time-embedded-c-and-c++/10_hardware_programming/nested_interrupts.svg)

---

## Context Saving

```c
// Manual context save (if not done by hardware)
typedef struct {
    uint32_t r0, r1, r2, r3;
    uint32_t r12, lr, pc, psr;
} hw_stack_frame_t;

typedef struct {
    uint32_t r4, r5, r6, r7;
    uint32_t r8, r9, r10, r11;
} sw_stack_frame_t;

// Context switch handler
__attribute__((naked))
void PendSV_Handler(void) {
    __asm__ volatile (
        "mrs r0, psp\n"           // Get process stack
        "stmdb r0!, {r4-r11}\n"   // Save registers

        "bl save_context\n"       // Save current task
        "bl select_next_task\n"   // Get next task
        "bl restore_context\n"    // Restore next task

        "ldmia r0!, {r4-r11}\n"   // Restore registers
        "msr psp, r0\n"           // Update stack pointer
        "bx lr\n"                 // Return
    );
}
```

---

## Hardware vs Software Interrupts

```c
// Hardware interrupt - external event
void EXTI0_IRQHandler(void) {
    if (EXTI->PR & EXTI_PR_PR0) {
        EXTI->PR = EXTI_PR_PR0;  // Clear flag

        // Handle button press
        button_pressed = true;

        // Trigger software interrupt for processing
        NVIC_SetPendingIRQ(EXTI15_10_IRQn);
    }
}

// Software interrupt - deferred processing
void EXTI15_10_IRQHandler(void) {
    if (button_pressed) {
        button_pressed = false;

        // Do time-consuming processing
        process_button_event();
    }
}

// Trigger software interrupt
void trigger_software_irq(void) {
    NVIC->STIR = EXTI15_10_IRQn;
}
```

---

## Interrupt Latency

```c
// Measure interrupt latency
volatile uint32_t irq_latency;

void trigger_test_interrupt(void) {
    uint32_t start = DWT->CYCCNT;

    // Trigger interrupt
    NVIC_SetPendingIRQ(TIM2_IRQn);

    // Wait for interrupt to complete
    while (!irq_complete);

    uint32_t cycles = DWT->CYCCNT - start;
    printf("Latency: %u cycles\n", cycles);
}

void TIM2_IRQHandler(void) {
    irq_latency = DWT->CYCCNT;
    irq_complete = true;
}
```

---

## Interrupt Dispatcher Pattern

```c
// Interrupt dispatcher for multiple sources
typedef struct {
    uint32_t mask;
    void (*handler)(void);
} irq_handler_t;

static const irq_handler_t uart_handlers[] = {
    { UART_IT_RXNE, uart_rx_handler },
    { UART_IT_TXE,  uart_tx_handler },
    { UART_IT_TC,   uart_tc_handler },
    { UART_IT_ERR,  uart_error_handler },
};

void USART1_IRQHandler(void) {
    uint32_t status = USART1->SR;
    uint32_t enabled = USART1->CR1;

    for (int i = 0; i < ARRAY_SIZE(uart_handlers); i++) {
        if ((status & enabled) & uart_handlers[i].mask) {
            uart_handlers[i].handler();
        }
    }
}
```

---

## Deferred Interrupt Processing

```c
// Two-level interrupt handling
typedef struct {
    void (*handler)(void* param);
    void* param;
} deferred_handler_t;

#define MAX_DEFERRED 16
static deferred_handler_t deferred_queue[MAX_DEFERRED];
static volatile uint32_t deferred_head = 0;
static volatile uint32_t deferred_tail = 0;

// Fast ISR - minimal processing
void high_priority_isr(void) {
    // Clear interrupt
    PERIPHERAL->FLAG = 0;

    // Queue deferred work
    uint32_t next = (deferred_head + 1) % MAX_DEFERRED;
    if (next != deferred_tail) {
        deferred_queue[deferred_head].handler = process_data;
        deferred_queue[deferred_head].param = get_data();
        deferred_head = next;

        // Trigger low priority interrupt
        NVIC_SetPendingIRQ(PendSV_IRQn);
    }
}

// Deferred processing
void PendSV_Handler(void) {
    while (deferred_tail != deferred_head) {
        deferred_handler_t* task = &deferred_queue[deferred_tail];
        task->handler(task->param);
        deferred_tail = (deferred_tail + 1) % MAX_DEFERRED;
    }
}
```

---

## Critical Sections in ISRs

```c
// Interrupt-safe critical sections
uint32_t enter_critical_from_isr(void) {
    uint32_t primask = __get_PRIMASK();
    __disable_irq();
    return primask;
}

void exit_critical_from_isr(uint32_t primask) {
    __set_PRIMASK(primask);
}

// ISR with critical section
void SPI1_IRQHandler(void) {
    if (SPI1->SR & SPI_SR_RXNE) {
        uint8_t data = SPI1->DR;

        // Critical section for shared data
        uint32_t state = enter_critical_from_isr();
        shared_buffer[write_idx++] = data;
        write_idx %= BUFFER_SIZE;
        exit_critical_from_isr(state);
    }
}
```

---

## Interrupt Sharing

```c
// Multiple peripherals sharing interrupt
void DMA1_Channel1_IRQHandler(void) {
    uint32_t isr = DMA1->ISR;

    // Channel 1 complete
    if (isr & DMA_ISR_TCIF1) {
        DMA1->IFCR = DMA_IFCR_CTCIF1;
        dma_ch1_complete();
    }

    // Channel 1 error
    if (isr & DMA_ISR_TEIF1) {
        DMA1->IFCR = DMA_IFCR_CTEIF1;
        dma_ch1_error();
    }

    // Channel 2 complete
    if (isr & DMA_ISR_TCIF2) {
        DMA1->IFCR = DMA_IFCR_CTCIF2;
        dma_ch2_complete();
    }
}
```

---

## Interrupt Coalescing

```c
// Reduce interrupt overhead
typedef struct {
    volatile uint32_t pending;
    uint32_t threshold;
    uint32_t timeout;
} irq_coalesce_t;

static irq_coalesce_t rx_coalesce = {
    .threshold = 8,    // 8 packets
    .timeout = 1000    // 1ms
};

void ETH_RX_IRQHandler(void) {
    rx_coalesce.pending++;

    // Process if threshold reached
    if (rx_coalesce.pending >= rx_coalesce.threshold) {
        process_rx_packets(rx_coalesce.pending);
        rx_coalesce.pending = 0;
        restart_timeout_timer();
    }
}

void TIMEOUT_IRQHandler(void) {
    if (rx_coalesce.pending > 0) {
        process_rx_packets(rx_coalesce.pending);
        rx_coalesce.pending = 0;
    }
}
```

---

## Exception Handling

```c
// Fault handler with context
void HardFault_Handler_C(uint32_t* stack_frame) {
    // Extract fault information
    uint32_t r0 = stack_frame[0];
    uint32_t r1 = stack_frame[1];
    uint32_t r2 = stack_frame[2];
    uint32_t r3 = stack_frame[3];
    uint32_t r12 = stack_frame[4];
    uint32_t lr = stack_frame[5];
    uint32_t pc = stack_frame[6];
    uint32_t psr = stack_frame[7];

    // Fault status registers
    uint32_t cfsr = SCB->CFSR;
    uint32_t hfsr = SCB->HFSR;
    uint32_t dfsr = SCB->DFSR;
    uint32_t afsr = SCB->AFSR;
    uint32_t bfar = SCB->BFAR;
    uint32_t mmar = SCB->MMAR;

    // Log fault information
    fault_log(pc, lr, cfsr, hfsr);

    // Reset or halt
    NVIC_SystemReset();
}

// Assembly wrapper
__attribute__((naked))
void HardFault_Handler(void) {
    __asm__ volatile (
        "tst lr, #4\n"
        "ite eq\n"
        "mrseq r0, msp\n"
        "mrsne r0, psp\n"
        "b HardFault_Handler_C\n"
    );
}
```

---

## Interrupt Priorities and Preemption

![interrupt_priorities_and_preemption](svg/courses/embedded/effective-real-time-embedded-c-and-c++/10_hardware_programming/interrupt_priorities_and_preemption.svg)

---

## SysTick Timer

```c
// Configure SysTick for 1ms interrupts
void systick_init(void) {
    // Assuming 168MHz system clock
    SysTick->LOAD = 168000 - 1;  // 1ms
    SysTick->VAL = 0;
    SysTick->CTRL = SysTick_CTRL_CLKSOURCE_Msk |
                    SysTick_CTRL_TICKINT_Msk |
                    SysTick_CTRL_ENABLE_Msk;
}

// SysTick handler
volatile uint32_t system_ticks = 0;

void SysTick_Handler(void) {
    system_ticks++;

    // Run scheduler every 10ms
    if ((system_ticks % 10) == 0) {
        scheduler_tick();
    }
}

// Delay function
void delay_ms(uint32_t ms) {
    uint32_t start = system_ticks;
    while ((system_ticks - start) < ms) {
        __WFI();  // Sleep until interrupt
    }
}
```

---

## External Interrupt Configuration

```c
// Configure GPIO for external interrupt
void configure_button_interrupt(void) {
    // Enable GPIO clock
    RCC->AHB1ENR |= RCC_AHB1ENR_GPIOAEN;

    // Configure PA0 as input with pull-up
    GPIOA->MODER &= ~(3U << 0);
    GPIOA->PUPDR |= (1U << 0);

    // Enable SYSCFG clock
    RCC->APB2ENR |= RCC_APB2ENR_SYSCFGEN;

    // Connect EXTI0 to PA0
    SYSCFG->EXTICR[0] &= ~SYSCFG_EXTICR1_EXTI0;
    SYSCFG->EXTICR[0] |= SYSCFG_EXTICR1_EXTI0_PA;

    // Configure falling edge trigger
    EXTI->FTSR |= EXTI_FTSR_TR0;

    // Enable interrupt
    EXTI->IMR |= EXTI_IMR_MR0;

    // Set priority and enable in NVIC
    NVIC_SetPriority(EXTI0_IRQn, 10);
    NVIC_EnableIRQ(EXTI0_IRQn);
}
```

---

## DMA Interrupt Handling

```c
// DMA transfer with interrupts
void start_dma_transfer(void* src, void* dst, size_t count) {
    // Disable DMA channel
    DMA1_Channel1->CCR &= ~DMA_CCR_EN;

    // Configure addresses and count
    DMA1_Channel1->CPAR = (uint32_t)src;
    DMA1_Channel1->CMAR = (uint32_t)dst;
    DMA1_Channel1->CNDTR = count;

    // Configure channel
    DMA1_Channel1->CCR = DMA_CCR_MINC |    // Memory increment
                         DMA_CCR_PINC |    // Peripheral increment
                         DMA_CCR_MSIZE_1 | // 32-bit memory
                         DMA_CCR_PSIZE_1 | // 32-bit peripheral
                         DMA_CCR_TCIE |    // Transfer complete IRQ
                         DMA_CCR_TEIE;     // Transfer error IRQ

    // Clear flags
    DMA1->IFCR = DMA_IFCR_CGIF1;

    // Enable DMA
    DMA1_Channel1->CCR |= DMA_CCR_EN;
}

void DMA1_Channel1_IRQHandler(void) {
    if (DMA1->ISR & DMA_ISR_TCIF1) {
        DMA1->IFCR = DMA_IFCR_CTCIF1;
        dma_complete_callback();
    }

    if (DMA1->ISR & DMA_ISR_TEIF1) {
        DMA1->IFCR = DMA_IFCR_CTEIF1;
        dma_error_callback();
    }
}
```

---

## Timer Interrupts

```c
// Configure timer for periodic interrupts
void timer_init(uint32_t frequency) {
    // Enable timer clock
    RCC->APB1ENR |= RCC_APB1ENR_TIM2EN;

    // Calculate prescaler and period
    uint32_t timer_clock = 84000000;  // APB1 timer clock
    uint32_t prescaler = 84 - 1;       // 1MHz after prescaling
    uint32_t period = (1000000 / frequency) - 1;

    // Configure timer
    TIM2->PSC = prescaler;
    TIM2->ARR = period;
    TIM2->CR1 = TIM_CR1_ARPE;  // Auto-reload preload

    // Enable update interrupt
    TIM2->DIER = TIM_DIER_UIE;

    // Start timer
    TIM2->CR1 |= TIM_CR1_CEN;

    // Enable interrupt in NVIC
    NVIC_EnableIRQ(TIM2_IRQn);
}

void TIM2_IRQHandler(void) {
    if (TIM2->SR & TIM_SR_UIF) {
        TIM2->SR &= ~TIM_SR_UIF;  // Clear flag

        // Toggle LED
        GPIOA->ODR ^= GPIO_ODR_OD5;

        // Update timing statistics
        timing_update();
    }
}
```

---

## UART Interrupts

```c
// UART interrupt-driven communication
typedef struct {
    uint8_t* buffer;
    size_t size;
    volatile size_t head;
    volatile size_t tail;
} uart_buffer_t;

static uart_buffer_t uart_rx_buf = {
    .buffer = rx_buffer,
    .size = RX_BUFFER_SIZE
};

void USART1_IRQHandler(void) {
    uint32_t sr = USART1->SR;

    // Receive interrupt
    if ((sr & USART_SR_RXNE) && (USART1->CR1 & USART_CR1_RXNEIE)) {
        uint8_t data = USART1->DR;

        size_t next = (uart_rx_buf.head + 1) % uart_rx_buf.size;
        if (next != uart_rx_buf.tail) {
            uart_rx_buf.buffer[uart_rx_buf.head] = data;
            uart_rx_buf.head = next;
        }
    }

    // Transmit interrupt
    if ((sr & USART_SR_TXE) && (USART1->CR1 & USART_CR1_TXEIE)) {
        if (uart_tx_buf.head != uart_tx_buf.tail) {
            USART1->DR = uart_tx_buf.buffer[uart_tx_buf.tail];
            uart_tx_buf.tail = (uart_tx_buf.tail + 1) % uart_tx_buf.size;
        } else {
            // Disable TX interrupt when buffer empty
            USART1->CR1 &= ~USART_CR1_TXEIE;
        }
    }

    // Error handling
    if (sr & (USART_SR_ORE | USART_SR_FE | USART_SR_PE)) {
        volatile uint8_t dummy = USART1->DR;  // Clear errors
        uart_error_count++;
    }
}
```

---

## Wake-up Interrupts

```c
// Configure wake-up from low power mode
void configure_wakeup_interrupt(void) {
    // Configure RTC wake-up
    RTC->CR &= ~RTC_CR_WUTE;  // Disable wake-up timer

    // Wait for access
    while (!(RTC->ISR & RTC_ISR_WUTWF));

    // Set wake-up period (1 second)
    RTC->WUTR = 0x0FFF;

    // Select clock source
    RTC->CR &= ~RTC_CR_WUCKSEL;
    RTC->CR |= RTC_CR_WUCKSEL_2;  // ck_spre (1Hz)

    // Enable wake-up timer and interrupt
    RTC->CR |= RTC_CR_WUTIE | RTC_CR_WUTE;

    // Enable EXTI line 22 (RTC wake-up)
    EXTI->IMR |= EXTI_IMR_MR22;
    EXTI->RTSR |= EXTI_RTSR_TR22;

    // Enable interrupt in NVIC
    NVIC_EnableIRQ(RTC_WKUP_IRQn);
}

void RTC_WKUP_IRQHandler(void) {
    if (RTC->ISR & RTC_ISR_WUTF) {
        RTC->ISR &= ~RTC_ISR_WUTF;  // Clear flag
        EXTI->PR = EXTI_PR_PR22;     // Clear EXTI

        // Perform periodic task
        wakeup_task();
    }
}
```

---

## Interrupt Statistics

```c
// Track interrupt performance
typedef struct {
    uint32_t count;
    uint32_t max_latency;
    uint32_t total_time;
    uint32_t max_duration;
} irq_stats_t;

static irq_stats_t irq_stats[MAX_IRQ_NUM];

#define IRQ_MEASURE_START(irq_num) \
    uint32_t _start_##irq_num = DWT->CYCCNT

#define IRQ_MEASURE_END(irq_num) do { \
    uint32_t _cycles = DWT->CYCCNT - _start_##irq_num; \
    irq_stats[irq_num].count++; \
    irq_stats[irq_num].total_time += _cycles; \
    if (_cycles > irq_stats[irq_num].max_duration) { \
        irq_stats[irq_num].max_duration = _cycles; \
    } \
} while(0)

// Example usage
void USART1_IRQHandler(void) {
    IRQ_MEASURE_START(USART1_IRQn);

    // Handler code...

    IRQ_MEASURE_END(USART1_IRQn);
}
```

---

## Best Practices

1. **Keep ISRs short** - defer heavy processing
1. **Clear flags early** - prevent re-entry
1. **Use volatile** - for ISR-shared variables
1. **Avoid blocking** - no delays or waits
1. **Minimize stack usage** - limited ISR stack

---

## Common Pitfalls

```c
// BAD: Long ISR
void BAD_IRQHandler(void) {
    for (int i = 0; i < 1000; i++) {
        process_data(i);  // Too long!
    }
}

// GOOD: Defer processing
void GOOD_IRQHandler(void) {
    set_flag();  // Quick
    trigger_deferred_processing();
}

// BAD: Calling non-reentrant functions
void BAD_IRQHandler2(void) {
    printf("Interrupt!\n");  // Not interrupt-safe!
}

// GOOD: Use interrupt-safe alternatives
void GOOD_IRQHandler2(void) {
    debug_puts("Interrupt!\n");  // ISR-safe version
}
```

---

## Summary

1. Understand interrupt architecture and priorities
1. Implement efficient interrupt handlers
1. Use proper context switching techniques
1. Leverage hardware features effectively
1. Monitor and optimize interrupt performance

---

## Key Takeaways

1. **ISRs** should be fast and deterministic
1. **Priorities** control preemption behavior
1. **Context** must be properly saved/restored
1. **Deferred processing** for complex operations
1. **Measurement** helps optimization
