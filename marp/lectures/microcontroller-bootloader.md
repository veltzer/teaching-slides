# Writing Bootloaders for Microcontrollers
## From Reset Vector to Application Launch

Building robust firmware update systems for embedded devices

---

## What is a Bootloader?

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

<svg width="600" height="400" viewBox="0 0 600 400">
  <!-- Flash Memory Layout -->
  <rect x="50" y="50" width="150" height="300" fill="#f5f5f5" stroke="#333" stroke-width="2"/>
  <text x="125" y="40" text-anchor="middle" font-size="14" font-weight="bold">Flash Memory</text>

  <!-- Bootloader Section -->
  <rect x="60" y="60" width="130" height="60" fill="#ffcdd2" stroke="#d32f2f" stroke-width="2"/>
  <text x="125" y="85" text-anchor="middle" font-size="12">Bootloader</text>
  <text x="125" y="105" text-anchor="middle" font-size="10">0x08000000</text>

  <!-- Application Section -->
  <rect x="60" y="130" width="130" height="120" fill="#c8e6c9" stroke="#388e3c" stroke-width="2"/>
  <text x="125" y="155" text-anchor="middle" font-size="12">Application</text>
  <text x="125" y="175" text-anchor="middle" font-size="10">0x08004000</text>

  <!-- Config/Data Section -->
  <rect x="60" y="260" width="130" height="80" fill="#fff3e0" stroke="#f57c00" stroke-width="2"/>
  <text x="125" y="285" text-anchor="middle" font-size="12">Config/Data</text>
  <text x="125" y="305" text-anchor="middle" font-size="10">0x08080000</text>

  <!-- Boot Process Flow -->
  <rect x="300" y="80" width="120" height="40" fill="#e3f2fd" stroke="#1976d2" stroke-width="2" rx="5"/>
  <text x="360" y="105" text-anchor="middle" font-size="11">Power On Reset</text>

  <rect x="300" y="140" width="120" height="40" fill="#fff3e0" stroke="#f57c00" stroke-width="2" rx="5"/>
  <text x="360" y="165" text-anchor="middle" font-size="11">Hardware Init</text>

  <rect x="300" y="200" width="120" height="40" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2" rx="5"/>
  <text x="360" y="225" text-anchor="middle" font-size="11">Check for Update</text>

  <rect x="300" y="260" width="120" height="40" fill="#e8f5e8" stroke="#388e3c" stroke-width="2" rx="5"/>
  <text x="360" y="285" text-anchor="middle" font-size="11">Launch App</text>

  <!-- Arrows -->
  <path d="M 360 120 L 360 140" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M 360 180 L 360 200" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M 360 240 L 360 260" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>

  <!-- Connection from bootloader to process -->
  <path d="M 200 90 L 300 100" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>

  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Memory Layout Fundamentals

**Typical STM32 Layout:**

```text
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

<svg width="700" height="300" viewBox="0 0 700 300">
  <!-- Method boxes -->
  <rect x="50" y="50" width="120" height="80" fill="#e3f2fd" stroke="#1976d2" stroke-width="2" rx="5"/>
  <text x="110" y="75" text-anchor="middle" font-size="11" font-weight="bold">GPIO Button</text>
  <text x="110" y="95" text-anchor="middle" font-size="9">Hold during reset</text>
  <text x="110" y="110" text-anchor="middle" font-size="9">Simple & reliable</text>

  <rect x="190" y="50" width="120" height="80" fill="#fff3e0" stroke="#f57c00" stroke-width="2" rx="5"/>
  <text x="250" y="75" text-anchor="middle" font-size="11" font-weight="bold">Magic Value</text>
  <text x="250" y="95" text-anchor="middle" font-size="9">RAM/EEPROM flag</text>
  <text x="250" y="110" text-anchor="middle" font-size="9">Software triggered</text>

  <rect x="330" y="50" width="120" height="80" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2" rx="5"/>
  <text x="390" y="75" text-anchor="middle" font-size="11" font-weight="bold">Timeout</text>
  <text x="390" y="95" text-anchor="middle" font-size="9">Wait for command</text>
  <text x="390" y="110" text-anchor="middle" font-size="9">Network updates</text>

  <rect x="470" y="50" width="120" height="80" fill="#e8f5e8" stroke="#388e3c" stroke-width="2" rx="5"/>
  <text x="530" y="75" text-anchor="middle" font-size="11" font-weight="bold">App Invalid</text>
  <text x="530" y="95" text-anchor="middle" font-size="9">CRC/checksum</text>
  <text x="530" y="110" text-anchor="middle" font-size="9">Automatic recovery</text>

  <!-- Decision flow -->
  <rect x="250" y="180" width="200" height="40" fill="#ffebee" stroke="#d32f2f" stroke-width="2" rx="5"/>
  <text x="350" y="205" text-anchor="middle" font-size="12">Enter Bootloader Mode</text>

  <!-- Arrows -->
  <path d="M 110 130 L 320 180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M 250 130 L 330 180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M 390 130 L 370 180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M 530 130 L 380 180" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>

  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333"/>
    </marker>
  </defs>
</svg>

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

<svg width="700" height="350" viewBox="0 0 700 350">
  <!-- Flash Banks -->
  <rect x="50" y="50" width="120" height="250" fill="#f5f5f5" stroke="#333" stroke-width="2"/>
  <text x="110" y="40" text-anchor="middle" font-size="14" font-weight="bold">Bank 1</text>

  <rect x="200" y="50" width="120" height="250" fill="#f5f5f5" stroke="#333" stroke-width="2"/>
  <text x="260" y="40" text-anchor="middle" font-size="14" font-weight="bold">Bank 2</text>

  <!-- Bootloader in both banks -->
  <rect x="60" y="60" width="100" height="40" fill="#ffcdd2" stroke="#d32f2f" stroke-width="2"/>
  <text x="110" y="85" text-anchor="middle" font-size="11">Bootloader</text>

  <rect x="210" y="60" width="100" height="40" fill="#ffcdd2" stroke="#d32f2f" stroke-width="2"/>
  <text x="260" y="85" text-anchor="middle" font-size="11">Bootloader</text>

  <!-- Applications -->
  <rect x="60" y="110" width="100" height="80" fill="#c8e6c9" stroke="#388e3c" stroke-width="2"/>
  <text x="110" y="135" text-anchor="middle" font-size="11">App v1.0</text>
  <text x="110" y="155" text-anchor="middle" font-size="10">(Running)</text>

  <rect x="210" y="110" width="100" height="80" fill="#fff3e0" stroke="#f57c00" stroke-width="2"/>
  <text x="260" y="135" text-anchor="middle" font-size="11">App v1.1</text>
  <text x="260" y="155" text-anchor="middle" font-size="10">(Staging)</text>

  <!-- Process -->
  <rect x="400" y="80" width="140" height="30" fill="#e3f2fd" stroke="#1976d2" stroke-width="2" rx="5"/>
  <text x="470" y="100" text-anchor="middle" font-size="11">1. Download to Bank 2</text>

  <rect x="400" y="120" width="140" height="30" fill="#fff3e0" stroke="#f57c00" stroke-width="2" rx="5"/>
  <text x="470" y="140" text-anchor="middle" font-size="11">2. Verify Integrity</text>

  <rect x="400" y="160" width="140" height="30" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2" rx="5"/>
  <text x="470" y="180" text-anchor="middle" font-size="11">3. Update Boot Flag</text>

  <rect x="400" y="200" width="140" height="30" fill="#e8f5e8" stroke="#388e3c" stroke-width="2" rx="5"/>
  <text x="470" y="220" text-anchor="middle" font-size="11">4. Reboot to Bank 2</text>

  <!-- Arrows -->
  <path d="M 320 150 L 400 95" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M 470 110 L 470 120" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M 470 150 L 470 160" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M 470 190 L 470 200" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>

  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333"/>
    </marker>
  </defs>
</svg>

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

<svg width="650" height="400" viewBox="0 0 650 400">
  <!-- States -->
  <circle cx="100" cy="80" r="30" fill="#e3f2fd" stroke="#1976d2" stroke-width="2"/>
  <text x="100" y="85" text-anchor="middle" font-size="10">IDLE</text>

  <circle cx="250" cy="80" r="30" fill="#fff3e0" stroke="#f57c00" stroke-width="2"/>
  <text x="250" y="85" text-anchor="middle" font-size="10">SYNC</text>

  <circle cx="400" cy="80" r="30" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2"/>
  <text x="400" y="85" text-anchor="middle" font-size="10">RECEIVE</text>

  <circle cx="550" cy="80" r="30" fill="#e8f5e8" stroke="#388e3c" stroke-width="2"/>
  <text x="550" y="85" text-anchor="middle" font-size="10">VERIFY</text>

  <circle cx="400" cy="200" r="30" fill="#ffebee" stroke="#d32f2f" stroke-width="2"/>
  <text x="400" y="205" text-anchor="middle" font-size="10">ERROR</text>

  <circle cx="250" cy="280" r="30" fill="#e8f5e8" stroke="#388e3c" stroke-width="2"/>
  <text x="250" y="285" text-anchor="middle" font-size="10">COMPLETE</text>

  <!-- Transitions -->
  <path d="M 130 80 L 220 80" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
  <text x="175" y="75" text-anchor="middle" font-size="9">START</text>

  <path d="M 280 80 L 370 80" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
  <text x="325" y="75" text-anchor="middle" font-size="9">BEGIN</text>

  <path d="M 430 80 L 520 80" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
  <text x="475" y="75" text-anchor="middle" font-size="9">END</text>

  <path d="M 400 110 L 400 170" stroke="#d32f2f" stroke-width="2" marker-end="url(#arrowhead)"/>
  <text x="425" y="140" text-anchor="middle" font-size="9">ERROR</text>

  <path d="M 520 80 L 280 280" stroke="#388e3c" stroke-width="2" marker-end="url(#arrowhead)"/>
  <text x="450" y="160" text-anchor="middle" font-size="9">SUCCESS</text>

  <path d="M 370 200 L 130 80" stroke="#d32f2f" stroke-width="2" marker-end="url(#arrowhead)"/>
  <text x="200" y="150" text-anchor="middle" font-size="9">RETRY</text>

  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333"/>
    </marker>
  </defs>
</svg>

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

<svg width="650" height="300" viewBox="0 0 650 300">
  <!-- Test Setup -->
  <rect x="50" y="50" width="100" height="60" fill="#e3f2fd" stroke="#1976d2" stroke-width="2" rx="5"/>
  <text x="100" y="75" text-anchor="middle" font-size="11">Test PC</text>
  <text x="100" y="90" text-anchor="middle" font-size="9">Python Script</text>

  <rect x="200" y="50" width="100" height="60" fill="#fff3e0" stroke="#f57c00" stroke-width="2" rx="5"/>
  <text x="250" y="75" text-anchor="middle" font-size="11">Debug Probe</text>
  <text x="250" y="90" text-anchor="middle" font-size="9">ST-Link/J-Link</text>

  <rect x="350" y="50" width="100" height="60" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2" rx="5"/>
  <text x="400" y="75" text-anchor="middle" font-size="11">Target MCU</text>
  <text x="400" y="90" text-anchor="middle" font-size="9">STM32</text>

  <rect x="500" y="50" width="100" height="60" fill="#e8f5e8" stroke="#388e3c" stroke-width="2" rx="5"/>
  <text x="550" y="75" text-anchor="middle" font-size="11">Power Supply</text>
  <text x="550" y="90" text-anchor="middle" font-size="9">Controllable</text>

  <!-- Connections -->
  <path d="M 150 80 L 200 80" stroke="#333" stroke-width="2"/>
  <text x="175" y="75" text-anchor="middle" font-size="9">USB</text>

  <path d="M 300 80 L 350 80" stroke="#333" stroke-width="2"/>
  <text x="325" y="75" text-anchor="middle" font-size="9">SWD</text>

  <path d="M 450 80 L 500 80" stroke="#333" stroke-width="2"/>
  <text x="475" y="75" text-anchor="middle" font-size="9">Power</text>

  <!-- Test Cases -->
  <rect x="50" y="150" width="550" height="120" fill="#f5f5f5" stroke="#333" stroke-width="1" rx="5"/>
  <text x="325" y="170" text-anchor="middle" font-size="12" font-weight="bold">Automated Test Cases</text>

  <text x="70" y="190" font-size="10">• Power-on reset behavior</text>
  <text x="70" y="205" font-size="10">• Bootloader timeout handling</text>
  <text x="70" y="220" font-size="10">• Firmware update via UART/USB</text>
  <text x="70" y="235" font-size="10">• Application validation & launch</text>
  <text x="70" y="250" font-size="10">• Recovery from corrupted firmware</text>

  <text x="350" y="190" font-size="10">• Brown-out detection</text>
  <text x="350" y="205" font-size="10">• Watchdog reset scenarios</text>
  <text x="350" y="220" font-size="10">• Flash programming errors</text>
  <text x="350" y="235" font-size="10">• Communication protocol edge cases</text>
  <text x="350" y="250" font-size="10">• Multi-bank switching</text>
</svg>

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
2. **Set option bytes** (boot configuration)
3. **Program initial application**
4. **Set security features** (RDP, write protection)
5. **Quality testing**

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

<svg width="700" height="350" viewBox="0 0 700 350">
  <!-- Cloud Server -->
  <ellipse cx="100" cy="100" rx="60" ry="40" fill="#e3f2fd" stroke="#1976d2" stroke-width="2"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Update Server</text>

  <!-- WiFi/Internet -->
  <path d="M 180 100 Q 250 60 320 100" stroke="#333" stroke-width="3" fill="none"/>
  <path d="M 180 100 Q 250 80 320 100" stroke="#333" stroke-width="3" fill="none"/>
  <path d="M 180 100 Q 250 120 320 100" stroke="#333" stroke-width="3" fill="none"/>
  <text x="250" y="140" text-anchor="middle" font-size="10">WiFi/Cellular</text>

  <!-- Device -->
  <rect x="350" y="70" width="80" height="60" fill="#fff3e0" stroke="#f57c00" stroke-width="2" rx="5"/>
  <text x="390" y="105" text-anchor="middle" font-size="12">IoT Device</text>

  <!-- Process Steps -->
  <rect x="500" y="50" width="150" height="25" fill="#e8f5e8" stroke="#388e3c" stroke-width="1" rx="3"/>
  <text x="575" y="67" text-anchor="middle" font-size="10">1. Check for updates</text>

  <rect x="500" y="80" width="150" height="25" fill="#fff3e0" stroke="#f57c00" stroke-width="1" rx="3"/>
  <text x="575" y="97" text-anchor="middle" font-size="10">2. Download firmware</text>

  <rect x="500" y="110" width="150" height="25" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="1" rx="3"/>
  <text x="575" y="127" text-anchor="middle" font-size="10">3. Verify signature</text>

  <rect x="500" y="140" width="150" height="25" fill="#ffebee" stroke="#d32f2f" stroke-width="1" rx="3"/>
  <text x="575" y="157" text-anchor="middle" font-size="10">4. Install & reboot</text>

  <rect x="500" y="170" width="150" height="25" fill="#e3f2fd" stroke="#1976d2" stroke-width="1" rx="3"/>
  <text x="575" y="187" text-anchor="middle" font-size="10">5. Confirm success</text>

  <!-- Arrow from device to steps -->
  <path d="M 430 100 L 500 100" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>

  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333"/>
    </marker>
  </defs>
</svg>

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
