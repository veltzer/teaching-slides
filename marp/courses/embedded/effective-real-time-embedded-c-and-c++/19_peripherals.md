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

## Overview of Embedded Peripherals: Details

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

## Universal Asynchronous Receiver-Transmitter (UART): Details

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

## UART Error Handling: Flags and Enum

Managing UART transmission errors:

```cpp
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
```

---

## UART Error Handling: Check Routine

```cpp
UARTStatus uartReceiveByteWithErrorCheck(uint8_t* data) {
    while (!(UART1->SR & (1U << 5)));

    uint32_t status = UART1->SR;
    *data = UART1->DR;

    if (status & UART_ERROR_OVERRUN) {
        UART1->SR &= ~UART_ERROR_OVERRUN;
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

## Analog-to-Digital Converter (ADC): Details

ADC converts analog voltages to digital values:
- **Resolution**: 8, 10, 12, 16 bits typical
- **Reference voltage**: Determines full-scale range
- **Sampling rate**: Conversions per second
- **Multiple channels**: Multiplexed inputs

---

## Analog-to-Digital Converter (ADC)

![analog_to_digital_converter_adc](svg/courses/embedded/effective-real-time-embedded-c-and-c++/19_peripherals/analog_to_digital_converter_adc.svg)

---

## ADC Configuration: Register Layout

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
```

---

## ADC Configuration: Initialization

```cpp
void configureADC() {
    enableADCClock();

    ADC1->CR2 = 0;
    ADC1->CR2 |= (1U << 0);   // ADON

    ADC1->SMPR2 |= (7U << 0);  // 239.5 cycles for channel 0

    ADC1->CR1 = 0;
    ADC1->CR2 |= (1U << 1);   // Continuous conversion

    ADC1->SQR1 = 0;

    ADC1->CR2 |= (1U << 3);
    while (ADC1->CR2 & (1U << 3));
    ADC1->CR2 |= (1U << 2);
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

## ADC with DMA: Setup

Using DMA for automatic data transfer:

```cpp
uint16_t adcBuffer[100];
volatile bool conversionComplete = false;

void configureADCWithDMA() {
    ADC1->CR2 |= (1U << 8);   // Enable DMA mode
    ADC1->CR2 |= (1U << 1);   // Continuous conversion

    configureDMAForADC();

    ADC1->CR2 |= (1U << 30);  // Start conversion
}
```

---

## ADC with DMA: DMA Channel Setup

```cpp
void configureDMAForADC() {
    enableDMAClock();

    DMA1_Channel1->CPAR = (uint32_t)&ADC1->DR;
    DMA1_Channel1->CMAR = (uint32_t)adcBuffer;
    DMA1_Channel1->CNDTR = sizeof(adcBuffer)/sizeof(uint16_t);

    DMA1_Channel1->CCR = 0;
    DMA1_Channel1->CCR |= (1U << 5);   // Circular mode
    DMA1_Channel1->CCR |= (1U << 7);   // Memory increment
    DMA1_Channel1->CCR |= (1U << 10);  // 16-bit memory size
    DMA1_Channel1->CCR |= (1U << 8);   // 16-bit peripheral size
    DMA1_Channel1->CCR |= (1U << 1);   // Transfer complete interrupt

    DMA1_Channel1->CCR |= (1U << 0);
}

void DMA1_Channel1_IRQHandler() {
    if (DMA1->ISR & (1U << 1)) {
        DMA1->IFCR |= (1U << 1);
        conversionComplete = true;
    }
}
```

---

## Serial Peripheral Interface (SPI): Details

SPI provides high-speed synchronous communication:
- **Full duplex**: Simultaneous TX and RX
- **Master/Slave**: One master, multiple slaves
- **Four wires**: MOSI, MISO, SCK, CS/SS
- **High speed**: Typically MHz range

---

## Serial Peripheral Interface (SPI)

![serial_peripheral_interface_spi](svg/courses/embedded/effective-real-time-embedded-c-and-c++/19_peripherals/serial_peripheral_interface_spi.svg)

---

## SPI Configuration: Registers

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
```

---

## SPI Configuration: Master Setup

```cpp
void configureSPIMaster() {
    enableSPIClock();

    SPI1->CR1 = 0;
    SPI1->CR1 |= (1U << 2);   // Master mode
    SPI1->CR1 |= (1U << 1);   // Clock polarity = 0
    SPI1->CR1 |= (0U << 0);   // Clock phase = 0
    SPI1->CR1 |= (3U << 3);   // Baud rate prescaler (/16)
    SPI1->CR1 |= (1U << 9);   // Software slave management
    SPI1->CR1 |= (1U << 8);   // Internal slave select

    SPI1->CR1 |= (0U << 11);  // 8-bit data frame
    SPI1->CR1 |= (0U << 7);   // MSB first

    SPI1->CR1 |= (1U << 6);   // Enable SPI

    configureSPIPins();
}
```

---

## SPI Configuration: Slave Setup

```cpp
void configureSPISlave() {
    enableSPIClock();

    SPI1->CR1 = 0;
    SPI1->CR1 &= ~(1U << 2);  // Slave mode
    SPI1->CR1 |= (1U << 6);   // Enable SPI

    configureSPIPins();
}
```

---

## SPI Data Transfer: Blocking

Transmitting and receiving SPI data:

```cpp
uint8_t spiTransferByte(uint8_t data) {
    while (!(SPI1->SR & (1U << 1)));
    SPI1->DR = data;
    while (!(SPI1->SR & (1U << 0)));
    return SPI1->DR;
}

void spiTransferBuffer(uint8_t* txBuffer, uint8_t* rxBuffer, uint16_t size) {
    for (uint16_t i = 0; i < size; i++) {
        rxBuffer[i] = spiTransferByte(txBuffer[i]);
    }
}
```

---

## SPI Data Transfer: Chip Select

```cpp
void spiSelectSlave(uint8_t slaveNumber) {
    GPIOA->BSRR = (0xFF << 16);
    GPIOA->BSRR = (1U << slaveNumber);
}

void spiDeselectAll() {
    GPIOA->BSRR = (0xFF << 16);
}

void spiTransaction(uint8_t slave, uint8_t* txData, uint8_t* rxData, uint16_t size) {
    spiSelectSlave(slave);
    spiTransferBuffer(txData, rxData, size);
    spiDeselectAll();
}
```

---

## SPI Data Transfer: Non-Blocking

```cpp
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

## Inter-Integrated Circuit (I2C): Details

I2C provides multi-master, multi-slave communication:
- **Two wires**: SDA (data) and SCL (clock)
- **Addressing**: 7-bit or 10-bit slave addresses
- **Open drain**: Requires pull-up resistors
- **Arbitration**: Multiple masters can coexist

---

## Inter-Integrated Circuit (I2C)

![inter_integrated_circuit_i2c](svg/courses/embedded/effective-real-time-embedded-c-and-c++/19_peripherals/inter_integrated_circuit_i2c.svg)

---

## I2C Configuration: Registers

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
```

---

## I2C Configuration: Initialization

```cpp
void configureI2C(uint32_t clockSpeed) {
    enableI2CClock();

    I2C1->CR1 |= (1U << 15);
    I2C1->CR1 &= ~(1U << 15);

    uint32_t pclk1 = getAPB1Frequency();
    I2C1->CR2 = (pclk1 / 1000000) & 0x3F;

    if (clockSpeed <= 100000) {
        I2C1->CCR = pclk1 / (clockSpeed * 2);
        I2C1->TRISE = (pclk1 / 1000000) + 1;
    } else {
        I2C1->CCR = pclk1 / (clockSpeed * 3);
        I2C1->CCR |= (1U << 15);
        I2C1->TRISE = ((pclk1 * 300) / 1000000000) + 1;
    }

    I2C1->CR1 |= (1U << 0);

    configureI2CPins();
}
```

---

## I2C Master Operations: Flags

Implementing I2C master functionality:

```cpp
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
```

---

## I2C Master Operations: Start and Address

```cpp
I2CStatus i2cStart() {
    I2C1->CR1 |= (1U << 8);

    uint32_t timeout = 10000;
    while (!(I2C1->SR1 & I2C_FLAG_SB) && timeout--);

    return (timeout > 0) ? I2C_OK : I2C_ERROR_TIMEOUT;
}

I2CStatus i2cSendAddress(uint8_t address, bool read) {
    I2C1->DR = (address << 1) | (read ? 1 : 0);

    uint32_t timeout = 10000;
    while (!(I2C1->SR1 & I2C_FLAG_ADDR) && timeout--);

    if (timeout == 0) return I2C_ERROR_TIMEOUT;

    volatile uint32_t dummy = I2C1->SR1;
    dummy = I2C1->SR2;
    (void)dummy;

    return I2C_OK;
}

void i2cStop() {
    I2C1->CR1 |= (1U << 9);
}
```

---

## I2C Data Transfer: Byte Operations

Reading and writing I2C data:

```cpp
I2CStatus i2cWriteByte(uint8_t data) {
    uint32_t timeout = 10000;
    while (!(I2C1->SR1 & I2C_FLAG_TXE) && timeout--);

    if (timeout == 0) return I2C_ERROR_TIMEOUT;

    I2C1->DR = data;

    timeout = 10000;
    while (!(I2C1->SR1 & I2C_FLAG_BTF) && timeout--);

    return (timeout > 0) ? I2C_OK : I2C_ERROR_TIMEOUT;
}

I2CStatus i2cReadByte(uint8_t* data, bool sendNack) {
    if (sendNack) {
        I2C1->CR1 &= ~(1U << 10);
    } else {
        I2C1->CR1 |= (1U << 10);
    }

    uint32_t timeout = 10000;
    while (!(I2C1->SR1 & I2C_FLAG_RXNE) && timeout--);

    if (timeout == 0) return I2C_ERROR_TIMEOUT;

    *data = I2C1->DR;

    return I2C_OK;
}
```

---

## I2C Data Transfer: High-Level Write

```cpp
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
```

---

## I2C Data Transfer: High-Level Read

```cpp
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

## Direct Memory Access (DMA): Details

DMA enables data transfer without CPU intervention:
- **Memory-to-Memory**: Copy data between memory locations
- **Memory-to-Peripheral**: Send data to peripherals
- **Peripheral-to-Memory**: Receive data from peripherals
- **Circular mode**: Continuous operation for streaming

---

## Direct Memory Access (DMA)

![direct_memory_access_dma](svg/courses/embedded/effective-real-time-embedded-c-and-c++/19_peripherals/direct_memory_access_dma.svg)

---

## DMA Configuration: Registers

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
```

---

## DMA Configuration: Setup Function

```cpp
void configureDMA(uint8_t channel, uint32_t peripheral, uint32_t memory,
                  uint16_t size, uint32_t direction) {
    enableDMAClock();

    DMA_Channel_TypeDef* dmaChannel = getDMAChannel(channel);

    dmaChannel->CCR &= ~(1U << 0);

    dmaChannel->CPAR = peripheral;
    dmaChannel->CMAR = memory;
    dmaChannel->CNDTR = size;

    dmaChannel->CCR = 0;
    dmaChannel->CCR |= direction;
    dmaChannel->CCR |= (1U << 7);
    dmaChannel->CCR |= (1U << 1);
    dmaChannel->CCR |= (1U << 2);

    dmaChannel->CCR |= (1U << 0);
}

#define DMA_DIR_PERIPHERAL_TO_MEMORY  0
#define DMA_DIR_MEMORY_TO_PERIPHERAL  (1U << 4)
#define DMA_DIR_MEMORY_TO_MEMORY      (1U << 14)
```

---

## DMA with Peripherals: UART

Using DMA with UART and SPI:

```cpp
uint8_t txBuffer[100];
volatile bool dmaTransmitComplete = false;

void uartTransmitDMA(uint8_t* data, uint16_t size) {
    memcpy(txBuffer, data, size);

    configureDMA(4, (uint32_t)&UART1->DR, (uint32_t)txBuffer,
                 size, DMA_DIR_MEMORY_TO_PERIPHERAL);

    UART1->CR3 |= (1U << 7);  // DMAT

    dmaTransmitComplete = false;
}
```

---

## DMA with Peripherals: ADC Circular Buffer

```cpp
#define ADC_BUFFER_SIZE 256
uint16_t adcBuffer[ADC_BUFFER_SIZE];
volatile uint16_t adcBufferIndex = 0;

void adcStartDMACircular() {
    DMA1_Channel1->CCR &= ~(1U << 0);

    DMA1_Channel1->CPAR = (uint32_t)&ADC1->DR;
    DMA1_Channel1->CMAR = (uint32_t)adcBuffer;
    DMA1_Channel1->CNDTR = ADC_BUFFER_SIZE;

    DMA1_Channel1->CCR = 0;
    DMA1_Channel1->CCR |= (1U << 5);   // Circular mode
    DMA1_Channel1->CCR |= (1U << 7);   // Memory increment
    DMA1_Channel1->CCR |= (1U << 10);
    DMA1_Channel1->CCR |= (1U << 8);
    DMA1_Channel1->CCR |= (1U << 2);
    DMA1_Channel1->CCR |= (1U << 1);

    DMA1_Channel1->CCR |= (1U << 0);

    ADC1->CR2 |= (1U << 8);
    ADC1->CR2 |= (1U << 1);

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

## Interrupt Service Routines: Timer ISR

Writing efficient interrupt handlers:

```cpp
volatile uint32_t systemTick = 0;
volatile bool timerFlag = false;

void TIM2_IRQHandler() {
    if (TIM2->SR & (1U << 0)) {
        TIM2->SR &= ~(1U << 0);

        systemTick++;
        timerFlag = true;

        if (systemTick % 1000 == 0) {
            GPIOA->ODR ^= (1U << 5);
        }
    }
}
```

---

## Interrupt Service Routines: UART RX ISR

```cpp
#define UART_RX_BUFFER_SIZE 64
volatile uint8_t uartRxBuffer[UART_RX_BUFFER_SIZE];
volatile uint16_t uartRxHead = 0;
volatile uint16_t uartRxTail = 0;

void UART1_IRQHandler() {
    if (UART1->SR & (1U << 5)) {
        uint8_t data = UART1->DR;

        uint16_t nextHead = (uartRxHead + 1) % UART_RX_BUFFER_SIZE;
        if (nextHead != uartRxTail) {
            uartRxBuffer[uartRxHead] = data;
            uartRxHead = nextHead;
        }
    }
}

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

## General Purpose Timers (TIM): Overview

Hardware timers provide precise timing and PWM:

- **Count modes**: Up, down, up/down counting
- **PWM generation**: Variable duty cycle output
- **Input capture**: Measure external signal timing
- **Output compare**: Generate precise timing events

---

## General Purpose Timers: Registers

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
```

---

## General Purpose Timers: Configuration

```cpp
void configureTimer(uint32_t frequency) {
    enableTimerClock();

    uint32_t timerClock = getTimerClockFrequency();
    uint32_t prescaler = (timerClock / frequency) - 1;

    TIM2->PSC = prescaler;
    TIM2->ARR = 999;

    TIM2->DIER |= (1U << 0);

    TIM2->CR1 |= (1U << 0);

    nvicEnableInterrupt(28);
}
```

---

## PWM Generation: Configuration

Creating PWM signals with timers:

```cpp
void configurePWM(uint8_t channel, uint16_t dutyCycle) {
    TIM2->CR1 &= ~(1U << 0);

    TIM2->PSC = 71;
    TIM2->ARR = 999;

    if (channel == 1) {
        TIM2->CCMR1 &= ~(0x7 << 4);
        TIM2->CCMR1 |= (0x6 << 4);
        TIM2->CCMR1 |= (1U << 3);
        TIM2->CCER |= (1U << 0);
        TIM2->CCR1 = dutyCycle;
    }

    TIM2->CR1 |= (1U << 0);

    configurePWMPin(channel);
}
```

---

## PWM Generation: Duty Cycle Control

```cpp
void setPWMDutyCycle(uint8_t channel, uint16_t dutyCycle) {
    switch (channel) {
        case 1: TIM2->CCR1 = dutyCycle; break;
        case 2: TIM2->CCR2 = dutyCycle; break;
        case 3: TIM2->CCR3 = dutyCycle; break;
        case 4: TIM2->CCR4 = dutyCycle; break;
    }
}

uint16_t percentageToCounts(float percentage, uint16_t maxCounts) {
    if (percentage > 100.0f) percentage = 100.0f;
    if (percentage < 0.0f) percentage = 0.0f;
    return (uint16_t)(percentage * maxCounts / 100.0f);
}
```

---

## System Tick Timer (SysTick): Overview

SysTick provides system timing for RTOS and delays:

- **24-bit counter**: Counts down from reload value
- **System clock**: Derives from CPU clock
- **RTOS support**: Common timebase for task scheduling
- **Delay functions**: Precise timing delays

---

## System Tick Timer: Configuration

```cpp
#define SYSTICK_CSR   ((volatile uint32_t*)0xE000E010)
#define SYSTICK_RVR   ((volatile uint32_t*)0xE000E014)
#define SYSTICK_CVR   ((volatile uint32_t*)0xE000E018)

volatile uint32_t sysTickCounter = 0;

void configureSysTick(uint32_t frequency) {
    uint32_t systemClock = getSystemClockFrequency();
    uint32_t reloadValue = (systemClock / frequency) - 1;

    *SYSTICK_RVR = reloadValue & 0x00FFFFFF;
    *SYSTICK_CVR = 0;

    *SYSTICK_CSR = 0;
    *SYSTICK_CSR |= (1U << 0);
    *SYSTICK_CSR |= (1U << 1);
    *SYSTICK_CSR |= (1U << 2);
}

void SysTick_Handler() {
    sysTickCounter++;
}
```

---

## System Tick Timer: Delay Functions

```cpp
void delayMs(uint32_t milliseconds) {
    uint32_t startTick = sysTickCounter;
    while ((sysTickCounter - startTick) < milliseconds);
}

uint32_t getSystemTime() {
    return sysTickCounter;
}
```

---

## System Tick Timer: Non-Blocking Timer

```cpp
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

## Peripheral Integration: State Struct

Complete example integrating multiple peripherals:

```cpp
typedef struct {
    uint16_t adcValue;
    float temperature;
    uint8_t pwmDutyCycle;
    bool buttonPressed;
    char displayBuffer[32];
} SystemState_t;

SystemState_t systemState = {0};
```

---

## Peripheral Integration: System Init

```cpp
void initializeSystem() {
    initializeClocks();

    configureGPIO();
    configureSysTick(1000);
    configureADC();
    configurePWM(1, 0);
    configureUART(115200);

    nvicEnableInterrupt(ADC1_2_IRQn);
    nvicEnableInterrupt(UART1_IRQn);

    ADC1->CR2 |= (1U << 0);
}
```

---

## Peripheral Integration: Main Loop

```cpp
void applicationLoop() {
    static Timer_t displayTimer;
    timerStart(&displayTimer, 100);

    while (1) {
        systemState.buttonPressed = readButton();
        systemState.temperature = adcToTemperature(systemState.adcValue);

        if (systemState.temperature > 25.0f) {
            systemState.pwmDutyCycle = 75;
        } else if (systemState.temperature > 20.0f) {
            systemState.pwmDutyCycle = 50;
        } else {
            systemState.pwmDutyCycle = 0;
        }
        setPWMDutyCycle(1, percentageToCounts(systemState.pwmDutyCycle, 999));
```

---

## Peripheral Integration: Display and Button

```cpp
        if (timerExpired(&displayTimer)) {
            snprintf(systemState.displayBuffer, sizeof(systemState.displayBuffer),
                    "Temp: %.1f°C, Fan: %d%%\r\n",
                    systemState.temperature, systemState.pwmDutyCycle);
            uartSendString(systemState.displayBuffer);
            timerStart(&displayTimer, 100);
        }

        if (systemState.buttonPressed) {
            uartSendString("Button pressed!\r\n");
            delayMs(200);
        }

        __WFI();
    }
}
```

---

## Peripheral Integration: Sensor Handlers

```cpp
void ADC1_2_IRQHandler() {
    if (ADC1->SR & (1U << 1)) {
        systemState.adcValue = ADC1->DR;
    }
}

float adcToTemperature(uint16_t adcValue) {
    float voltage = (adcValue * 3.3f) / 4095.0f;
    return (voltage - 0.5f) * 100.0f;
}
```

---

## Power Management: Modes

Optimizing power consumption in embedded systems:

```cpp
typedef enum {
    POWER_RUN,
    POWER_SLEEP,
    POWER_STOP,
    POWER_STANDBY
} PowerMode_t;

void enterLowPowerMode(PowerMode_t mode) {
    switch (mode) {
        case POWER_SLEEP:
            __WFI();
            break;

        case POWER_STOP:
            PWR->CR |= (1U << 0);
            SCB->SCR |= (1U << 2);
            __WFI();
            SCB->SCR &= ~(1U << 2);
            initializeClocks();
            break;
```

---

## Power Management: Standby and Wake-Up

```cpp
        case POWER_STANDBY:
            PWR->CR |= (1U << 2);
            PWR->CR |= (1U << 1);
            SCB->SCR |= (1U << 2);
            __WFI();
            break;

        default:
            break;
    }
}

void configureWakeUpSources() {
    PWR->CSR |= (1U << 8);

    nvicEnableInterrupt(EXTI0_IRQn);
}
```

---

## Error Handling: Error Codes

Robust error handling for peripheral operations:

```cpp
typedef enum {
    PERIPHERAL_OK = 0,
    PERIPHERAL_ERROR_TIMEOUT,
    PERIPHERAL_ERROR_BUSY,
    PERIPHERAL_ERROR_INVALID_PARAM,
    PERIPHERAL_ERROR_HARDWARE_FAULT
} PeripheralError_t;

#define MAX_ERROR_LOG 16
typedef struct {
    uint32_t timestamp;
    PeripheralError_t errorCode;
    uint8_t peripheralId;
    uint32_t errorData;
} ErrorLog_t;

ErrorLog_t errorLog[MAX_ERROR_LOG];
uint8_t errorLogIndex = 0;
```

---

## Error Handling: Log and Timeout

```cpp
void logError(PeripheralError_t error, uint8_t peripheral, uint32_t data) {
    errorLog[errorLogIndex].timestamp = getSystemTime();
    errorLog[errorLogIndex].errorCode = error;
    errorLog[errorLogIndex].peripheralId = peripheral;
    errorLog[errorLogIndex].errorData = data;

    errorLogIndex = (errorLogIndex + 1) % MAX_ERROR_LOG;

    char errorMsg[64];
    snprintf(errorMsg, sizeof(errorMsg),
            "ERROR: P%d, Code:%d, Data:0x%08lX\r\n",
            peripheral, error, data);
    uartSendString(errorMsg);
}

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
```

---

## Error Handling: Fault Detection

```cpp
void checkHardwareFaults() {
    if (RCC->CIR & (1U << 7)) {
        logError(PERIPHERAL_ERROR_HARDWARE_FAULT, 0xFF, RCC->CIR);
    }

    if (UART1->SR & (1U << 3)) {
        logError(PERIPHERAL_ERROR_HARDWARE_FAULT, 1, UART1->SR);
        UART1->SR &= ~(1U << 3);
    }

    if (DMA1->ISR & (1U << 3)) {
        logError(PERIPHERAL_ERROR_HARDWARE_FAULT, 2, DMA1->ISR);
        DMA1->IFCR |= (1U << 3);
    }
}
```

---

## Performance Optimization: GPIO and DMA

Optimizing peripheral performance:

```cpp
void gpioSetMultiplePinsOptimized(GPIO_TypeDef* gpio, uint16_t pins) {
    gpio->BSRR = pins;
}

static inline void fastRegisterWrite(volatile uint32_t* reg, uint32_t value) {
    *reg = value;
}

void configureDMAForHighThroughput() {
    DMA1_Channel1->CCR |= (1U << 14);
    DMA1_Channel1->CCR |= (2U << 8);
    DMA1_Channel1->CCR |= (2U << 10);
    DMA1_Channel1->CCR |= (3U << 12);
}
```

---

## Performance Optimization: ISR and Critical Sections

```cpp
void optimizedInterruptHandler() {
    static uint32_t counter = 0;

    TIM2->SR &= ~(1U << 0);

    counter++;

    timerFlag = true;
}

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

## Debugging: Debug Macros

Tools and techniques for peripheral debugging:

```cpp
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

void dumpGPIORegisters(GPIO_TypeDef* gpio) {
    DEBUG_PRINT("GPIO Registers:");
    DEBUG_PRINT("MODER:   0x%08lX", gpio->MODER);
    DEBUG_PRINT("OTYPER:  0x%08lX", gpio->OTYPER);
    DEBUG_PRINT("OSPEEDR: 0x%08lX", gpio->OSPEEDR);
    DEBUG_PRINT("PUPDR:   0x%08lX", gpio->PUPDR);
    DEBUG_PRINT("IDR:     0x%08lX", gpio->IDR);
    DEBUG_PRINT("ODR:     0x%08lX", gpio->ODR);
}
```

---

## Debugging: Performance and Self-Test

```cpp
uint32_t measureFunctionTime(void (*func)(void)) {
    uint32_t startTime = *SYSTICK_CVR;
    func();
    uint32_t endTime = *SYSTICK_CVR;

    return (startTime > endTime) ? (startTime - endTime) :
                                  (startTime + (*SYSTICK_RVR - endTime));
}

bool testUARTLoopback() {
    const char testString[] = "TEST";
    bool result = true;

    for (int i = 0; testString[i]; i++) {
        uartSendByte(testString[i]);
    }

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
```

---

## Debugging: Health Monitoring

```cpp
typedef struct {
    uint32_t operationCount;
    uint32_t errorCount;
    uint32_t lastErrorTime;
} PeripheralHealth_t;

PeripheralHealth_t peripheralHealth[8];

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

## Best Practices Summary: Principles

Key principles for effective peripheral programming:

1. 1. **Initialize peripherals in correct order**
    - Clocks first, then GPIO, then complex peripherals
1. 1. **Use appropriate data types**
    - volatile for hardware registers
    - const for configuration data
1. 1. **Handle errors gracefully**
    - Check return values and status flags
    - Implement timeout mechanisms
1. 1. **Optimize for your application**
    - Use DMA for high-throughput applications
    - Use interrupts for real-time response

---

## Best Practices Summary: ISRs, Documentation, Testing, Power

1. 1. **Keep interrupt handlers short**
    - Minimal processing in ISRs
    - Use flags for main loop processing
1. 1. **Document hardware dependencies**
    - Pin assignments and alternate functions
    - Timing requirements and constraints
1. 1. **Test thoroughly**
    - Unit tests for individual peripherals
    - Integration tests for complete systems
1. 1. **Consider power consumption**
    - Disable unused peripherals
    - Use appropriate low-power modes

---

## Best Practices Summary: Example Init

```cpp
void initializePeripheralsCorrectly() {
    enableSystemClocks();

    configureGPIO();
    configureSysTick(1000);

    configureUART(115200);
    configureSPI();
    configureI2C(100000);

    configureADC();
    configureDMA();
    configureTimers();

    nvicEnableInterrupt(UART1_IRQn);
    nvicEnableInterrupt(ADC1_2_IRQn);
    nvicEnableInterrupt(TIM2_IRQn);

    startPeripheralOperations();
}
```

---

## Timer Peripheral Modes

![timer_peripheral_modes](svg/courses/embedded/effective-real-time-embedded-c-and-c++/19_peripherals/timer_peripheral_modes.svg)
