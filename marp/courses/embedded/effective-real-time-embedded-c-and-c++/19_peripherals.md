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
# Peripherals

---
## Overview of Embedded Peripherals

Embedded systems interact with the physical world through peripherals:
- **GPIO**: General Purpose Input/Output pins
- **UART**: Serial communication interface
- **ADC**: Analog-to-Digital Converter
- **SPI**: Serial Peripheral Interface
- **I2C**: Inter-Integrated Circuit bus
- **DMA**: Direct Memory Access controller
- **Timers**: Hardware timing and PWM generation

---
## Overview of Embedded Peripherals

![overview_of_embedded_peripherals](svg/courses/embedded/effective-real-time-embedded-c-and-c++/19_peripherals/overview_of_embedded_peripherals.svg)

---

## General Purpose Input/Output (GPIO)

GPIO pins provide basic digital I/O functionality:
- **Input mode**: Read digital signals (0V or VCC)
- **Output mode**: Drive pins high or low
- **Alternative functions**: UART, SPI, PWM, etc.
- **Configuration options**: Pull-up/down, drive strength, slew rate

```cpp
// Typical GPIO register structure
struct GPIO_TypeDef {
    volatile uint32_t MODER;    // Mode register
    volatile uint32_t OTYPER;   // Output type register
    volatile uint32_t OSPEEDR;  // Output speed register
    volatile uint32_t PUPDR;    // Pull-up/pull-down register
    volatile uint32_t IDR;      // Input data register
    volatile uint32_t ODR;      // Output data register
    volatile uint32_t BSRR;     // Bit set/reset register
};
```

---

## GPIO Configuration Example

Configuring GPIO pins for different functions:

```cpp
#include <stdint.h>

// GPIO base addresses (example for STM32)
#define GPIOA_BASE 0x40020000
#define GPIOB_BASE 0x40020400

#define GPIOA ((GPIO_TypeDef*)GPIOA_BASE)
#define GPIOB ((GPIO_TypeDef*)GPIOB_BASE)

void configureGPIO() {
    // Enable GPIO clock (implementation specific)
    enableGPIOClock(GPIOA);

    // Configure PA5 as output (LED)
    GPIOA->MODER &= ~(3U << (5 * 2));    // Clear mode bits
    GPIOA->MODER |= (1U << (5 * 2));     // Set as output

    // Configure PA0 as input (button)
    GPIOA->MODER &= ~(3U << (0 * 2));    // Input mode (reset state)
    GPIOA->PUPDR |= (1U << (0 * 2));     // Enable pull-up
}

void toggleLED() {
    GPIOA->ODR ^= (1U << 5);  // Toggle PA5
}

bool readButton() {
    return (GPIOA->IDR & (1U << 0)) == 0;  // Active low with pull-up
}
```

---

## GPIO Bit Manipulation Techniques

Efficient GPIO operations using bit manipulation:

```cpp
// Atomic bit operations using BSRR register
void setPin(GPIO_TypeDef* gpio, uint8_t pin) {
    gpio->BSRR = (1U << pin);  // Set bit
}

void clearPin(GPIO_TypeDef* gpio, uint8_t pin) {
    gpio->BSRR = (1U << (pin + 16));  // Reset bit
}

// Multiple pin operations
void setMultiplePins(GPIO_TypeDef* gpio, uint16_t pins) {
    gpio->BSRR = pins;
}

void clearMultiplePins(GPIO_TypeDef* gpio, uint16_t pins) {
    gpio->BSRR = (pins << 16);
}

// Read multiple pins efficiently
uint16_t readPins(GPIO_TypeDef* gpio, uint16_t mask) {
    return gpio->IDR & mask;
}

// Safe read-modify-write for ODR
void updateOutput(GPIO_TypeDef* gpio, uint16_t mask, uint16_t value) {
    uint32_t temp = gpio->ODR;
    temp &= ~mask;           // Clear relevant bits
    temp |= (value & mask);  // Set new values
    gpio->ODR = temp;
}
```

---
## Universal Asynchronous Receiver-Transmitter (UART)

UART provides serial communication:
- **Asynchronous**: No clock line needed
- **Configurable**: Baud rate, data bits, parity, stop bits
- **Full duplex**: Simultaneous TX and RX
- **Flow control**: RTS/CTS hardware handshaking

---
## Universal Asynchronous Receiver-Transmitter (UART)

![universal_asynchronous_receiver_transmitter_uart](svg/courses/embedded/effective-real-time-embedded-c-and-c++/19_peripherals/universal_asynchronous_receiver_transmitter_uart.svg)

---

## UART Configuration

Setting up UART communication:

```cpp
#include <stdint.h>

struct UART_TypeDef {
    volatile uint32_t DR;     // Data register
    volatile uint32_t SR;     // Status register
    volatile uint32_t BRR;    // Baud rate register
    volatile uint32_t CR1;    // Control register 1
    volatile uint32_t CR2;    // Control register 2
    volatile uint32_t CR3;    // Control register 3
};

#define UART1 ((UART_TypeDef*)0x40011000)

void configureUART(uint32_t baudrate) {
    // Enable UART clock
    enableUARTClock();

    // Calculate baud rate divisor
    uint32_t apb_freq = getAPBFrequency();
    UART1->BRR = apb_freq / baudrate;

    // Configure format: 8N1 (8 data bits, no parity, 1 stop bit)
    UART1->CR1 = 0;
    UART1->CR1 |= (1U << 13);  // Enable UART
    UART1->CR1 |= (1U << 2);   // Enable RX
    UART1->CR1 |= (1U << 3);   // Enable TX

    // Configure GPIO pins for UART alternate function
    configureUARTPins();
}
```

---

## UART Data Transmission

Sending and receiving data via UART:

```cpp
// Blocking transmit
void uartSendByte(uint8_t data) {
    while (!(UART1->SR & (1U << 7)));  // Wait for TXE (transmit empty)
    UART1->DR = data;
}

void uartSendString(const char* str) {
    while (*str) {
        uartSendByte(*str++);
    }
}

// Blocking receive
uint8_t uartReceiveByte() {
    while (!(UART1->SR & (1U << 5)));  // Wait for RXNE (receive not empty)
    return UART1->DR;
}

// Non-blocking operations
bool uartTxReady() {
    return (UART1->SR & (1U << 7)) != 0;
}

bool uartRxReady() {
    return (UART1->SR & (1U << 5)) != 0;
}

bool uartSendByteNonBlocking(uint8_t data) {
    if (uartTxReady()) {
        UART1->DR = data;
        return true;
    }
    return false;
}
```

---

## UART Error Handling

Managing UART transmission errors:

```cpp
// UART error flags
#define UART_ERROR_OVERRUN  (1U << 3)
#define UART_ERROR_NOISE    (1U << 2)
#define UART_ERROR_FRAMING  (1U << 1)
#define UART_ERROR_PARITY   (1U << 0)

typedef enum {
    UART_OK,
    UART_ERROR_OVERRUN_ERR,
    UART_ERROR_NOISE_ERR,
    UART_ERROR_FRAME_ERR,
    UART_ERROR_PARITY_ERR
} UARTStatus;

UARTStatus uartReceiveByteWithErrorCheck(uint8_t* data) {
    // Wait for data
    while (!(UART1->SR & (1U << 5)));

    // Check for errors
    uint32_t status = UART1->SR;
    *data = UART1->DR;  // Reading DR clears RXNE flag

    if (status & UART_ERROR_OVERRUN) {
        UART1->SR &= ~UART_ERROR_OVERRUN;  // Clear error
        return UART_ERROR_OVERRUN_ERR;
    }
    if (status & UART_ERROR_NOISE) {
        return UART_ERROR_NOISE_ERR;
    }
    if (status & UART_ERROR_FRAMING) {
        return UART_ERROR_FRAME_ERR;
    }
    if (status & UART_ERROR_PARITY) {
        return UART_ERROR_PARITY_ERR;
    }

    return UART_OK;
}
```

---
## Analog-to-Digital Converter (ADC)

ADC converts analog voltages to digital values:
- **Resolution**: 8, 10, 12, 16 bits typical
- **Reference voltage**: Determines full-scale range
- **Sampling rate**: Conversions per second
- **Multiple channels**: Multiplexed inputs

---
## Analog-to-Digital Converter (ADC)

![analog_to_digital_converter_adc](svg/courses/embedded/effective-real-time-embedded-c-and-c++/19_peripherals/analog_to_digital_converter_adc.svg)

---

## ADC Configuration

Setting up the ADC for measurements:

```cpp
struct ADC_TypeDef {
    volatile uint32_t SR;     // Status register
    volatile uint32_t CR1;    // Control register 1
    volatile uint32_t CR2;    // Control register 2
    volatile uint32_t SMPR1;  // Sample time register 1
    volatile uint32_t SMPR2;  // Sample time register 2
    volatile uint32_t SQR1;   // Sequence register 1
    volatile uint32_t SQR2;   // Sequence register 2
    volatile uint32_t SQR3;   // Sequence register 3
    volatile uint32_t DR;     // Data register
};

#define ADC1 ((ADC_TypeDef*)0x40012000)

void configureADC() {
    // Enable ADC clock
    enableADCClock();

    // Configure ADC
    ADC1->CR2 = 0;
    ADC1->CR2 |= (1U << 0);   // Enable ADC (ADON)

    // Set sample time for channel 0 (longest time for accuracy)
    ADC1->SMPR2 |= (7U << 0);  // 239.5 cycles for channel 0

    // Configure single conversion mode
    ADC1->CR1 = 0;
    ADC1->CR2 |= (1U << 1);   // Continuous conversion

    // Set sequence length to 1
    ADC1->SQR1 = 0;  // Length = 1 conversion

    // Calibration (if supported)
    ADC1->CR2 |= (1U << 3);   // Reset calibration
    while (ADC1->CR2 & (1U << 3));
    ADC1->CR2 |= (1U << 2);   // Start calibration
    while (ADC1->CR2 & (1U << 2));
}
```

---

## ADC Conversion Operations

Performing ADC conversions:

```cpp
// Single channel conversion
uint16_t adcReadChannel(uint8_t channel) {
    // Select channel in sequence register
    ADC1->SQR3 = channel;

    // Start conversion
    ADC1->CR2 |= (1U << 0);   // Start conversion (SWSTART)

    // Wait for conversion complete
    while (!(ADC1->SR & (1U << 1)));  // Wait for EOC

    // Read result
    return ADC1->DR;
}

// Convert voltage to digital value
float adcToVoltage(uint16_t adcValue, float vref, uint8_t resolution) {
    uint16_t maxValue = (1U << resolution) - 1;
    return (adcValue * vref) / maxValue;
}

// Multi-channel scanning
void adcConfigureMultiChannel(uint8_t* channels, uint8_t count) {
    // Set sequence length
    ADC1->SQR1 = (count - 1) << 20;

    // Configure channels in sequence
    for (uint8_t i = 0; i < count && i < 16; i++) {
        if (i < 6) {
            ADC1->SQR3 |= (channels[i] << (i * 5));
        } else if (i < 12) {
            ADC1->SQR2 |= (channels[i] << ((i - 6) * 5));
        } else {
            ADC1->SQR1 |= (channels[i] << ((i - 12) * 5));
        }
    }
}
```

---

## ADC with DMA for Continuous Sampling

Using DMA for automatic data transfer:

```cpp
// Buffer for ADC results
uint16_t adcBuffer[100];
volatile bool conversionComplete = false;

void configureADCWithDMA() {
    // Configure ADC for DMA
    ADC1->CR2 |= (1U << 8);   // Enable DMA mode
    ADC1->CR2 |= (1U << 1);   // Continuous conversion

    // Configure DMA
    configureDMAForADC();

    // Start conversions
    ADC1->CR2 |= (1U << 30);  // Start conversion
}

void configureDMAForADC() {
    // Enable DMA clock
    enableDMAClock();

    // Configure DMA channel for ADC
    DMA1_Channel1->CPAR = (uint32_t)&ADC1->DR;          // Peripheral address
    DMA1_Channel1->CMAR = (uint32_t)adcBuffer;          // Memory address
    DMA1_Channel1->CNDTR = sizeof(adcBuffer)/sizeof(uint16_t);  // Data count

    // Configure DMA
    DMA1_Channel1->CCR = 0;
    DMA1_Channel1->CCR |= (1U << 5);   // Circular mode
    DMA1_Channel1->CCR |= (1U << 7);   // Memory increment
    DMA1_Channel1->CCR |= (1U << 10);  // 16-bit memory size
    DMA1_Channel1->CCR |= (1U << 8);   // 16-bit peripheral size
    DMA1_Channel1->CCR |= (1U << 1);   // Transfer complete interrupt

    // Enable DMA channel
    DMA1_Channel1->CCR |= (1U << 0);
}

// DMA interrupt handler
void DMA1_Channel1_IRQHandler() {
    if (DMA1->ISR & (1U << 1)) {  // Transfer complete
        DMA1->IFCR |= (1U << 1);  // Clear flag
        conversionComplete = true;
    }
}
```

---
## Serial Peripheral Interface (SPI)

SPI provides high-speed synchronous communication:
- **Full duplex**: Simultaneous TX and RX
- **Master/Slave**: One master, multiple slaves
- **Four wires**: MOSI, MISO, SCK, CS/SS
- **High speed**: Typically MHz range

---
## Serial Peripheral Interface (SPI)

![serial_peripheral_interface_spi](svg/courses/embedded/effective-real-time-embedded-c-and-c++/19_peripherals/serial_peripheral_interface_spi.svg)

---

## SPI Configuration

Setting up SPI communication:

```cpp
struct SPI_TypeDef {
    volatile uint32_t CR1;    // Control register 1
    volatile uint32_t CR2;    // Control register 2
    volatile uint32_t SR;     // Status register
    volatile uint32_t DR;     // Data register
    volatile uint32_t CRCPR;  // CRC polynomial register
    volatile uint32_t RXCRCR; // RX CRC register
    volatile uint32_t TXCRCR; // TX CRC register
};

#define SPI1 ((SPI_TypeDef*)0x40013000)

void configureSPIMaster() {
    // Enable SPI clock
    enableSPIClock();

    // Configure SPI as master
    SPI1->CR1 = 0;
    SPI1->CR1 |= (1U << 2);   // Master mode
    SPI1->CR1 |= (1U << 1);   // Clock polarity = 0
    SPI1->CR1 |= (0U << 0);   // Clock phase = 0 (sample on first edge)
    SPI1->CR1 |= (3U << 3);   // Baud rate prescaler (/16)
    SPI1->CR1 |= (1U << 9);   // Software slave management
    SPI1->CR1 |= (1U << 8);   // Internal slave select

    // Data frame format
    SPI1->CR1 |= (0U << 11);  // 8-bit data frame
    SPI1->CR1 |= (0U << 7);   // MSB first

    // Enable SPI
    SPI1->CR1 |= (1U << 6);

    // Configure GPIO pins for SPI
    configureSPIPins();
}

void configureSPISlave() {
    enableSPIClock();

    SPI1->CR1 = 0;
    SPI1->CR1 &= ~(1U << 2);  // Slave mode
    // Clock polarity and phase should match master
    SPI1->CR1 |= (1U << 6);   // Enable SPI

    configureSPIPins();
}
```

---

## SPI Data Transfer

Transmitting and receiving SPI data:

```cpp
// Basic SPI transfer (blocking)
uint8_t spiTransferByte(uint8_t data) {
    // Wait for TX buffer empty
    while (!(SPI1->SR & (1U << 1)));

    // Send data
    SPI1->DR = data;

    // Wait for RX buffer not empty
    while (!(SPI1->SR & (1U << 0)));

    // Return received data
    return SPI1->DR;
}

// Multi-byte transfer
void spiTransferBuffer(uint8_t* txBuffer, uint8_t* rxBuffer, uint16_t size) {
    for (uint16_t i = 0; i < size; i++) {
        rxBuffer[i] = spiTransferByte(txBuffer[i]);
    }
}

// Chip select control
void spiSelectSlave(uint8_t slaveNumber) {
    // Assuming active-low chip selects
    GPIOA->BSRR = (0xFF << 16);  // Deselect all (set high)
    GPIOA->BSRR = (1U << slaveNumber);  // Select specific slave (set low)
}

void spiDeselectAll() {
    GPIOA->BSRR = (0xFF << 16);  // Deselect all slaves
}

// Complete transaction
void spiTransaction(uint8_t slave, uint8_t* txData, uint8_t* rxData, uint16_t size) {
    spiSelectSlave(slave);
    spiTransferBuffer(txData, rxData, size);
    spiDeselectAll();
}

// Non-blocking operations
bool spiTxReady() {
    return (SPI1->SR & (1U << 1)) != 0;
}

bool spiRxReady() {
    return (SPI1->SR & (1U << 0)) != 0;
}

bool spiSendByteNonBlocking(uint8_t data) {
    if (spiTxReady()) {
        SPI1->DR = data;
        return true;
    }
    return false;
}
```

---
## Inter-Integrated Circuit (I2C)

I2C provides multi-master, multi-slave communication:
- **Two wires**: SDA (data) and SCL (clock)
- **Addressing**: 7-bit or 10-bit slave addresses
- **Open drain**: Requires pull-up resistors
- **Arbitration**: Multiple masters can coexist

---
## Inter-Integrated Circuit (I2C)

![inter_integrated_circuit_i2c](svg/courses/embedded/effective-real-time-embedded-c-and-c++/19_peripherals/inter_integrated_circuit_i2c.svg)

---

## I2C Configuration

Setting up I2C communication:

```cpp
struct I2C_TypeDef {
    volatile uint32_t CR1;    // Control register 1
    volatile uint32_t CR2;    // Control register 2
    volatile uint32_t OAR1;   // Own address register 1
    volatile uint32_t OAR2;   // Own address register 2
    volatile uint32_t DR;     // Data register
    volatile uint32_t SR1;    // Status register 1
    volatile uint32_t SR2;    // Status register 2
    volatile uint32_t CCR;    // Clock control register
    volatile uint32_t TRISE;  // Rise time register
};

#define I2C1 ((I2C_TypeDef*)0x40005400)

void configureI2C(uint32_t clockSpeed) {
    // Enable I2C clock
    enableI2CClock();

    // Reset I2C
    I2C1->CR1 |= (1U << 15);
    I2C1->CR1 &= ~(1U << 15);

    // Configure timing
    uint32_t pclk1 = getAPB1Frequency();
    I2C1->CR2 = (pclk1 / 1000000) & 0x3F;  // APB1 frequency in MHz

    if (clockSpeed <= 100000) {
        // Standard mode (100 kHz)
        I2C1->CCR = pclk1 / (clockSpeed * 2);
        I2C1->TRISE = (pclk1 / 1000000) + 1;
    } else {
        // Fast mode (400 kHz)
        I2C1->CCR = pclk1 / (clockSpeed * 3);
        I2C1->CCR |= (1U << 15);  // Fast mode enable
        I2C1->TRISE = ((pclk1 * 300) / 1000000000) + 1;
    }

    // Enable I2C
    I2C1->CR1 |= (1U << 0);

    // Configure GPIO pins for I2C
    configureI2CPins();
}
```

---

## I2C Master Operations

Implementing I2C master functionality:

```cpp
// I2C status flags
#define I2C_FLAG_SB     (1U << 0)   // Start bit
#define I2C_FLAG_ADDR   (1U << 1)   // Address sent
#define I2C_FLAG_BTF    (1U << 2)   // Byte transfer finished
#define I2C_FLAG_TXE    (1U << 7)   // Transmit buffer empty
#define I2C_FLAG_RXNE   (1U << 6)   // Receive buffer not empty

typedef enum {
    I2C_OK,
    I2C_ERROR_TIMEOUT,
    I2C_ERROR_ACK_FAILURE,
    I2C_ERROR_BUS_ERROR
} I2CStatus;

I2CStatus i2cStart() {
    // Generate start condition
    I2C1->CR1 |= (1U << 8);

    // Wait for start bit to be set
    uint32_t timeout = 10000;
    while (!(I2C1->SR1 & I2C_FLAG_SB) && timeout--);

    return (timeout > 0) ? I2C_OK : I2C_ERROR_TIMEOUT;
}

I2CStatus i2cSendAddress(uint8_t address, bool read) {
    // Send address with read/write bit
    I2C1->DR = (address << 1) | (read ? 1 : 0);

    // Wait for address to be sent
    uint32_t timeout = 10000;
    while (!(I2C1->SR1 & I2C_FLAG_ADDR) && timeout--);

    if (timeout == 0) return I2C_ERROR_TIMEOUT;

    // Clear ADDR flag by reading SR1 and SR2
    volatile uint32_t dummy = I2C1->SR1;
    dummy = I2C1->SR2;
    (void)dummy;

    return I2C_OK;
}

void i2cStop() {
    I2C1->CR1 |= (1U << 9);  // Generate stop condition
}
```

---

## I2C Data Transfer Functions

Reading and writing I2C data:

```cpp
I2CStatus i2cWriteByte(uint8_t data) {
    // Wait for transmit buffer empty
    uint32_t timeout = 10000;
    while (!(I2C1->SR1 & I2C_FLAG_TXE) && timeout--);

    if (timeout == 0) return I2C_ERROR_TIMEOUT;

    // Send data
    I2C1->DR = data;

    // Wait for byte transfer finished
    timeout = 10000;
    while (!(I2C1->SR1 & I2C_FLAG_BTF) && timeout--);

    return (timeout > 0) ? I2C_OK : I2C_ERROR_TIMEOUT;
}

I2CStatus i2cReadByte(uint8_t* data, bool sendNack) {
    if (sendNack) {
        I2C1->CR1 &= ~(1U << 10);  // Disable ACK
    } else {
        I2C1->CR1 |= (1U << 10);   // Enable ACK
    }

    // Wait for receive buffer not empty
    uint32_t timeout = 10000;
    while (!(I2C1->SR1 & I2C_FLAG_RXNE) && timeout--);

    if (timeout == 0) return I2C_ERROR_TIMEOUT;

    // Read data
    *data = I2C1->DR;

    return I2C_OK;
}

// High-level write function
I2CStatus i2cWriteData(uint8_t address, uint8_t* data, uint16_t size) {
    I2CStatus status;

    if ((status = i2cStart()) != I2C_OK) return status;
    if ((status = i2cSendAddress(address, false)) != I2C_OK) return status;

    for (uint16_t i = 0; i < size; i++) {
        if ((status = i2cWriteByte(data[i])) != I2C_OK) break;
    }

    i2cStop();
    return status;
}

// High-level read function
I2CStatus i2cReadData(uint8_t address, uint8_t* data, uint16_t size) {
    I2CStatus status;

    if ((status = i2cStart()) != I2C_OK) return status;
    if ((status = i2cSendAddress(address, true)) != I2C_OK) return status;

    for (uint16_t i = 0; i < size; i++) {
        bool lastByte = (i == size - 1);
        if ((status = i2cReadByte(&data[i], lastByte)) != I2C_OK) break;
    }

    i2cStop();
    return status;
}
```

---
## Direct Memory Access (DMA)

DMA enables data transfer without CPU intervention:
- **Memory-to-Memory**: Copy data between memory locations
- **Memory-to-Peripheral**: Send data to peripherals
- **Peripheral-to-Memory**: Receive data from peripherals
- **Circular mode**: Continuous operation for streaming

---
## Direct Memory Access (DMA)

![direct_memory_access_dma](svg/courses/embedded/effective-real-time-embedded-c-and-c++/19_peripherals/direct_memory_access_dma.svg)

---

## DMA Configuration

Setting up DMA channels:

```cpp
struct DMA_Channel_TypeDef {
    volatile uint32_t CCR;    // Configuration register
    volatile uint32_t CNDTR;  // Number of data register
    volatile uint32_t CPAR;   // Peripheral address register
    volatile uint32_t CMAR;   // Memory address register
};

struct DMA_TypeDef {
    volatile uint32_t ISR;    // Interrupt status register
    volatile uint32_t IFCR;   // Interrupt flag clear register
};

#define DMA1 ((DMA_TypeDef*)0x40020000)
#define DMA1_Channel1 ((DMA_Channel_TypeDef*)0x40020008)

void configureDMA(uint8_t channel, uint32_t peripheral, uint32_t memory,
                  uint16_t size, uint32_t direction) {
    // Enable DMA clock
    enableDMAClock();

    DMA_Channel_TypeDef* dmaChannel = getDMAChannel(channel);

    // Disable DMA channel
    dmaChannel->CCR &= ~(1U << 0);

    // Configure addresses
    dmaChannel->CPAR = peripheral;
    dmaChannel->CMAR = memory;
    dmaChannel->CNDTR = size;

    // Configure channel
    dmaChannel->CCR = 0;
    dmaChannel->CCR |= direction;        // Transfer direction
    dmaChannel->CCR |= (1U << 7);        // Memory increment
    dmaChannel->CCR |= (1U << 1);        // Transfer complete interrupt
    dmaChannel->CCR |= (1U << 2);        // Transfer error interrupt

    // Enable DMA channel
    dmaChannel->CCR |= (1U << 0);
}

// DMA direction constants
#define DMA_DIR_PERIPHERAL_TO_MEMORY  0
#define DMA_DIR_MEMORY_TO_PERIPHERAL  (1U << 4)
#define DMA_DIR_MEMORY_TO_MEMORY      (1U << 14)
```

---

## DMA with Peripherals

Using DMA with UART and SPI:

```cpp
// DMA-based UART transmission
uint8_t txBuffer[100];
volatile bool dmaTransmitComplete = false;

void uartTransmitDMA(uint8_t* data, uint16_t size) {
    // Copy data to DMA buffer
    memcpy(txBuffer, data, size);

    // Configure DMA for UART TX
    configureDMA(4, (uint32_t)&UART1->DR, (uint32_t)txBuffer,
                 size, DMA_DIR_MEMORY_TO_PERIPHERAL);

    // Enable UART DMA mode
    UART1->CR3 |= (1U << 7);  // DMAT (DMA enable transmitter)

    dmaTransmitComplete = false;
}

// DMA-based ADC with circular buffer
#define ADC_BUFFER_SIZE 256
uint16_t adcBuffer[ADC_BUFFER_SIZE];
volatile uint16_t adcBufferIndex = 0;

void adcStartDMACircular() {
    // Configure DMA for ADC in circular mode
    DMA1_Channel1->CCR &= ~(1U << 0);  // Disable channel

    DMA1_Channel1->CPAR = (uint32_t)&ADC1->DR;
    DMA1_Channel1->CMAR = (uint32_t)adcBuffer;
    DMA1_Channel1->CNDTR = ADC_BUFFER_SIZE;

    DMA1_Channel1->CCR = 0;
    DMA1_Channel1->CCR |= (1U << 5);   // Circular mode
    DMA1_Channel1->CCR |= (1U << 7);   // Memory increment
    DMA1_Channel1->CCR |= (1U << 10);  // 16-bit memory size
    DMA1_Channel1->CCR |= (1U << 8);   // 16-bit peripheral size
    DMA1_Channel1->CCR |= (1U << 2);   // Half transfer interrupt
    DMA1_Channel1->CCR |= (1U << 1);   // Transfer complete interrupt

    // Enable DMA channel
    DMA1_Channel1->CCR |= (1U << 0);

    // Configure ADC for DMA
    ADC1->CR2 |= (1U << 8);   // DMA enable
    ADC1->CR2 |= (1U << 1);   // Continuous conversion

    // Start ADC
    ADC1->CR2 |= (1U << 0);
}
```

---

## Nested Vector Interrupt Controller (NVIC)

NVIC manages interrupt priorities and handling:
- **Priority levels**: Configurable interrupt priorities
- **Preemption**: Higher priority interrupts can preempt lower ones
- **Nesting**: Support for nested interrupts
- **Enable/Disable**: Individual interrupt control

```cpp
// NVIC register definitions
#define NVIC_ISER0 ((volatile uint32_t*)0xE000E100)  // Interrupt Set Enable
#define NVIC_ICER0 ((volatile uint32_t*)0xE000E180)  // Interrupt Clear Enable
#define NVIC_ISPR0 ((volatile uint32_t*)0xE000E200)  // Interrupt Set Pending
#define NVIC_ICPR0 ((volatile uint32_t*)0xE000E280)  // Interrupt Clear Pending
#define NVIC_IPR0  ((volatile uint32_t*)0xE000E400)  // Interrupt Priority

// Enable interrupt
void nvicEnableInterrupt(uint8_t irqNumber) {
    uint8_t regIndex = irqNumber / 32;
    uint8_t bitPosition = irqNumber % 32;
    NVIC_ISER0[regIndex] |= (1U << bitPosition);
}

// Disable interrupt
void nvicDisableInterrupt(uint8_t irqNumber) {
    uint8_t regIndex = irqNumber / 32;
    uint8_t bitPosition = irqNumber % 32;
    NVIC_ICER0[regIndex] |= (1U << bitPosition);
}

// Set interrupt priority
void nvicSetPriority(uint8_t irqNumber, uint8_t priority) {
    uint8_t regIndex = irqNumber / 4;
    uint8_t bitPosition = (irqNumber % 4) * 8;

    NVIC_IPR0[regIndex] &= ~(0xFF << bitPosition);
    NVIC_IPR0[regIndex] |= (priority << (bitPosition + 4));  // Upper 4 bits
}
```

---

## Interrupt Service Routines

Writing efficient interrupt handlers:

```cpp
// Timer interrupt example
volatile uint32_t systemTick = 0;
volatile bool timerFlag = false;

void TIM2_IRQHandler() {
    // Check timer interrupt flag
    if (TIM2->SR & (1U << 0)) {
        // Clear interrupt flag
        TIM2->SR &= ~(1U << 0);

        // Handle interrupt
        systemTick++;
        timerFlag = true;

        // Toggle LED every 1000ms
        if (systemTick % 1000 == 0) {
            GPIOA->ODR ^= (1U << 5);
        }
    }
}

// UART receive interrupt
#define UART_RX_BUFFER_SIZE 64
volatile uint8_t uartRxBuffer[UART_RX_BUFFER_SIZE];
volatile uint16_t uartRxHead = 0;
volatile uint16_t uartRxTail = 0;

void UART1_IRQHandler() {
    // Check for receive interrupt
    if (UART1->SR & (1U << 5)) {  // RXNE flag
        uint8_t data = UART1->DR;  // Reading DR clears RXNE

        // Store in circular buffer
        uint16_t nextHead = (uartRxHead + 1) % UART_RX_BUFFER_SIZE;
        if (nextHead != uartRxTail) {
            uartRxBuffer[uartRxHead] = data;
            uartRxHead = nextHead;
        }
        // If buffer full, data is lost (overrun)
    }
}

// Function to read from UART buffer
bool uartReceiveBuffered(uint8_t* data) {
    if (uartRxHead != uartRxTail) {
        *data = uartRxBuffer[uartRxTail];
        uartRxTail = (uartRxTail + 1) % UART_RX_BUFFER_SIZE;
        return true;
    }
    return false;
}
```

---

## General Purpose Timers (TIM)

Hardware timers provide precise timing and PWM:
- **Count modes**: Up, down, up/down counting
- **PWM generation**: Variable duty cycle output
- **Input capture**: Measure external signal timing
- **Output compare**: Generate precise timing events

```cpp
struct TIM_TypeDef {
    volatile uint32_t CR1;    // Control register 1
    volatile uint32_t CR2;    // Control register 2
    volatile uint32_t SMCR;   // Slave mode control register
    volatile uint32_t DIER;   // Interrupt enable register
    volatile uint32_t SR;     // Status register
    volatile uint32_t EGR;    // Event generation register
    volatile uint32_t CCMR1;  // Capture/compare mode register 1
    volatile uint32_t CCMR2;  // Capture/compare mode register 2
    volatile uint32_t CCER;   // Capture/compare enable register
    volatile uint32_t CNT;    // Counter register
    volatile uint32_t PSC;    // Prescaler register
    volatile uint32_t ARR;    // Auto-reload register
    volatile uint32_t CCR1;   // Capture/compare register 1
    volatile uint32_t CCR2;   // Capture/compare register 2
    volatile uint32_t CCR3;   // Capture/compare register 3
    volatile uint32_t CCR4;   // Capture/compare register 4
};

#define TIM2 ((TIM_TypeDef*)0x40000000)

void configureTimer(uint32_t frequency) {
    // Enable timer clock
    enableTimerClock();

    // Configure timer for desired frequency
    uint32_t timerClock = getTimerClockFrequency();
    uint32_t prescaler = (timerClock / frequency) - 1;

    TIM2->PSC = prescaler;
    TIM2->ARR = 999;  // Auto-reload value (1000 counts)

    // Enable update interrupt
    TIM2->DIER |= (1U << 0);

    // Enable timer
    TIM2->CR1 |= (1U << 0);

    // Enable NVIC interrupt
    nvicEnableInterrupt(28);  // TIM2 IRQ number
}
```

---

## PWM Generation

Creating PWM signals with timers:

```cpp
void configurePWM(uint8_t channel, uint16_t dutyCycle) {
    // Configure timer for PWM mode
    TIM2->CR1 &= ~(1U << 0);  // Disable timer

    // Configure PWM frequency
    TIM2->PSC = 71;           // Prescaler for 1MHz timer clock
    TIM2->ARR = 999;          // 1kHz PWM frequency (1MHz / 1000)

    // Configure channel for PWM mode 1
    if (channel == 1) {
        TIM2->CCMR1 &= ~(0x7 << 4);   // Clear OC1M bits
        TIM2->CCMR1 |= (0x6 << 4);    // PWM mode 1
        TIM2->CCMR1 |= (1U << 3);     // OC1PE (preload enable)
        TIM2->CCER |= (1U << 0);      // CC1E (enable output)
        TIM2->CCR1 = dutyCycle;       // Set duty cycle
    }
    // Similar configuration for other channels...

    // Enable timer
    TIM2->CR1 |= (1U << 0);

    // Configure GPIO pin for PWM output
    configurePWMPin(channel);
}

void setPWMDutyCycle(uint8_t channel, uint16_t dutyCycle) {
    switch (channel) {
        case 1: TIM2->CCR1 = dutyCycle; break;
        case 2: TIM2->CCR2 = dutyCycle; break;
        case 3: TIM2->CCR3 = dutyCycle; break;
        case 4: TIM2->CCR4 = dutyCycle; break;
    }
}

// Convert percentage to timer counts
uint16_t percentageToCounts(float percentage, uint16_t maxCounts) {
    if (percentage > 100.0f) percentage = 100.0f;
    if (percentage < 0.0f) percentage = 0.0f;
    return (uint16_t)(percentage * maxCounts / 100.0f);
}
```

---

## System Tick Timer (SysTick)

SysTick provides system timing for RTOS and delays:
- **24-bit counter**: Counts down from reload value
- **System clock**: Derives from CPU clock
- **RTOS support**: Common timebase for task scheduling
- **Delay functions**: Precise timing delays

```cpp
// SysTick register definitions
#define SYSTICK_CSR   ((volatile uint32_t*)0xE000E010)  // Control/Status
#define SYSTICK_RVR   ((volatile uint32_t*)0xE000E014)  // Reload Value
#define SYSTICK_CVR   ((volatile uint32_t*)0xE000E018)  // Current Value

volatile uint32_t sysTickCounter = 0;

void configureSysTick(uint32_t frequency) {
    uint32_t systemClock = getSystemClockFrequency();
    uint32_t reloadValue = (systemClock / frequency) - 1;

    // Configure SysTick
    *SYSTICK_RVR = reloadValue & 0x00FFFFFF;  // 24-bit reload value
    *SYSTICK_CVR = 0;                         // Clear current value

    // Configure control register
    *SYSTICK_CSR = 0;
    *SYSTICK_CSR |= (1U << 0);  // Enable SysTick
    *SYSTICK_CSR |= (1U << 1);  // Enable interrupt
    *SYSTICK_CSR |= (1U << 2);  // Use processor clock
}

// SysTick interrupt handler
void SysTick_Handler() {
    sysTickCounter++;
}

// Delay functions
void delayMs(uint32_t milliseconds) {
    uint32_t startTick = sysTickCounter;
    while ((sysTickCounter - startTick) < milliseconds);
}

uint32_t getSystemTime() {
    return sysTickCounter;
}

// Non-blocking timer
typedef struct {
    uint32_t startTime;
    uint32_t duration;
    bool active;
} Timer_t;

void timerStart(Timer_t* timer, uint32_t durationMs) {
    timer->startTime = sysTickCounter;
    timer->duration = durationMs;
    timer->active = true;
}

bool timerExpired(Timer_t* timer) {
    if (!timer->active) return false;

    if ((sysTickCounter - timer->startTime) >= timer->duration) {
        timer->active = false;
        return true;
    }
    return false;
}
```

---

## Peripheral Integration Example

Complete example integrating multiple peripherals:

```cpp
// System state structure
typedef struct {
    uint16_t adcValue;
    float temperature;
    uint8_t pwmDutyCycle;
    bool buttonPressed;
    char displayBuffer[32];
} SystemState_t;

SystemState_t systemState = {0};

// Main system initialization
void initializeSystem() {
    // Initialize clocks
    initializeClocks();

    // Configure peripherals
    configureGPIO();
    configureSysTick(1000);  // 1ms tick
    configureADC();
    configurePWM(1, 0);      // Start with 0% duty cycle
    configureUART(115200);

    // Enable interrupts
    nvicEnableInterrupt(ADC1_2_IRQn);
    nvicEnableInterrupt(UART1_IRQn);

    // Start continuous ADC conversion
    ADC1->CR2 |= (1U << 0);  // Start conversion
}

// Main application loop
void applicationLoop() {
    static Timer_t displayTimer;
    timerStart(&displayTimer, 100);  // Update display every 100ms

    while (1) {
// Main application loop
void applicationLoop() {
    static Timer_t displayTimer;
    timerStart(&displayTimer, 100);  // Update display every 100ms

    while (1) {
        // Read button state
        systemState.buttonPressed = readButton();

        // Process ADC data (updated via interrupt)
        systemState.temperature = adcToTemperature(systemState.adcValue);

        // Control PWM based on temperature
        if (systemState.temperature > 25.0f) {
            systemState.pwmDutyCycle = 75;  // Fan at 75%
        } else if (systemState.temperature > 20.0f) {
            systemState.pwmDutyCycle = 50;  // Fan at 50%
        } else {
            systemState.pwmDutyCycle = 0;   // Fan off
        }
        setPWMDutyCycle(1, percentageToCounts(systemState.pwmDutyCycle, 999));

        // Update display periodically
        if (timerExpired(&displayTimer)) {
            snprintf(systemState.displayBuffer, sizeof(systemState.displayBuffer),
                    "Temp: %.1f°C, Fan: %d%%\r\n",
                    systemState.temperature, systemState.pwmDutyCycle);
            uartSendString(systemState.displayBuffer);
            timerStart(&displayTimer, 100);
        }

        // Handle button press
        if (systemState.buttonPressed) {
            uartSendString("Button pressed!\r\n");
            delayMs(200);  // Debounce
        }

        // Low power mode when idle
        __WFI();  // Wait for interrupt
    }
}

// ADC conversion complete interrupt
void ADC1_2_IRQHandler() {
    if (ADC1->SR & (1U << 1)) {  // EOC flag
        systemState.adcValue = ADC1->DR;  // Reading DR clears EOC
    }
}

float adcToTemperature(uint16_t adcValue) {
    // Convert ADC reading to temperature (example calculation)
    float voltage = (adcValue * 3.3f) / 4095.0f;  // 12-bit ADC
    return (voltage - 0.5f) * 100.0f;  // TMP36 sensor formula
}
```

---

## Power Management and Low Power Modes

Optimizing power consumption in embedded systems:

```cpp
// Power mode definitions
typedef enum {
    POWER_RUN,
    POWER_SLEEP,
    POWER_STOP,
    POWER_STANDBY
} PowerMode_t;

void enterLowPowerMode(PowerMode_t mode) {
    switch (mode) {
        case POWER_SLEEP:
            // Sleep mode - CPU stops, peripherals continue
            __WFI();  // Wait for interrupt
            break;

        case POWER_STOP:
            // Stop mode - CPU and most peripherals stop
            // Configure wake-up sources first
            PWR->CR |= (1U << 0);   // Clear wake-up flag
            SCB->SCR |= (1U << 2);  // SLEEPDEEP bit
            __WFI();
            SCB->SCR &= ~(1U << 2); // Clear SLEEPDEEP
            // Restore clocks after wake-up
            initializeClocks();
            break;

        case POWER_STANDBY:
            // Standby mode - lowest power consumption
            PWR->CR |= (1U << 2);   // Clear standby flag
            PWR->CR |= (1U << 1);   // Power down deepsleep
            SCB->SCR |= (1U << 2);  // SLEEPDEEP bit
            __WFI();
            // System will reset on wake-up
            break;

        default:
            break;
    }
}

void configureWakeUpSources() {
    // Configure wake-up pin
    PWR->CSR |= (1U << 8);  // Enable wake-up pin

    // Configure RTC wake-up (if needed)
    // enableRTCWakeUp();

    // Configure external interrupt as wake-up source
    nvicEnableInterrupt(EXTI0_IRQn);
}
```

---

## Error Handling and Diagnostics

Robust error handling for peripheral operations:

```cpp
// Error code definitions
typedef enum {
    PERIPHERAL_OK = 0,
    PERIPHERAL_ERROR_TIMEOUT,
    PERIPHERAL_ERROR_BUSY,
    PERIPHERAL_ERROR_INVALID_PARAM,
    PERIPHERAL_ERROR_HARDWARE_FAULT
} PeripheralError_t;

// Error logging system
#define MAX_ERROR_LOG 16
typedef struct {
    uint32_t timestamp;
    PeripheralError_t errorCode;
    uint8_t peripheralId;
    uint32_t errorData;
} ErrorLog_t;

ErrorLog_t errorLog[MAX_ERROR_LOG];
uint8_t errorLogIndex = 0;

void logError(PeripheralError_t error, uint8_t peripheral, uint32_t data) {
    errorLog[errorLogIndex].timestamp = getSystemTime();
    errorLog[errorLogIndex].errorCode = error;
    errorLog[errorLogIndex].peripheralId = peripheral;
    errorLog[errorLogIndex].errorData = data;

    errorLogIndex = (errorLogIndex + 1) % MAX_ERROR_LOG;

    // Send error notification
    char errorMsg[64];
    snprintf(errorMsg, sizeof(errorMsg),
            "ERROR: P%d, Code:%d, Data:0x%08lX\r\n",
            peripheral, error, data);
    uartSendString(errorMsg);
}

// Timeout-based operations
PeripheralError_t waitForFlag(volatile uint32_t* reg, uint32_t flag,
                             uint32_t timeoutMs, bool waitForSet) {
    uint32_t startTime = getSystemTime();

    while ((getSystemTime() - startTime) < timeoutMs) {
        bool flagState = (*reg & flag) != 0;
        if (flagState == waitForSet) {
            return PERIPHERAL_OK;
        }
    }

    return PERIPHERAL_ERROR_TIMEOUT;
}

// Hardware fault detection
void checkHardwareFaults() {
    // Check for clock failures
    if (RCC->CIR & (1U << 7)) {  // CSS flag
        logError(PERIPHERAL_ERROR_HARDWARE_FAULT, 0xFF, RCC->CIR);
        // Handle clock security system failure
    }

    // Check peripheral-specific faults
    if (UART1->SR & (1U << 3)) {  // Overrun error
        logError(PERIPHERAL_ERROR_HARDWARE_FAULT, 1, UART1->SR);
        UART1->SR &= ~(1U << 3);  // Clear error
    }

    // Check DMA errors
    if (DMA1->ISR & (1U << 3)) {  // Transfer error
        logError(PERIPHERAL_ERROR_HARDWARE_FAULT, 2, DMA1->ISR);
        DMA1->IFCR |= (1U << 3);  // Clear error
    }
}
```

---

## Performance Optimization Techniques

Optimizing peripheral performance:

```cpp
// Burst operations for improved efficiency
void gpioSetMultiplePinsOptimized(GPIO_TypeDef* gpio, uint16_t pins) {
    // Use BSRR for atomic operations
    gpio->BSRR = pins;  // More efficient than individual bit operations
}

// Efficient register access patterns
static inline void fastRegisterWrite(volatile uint32_t* reg, uint32_t value) {
    *reg = value;  // Direct assignment is often optimized better
}

// DMA optimization for high-throughput applications
void configureDMAForHighThroughput() {
    // Use memory-to-memory mode for fast copying
    DMA1_Channel1->CCR |= (1U << 14);  // Memory-to-memory mode

    // Configure for 32-bit transfers when possible
    DMA1_Channel1->CCR |= (2U << 8);   // 32-bit peripheral size
    DMA1_Channel1->CCR |= (2U << 10);  // 32-bit memory size

    // Enable high priority
    DMA1_Channel1->CCR |= (3U << 12);  // Very high priority
}

// Interrupt optimization
void optimizedInterruptHandler() {
    // Keep ISRs short and fast
    // Use static variables to avoid stack overhead
    static uint32_t counter = 0;

    // Clear interrupt flag immediately
    TIM2->SR &= ~(1U << 0);

    // Minimal processing in ISR
    counter++;

    // Set flag for main loop processing
    timerFlag = true;
}

// Compiler optimization hints
__attribute__((always_inline))
static inline void criticalSectionEnter() {
    __disable_irq();
}

__attribute__((always_inline))
static inline void criticalSectionExit() {
    __enable_irq();
}
```

---

## Debugging and Testing Peripherals

Tools and techniques for peripheral debugging:

```cpp
// Debug output system
#ifdef DEBUG
#define DEBUG_PRINT(fmt, ...) \
    do { \
        char debugBuf[128]; \
        snprintf(debugBuf, sizeof(debugBuf), "[DEBUG] " fmt "\r\n", ##__VA_ARGS__); \
        uartSendString(debugBuf); \
    } while(0)
#else
#define DEBUG_PRINT(fmt, ...)
#endif

// Register dump functions
void dumpGPIORegisters(GPIO_TypeDef* gpio) {
    DEBUG_PRINT("GPIO Registers:");
    DEBUG_PRINT("MODER:   0x%08lX", gpio->MODER);
    DEBUG_PRINT("OTYPER:  0x%08lX", gpio->OTYPER);
    DEBUG_PRINT("OSPEEDR: 0x%08lX", gpio->OSPEEDR);
    DEBUG_PRINT("PUPDR:   0x%08lX", gpio->PUPDR);
    DEBUG_PRINT("IDR:     0x%08lX", gpio->IDR);
    DEBUG_PRINT("ODR:     0x%08lX", gpio->ODR);
}

// Performance measurement
uint32_t measureFunctionTime(void (*func)(void)) {
    uint32_t startTime = *SYSTICK_CVR;
    func();
    uint32_t endTime = *SYSTICK_CVR;

    // SysTick counts down
    return (startTime > endTime) ? (startTime - endTime) :
                                  (startTime + (*SYSTICK_RVR - endTime));
}

// Self-test functions
bool testUARTLoopback() {
    const char testString[] = "TEST";
    bool result = true;

    // Send test data
    for (int i = 0; testString[i]; i++) {
        uartSendByte(testString[i]);
    }

    // Verify received data (requires loopback)
    for (int i = 0; testString[i]; i++) {
        uint8_t received = uartReceiveByte();
        if (received != testString[i]) {
            result = false;
            break;
        }
    }

    DEBUG_PRINT("UART loopback test: %s", result ? "PASS" : "FAIL");
    return result;
}

// Peripheral health monitoring
typedef struct {
    uint32_t operationCount;
    uint32_t errorCount;
    uint32_t lastErrorTime;
} PeripheralHealth_t;

PeripheralHealth_t peripheralHealth[8];  // Track up to 8 peripherals

void updatePeripheralHealth(uint8_t peripheralId, bool success) {
    if (peripheralId < 8) {
        peripheralHealth[peripheralId].operationCount++;
        if (!success) {
            peripheralHealth[peripheralId].errorCount++;
            peripheralHealth[peripheralId].lastErrorTime = getSystemTime();
        }
    }
}

float getPeripheralReliability(uint8_t peripheralId) {
    if (peripheralId >= 8 || peripheralHealth[peripheralId].operationCount == 0) {
        return 0.0f;
    }

    uint32_t successful = peripheralHealth[peripheralId].operationCount -
                         peripheralHealth[peripheralId].errorCount;
    return (float)successful / peripheralHealth[peripheralId].operationCount;
}
```

---

## Best Practices Summary

Key principles for effective peripheral programming:

1. **Initialize peripherals in correct order**
   - Clocks first, then GPIO, then complex peripherals
1. **Use appropriate data types**
   - volatile for hardware registers
   - const for configuration data
1. **Handle errors gracefully**
   - Check return values and status flags
   - Implement timeout mechanisms
1. **Optimize for your application**
   - Use DMA for high-throughput applications
   - Use interrupts for real-time response
1. **Keep interrupt handlers short**
   - Minimal processing in ISRs
   - Use flags for main loop processing
1. **Document hardware dependencies**
   - Pin assignments and alternate functions
   - Timing requirements and constraints
1. **Test thoroughly**
   - Unit tests for individual peripherals
   - Integration tests for complete systems
1. **Consider power consumption**
   - Disable unused peripherals
   - Use appropriate low-power modes

```cpp
// Example of good peripheral initialization
void initializePeripheralsCorrectly() {
    // 1. Enable clocks first
    enableSystemClocks();

    // 2. Configure basic peripherals
    configureGPIO();
    configureSysTick(1000);

    // 3. Configure communication peripherals
    configureUART(115200);
    configureSPI();
    configureI2C(100000);

    // 4. Configure complex peripherals
    configureADC();
    configureDMA();
    configureTimers();

    // 5. Enable interrupts last
    nvicEnableInterrupt(UART1_IRQn);
    nvicEnableInterrupt(ADC1_2_IRQn);
    nvicEnableInterrupt(TIM2_IRQn);

    // 6. Start operations
    startPeripheralOperations();
}
```
