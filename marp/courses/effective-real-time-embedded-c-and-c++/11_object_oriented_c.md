# Object Oriented C

---

## Chapter Overview

1. Implementing OOP concepts in C
1. Encapsulation and data hiding
1. Polymorphism through function pointers
1. Inheritance patterns in C
1. Mixing C and C++ code

---

## Why OOP in C?

<svg width="400" height="250" xmlns="http://www.w3.org/2000/svg">
  <text x="200" y="30" text-anchor="middle" font-size="18" font-weight="bold">OOP Benefits in Embedded C</text>
  <rect x="50" y="60" width="150" height="40" fill="#ffcccc" stroke="#333"/>
  <text x="125" y="85" text-anchor="middle" font-size="14">Code Reuse</text>
  <rect x="220" y="60" width="150" height="40" fill="#ccffcc" stroke="#333"/>
  <text x="295" y="85" text-anchor="middle" font-size="14">Modularity</text>
  <rect x="50" y="120" width="150" height="40" fill="#ccccff" stroke="#333"/>
  <text x="125" y="145" text-anchor="middle" font-size="14">Maintainability</text>
  <rect x="220" y="120" width="150" height="40" fill="#ffffcc" stroke="#333"/>
  <text x="295" y="145" text-anchor="middle" font-size="14">Abstraction</text>
  <text x="200" y="200" text-anchor="middle" font-size="14">Without C++ overhead!</text>
</svg>

---

## Basic Object Structure

```c
// Object-oriented LED driver
typedef struct {
    // Private data (by convention)
    GPIO_TypeDef* _port;
    uint16_t _pin;
    bool _active_low;

    // Public methods (function pointers)
    void (*on)(struct led_t* self);
    void (*off)(struct led_t* self);
    void (*toggle)(struct led_t* self);
    bool (*is_on)(const struct led_t* self);
} led_t;

// Method implementations
static void led_on(led_t* self) {
    if (self->_active_low) {
        self->_port->ODR &= ~self->_pin;
    } else {
        self->_port->ODR |= self->_pin;
    }
}

static void led_off(led_t* self) {
    if (self->_active_low) {
        self->_port->ODR |= self->_pin;
    } else {
        self->_port->ODR &= ~self->_pin;
    }
}
```

---

## Constructor Pattern

```c
// Constructor function
led_t* led_create(GPIO_TypeDef* port, uint16_t pin, bool active_low) {
    led_t* led = malloc(sizeof(led_t));
    if (!led) return NULL;

    // Initialize private data
    led->_port = port;
    led->_pin = pin;
    led->_active_low = active_low;

    // Bind methods
    led->on = led_on;
    led->off = led_off;
    led->toggle = led_toggle;
    led->is_on = led_is_on;

    // Configure hardware
    gpio_set_mode(port, pin, GPIO_MODE_OUTPUT);
    led->off(led);  // Start in off state

    return led;
}

// Destructor
void led_destroy(led_t* led) {
    if (led) {
        led->off(led);  // Clean shutdown
        free(led);
    }
}
```

---

## Static Allocation Alternative

```c
// Stack-allocated objects
typedef struct {
    // Same private data
    GPIO_TypeDef* _port;
    uint16_t _pin;
    bool _active_low;
} led_data_t;

// Methods take data pointer
void led_init(led_data_t* led, GPIO_TypeDef* port,
              uint16_t pin, bool active_low) {
    led->_port = port;
    led->_pin = pin;
    led->_active_low = active_low;

    gpio_set_mode(port, pin, GPIO_MODE_OUTPUT);
    led_off(led);
}

// Usage
led_data_t status_led;
led_init(&status_led, GPIOA, GPIO_PIN_5, false);
led_on(&status_led);
```

---

## Encapsulation with Opaque Pointers

```c
// In header file (public interface)
typedef struct uart_handle uart_t;  // Opaque type

// Public API
uart_t* uart_create(uint32_t baud_rate);
void uart_destroy(uart_t* uart);
void uart_send(uart_t* uart, const uint8_t* data, size_t len);
size_t uart_receive(uart_t* uart, uint8_t* buffer, size_t max_len);

// In source file (private implementation)
struct uart_handle {
    USART_TypeDef* periph;
    uint32_t baud_rate;
    ring_buffer_t tx_buffer;
    ring_buffer_t rx_buffer;
    // Private members not visible to users
};

uart_t* uart_create(uint32_t baud_rate) {
    uart_t* uart = malloc(sizeof(struct uart_handle));
    // Initialize private members...
    return uart;
}
```

---

## Inheritance in C

```c
// Base "class"
typedef struct {
    uint32_t id;
    char name[32];
    void (*update)(struct sensor_t* self);
    float (*read)(struct sensor_t* self);
} sensor_t;

// Derived "class" - temperature sensor
typedef struct {
    sensor_t base;  // Must be first member!

    // Additional members
    float offset;
    float scale;
    ADC_TypeDef* adc;
    uint8_t channel;
} temp_sensor_t;

// "Override" methods
static float temp_sensor_read(sensor_t* self) {
    temp_sensor_t* temp = (temp_sensor_t*)self;

    uint16_t raw = adc_read(temp->adc, temp->channel);
    return (raw * temp->scale) + temp->offset;
}

// Constructor
temp_sensor_t* temp_sensor_create(uint32_t id, const char* name,
                                  ADC_TypeDef* adc, uint8_t ch) {
    temp_sensor_t* temp = malloc(sizeof(temp_sensor_t));

    // Initialize base
    temp->base.id = id;
    strncpy(temp->base.name, name, sizeof(temp->base.name));
    temp->base.read = temp_sensor_read;

    // Initialize derived
    temp->adc = adc;
    temp->channel = ch;

    return temp;
}
```

---

## Polymorphism Example

```c
// Generic sensor interface
void process_sensor(sensor_t* sensor) {
    printf("Reading %s: ", sensor->name);
    float value = sensor->read(sensor);  // Polymorphic call
    printf("%.2f\n", value);
}

// Usage with different sensor types
temp_sensor_t* temp1 = temp_sensor_create(1, "CPU Temp", ADC1, 0);
pressure_sensor_t* pres1 = pressure_sensor_create(2, "Pressure", SPI1);

// Polymorphic usage
process_sensor((sensor_t*)temp1);  // Calls temp_sensor_read
process_sensor((sensor_t*)pres1);  // Calls pressure_sensor_read

// Array of different sensors
sensor_t* sensors[] = {
    (sensor_t*)temp1,
    (sensor_t*)pres1,
    // More sensors...
};

for (int i = 0; i < NUM_SENSORS; i++) {
    sensors[i]->update(sensors[i]);
}
```

---

## Virtual Function Table Pattern

```c
// Method table for polymorphism
typedef struct {
    void (*start)(void* self);
    void (*stop)(void* self);
    void (*process)(void* self, const uint8_t* data, size_t len);
    const char* (*get_name)(void* self);
} protocol_vtable_t;

// Base protocol structure
typedef struct {
    const protocol_vtable_t* vtable;
    // Common data
    uint8_t id;
    bool active;
} protocol_t;

// UART protocol implementation
typedef struct {
    protocol_t base;
    USART_TypeDef* uart;
    uint32_t baud_rate;
} uart_protocol_t;

// UART method implementations
static void uart_start(void* self) {
    uart_protocol_t* uart = (uart_protocol_t*)self;
    // Initialize UART...
}

static const protocol_vtable_t uart_vtable = {
    .start = uart_start,
    .stop = uart_stop,
    .process = uart_process,
    .get_name = uart_get_name
};

// Constructor
uart_protocol_t* uart_protocol_create(USART_TypeDef* uart) {
    uart_protocol_t* protocol = malloc(sizeof(uart_protocol_t));
    protocol->base.vtable = &uart_vtable;
    protocol->uart = uart;
    return protocol;
}
```

---

## Using Virtual Functions

```c
// Generic protocol handler
void protocol_handler(protocol_t* protocol,
                     const uint8_t* data, size_t len) {
    if (!protocol->active) {
        protocol->vtable->start(protocol);
        protocol->active = true;
    }

    protocol->vtable->process(protocol, data, len);
}

// Usage
uart_protocol_t* uart_proto = uart_protocol_create(USART1);
spi_protocol_t* spi_proto = spi_protocol_create(SPI1);

// Polymorphic usage
protocol_handler((protocol_t*)uart_proto, data1, len1);
protocol_handler((protocol_t*)spi_proto, data2, len2);

// Get protocol info
printf("Protocol: %s\n",
       ((protocol_t*)uart_proto)->vtable->get_name(uart_proto));
```

---

## Composition Over Inheritance

```c
// Component interfaces
typedef struct {
    void (*send)(void* self, uint8_t byte);
    uint8_t (*receive)(void* self);
} serial_interface_t;

typedef struct {
    void (*write)(void* self, uint32_t addr, uint8_t value);
    uint8_t (*read)(void* self, uint32_t addr);
} memory_interface_t;

// Device with multiple interfaces
typedef struct {
    // Composition - has-a relationship
    serial_interface_t* serial;
    memory_interface_t* memory;

    // Device-specific data
    uint32_t device_id;
    char model[16];
} device_t;

// Create device with specific implementations
device_t* create_device(serial_interface_t* serial,
                       memory_interface_t* memory) {
    device_t* dev = malloc(sizeof(device_t));
    dev->serial = serial;
    dev->memory = memory;
    return dev;
}

// Use composed functionality
void device_operation(device_t* dev) {
    uint8_t config = dev->memory->read(dev->memory, 0x00);
    dev->serial->send(dev->serial, config);
}
```

---

## Interface Segregation

```c
// Separate interfaces for different capabilities
typedef struct {
    float (*read)(void* self);
} readable_t;

typedef struct {
    void (*write)(void* self, float value);
} writable_t;

typedef struct {
    void (*calibrate)(void* self);
} calibratable_t;

// Sensor that implements multiple interfaces
typedef struct {
    // Interface pointers
    readable_t readable;
    calibratable_t calibratable;

    // Private data
    float value;
    float offset;
} sensor_impl_t;

// Cast to specific interface
readable_t* get_readable(sensor_impl_t* sensor) {
    return &sensor->readable;
}

// Use only needed interface
float read_value(readable_t* readable) {
    return readable->read(readable);
}
```

---

## Factory Pattern

```c
// Device types
typedef enum {
    DEVICE_TYPE_UART,
    DEVICE_TYPE_SPI,
    DEVICE_TYPE_I2C
} device_type_t;

// Factory function
protocol_t* protocol_factory(device_type_t type, void* config) {
    switch (type) {
    case DEVICE_TYPE_UART: {
        uart_config_t* cfg = (uart_config_t*)config;
        return (protocol_t*)uart_protocol_create(cfg->uart,
                                                 cfg->baud_rate);
    }

    case DEVICE_TYPE_SPI: {
        spi_config_t* cfg = (spi_config_t*)config;
        return (protocol_t*)spi_protocol_create(cfg->spi,
                                               cfg->speed);
    }

    case DEVICE_TYPE_I2C: {
        i2c_config_t* cfg = (i2c_config_t*)config;
        return (protocol_t*)i2c_protocol_create(cfg->i2c,
                                               cfg->address);
    }

    default:
        return NULL;
    }
}
```

---

## Singleton Pattern

```c
// Logger singleton
typedef struct {
    void (*log)(const char* message);
    void (*set_level)(int level);
    int level;
    // Private data...
} logger_t;

// Static instance
static logger_t* logger_instance = NULL;

// Get singleton instance
logger_t* logger_get_instance(void) {
    if (!logger_instance) {
        logger_instance = malloc(sizeof(logger_t));
        logger_instance->log = logger_log_impl;
        logger_instance->set_level = logger_set_level_impl;
        logger_instance->level = LOG_INFO;
        // Initialize...
    }
    return logger_instance;
}

// Usage
#define LOG(msg) logger_get_instance()->log(msg)

void application(void) {
    LOG("Application started");
    // ...
}
```

---

## Observer Pattern

```c
// Observer interface
typedef struct {
    void (*notify)(void* self, uint32_t event, void* data);
} observer_t;

// Subject that can be observed
typedef struct {
    observer_t* observers[MAX_OBSERVERS];
    size_t observer_count;
} subject_t;

void subject_attach(subject_t* subject, observer_t* observer) {
    if (subject->observer_count < MAX_OBSERVERS) {
        subject->observers[subject->observer_count++] = observer;
    }
}

void subject_notify(subject_t* subject, uint32_t event, void* data) {
    for (size_t i = 0; i < subject->observer_count; i++) {
        subject->observers[i]->notify(subject->observers[i],
                                     event, data);
    }
}

// Temperature sensor with observers
typedef struct {
    subject_t subject;
    float temperature;
} temp_monitor_t;

void temp_monitor_update(temp_monitor_t* monitor, float temp) {
    monitor->temperature = temp;
    subject_notify(&monitor->subject, EVENT_TEMP_CHANGE, &temp);
}
```

---

## State Pattern

```c
// State interface
typedef struct state_t state_t;
struct state_t {
    void (*enter)(state_t* self, void* context);
    void (*exit)(state_t* self, void* context);
    state_t* (*update)(state_t* self, void* context);
    const char* name;
};

// Concrete states
static state_t* idle_update(state_t* self, void* context) {
    system_t* sys = (system_t*)context;
    if (sys->start_requested) {
        return &running_state;
    }
    return self;  // Stay in idle
}

static state_t idle_state = {
    .enter = idle_enter,
    .exit = idle_exit,
    .update = idle_update,
    .name = "IDLE"
};

// State machine
typedef struct {
    state_t* current_state;
    // Context data
} state_machine_t;

void state_machine_update(state_machine_t* sm) {
    state_t* new_state = sm->current_state->update(sm->current_state, sm);

    if (new_state != sm->current_state) {
        sm->current_state->exit(sm->current_state, sm);
        new_state->enter(new_state, sm);
        sm->current_state = new_state;
    }
}
```

---

## Method Chaining

```c
// Builder pattern with chaining
typedef struct {
    uint32_t baud_rate;
    uint8_t data_bits;
    uint8_t stop_bits;
    char parity;

    // Methods return self for chaining
    struct uart_config_t* (*set_baud)(struct uart_config_t* self, uint32_t baud);
    struct uart_config_t* (*set_format)(struct uart_config_t* self,
                                        uint8_t data, uint8_t stop, char parity);
    void (*apply)(struct uart_config_t* self, USART_TypeDef* uart);
} uart_config_t;

// Method implementations
static uart_config_t* set_baud(uart_config_t* self, uint32_t baud) {
    self->baud_rate = baud;
    return self;  // Enable chaining
}

// Usage with method chaining
uart_config_t config;
uart_config_init(&config);

config.set_baud(&config, 115200)
      ->set_format(&config, 8, 1, 'N')
      ->apply(&config, USART1);
```

---

## Error Handling in OOP C

```c
// Result type pattern
typedef enum {
    RESULT_OK,
    RESULT_ERROR_NULL_PTR,
    RESULT_ERROR_INVALID_PARAM,
    RESULT_ERROR_TIMEOUT,
    RESULT_ERROR_BUSY
} result_t;

// Methods return results
typedef struct {
    result_t (*open)(void* self);
    result_t (*close)(void* self);
    result_t (*read)(void* self, uint8_t* buffer, size_t* len);
    result_t (*write)(void* self, const uint8_t* data, size_t len);
} io_interface_t;

// Error context
typedef struct {
    result_t last_error;
    const char* error_msg;
    uint32_t error_count;
} error_context_t;

// Object with error handling
typedef struct {
    io_interface_t interface;
    error_context_t error;
    // Other members...
} device_with_error_t;
```

---

## Memory Management Patterns

```c
// Reference counting
typedef struct {
    void* obj;
    size_t ref_count;
    void (*destructor)(void* obj);
} ref_counted_t;

ref_counted_t* ref_create(void* obj, void (*destructor)(void*)) {
    ref_counted_t* ref = malloc(sizeof(ref_counted_t));
    ref->obj = obj;
    ref->ref_count = 1;
    ref->destructor = destructor;
    return ref;
}

void ref_retain(ref_counted_t* ref) {
    ref->ref_count++;
}

void ref_release(ref_counted_t* ref) {
    if (--ref->ref_count == 0) {
        if (ref->destructor) {
            ref->destructor(ref->obj);
        }
        free(ref);
    }
}

// Smart pointer wrapper
#define SMART_PTR(type) \
    struct { \
        type* ptr; \
        ref_counted_t* ref; \
    }
```

---

## Mixing C and C++

```c
// C header with C++ guards
#ifdef __cplusplus
extern "C" {
#endif

// C interface
typedef struct device device_t;

device_t* device_create(const char* name);
void device_destroy(device_t* dev);
void device_process(device_t* dev);

#ifdef __cplusplus
}
#endif

// C++ implementation
#ifdef __cplusplus
class DeviceImpl {
private:
    std::string name;

public:
    DeviceImpl(const char* n) : name(n) {}
    void process() { /* C++ implementation */ }
};

extern "C" {
    struct device {
        DeviceImpl* impl;
    };

    device_t* device_create(const char* name) {
        device_t* dev = (device_t*)malloc(sizeof(device_t));
        dev->impl = new DeviceImpl(name);
        return dev;
    }

    void device_process(device_t* dev) {
        dev->impl->process();
    }
}
#endif
```

---

## Name Mangling Issues

```c
// Prevent C++ name mangling for C functions
#ifdef __cplusplus
extern "C" {
#endif

// These functions keep C linkage
void uart_init(void);
void uart_send(uint8_t data);
uint8_t uart_receive(void);

#ifdef __cplusplus
}
#endif

// C++ wrapper class
#ifdef __cplusplus
class UartWrapper {
public:
    UartWrapper() { uart_init(); }
    void send(uint8_t data) { uart_send(data); }
    uint8_t receive() { return uart_receive(); }
};
#endif
```

---

## Type Safety in OOP C

```c
// Type-safe handles
#define DECLARE_HANDLE(name) \
    typedef struct name##_handle_t* name##_t

DECLARE_HANDLE(file);
DECLARE_HANDLE(socket);
DECLARE_HANDLE(mutex);

// Now file_t, socket_t, mutex_t are distinct types

// Type checking at compile time
file_t file = file_open("data.txt");
socket_t sock = socket_create();

// This would cause compilation error:
// file_write(sock, data, len);  // Type mismatch!

// Correct usage
file_write(file, data, len);
socket_send(sock, data, len);
```

---

## Performance Considerations

```c
// Static dispatch vs dynamic dispatch
// Static - resolved at compile time
static inline void led_on_static(led_t* led) {
    GPIO_SetBits(led->port, led->pin);
}

// Dynamic - through function pointer
void led_on_dynamic(led_t* led) {
    led->vtable->on(led);  // Extra indirection
}

// Devirtualization for hot paths
#define LED_ON(led) \
    do { \
        if ((led)->type == LED_TYPE_GPIO) { \
            GPIO_SetBits((led)->port, (led)->pin); \
        } else { \
            (led)->vtable->on(led); \
        } \
    } while(0)
```

---

## Best Practices

1. **Consistent naming** - prefix methods with "class" name
1. **Opaque pointers** - hide implementation details
1. **Constructor/destructor** - manage resources properly
1. **Const correctness** - mark read-only methods
1. **Error handling** - return status codes
1. **Documentation** - clear ownership and lifetime

---

## Summary

1. OOP improves code organization in C
1. Function pointers enable polymorphism
1. Careful struct layout enables inheritance
1. Opaque pointers provide encapsulation
1. Patterns from OOP languages can be adapted

---

## Key Takeaways

1. **Structure** creates objects in C
1. **Function pointers** enable methods
1. **First member** inheritance works
1. **Composition** often better than inheritance
1. **C/C++ mixing** requires care

Next: Inheritance and OO Design
