---
tags:
  - hardware-and-embedded:embedded
  - infrastructure:real-time
level: advanced
category: embedded
audience:
  - audiences:embedded-engineers
  - audiences:developers

---

# Timing

---

## Chapter Overview

1. Challenges in measuring time
1. Hardware and software timers
1. Watchdog timer implementation
1. Real-time debugging considerations
1. Time synchronization techniques

---

## Time Measurement Challenges

![time_measurement_challenges](svg/courses/embedded/effective-real-time-embedded-c-and-c++/11_timing/time_measurement_challenges.svg)

---

## Clock Sources

```c
// Typical embedded clock sources
typedef enum {
    CLOCK_HSI,      // High-speed internal (8-16 MHz)
    CLOCK_HSE,      // High-speed external (4-26 MHz)
    CLOCK_LSI,      // Low-speed internal (32-40 kHz)
    CLOCK_LSE,      // Low-speed external (32.768 kHz)
    CLOCK_PLL       // Phase-locked loop (up to 168 MHz)
} clock_source_t;

// Clock accuracy
typedef struct {
    uint32_t frequency;
    int32_t ppm_error;    // Parts per million
    float temp_drift;     // ppm/°C
} clock_info_t;

const clock_info_t clock_specs[] = {
    [CLOCK_HSI] = { 16000000, 10000, 30.0 },  // ±1%
    [CLOCK_HSE] = { 8000000,  50,    0.5 },   // Crystal
    [CLOCK_LSI] = { 32000,    150000, 100.0 }, // ±15%
    [CLOCK_LSE] = { 32768,    20,    0.04 }   // Crystal
};
```

---

## CPU Cycle Counter

```c
// ARM Cortex-M DWT (Data Watchpoint and Trace)
void enable_cycle_counter(void) {
    // Enable DWT
    CoreDebug->DEMCR |= CoreDebug_DEMCR_TRCENA_Msk;

    // Reset cycle counter
    DWT->CYCCNT = 0;

    // Enable cycle counter
    DWT->CTRL |= DWT_CTRL_CYCCNTENA_Msk;
}

// Measure execution time
uint32_t measure_cycles(void (*function)(void)) {
    uint32_t start = DWT->CYCCNT;
    function();
    return DWT->CYCCNT - start;
}

// Convert cycles to microseconds
uint32_t cycles_to_us(uint32_t cycles) {
    return cycles / (SystemCoreClock / 1000000);
}
```

---

## Hardware Timer Configuration

```c
// 32-bit timer for microsecond precision
void timer_init_us(void) {
    // Enable timer clock
    RCC->APB1ENR |= RCC_APB1ENR_TIM2EN;

    // Configure for 1 MHz (1 µs resolution)
    TIM2->PSC = (SystemCoreClock / 1000000) - 1;
    TIM2->ARR = 0xFFFFFFFF;  // Max period

    // Enable timer
    TIM2->CR1 = TIM_CR1_CEN;
}

uint32_t get_us(void) {
    return TIM2->CNT;
}

uint32_t elapsed_us(uint32_t start) {
    return get_us() - start;
}

// Delay function
void delay_us(uint32_t us) {
    uint32_t start = get_us();
    while (elapsed_us(start) < us) {
        __NOP();
    }
}
```

---

## Timer Cascade for Extended Range

```c
// 64-bit timer using two 32-bit timers
typedef struct {
    TIM_TypeDef* tim_low;
    TIM_TypeDef* tim_high;
    volatile uint32_t overflows;
} timer64_t;

void timer64_init(timer64_t* timer) {
    // Configure low timer
    timer->tim_low->PSC = 0;  // No prescaler
    timer->tim_low->ARR = 0xFFFFFFFF;
    timer->tim_low->CR1 = TIM_CR1_CEN;

    // Configure high timer (counts overflows)
    timer->tim_high->SMCR = TIM_SMCR_TS_0;  // ITR1
    timer->tim_high->SMCR |= TIM_SMCR_SMS_2 | TIM_SMCR_SMS_1;
    timer->tim_high->CR1 = TIM_CR1_CEN;
}

uint64_t timer64_get(timer64_t* timer) {
    uint32_t low, high;
    do {
        high = timer->tim_high->CNT;
        low = timer->tim_low->CNT;
    } while (high != timer->tim_high->CNT);  // Handle rollover

    return ((uint64_t)high << 32) | low;
}
```

---

## Periodic Timer Events

```c
// Timer callback system
typedef struct timer_event {
    uint32_t period;
    uint32_t next_time;
    void (*callback)(void* param);
    void* param;
    bool active;
    struct timer_event* next;
} timer_event_t;

static timer_event_t* timer_list = NULL;

void timer_tick_handler(void) {
    uint32_t current_time = get_system_time();
    timer_event_t* timer = timer_list;

    while (timer) {
        if (timer->active &&
            time_after_eq(current_time, timer->next_time)) {
            timer->callback(timer->param);
            timer->next_time = current_time + timer->period;
        }
        timer = timer->next;
    }
}

// Time comparison macros
#define time_after(a, b) ((int32_t)(b) - (int32_t)(a) < 0)
#define time_after_eq(a, b) ((int32_t)(a) - (int32_t)(b) >= 0)
```

---

## High-Resolution Timer

```c
// Capture/Compare for precise timing
void setup_input_capture(void) {
    // Configure TIM3 CH1 for input capture
    TIM3->CCMR1 = TIM_CCMR1_CC1S_0;  // Input on TI1
    TIM3->CCER = TIM_CCER_CC1E;      // Enable capture
    TIM3->DIER = TIM_DIER_CC1IE;     // Enable interrupt
    TIM3->CR1 = TIM_CR1_CEN;          // Start timer
}

volatile uint32_t pulse_width = 0;
volatile uint32_t last_capture = 0;

void TIM3_IRQHandler(void) {
    if (TIM3->SR & TIM_SR_CC1IF) {
        TIM3->SR &= ~TIM_SR_CC1IF;

        uint32_t capture = TIM3->CCR1;
        if (TIM3->CCER & TIM_CCER_CC1P) {
            // Falling edge - calculate pulse width
            pulse_width = capture - last_capture;
            TIM3->CCER &= ~TIM_CCER_CC1P;  // Next: rising
        } else {
            // Rising edge
            last_capture = capture;
            TIM3->CCER |= TIM_CCER_CC1P;   // Next: falling
        }
    }
}
```

---

## Watchdog Timer Types

![watchdog_timer_types](svg/courses/embedded/effective-real-time-embedded-c-and-c++/11_timing/watchdog_timer_types.svg)

---

## Independent Watchdog

```c
// IWDG - runs on LSI clock
void iwdg_init(uint32_t timeout_ms) {
    // Enable IWDG access
    IWDG->KR = 0x5555;

    // Set prescaler (LSI = 32kHz)
    // Prescaler 32 = 1ms per count
    IWDG->PR = IWDG_PR_PR_2;  // /32

    // Set reload value
    IWDG->RLR = timeout_ms;

    // Start watchdog
    IWDG->KR = 0xCCCC;
}

// Feed watchdog
void iwdg_feed(void) {
    IWDG->KR = 0xAAAA;
}

// Watchdog task
void watchdog_task(void) {
    static uint32_t last_feed = 0;

    // Check system health
    if (system_healthy()) {
        iwdg_feed();
        last_feed = get_system_time();
    } else {
        // Let watchdog expire
        log_error("System unhealthy - WDT reset pending");
    }
}
```

---

## Window Watchdog

```c
// WWDG - enforces min and max feed times
void wwdg_init(uint8_t window, uint8_t counter) {
    // Enable WWDG clock
    RCC->APB1ENR |= RCC_APB1ENR_WWDGEN;

    // Set window value (feed only when CNT < WIN)
    WWDG->CFR = WWDG_CFR_WDGTB_1 |  // Prescaler /4
                (window & 0x7F);

    // Enable and set counter
    WWDG->CR = WWDG_CR_WDGA |       // Enable
               (counter & 0x7F);      // Counter value

    // Enable early wakeup interrupt
    WWDG->CFR |= WWDG_CFR_EWI;
    NVIC_EnableIRQ(WWDG_IRQn);
}

void WWDG_IRQHandler(void) {
    // Clear flag
    WWDG->SR = 0;

    // Feed if system OK
    if (critical_checks_pass()) {
        WWDG->CR = 0x7F;  // Reset counter
    }
    // Otherwise, reset in ~50ms
}
```

---

## Software Timers

```c
// Lightweight software timer implementation
typedef struct sw_timer {
    uint32_t expiry;
    void (*handler)(void);
    struct sw_timer* next;
} sw_timer_t;

static sw_timer_t* active_timers = NULL;

void sw_timer_start(sw_timer_t* timer, uint32_t delay_ms) {
    timer->expiry = get_system_time() + delay_ms;

    // Insert sorted by expiry time
    sw_timer_t** pp = &active_timers;
    while (*pp && time_before((*pp)->expiry, timer->expiry)) {
        pp = &(*pp)->next;
    }
    timer->next = *pp;
    *pp = timer;
}

void sw_timer_process(void) {
    uint32_t now = get_system_time();

    while (active_timers &&
           time_after_eq(now, active_timers->expiry)) {
        sw_timer_t* timer = active_timers;
        active_timers = timer->next;
        timer->handler();
    }
}
```

---

## Time Synchronization

```c
// NTP-like time sync for embedded
typedef struct {
    uint32_t local_time;
    uint32_t reference_time;
    int32_t offset;
    int32_t drift_ppb;  // Parts per billion
} time_sync_t;

void time_sync_update(time_sync_t* sync,
                     uint32_t remote_time) {
    uint32_t local = get_local_time();

    // Calculate offset
    int32_t new_offset = remote_time - local;

    // Simple drift calculation
    if (sync->reference_time) {
        uint32_t elapsed = local - sync->local_time;
        int32_t offset_change = new_offset - sync->offset;

        // Drift in ppb
        sync->drift_ppb = ((int64_t)offset_change * 1000000000)
                         / elapsed;
    }

    sync->local_time = local;
    sync->reference_time = remote_time;
    sync->offset = new_offset;
}
```

---

## Time Synchronization: Get Synced Time

```c
uint32_t get_synchronized_time(time_sync_t* sync) {
    uint32_t local = get_local_time();
    uint32_t elapsed = local - sync->local_time;

    // Apply offset and drift correction
    int32_t drift_correction = (sync->drift_ppb * elapsed)
                              / 1000000000;

    return local + sync->offset + drift_correction;
}
```

---

## Real-Time Clock (RTC)

```c
// RTC configuration for timekeeping
void rtc_init(void) {
    // Enable PWR and RTC clocks
    RCC->APB1ENR |= RCC_APB1ENR_PWREN;
    PWR->CR |= PWR_CR_DBP;  // Disable backup protection

    // Reset RTC
    RCC->BDCR |= RCC_BDCR_BDRST;
    RCC->BDCR &= ~RCC_BDCR_BDRST;

    // Enable LSE
    RCC->BDCR |= RCC_BDCR_LSEON;
    while (!(RCC->BDCR & RCC_BDCR_LSERDY));

    // Select LSE as RTC clock
    RCC->BDCR |= RCC_BDCR_RTCSEL_0;
    RCC->BDCR |= RCC_BDCR_RTCEN;

    // Configure RTC
    RTC->WPR = 0xCA;  // Unlock
    RTC->WPR = 0x53;

    RTC->ISR |= RTC_ISR_INIT;
    while (!(RTC->ISR & RTC_ISR_INITF));

    // Set prescaler for 1Hz
    RTC->PRER = (127 << 16) | 255;  // Async=128, Sync=256

    RTC->ISR &= ~RTC_ISR_INIT;
    RTC->WPR = 0xFF;  // Lock
}
```

---

## Timestamp Capture

```c
// Hardware timestamp for events
typedef struct {
    uint32_t seconds;
    uint16_t subseconds;
    uint8_t event_type;
} timestamp_t;

void capture_timestamp(timestamp_t* ts, uint8_t event) {
    // Atomic read of RTC time and subseconds
    uint32_t ssr, tr, dr;

    do {
        ssr = RTC->SSR;
        tr = RTC->TR;
        dr = RTC->DR;
    } while (ssr != RTC->SSR);  // Ensure coherent read

    // Convert BCD to binary
    ts->seconds = bcd_to_bin(tr & 0x7F) +           // Seconds
                  bcd_to_bin((tr >> 8) & 0x7F) * 60 + // Minutes
                  bcd_to_bin((tr >> 16) & 0x3F) * 3600; // Hours

    ts->subseconds = ssr & 0xFFFF;
    ts->event_type = event;
}

uint8_t bcd_to_bin(uint8_t bcd) {
    return (bcd >> 4) * 10 + (bcd & 0x0F);
}
```

---

## Timing Constraints

```c
// Deadline monitoring
typedef struct {
    const char* name;
    uint32_t deadline_us;
    uint32_t worst_case_us;
    uint32_t violations;
} deadline_monitor_t;

#define DEADLINE_START(monitor) \
    uint32_t _deadline_start_##monitor = get_us()

#define DEADLINE_CHECK(monitor) do { \
    uint32_t _elapsed = get_us() - _deadline_start_##monitor; \
    if (_elapsed > (monitor).worst_case_us) { \
        (monitor).worst_case_us = _elapsed; \
    } \
    if (_elapsed > (monitor).deadline_us) { \
        (monitor).violations++; \
        deadline_violation(&(monitor), _elapsed); \
    } \
} while(0)

// Usage
deadline_monitor_t control_loop = {
    .name = "Control Loop",
    .deadline_us = 1000,  // 1ms deadline
};

void control_task(void) {
    DEADLINE_START(control_loop);

    // Time-critical processing
    read_sensors();
    compute_control();
    write_actuators();

    DEADLINE_CHECK(control_loop);
}
```

---

## Profiling with Timestamps

```c
// Function execution profiling
typedef struct {
    const char* name;
    uint32_t call_count;
    uint64_t total_cycles;
    uint32_t min_cycles;
    uint32_t max_cycles;
} profile_entry_t;

#define MAX_PROFILE_ENTRIES 50
static profile_entry_t profiles[MAX_PROFILE_ENTRIES];
static int profile_count = 0;

#define PROFILE_FUNC(func) \
    static profile_entry_t* _prof_##func = NULL; \
    if (!_prof_##func) { \
        _prof_##func = &profiles[profile_count++]; \
        _prof_##func->name = #func; \
        _prof_##func->min_cycles = UINT32_MAX; \
    } \
    uint32_t _start_##func = DWT->CYCCNT; \
    func; \
    uint32_t _cycles_##func = DWT->CYCCNT - _start_##func; \
    _prof_##func->call_count++; \
    _prof_##func->total_cycles += _cycles_##func; \
    if (_cycles_##func < _prof_##func->min_cycles) \
        _prof_##func->min_cycles = _cycles_##func; \
    if (_cycles_##func > _prof_##func->max_cycles) \
        _prof_##func->max_cycles = _cycles_##func
```

---

## Time-Based State Machines

```c
// State machine with timeouts
typedef enum {
    STATE_IDLE,
    STATE_WAIT_RESPONSE,
    STATE_PROCESSING,
    STATE_ERROR
} state_t;

typedef struct {
    state_t current_state;
    uint32_t state_entry_time;
    uint32_t timeout_ms;
} timed_fsm_t;
```

---

## Time-Based State Machines: Update

```c
void fsm_update(timed_fsm_t* fsm) {
    uint32_t elapsed = get_ms() - fsm->state_entry_time;

    switch (fsm->current_state) {
    case STATE_WAIT_RESPONSE:
        if (response_received()) {
            fsm_transition(fsm, STATE_PROCESSING);
        } else if (elapsed > fsm->timeout_ms) {
            fsm_transition(fsm, STATE_ERROR);
            log_timeout("Response timeout");
        }
        break;

    case STATE_PROCESSING:
        if (processing_complete()) {
            fsm_transition(fsm, STATE_IDLE);
        } else if (elapsed > PROCESSING_TIMEOUT) {
            fsm_transition(fsm, STATE_ERROR);
        }
        break;

    // Other states...
    }
}

void fsm_transition(timed_fsm_t* fsm, state_t new_state) {
    fsm->current_state = new_state;
    fsm->state_entry_time = get_ms();
}
```

---

## Debug Timer Conflicts

```c
// Debugging impact on timing
#ifdef DEBUG_TIMING
typedef struct {
    uint32_t uart_time;
    uint32_t printf_time;
    uint32_t log_time;
} debug_overhead_t;

static debug_overhead_t overhead;

void debug_printf(const char* fmt, ...) {
    uint32_t start = DWT->CYCCNT;

    va_list args;
    va_start(args, fmt);
    vprintf(fmt, args);
    va_end(args);

    overhead.printf_time += DWT->CYCCNT - start;
}

// Compensate for debug overhead
uint32_t get_compensated_time(void) {
    return get_us() - cycles_to_us(overhead.printf_time);
}
#else
#define debug_printf(...)
#endif
```

---

## Timer Interrupt Jitter

```c
// Measure and compensate for jitter
typedef struct {
    uint32_t period;
    uint32_t last_time;
    int32_t accumulated_error;
    uint32_t jitter_max;
} jitter_compensator_t;

void timer_irq_with_compensation(jitter_compensator_t* comp) {
    uint32_t now = get_us();
    uint32_t actual_period = now - comp->last_time;

    // Calculate jitter
    int32_t jitter = actual_period - comp->period;
    if (abs(jitter) > comp->jitter_max) {
        comp->jitter_max = abs(jitter);
    }

    // Accumulate error
    comp->accumulated_error += jitter;

    // Compensate next period
    int32_t compensation = comp->accumulated_error / 10;
    TIM2->ARR = comp->period - compensation;

    comp->accumulated_error -= compensation;
    comp->last_time = now;
}
```

---

## Low Power Timer Wake-up

```c
// Configure LPTIM for low-power timing
void lptim_init_wakeup(uint32_t period_ms) {
    // Enable LPTIM clock
    RCC->APB1ENR |= RCC_APB1ENR_LPTIM1EN;

    // Select LSE as clock source (32.768 kHz)
    RCC->CCIPR |= RCC_CCIPR_LPTIM1SEL_1 | RCC_CCIPR_LPTIM1SEL_0;

    // Configure LPTIM
    LPTIM1->CFGR = LPTIM_CFGR_PRESC_2;  // Prescaler /16 = 2048 Hz

    // Enable interrupt
    LPTIM1->IER = LPTIM_IER_ARRMIE;

    // Enable LPTIM
    LPTIM1->CR = LPTIM_CR_ENABLE;

    // Set auto-reload value
    LPTIM1->ARR = (period_ms * 2048) / 1000;

    // Start continuous mode
    LPTIM1->CR |= LPTIM_CR_CNTSTRT;
}

void LPTIM1_IRQHandler(void) {
    if (LPTIM1->ISR & LPTIM_ISR_ARRM) {
        LPTIM1->ICR = LPTIM_ICR_ARRMCF;

        // Periodic wake-up task
        low_power_task();
    }
}
```

---

## Multi-Core Timing

```c
// Time synchronization between cores
typedef struct {
    volatile uint32_t master_time;
    volatile uint32_t slave_time;
    volatile int32_t offset;
    volatile bool sync_request;
    volatile bool sync_complete;
} core_time_sync_t;

// Master core
void master_sync_time(core_time_sync_t* sync) {
    sync->master_time = get_local_time();
    sync->sync_request = true;

    // Wait for slave
    while (!sync->sync_complete) {
        __DMB();  // Memory barrier
    }

    // Calculate offset
    uint32_t round_trip = get_local_time() - sync->master_time;
    sync->offset = sync->slave_time - sync->master_time
                  - (round_trip / 2);

    sync->sync_complete = false;
}

// Slave core
void slave_sync_time(core_time_sync_t* sync) {
    while (!sync->sync_request) {
        __WFE();  // Wait for event
    }

    sync->slave_time = get_local_time();
    sync->sync_request = false;
    sync->sync_complete = true;
    __DSB();  // Ensure write visibility
}
```

---

## Timing Analysis Tools

```c
// Logic analyzer trigger for timing
void timing_trigger_output(uint8_t channel, bool state) {
    if (state) {
        GPIOB->BSRR = (1 << channel);      // Set pin
    } else {
        GPIOB->BSRR = (1 << (channel + 16)); // Reset pin
    }
}

// Timing markers
#define TIMING_MARK_START(ch) timing_trigger_output(ch, true)
#define TIMING_MARK_END(ch)   timing_trigger_output(ch, false)

// Example usage
void process_frame(void) {
    TIMING_MARK_START(0);  // Channel 0 high

    acquire_data();
    TIMING_MARK_START(1);  // Channel 1 high

    filter_data();
    TIMING_MARK_END(1);    // Channel 1 low

    output_results();
    TIMING_MARK_END(0);    // Channel 0 low
}
```

---

## Common Timing Pitfalls

```c
// BAD: Integer overflow in delay
void bad_delay_ms(uint32_t ms) {
    uint32_t start = get_ms();
    while (get_ms() < start + ms);  // Overflow!
}

// GOOD: Overflow-safe comparison
void good_delay_ms(uint32_t ms) {
    uint32_t start = get_ms();
    while ((get_ms() - start) < ms);  // Works across overflow
}

// BAD: Blocking in ISR
void bad_isr(void) {
    delay_ms(10);  // Never delay in ISR!
}

// GOOD: Non-blocking timeout
void good_isr(void) {
    static uint32_t next_time = 0;
    if (time_after_eq(get_ms(), next_time)) {
        do_periodic_task();
        next_time = get_ms() + 10;
    }
}
```

---

## Summary

1. Multiple timing sources with different trade-offs
1. Hardware timers for precision timing
1. Watchdog timers for system reliability
1. Careful handling of time overflow and jitter
1. Debug considerations for real-time systems

---

## Key Takeaways

1. **Resolution vs range** - choose appropriate timer
1. **Overflow handling** - use proper comparisons
1. **Jitter compensation** - for periodic events
1. **Watchdog design** - balance safety and false triggers
1. **Debug impact** - measure and compensate

---

## Scheduling Algorithms

![scheduling_algorithms](svg/courses/embedded/effective-real-time-embedded-c-and-c++/11_timing/scheduling_algorithms.svg)

---

## Jitter and Latency

![jitter_and_latency](svg/courses/embedded/effective-real-time-embedded-c-and-c++/11_timing/jitter_and_latency.svg)
