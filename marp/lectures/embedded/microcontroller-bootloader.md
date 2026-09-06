---
tags:
- concepts:embedded
- concepts:firmware
- concepts:bootloader
level: advanced
category: embedded
audience:
- audiences:developers

---

# Writing Bootloaders for Microcontrollers
## From Reset Vector to Application Launch
## Mark Veltzer
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)

---

## What is a Bootloader?

![title](svg/lectures/embedded/microcontroller-bootloader/title.svg)

---

## What is a Bootloader?: Details

A **bootloader** is the first piece of code that runs when a microcontroller starts up.
**Primary Functions:**
- Initialize basic hardware
- Check for firmware updates
- Validate application integrity
- Launch the main application
- Handle recovery scenarios
Think of it as the BIOS/UEFI of microcontrollers

---

## Why Write a Custom Bootloader?

**Built-in bootloaders are limited:**
- Fixed communication interfaces (UART, USB, SPI)
- No custom protocols
- No application validation
- No dual-bank switching
- No secure boot features

**Custom bootloaders enable:**
- Network updates (WiFi, Ethernet, Cellular)
- Cryptographic verification
- Multiple application slots
- Custom update protocols

---

## Bootloader Architecture Overview

![bootloader_architecture_overview](svg/lectures/embedded/microcontroller-bootloader/bootloader_architecture_overview.svg)

---

## Memory Layout Fundamentals

**Typical STM32 Layout:**

```output
0x08000000: Bootloader (16KB)
0x08004000: Application (variable size)
0x08080000: Configuration/EEPROM simulation
```

**Key Considerations:**
- Bootloader size should be power of 2
- Application must be relocated
- Reserve space for configuration data
- Consider dual-bank scenarios

---

## Vector Table Relocation

**Problem**: Application doesn't start at 0x08000000 anymore

**Solution**: Relocate the vector table

```c
// In application startup code
#define APPLICATION_ADDRESS 0x08004000

void relocate_vector_table(void) {
    SCB->VTOR = APPLICATION_ADDRESS;
}
```

**Linker script modification needed:**
```ld
MEMORY {
    FLASH (rx) : ORIGIN = 0x08004000, LENGTH = 240K
    RAM (xrw)  : ORIGIN = 0x20000000, LENGTH = 64K
}
```

---

## Bootloader Startup Sequence

```c
int main(void) {
    // 1. Critical hardware initialization
    SystemInit();
    configure_clock();

    // 2. Check for update conditions
    if (update_requested() || !application_valid()) {
        enter_update_mode();
    }

    // 3. Launch application
    launch_application(APPLICATION_ADDRESS);

    // Should never reach here
    while(1);
}
```

---

## Hardware Initialization

**Minimal requirements:**
```c
void bootloader_init(void) {
    // System clock (often HSI for reliability)
    SystemInit();
    // GPIO for status LED/button
    gpio_init();
    // Communication interface (UART, USB, etc.)
    comm_init();
    // Watchdog (if used)
    // iwdg_init();
}
```

**Keep it minimal** - avoid initializing peripherals the application will use

---

## Update Detection Methods

![update_detection_methods](svg/lectures/embedded/microcontroller-bootloader/update_detection_methods.svg)

---

## Application Validation

```c
typedef struct {
    uint32_t magic;        // 0xDEADBEEF
    uint32_t version;      // Application version
    uint32_t size;         // Size in bytes
    uint32_t crc32;        // CRC32 of application
    uint32_t entry_point;  // Application entry point
} app_header_t;

bool application_valid(void) {
    app_header_t *header = (app_header_t*)APPLICATION_ADDRESS;

    // Check magic number
    if (header->magic != 0xDEADBEEF) return false;

    // Verify CRC
    uint32_t calc_crc = calculate_crc32(
        (uint8_t*)(APPLICATION_ADDRESS + sizeof(app_header_t)),
        header->size
    );

    return (calc_crc == header->crc32);
}
```

---

## Launching the Application

```c
typedef void (*app_function_t)(void);

void launch_application(uint32_t app_address) {
    // Check if valid application exists
    uint32_t *app_stack = (uint32_t*)app_address;
    if (*app_stack == 0xFFFFFFFF) {
        return; // No application
    }

    // Disable interrupts
    __disable_irq();

    // Deinitialize bootloader peripherals
    deinit_bootloader();

    // Set vector table
    SCB->VTOR = app_address;

    // Set stack pointer
    __set_MSP(*app_stack);

    // Jump to application
    app_function_t app_entry = (app_function_t)(*(app_stack + 1));
    app_entry();
}
```

---

## Communication Protocols

UART (Simple & Reliable)

```c
// Basic UART bootloader protocol
typedef enum {
    CMD_PING    = 0x01,
    CMD_ERASE   = 0x02,
    CMD_WRITE   = 0x03,
    CMD_VERIFY  = 0x04,
    CMD_JUMP    = 0x05
} bootloader_cmd_t;

typedef struct {
    uint8_t cmd;
    uint8_t len;
    uint8_t data[256];
    uint8_t checksum;
} packet_t;
```

---

## USB DFU Implementation

```c
// USB Device Firmware Upgrade
void usb_dfu_init(void) {
    // Initialize USB stack
    usb_device_init();

    // Register DFU class callbacks
    usb_register_class(&dfu_class);
}

// DFU state machine
typedef enum {
    DFU_IDLE,
    DFU_DOWNLOAD_SYNC,
    DFU_DOWNLOAD_BUSY,
    DFU_DOWNLOAD_IDLE,
    DFU_MANIFEST_SYNC,
    DFU_MANIFEST,
    DFU_ERROR
} dfu_state_t;
```

---

## Flash Programming

```c
bool flash_write_page(uint32_t address, uint8_t *data, uint32_t size) {
    // Unlock flash
    HAL_FLASH_Unlock();

    // Erase page if needed
    if (address % FLASH_PAGE_SIZE == 0) {
        FLASH_PageErase(address);
    }

    // Program data
    for (uint32_t i = 0; i < size; i += 4) {
        uint32_t word = *(uint32_t*)(data + i);
        if (HAL_FLASH_Program(FLASH_TYPEPROGRAM_WORD,
                             address + i, word) != HAL_OK) {
            HAL_FLASH_Lock();
            return false;
        }
    }

    HAL_FLASH_Lock();
    return true;
}
```

---

## Error Handling & Recovery

```c
typedef enum {
    BOOT_OK = 0,
    BOOT_ERROR_NO_APP,
    BOOT_ERROR_INVALID_APP,
    BOOT_ERROR_FLASH_ERROR,
    BOOT_ERROR_COMM_TIMEOUT
} boot_error_t;

void handle_boot_error(boot_error_t error) {
    switch(error) {
        case BOOT_ERROR_NO_APP:
            // Force bootloader mode
            enter_update_mode();
            break;

        case BOOT_ERROR_INVALID_APP:
            // Try backup application
            if (backup_app_valid()) {
                restore_from_backup();
            } else {
                enter_update_mode();
            }
            break;
    }
}
```

---

## Dual Bank Bootloader

![dual_bank_bootloader](svg/lectures/embedded/microcontroller-bootloader/dual_bank_bootloader.svg)

---

## Secure Boot Fundamentals

```c
// Digital signature verification
bool verify_application_signature(void) {
    uint8_t *app_data = (uint8_t*)APPLICATION_ADDRESS;
    uint32_t app_size = get_application_size();

    // Extract signature from end of application
    uint8_t *signature = app_data + app_size - SIGNATURE_SIZE;

    // Calculate hash of application
    uint8_t hash[32];
    sha256_calculate(app_data, app_size - SIGNATURE_SIZE, hash);

    // Verify signature using public key
    return ecdsa_verify(public_key, hash, signature);
}
```

**Chain of Trust:**
Bootloader → Application → Runtime components

---

## Cryptographic Considerations

**Algorithms to consider:**
- **AES-256**: Firmware encryption
- **SHA-256**: Integrity checking
- **ECDSA P-256**: Digital signatures
- **Ed25519**: Alternative signature scheme

**Implementation:**
```c
// Use hardware crypto if available
#ifdef STM32_HAS_CRYPTO
    #include "stm32_crypto.h"
#else
    #include "mbedtls/sha256.h"
    #include "mbedtls/ecdsa.h"
#endif
```

---

## Bootloader Configuration

```c
typedef struct {
    uint32_t magic;                 // Configuration valid marker
    uint32_t boot_delay_ms;         // Bootloader timeout
    uint32_t comm_timeout_ms;       // Communication timeout
    uint8_t  comm_interface;        // UART, USB, etc.
    uint32_t baud_rate;            // For UART
    bool     secure_boot_enabled;   // Signature verification
    uint8_t  max_boot_attempts;    // Before fallback
    uint32_t backup_app_address;   // Backup application location
} bootloader_config_t;

// Store in dedicated flash sector
const bootloader_config_t __attribute__((section(".config")))
    bootloader_config = {
        .magic = 0xBEEFFACE,
        .boot_delay_ms = 3000,
        .comm_timeout_ms = 10000,
        // ... other defaults
    };
```

---

## Update Protocol State Machine

![update_protocol_state_machine](svg/lectures/embedded/microcontroller-bootloader/update_protocol_state_machine.svg)

---

## Packet Protocol Design

```c
// Bootloader packet format
typedef struct __attribute__((packed)) {
    uint8_t  sof;           // Start of frame (0x7E)
    uint8_t  cmd;           // Command byte
    uint16_t seq;           // Sequence number
    uint16_t len;           // Payload length
    uint8_t  payload[512];  // Data payload
    uint32_t crc32;         // CRC32 checksum
    uint8_t  eof;           // End of frame (0x7F)
} bootloader_packet_t;

// Commands
#define CMD_HANDSHAKE    0x01
#define CMD_ERASE_SECTOR 0x02
#define CMD_WRITE_BLOCK  0x03
#define CMD_READ_BLOCK   0x04
#define CMD_VERIFY_CRC   0x05
#define CMD_JUMP_APP     0x06
#define CMD_GET_VERSION  0x07
```

---

## UART Bootloader Implementation

```c
void uart_bootloader_task(void) {
    static uint8_t rx_buffer[sizeof(bootloader_packet_t)];
    static uint16_t rx_index = 0;

    while (uart_data_available()) {
        uint8_t byte = uart_read_byte();

        if (byte == 0x7E && rx_index == 0) {
            // Start of frame
            rx_buffer[rx_index++] = byte;
        } else if (rx_index > 0) {
            rx_buffer[rx_index++] = byte;

            if (byte == 0x7F) {
                // End of frame - process packet
                process_bootloader_packet(rx_buffer, rx_index);
                rx_index = 0;
            }
        }

        // Prevent buffer overflow
        if (rx_index >= sizeof(rx_buffer)) {
            rx_index = 0;
        }
    }
}
```

---

## USB Bootloader Class

```c
// USB HID bootloader (no drivers needed)
#define HID_REPORT_SIZE 64

typedef struct {
    uint8_t cmd;
    uint8_t seq;
    uint8_t len;
    uint8_t data[61];  // 64 - 3 header bytes
} hid_bootloader_report_t;

void usb_hid_bootloader_init(void) {
    usb_device_init();
    usb_hid_init();

    // Register HID report callback
    usb_hid_register_callback(hid_bootloader_callback);
}

void hid_bootloader_callback(uint8_t *report, uint16_t len) {
    hid_bootloader_report_t *cmd = (hid_bootloader_report_t*)report;
    process_hid_command(cmd);
}
```

---

## Network Bootloader (WiFi/Ethernet)

```c
// HTTP-based firmware update
void http_bootloader_task(void) {
    static enum {
        HTTP_IDLE,
        HTTP_CONNECTING,
        HTTP_DOWNLOADING,
        HTTP_COMPLETE
    } state = HTTP_IDLE;

    switch(state) {
        case HTTP_IDLE:
            if (check_update_available()) {
                start_download();
                state = HTTP_CONNECTING;
            }
            break;

        case HTTP_DOWNLOADING:
            if (download_chunk()) {
                if (download_complete()) {
                    state = HTTP_COMPLETE;
                }
            }
            break;
    }
}
```

---

## Differential Updates

**Problem**: Full firmware updates are large (100KB+)
**Solution**: Send only the differences

```c
// Binary diff/patch system
typedef struct {
    uint32_t old_offset;    // Offset in old firmware
    uint32_t new_offset;    // Offset in new firmware
    uint32_t length;        // Bytes to copy
    uint8_t  operation;     // COPY, INSERT, DELETE
} patch_operation_t;

bool apply_differential_update(uint8_t *patch_data, uint32_t patch_size) {
    uint8_t *old_fw = (uint8_t*)APPLICATION_ADDRESS;
    uint8_t *temp_fw = malloc(MAX_FIRMWARE_SIZE);

    patch_operation_t *ops = (patch_operation_t*)patch_data;
    uint32_t num_ops = patch_size / sizeof(patch_operation_t);

    for (uint32_t i = 0; i < num_ops; i++) {
        apply_patch_operation(&ops[i], old_fw, temp_fw);
    }

    // Write new firmware to flash
    return program_firmware(temp_fw);
}
```

---

## Bootloader Testing Strategy

**Unit Tests:**
```c
void test_crc_calculation(void) {
    uint8_t test_data[] = {0x01, 0x02, 0x03, 0x04};
    uint32_t expected_crc = 0x9140DAD6;
    uint32_t calculated_crc = calculate_crc32(test_data, 4);
    assert(calculated_crc == expected_crc);
}

void test_application_validation(void) {
    // Setup mock application with valid header
    mock_application_setup();
    assert(application_valid() == true);
    // Corrupt CRC and test
    corrupt_application_crc();
    assert(application_valid() == false);
}
```

---

## Hardware-in-the-Loop Testing

![hardware_in_the_loop_testing](svg/lectures/embedded/microcontroller-bootloader/hardware_in_the_loop_testing.svg)

---

## Debugging Bootloader Issues

**Common Problems:**
```c
// Stack overflow detection
void check_stack_usage(void) {
    extern uint32_t _stack_start;
    extern uint32_t _stack_end;
    uint32_t *stack_ptr = (uint32_t*)__get_MSP();
    uint32_t stack_used = &_stack_end - stack_ptr;
    if (stack_used > STACK_WARNING_THRESHOLD) {
        debug_printf("Stack usage: %lu bytes\n", stack_used * 4);
    }
}

// Flash programming verification
bool verify_flash_write(uint32_t address, uint8_t *data, uint32_t size) {
    for (uint32_t i = 0; i < size; i++) {
        if (*(uint8_t*)(address + i) != data[i]) {
            debug_printf("Flash verify failed at 0x%08lX\n", address + i);
            return false;
        }
    }
    return true;
}
```

---

## Performance Optimization

**Minimize Boot Time:**
```c
// Fast clock setup (HSI instead of HSE+PLL during boot)
void quick_clock_init(void) {
    // Use HSI (16MHz) for bootloader operations
    RCC->CR |= RCC_CR_HSION;
    while(!(RCC->CR & RCC_CR_HSIRDY));
    // Switch to HSI
    RCC->CFGR = (RCC->CFGR & ~RCC_CFGR_SW) | RCC_CFGR_SW_HSI;
}

// Optimize flash programming
void fast_flash_program(uint32_t address, uint8_t *data, uint32_t size) {
    // Use 64-bit programming mode if available
    HAL_FLASH_Unlock();
    for (uint32_t i = 0; i < size; i += 8) {
        uint64_t dword = *(uint64_t*)(data + i);
        HAL_FLASH_Program(FLASH_TYPEPROGRAM_DOUBLEWORD, address + i, dword);
    }
    HAL_FLASH_Lock();
}
```

---

## Memory Protection & Security

```c
// Memory Protection Unit (MPU) setup
void configure_mpu(void) {
    // Protect bootloader from application writes
    MPU_Region_InitTypeDef MPU_InitStruct = {0};

    HAL_MPU_Disable();

    // Bootloader region - Read-only for application
    MPU_InitStruct.Enable = MPU_REGION_ENABLE;
    MPU_InitStruct.Number = MPU_REGION_NUMBER0;
    MPU_InitStruct.BaseAddress = 0x08000000;
    MPU_InitStruct.Size = MPU_REGION_SIZE_16KB;
    MPU_InitStruct.AccessPermission = MPU_REGION_PRIV_RO;

    HAL_MPU_ConfigRegion(&MPU_InitStruct);
    HAL_MPU_Enable(MPU_PRIVILEGED_DEFAULT);
}

// Secure key storage
const uint8_t __attribute__((section(".keys")))
    public_key[64] = {
        // ECDSA P-256 public key
        0x04, 0x1B, 0x8C, 0x2A, /* ... */
    };
```

---

## Rollback Protection

```c
// Anti-rollback mechanism
typedef struct {
    uint32_t version_number;    // Monotonic version counter
    uint32_t security_version;  // Security patch level
    uint8_t  signature[64];     // Signature of version info
} version_info_t;

bool check_rollback_protection(version_info_t *new_version) {
    version_info_t *current = get_current_version();

    // Verify signature first
    if (!verify_version_signature(new_version)) {
        return false;
    }

    // Check for rollback attempt
    if (new_version->security_version < current->security_version) {
        log_security_event("Rollback attempt detected");
        return false;
    }

    return true;
}
```

---

## Bootloader Size Optimization

**Techniques to minimize size:**
```c
// Use -Os optimization flag
// Disable unused features
#ifndef BOOTLOADER_FEATURES_USB
#define USB_SUPPORT 0
#endif

// Minimal C library
#define printf(...)  // Remove in release builds
#define malloc(x) NULL  // No dynamic allocation

// Code size measurement
void __attribute__((constructor)) measure_bootloader_size(void) {
    extern uint32_t _flash_start;
    extern uint32_t _flash_end;
    uint32_t size = &_flash_end - &_flash_start;
    // Size should be < 16KB for most applications
}

// Use function attributes
__attribute__((always_inline)) static inline void critical_function(void);
__attribute__((noinline)) void rarely_used_function(void);
```

---

## Production Deployment

**Manufacturing Flow:**
1. **Program bootloader** via SWD/JTAG
1. **Set option bytes** (boot configuration)
1. **Program initial application**
1. **Set security features** (RDP, write protection)
1. **Quality testing**

```c
// Option bytes configuration
void configure_option_bytes(void) {
    FLASH_OBProgramInitTypeDef OBInit = {0};

    // Enable boot from Bank 1
    OBInit.OptionType = OPTIONBYTE_BOOTADDR_0;
    OBInit.BootAddr0 = 0x0800;  // Bootloader address

    // Set read protection level (careful!)
    // OBInit.OptionType |= OPTIONBYTE_RDP;
    // OBInit.RDPLevel = OB_RDP_LEVEL_1;

    HAL_FLASH_OB_Unlock();
    HAL_FLASHEx_OBProgram(&OBInit);
    HAL_FLASH_OB_Launch();  // Triggers reset
}
```

---

## Field Diagnostics

```c
// Bootloader diagnostic information
typedef struct {
    uint32_t boot_count;           // Number of boots
    uint32_t update_count;         // Successful updates
    uint32_t failed_boots;         // Failed boot attempts
    uint32_t last_error_code;      // Last error encountered
    uint32_t uptime_seconds;       // Total uptime
    char     last_app_version[16]; // Last known good app version
} diagnostic_info_t;

void log_boot_event(boot_event_t event) {
    diagnostic_info_t *diag = get_diagnostic_storage();

    switch(event) {
        case BOOT_EVENT_POWER_ON:
            diag->boot_count++;
            break;
        case BOOT_EVENT_APP_LAUNCH_FAILED:
            diag->failed_boots++;
            break;
        case BOOT_EVENT_UPDATE_SUCCESS:
            diag->update_count++;
            break;
    }

    save_diagnostic_info(diag);
}
```

---

## Multi-Core Bootloader (Dual Core MCUs)

```c
// For STM32H7 dual-core, ESP32, etc.
void dual_core_bootloader_init(void) {
    if (get_core_id() == CORE_M7) {
        // Master core (Cortex-M7)
        init_shared_memory();

        // Boot secondary core
        HAL_RCCEx_EnableBootCore(RCC_BOOT_C2);

        // Handle bootloader logic
        bootloader_main_task();

    } else if (get_core_id() == CORE_M4) {
        // Secondary core (Cortex-M4)
        wait_for_master_init();

        // Handle specific tasks (crypto, communication)
        bootloader_secondary_task();
    }
}

// Shared memory communication
typedef struct {
    volatile uint32_t core_m7_status;
    volatile uint32_t core_m4_status;
    volatile uint32_t shared_command;
    uint8_t update_buffer[SHARED_BUFFER_SIZE];
} shared_memory_t;
```

---

## Bootloader Metrics & Analytics

```c
// Telemetry for bootloader health monitoring
typedef struct {
    uint32_t avg_boot_time_ms;     // Average boot time
    uint32_t flash_wear_cycles;    // Flash erase cycles
    uint32_t communication_errors; // Protocol errors
    uint32_t temperature_max;      // Max operating temp
    uint32_t voltage_min;          // Min operating voltage
} bootloader_metrics_t;

void collect_boot_metrics(void) {
    static uint32_t boot_start_time;

    if (boot_start_time == 0) {
        boot_start_time = get_systick();
    } else {
        uint32_t boot_time = get_systick() - boot_start_time;
        update_metric(METRIC_BOOT_TIME, boot_time);
    }
}

// Transmit metrics during update sessions
void send_telemetry(void) {
    bootloader_metrics_t metrics;
    collect_all_metrics(&metrics);

    // Send to cloud service
    http_post_json("https://telemetry.company.com/bootloader", &metrics);
}
```

---

## Bootloader Standards & Compliance

**Common Standards:**
- **UDS (ISO 14229)**: Automotive diagnostics
- **XCP**: Measurement and calibration
- **DFU**: USB Device Firmware Upgrade
- **FOTA**: Firmware Over-The-Air (cellular)

```c
// UDS (Unified Diagnostic Services) example
void handle_uds_request(uint8_t *data, uint8_t len) {
    uint8_t service_id = data[0];

    switch(service_id) {
        case 0x10: // Diagnostic Session Control
            if (data[1] == 0x02) {  // Programming session
                enter_programming_mode();
                send_positive_response(0x50, data[1]);
            }
            break;

        case 0x27: // Security Access
            handle_security_challenge(data, len);
            break;

        case 0x34: // Request Download
            prepare_memory_download(data, len);
            break;
    }
}
```

---

## Bootloader Documentation

**Essential Documentation:**
- Memory map and linker scripts
- Communication protocol specification
- Update procedure manual
- Recovery instructions
- Security implementation details

```c
// Self-documenting bootloader info
typedef struct {
    char     version[16];          // "BL v2.1.0"
    char     build_date[16];       // "2024-01-15"
    char     supported_protocols[64]; // "UART,USB,CAN"
    uint32_t max_app_size;         // Maximum application size
    uint32_t flash_page_size;      // Flash programming granularity
    char     mcu_part_number[32];  // "STM32F407VG"
} bootloader_info_t;

const bootloader_info_t __attribute__((section(".bootloader_info")))
    bl_info = {
        .version = VERSION_STRING,
        .build_date = __DATE__,
        .supported_protocols = "UART,USB,CAN",
        .max_app_size = MAX_APPLICATION_SIZE,
        .flash_page_size = FLASH_PAGE_SIZE,
        .mcu_part_number = MCU_PART_NUMBER
    };
```

---

## Best Practices Summary

**✅ DO:**
- Keep bootloader simple and robust
- Validate all inputs and firmware
- Implement proper error handling
- Use cryptographic verification
- Test thoroughly before deployment
- Document memory layout clearly
- Plan for field updates from day one

**❌ DON'T:**
- Make bootloader too complex
- Skip input validation
- Use dynamic memory allocation
- Forget about stack overflow protection
- Deploy without extensive testing
- Hardcode configuration values

---

## Troubleshooting Common Issues

**Boot Loop Issues:**
```c
// Detect and handle boot loops
void check_boot_loop(void) {
    uint32_t *boot_count = (uint32_t*)BACKUP_SRAM_BASE;
    (*boot_count)++;
    if (*boot_count > MAX_BOOT_ATTEMPTS) {
        // Force bootloader mode
        *boot_count = 0;
        enter_safe_mode();
    }
    // Reset counter on successful app launch
    if (application_running()) {
        *boot_count = 0;
    }
}
```

**Communication Issues:**
- Check baud rate and parity settings
- Verify packet framing and checksums
- Test with known-good hardware
- Monitor with oscilloscope/logic analyzer

---

## Advanced Topics

**Real-Time Operating System Integration:**
```c
// FreeRTOS bootloader task
void bootloader_task(void *parameters) {
    while(1) {
        // Check for update requests
        if (xQueueReceive(update_queue, &update_cmd, pdMS_TO_TICKS(100))) {
            process_update_command(&update_cmd);
        }
        // Heartbeat
        toggle_status_led();
        vTaskDelay(pdMS_TO_TICKS(50));
    }
}
```

**Machine Learning Integration:**
```c
// Anomaly detection for boot behavior
bool detect_boot_anomaly(void) {
    boot_metrics_t current_metrics;
    collect_metrics(&current_metrics);
    // Simple threshold-based detection
    if (current_metrics.boot_time > NORMAL_BOOT_TIME * 2) {
        return true;  // Anomaly detected
    }
    return false;
}
```

---

## Future Trends

**Emerging Technologies:**
- **AI-assisted updates**: Predictive maintenance
- **Blockchain verification**: Immutable update logs
- **Edge computing**: Local update distribution
- **5G connectivity**: Ultra-fast updates
- **Hardware security modules**: Enhanced crypto

**Industry Evolution:**
- Standardization of update protocols
- Increased focus on security
- Cloud-native update infrastructure
- Zero-downtime update mechanisms

---

## Tools & Resources

**Development Tools:**
- **STM32CubeProgrammer**: ST bootloader tool
- **OpenOCD**: Open source debugging
- **MCUXpresso**: NXP development suite
- **ESP-IDF**: Espressif bootloader framework

**Testing Tools:**
- **Unity**: C unit testing framework
- **Renode**: Hardware simulation
- **QEMU**: System emulation
- **Wireshark**: Protocol analysis

**Libraries:**
- **mbedTLS**: Cryptography
- **FatFs**: File system
- **lwIP**: TCP/IP stack
- **TinyUSB**: USB device stack

---

## Conclusion

**Key Takeaways:**
- Bootloaders are critical for field-updatable devices
- Security and reliability are paramount
- Start simple, add features incrementally
- Test extensively before deployment
- Plan for the unexpected

**Success Factors:**
- Clear requirements definition
- Proper architecture design
- Thorough testing strategy
- Comprehensive documentation
- Post-deployment monitoring

**The bootloader is your insurance policy for the field!**

---

## Over-The-Air (OTA) Updates

![over_the_air_ota_updates](svg/lectures/embedded/microcontroller-bootloader/over_the_air_ota_updates.svg)

---

## OTA Update Implementation

```c
typedef struct {
    char version[16];       // "v1.2.3"
    char url[256];         // Download URL
    uint32_t size;         // Firmware size
    uint8_t sha256[32];    // File hash
    uint8_t signature[64]; // Digital signature
} ota_manifest_t;

bool check_for_updates(void) {
    // Query update server
    http_client_t client;
    if (http_get(&client, "https://updates.company.com/manifest.json") == HTTP_OK) {
        ota_manifest_t manifest;
        parse_manifest(client.response, &manifest);

        if (is_newer_version(manifest.version)) {
            return download_and_install(&manifest);
        }
    }
    return false;
}
```
