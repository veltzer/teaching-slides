---
tags:
  - infrastructure:linux
  - languages:c
  - concepts:systems-programming
level: advanced
category: operating-systems
audience:
  - audiences:developers
  - audiences:devops

---
# Working with Device Drivers

---

## Everything is a File

1. **UNIX philosophy** - Uniform interface for all I/O
1. **Device files** - Special files representing hardware
1. **Standard operations** - `open()`, `read()`, `write()`, `close()`
1. **Device nodes** - Located in `/dev` directory
1. **Transparent access** - Same API for files and devices

---

## The `/dev` Directory

```bash
# Common device files
/dev/null      # Null device - discards all data
/dev/zero      # Zero device - provides infinite zeros
/dev/random    # Hardware random number generator
/dev/urandom   # Userspace random number generator
/dev/tty       # Current terminal
/dev/stdin     # Standard input
/dev/stdout    # Standard output
/dev/stderr    # Standard error

# Block devices
/dev/sda       # First SCSI/SATA disk
/dev/nvme0n1   # First NVMe device

# Character devices
/dev/ttyS0     # First serial port
/dev/input/    # Input devices (keyboard, mouse)
```

---

## Device File Types

![device_file_types](svg/courses/operating_systems/linux-systems-programming/20_working_with_device_drivers/device_file_types.svg)

---

## Device Numbers

```c
#include <sys/sysmacros.h>
#include <sys/stat.h>

// Device numbers: major + minor
dev_t device_number = makedev(major, minor);
unsigned int major_num = major(device_number);
unsigned int minor_num = minor(device_number);

// Example: checking device type
struct stat st;
stat("/dev/sda", &st);

if (S_ISBLK(st.st_mode)) {
    printf("Block device: major=%u, minor=%u\n",
           major(st.st_rdev), minor(st.st_rdev));
} else if (S_ISCHR(st.st_mode)) {
    printf("Character device: major=%u, minor=%u\n",
           major(st.st_rdev), minor(st.st_rdev));
}
```

1. **Major number** - Device driver type
1. **Minor number** - Specific device instance
1. **Kernel routing** - Major number selects driver

---

## Basic Device Operations

```c
#include <fcntl.h>
#include <unistd.h>

// Open device file
int fd = open("/dev/ttyS0", O_RDWR | O_NOCTTY);
if (fd == -1) {
    perror("open");
    exit(1);
}

// Read from device
char buffer[256];
ssize_t bytes = read(fd, buffer, sizeof(buffer));

// Write to device
const char *message = "Hello device\n";
ssize_t written = write(fd, message, strlen(message));

// Close device
close(fd);
```

---

## The `ioctl()` System Call

```c
#include <sys/ioctl.h>

int ioctl(int fd, unsigned long request, ...);

// Example: Get terminal window size
struct winsize ws;
if (ioctl(STDOUT_FILENO, TIOCGWINSZ, &ws) == 0) {
    printf("Terminal size: %dx%d\n", ws.ws_col, ws.ws_row);
}

// Example: Set serial port parameters
struct termios tio;
tcgetattr(fd, &tio);
tio.c_cflag = B9600 | CS8 | CLOCAL | CREAD;
ioctl(fd, TCSETS, &tio);
```

1. **Device-specific operations** - Beyond read/write/seek
1. **Control interface** - Configure device behavior
1. **Non-standard operations** - Device-dependent functionality

---

## Serial Port Programming

```c
#include <termios.h>

int setup_serial_port(const char *device, int baudrate) {
    int fd = open(device, O_RDWR | O_NOCTTY | O_SYNC);
    if (fd == -1) {
        return -1;
    }

    struct termios tty;
    if (tcgetattr(fd, &tty) != 0) {
        close(fd);
        return -1;
    }

    // Set baud rate
    cfsetospeed(&tty, baudrate);
    cfsetispeed(&tty, baudrate);

    // 8-bit chars
    tty.c_cflag = (tty.c_cflag & ~CSIZE) | CS8;

    // Disable break processing
    tty.c_iflag &= ~IGNBRK;

    // No signaling chars, no echo, no canonical processing
    tty.c_lflag = 0;

    // No remapping, no delays
    tty.c_oflag = 0;

    // Read doesn't block
    tty.c_cc[VMIN] = 0;
    tty.c_cc[VTIME] = 5; // 0.5 second read timeout

    // Make raw
    cfmakeraw(&tty);

    if (tcsetattr(fd, TCSANOW, &tty) != 0) {
        close(fd);
        return -1;
    }

    return fd;
}
```

---

## Serial Communication Example

```c
int serial_communication_example() {
    int fd = setup_serial_port("/dev/ttyUSB0", B115200);
    if (fd == -1) {
        perror("Failed to open serial port");
        return -1;
    }

    // Send command
    const char *command = "AT\r\n";
    write(fd, command, strlen(command));

    // Read response
    char response[256];
    ssize_t bytes = read(fd, response, sizeof(response) - 1);
    if (bytes > 0) {
        response[bytes] = '\0';
        printf("Device response: %s", response);
    }

    close(fd);
    return 0;
}
```

---

## Memory-Mapped Device I/O

```c
#include <sys/mman.h>

// Map device memory into process space
void *map_device_memory(const char *device, size_t size) {
    int fd = open(device, O_RDWR);
    if (fd == -1) {
        return MAP_FAILED;
    }

    void *mapped = mmap(NULL, size, PROT_READ | PROT_WRITE,
                       MAP_SHARED, fd, 0);

    close(fd);
    return mapped;
}

// Example: GPIO memory mapping (Raspberry Pi)
#define GPIO_BASE 0x20200000
#define GPIO_SIZE 0x1000

volatile uint32_t *gpio = map_device_memory("/dev/mem", GPIO_SIZE);
if (gpio != MAP_FAILED) {
    // Direct hardware access
    gpio[GPIO_SET] = 1 << pin_number; // Set GPIO pin
    gpio[GPIO_CLR] = 1 << pin_number; // Clear GPIO pin
}
```

---

## Device Driver Communication

![device_driver_communication](svg/courses/operating_systems/linux-systems-programming/20_working_with_device_drivers/device_driver_communication.svg)

---

## Input Device Handling

```c
#include <linux/input.h>

// Read input events from devices
int read_input_events(const char *device) {
    int fd = open(device, O_RDONLY);
    if (fd == -1) {
        return -1;
    }

    struct input_event ev;
    while (1) {
        ssize_t bytes = read(fd, &ev, sizeof(ev));
        if (bytes == sizeof(ev)) {
            printf("Event: type=%d code=%d value=%d\n",
                   ev.type, ev.code, ev.value);

            switch (ev.type) {
                case EV_KEY:
                    printf("Key %s: %d\n",
                           ev.value ? "pressed" : "released", ev.code);
                    break;
                case EV_REL:
                    printf("Relative movement: axis=%d value=%d\n",
                           ev.code, ev.value);
                    break;
                case EV_ABS:
                    printf("Absolute position: axis=%d value=%d\n",
                           ev.code, ev.value);
                    break;
            }
        }
    }

    close(fd);
    return 0;
}
```

---

## Network Interface Control

```c
#include <sys/socket.h>
#include <linux/if.h>
#include <linux/sockios.h>

// Get network interface information
int get_interface_info(const char *ifname) {
    int fd = socket(AF_INET, SOCK_DGRAM, 0);
    if (fd == -1) {
        return -1;
    }

    struct ifreq ifr;
    strncpy(ifr.ifr_name, ifname, IFNAMSIZ - 1);

    // Get interface flags
    if (ioctl(fd, SIOCGIFFLAGS, &ifr) == 0) {
        printf("Interface %s: %s\n", ifname,
               (ifr.ifr_flags & IFF_UP) ? "UP" : "DOWN");
    }

    // Get MAC address
    if (ioctl(fd, SIOCGIFHWADDR, &ifr) == 0) {
        unsigned char *mac = (unsigned char*)ifr.ifr_hwaddr.sa_data;
        printf("MAC: %02x:%02x:%02x:%02x:%02x:%02x\n",
               mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);
    }

    // Get IP address
    if (ioctl(fd, SIOCGIFADDR, &ifr) == 0) {
        struct sockaddr_in *addr = (struct sockaddr_in*)&ifr.ifr_addr;
        printf("IP: %s\n", inet_ntoa(addr->sin_addr));
    }

    close(fd);
    return 0;
}
```

---

## Framebuffer Programming

```c
#include <linux/fb.h>

struct framebuffer {
    int fd;
    void *mapped;
    struct fb_var_screeninfo vinfo;
    struct fb_fix_screeninfo finfo;
    size_t screensize;
};

struct framebuffer *open_framebuffer(const char *device) {
    struct framebuffer *fb = malloc(sizeof(*fb));

    fb->fd = open(device, O_RDWR);
    if (fb->fd == -1) {
        free(fb);
        return NULL;
    }

    // Get fixed screen info
    ioctl(fb->fd, FBIOGET_FSCREENINFO, &fb->finfo);

    // Get variable screen info
    ioctl(fb->fd, FBIOGET_VSCREENINFO, &fb->vinfo);

    // Calculate screen size
    fb->screensize = fb->vinfo.xres * fb->vinfo.yres *
                     fb->vinfo.bits_per_pixel / 8;

    // Map framebuffer to memory
    fb->mapped = mmap(NULL, fb->screensize, PROT_READ | PROT_WRITE,
                      MAP_SHARED, fb->fd, 0);

    if (fb->mapped == MAP_FAILED) {
        close(fb->fd);
        free(fb);
        return NULL;
    }

    return fb;
}

void draw_pixel(struct framebuffer *fb, int x, int y, uint32_t color) {
    if (x < 0 || x >= fb->vinfo.xres || y < 0 || y >= fb->vinfo.yres) {
        return;
    }

    uint32_t *pixel = (uint32_t*)fb->mapped;
    pixel[y * fb->vinfo.xres + x] = color;
}
```

---

## V4L2 Video Device Programming

```c
#include <linux/videodev2.h>

// Video4Linux2 device handling
int setup_video_device(const char *device) {
    int fd = open(device, O_RDWR);
    if (fd == -1) {
        return -1;
    }

    // Query device capabilities
    struct v4l2_capability cap;
    if (ioctl(fd, VIDIOC_QUERYCAP, &cap) == -1) {
        close(fd);
        return -1;
    }

    printf("Device: %s\n", cap.card);
    printf("Driver: %s\n", cap.driver);

    if (!(cap.capabilities & V4L2_CAP_VIDEO_CAPTURE)) {
        printf("Device does not support video capture\n");
        close(fd);
        return -1;
    }

    // Set video format
    struct v4l2_format fmt = {0};
    fmt.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
    fmt.fmt.pix.width = 640;
    fmt.fmt.pix.height = 480;
    fmt.fmt.pix.pixelformat = V4L2_PIX_FMT_RGB24;
    fmt.fmt.pix.field = V4L2_FIELD_INTERLACED;

    if (ioctl(fd, VIDIOC_S_FMT, &fmt) == -1) {
        perror("Setting format");
        close(fd);
        return -1;
    }

    return fd;
}
```

---

## Sound Device Programming

```c
#include <sys/soundcard.h>

// Open and configure sound device
int setup_audio_device(const char *device, int rate, int channels) {
    int fd = open(device, O_WRONLY);
    if (fd == -1) {
        return -1;
    }

    // Set audio format
    int format = AFMT_S16_LE; // 16-bit little endian
    if (ioctl(fd, SNDCTL_DSP_SETFMT, &format) == -1) {
        close(fd);
        return -1;
    }

    // Set number of channels
    if (ioctl(fd, SNDCTL_DSP_CHANNELS, &channels) == -1) {
        close(fd);
        return -1;
    }

    // Set sample rate
    if (ioctl(fd, SNDCTL_DSP_SPEED, &rate) == -1) {
        close(fd);
        return -1;
    }

    return fd;
}

// Play audio data
int play_audio(int fd, const int16_t *samples, size_t count) {
    size_t bytes_to_write = count * sizeof(int16_t);
    ssize_t written = write(fd, samples, bytes_to_write);
    return written == bytes_to_write ? 0 : -1;
}
```

---

## GPIO Control

```c
// GPIO control through sysfs interface
int gpio_export(int pin) {
    int fd = open("/sys/class/gpio/export", O_WRONLY);
    if (fd == -1) {
        return -1;
    }

    char buffer[16];
    snprintf(buffer, sizeof(buffer), "%d", pin);
    write(fd, buffer, strlen(buffer));
    close(fd);

    return 0;
}

int gpio_set_direction(int pin, const char *direction) {
    char path[64];
    snprintf(path, sizeof(path), "/sys/class/gpio/gpio%d/direction", pin);

    int fd = open(path, O_WRONLY);
    if (fd == -1) {
        return -1;
    }

    write(fd, direction, strlen(direction));
    close(fd);

    return 0;
}

int gpio_write(int pin, int value) {
    char path[64];
    snprintf(path, sizeof(path), "/sys/class/gpio/gpio%d/value", pin);

    int fd = open(path, O_WRONLY);
    if (fd == -1) {
        return -1;
    }

    char buffer[2];
    snprintf(buffer, sizeof(buffer), "%d", value);
    write(fd, buffer, 1);
    close(fd);

    return 0;
}
```

---

## I2C Device Communication

```c
#include <linux/i2c-dev.h>
#include <i2c/smbus.h>

// I2C device communication
int i2c_open_device(const char *device, uint8_t slave_addr) {
    int fd = open(device, O_RDWR);
    if (fd == -1) {
        return -1;
    }

    if (ioctl(fd, I2C_SLAVE, slave_addr) < 0) {
        close(fd);
        return -1;
    }

    return fd;
}

// Read byte from I2C device register
int i2c_read_byte(int fd, uint8_t reg) {
    return i2c_smbus_read_byte_data(fd, reg);
}

// Write byte to I2C device register
int i2c_write_byte(int fd, uint8_t reg, uint8_t value) {
    return i2c_smbus_write_byte_data(fd, reg, value);
}

// Example: Read temperature from I2C sensor
float read_temperature_sensor(const char *device, uint8_t addr) {
    int fd = i2c_open_device(device, addr);
    if (fd == -1) {
        return -1.0f;
    }

    // Read temperature registers (example for common sensor)
    int temp_high = i2c_read_byte(fd, 0x00);
    int temp_low = i2c_read_byte(fd, 0x01);

    close(fd);

    if (temp_high < 0 || temp_low < 0) {
        return -1.0f;
    }

    // Convert to temperature (sensor-specific calculation)
    int16_t temp_raw = (temp_high << 8) | temp_low;
    return temp_raw / 256.0f;
}
```

---

## SPI Device Communication

```c
#include <linux/spi/spidev.h>

struct spi_device {
    int fd;
    uint8_t mode;
    uint8_t bits_per_word;
    uint32_t speed;
};

struct spi_device *spi_open(const char *device) {
    struct spi_device *spi = malloc(sizeof(*spi));

    spi->fd = open(device, O_RDWR);
    if (spi->fd == -1) {
        free(spi);
        return NULL;
    }

    // Set SPI parameters
    spi->mode = SPI_MODE_0;
    spi->bits_per_word = 8;
    spi->speed = 500000; // 500kHz

    ioctl(spi->fd, SPI_IOC_WR_MODE, &spi->mode);
    ioctl(spi->fd, SPI_IOC_WR_BITS_PER_WORD, &spi->bits_per_word);
    ioctl(spi->fd, SPI_IOC_WR_MAX_SPEED_HZ, &spi->speed);

    return spi;
}

int spi_transfer(struct spi_device *spi, uint8_t *tx_buf,
                uint8_t *rx_buf, size_t len) {
    struct spi_ioc_transfer tr = {
        .tx_buf = (unsigned long)tx_buf,
        .rx_buf = (unsigned long)rx_buf,
        .len = len,
        .speed_hz = spi->speed,
        .bits_per_word = spi->bits_per_word,
    };

    return ioctl(spi->fd, SPI_IOC_MESSAGE(1), &tr);
}
```

---

## USB Device Handling

```c
#include <libudev.h>

// Monitor USB device events
void monitor_usb_devices() {
    struct udev *udev = udev_new();
    if (!udev) {
        return;
    }

    struct udev_monitor *mon = udev_monitor_new_from_netlink(udev, "udev");
    udev_monitor_filter_add_match_subsystem_devtype(mon, "usb", NULL);
    udev_monitor_enable_receiving(mon);

    int fd = udev_monitor_get_fd(mon);

    while (1) {
        fd_set fds;
        FD_ZERO(&fds);
        FD_SET(fd, &fds);

        int ret = select(fd + 1, &fds, NULL, NULL, NULL);
        if (ret > 0 && FD_ISSET(fd, &fds)) {
            struct udev_device *dev = udev_monitor_receive_device(mon);
            if (dev) {
                const char *action = udev_device_get_action(dev);
                const char *devnode = udev_device_get_devnode(dev);

                printf("USB device %s: %s\n", action,
                       devnode ? devnode : "unknown");

                udev_device_unref(dev);
            }
        }
    }

    udev_monitor_unref(mon);
    udev_unref(udev);
}
```

---

## Interrupt Handling

```c
// Handle device interrupts using signalfd
#include <sys/signalfd.h>

int setup_signal_handling() {
    sigset_t mask;
    sigemptyset(&mask);
    sigaddset(&mask, SIGIO); // I/O signal

    // Block signal for all threads
    pthread_sigmask(SIG_BLOCK, &mask, NULL);

    // Create signalfd
    int sfd = signalfd(-1, &mask, SFD_CLOEXEC);
    return sfd;
}

void handle_device_interrupts(int signal_fd, int device_fd) {
    // Enable async I/O on device
    fcntl(device_fd, F_SETOWN, getpid());
    fcntl(device_fd, F_SETFL, fcntl(device_fd, F_GETFL) | O_ASYNC);

    struct signalfd_siginfo si;
    while (1) {
        ssize_t s = read(signal_fd, &si, sizeof(si));
        if (s == sizeof(si)) {
            if (si.ssi_signo == SIGIO) {
                printf("Device interrupt received\n");
                handle_device_ready(device_fd);
            }
        }
    }
}
```

---

## Device Performance Optimization

```c
// Optimize device I/O performance
int optimize_device_io(int fd) {
    // Disable system buffering
    fcntl(fd, F_SETFL, O_DIRECT);

    // Set I/O scheduler
    char scheduler_path[256];
    snprintf(scheduler_path, sizeof(scheduler_path),
             "/sys/block/%s/queue/scheduler", get_device_name(fd));

    int sched_fd = open(scheduler_path, O_WRONLY);
    if (sched_fd != -1) {
        write(sched_fd, "noop", 4); // Use noop scheduler
        close(sched_fd);
    }

    // Set read-ahead
    posix_fadvise(fd, 0, 0, POSIX_FADV_SEQUENTIAL);

    return 0;
}

// Use aligned buffers for device I/O
void *allocate_device_buffer(size_t size) {
    void *buffer;
    if (posix_memalign(&buffer, 4096, size) != 0) {
        return NULL;
    }

    // Lock buffer in memory
    mlock(buffer, size);

    return buffer;
}
```

---

## Error Handling and Recovery

```c
// Robust device error handling
int robust_device_operation(int fd, void *buffer, size_t size) {
    int retry_count = 0;
    const int max_retries = 3;

    while (retry_count < max_retries) {
        ssize_t result = read(fd, buffer, size);

        if (result == size) {
            return 0; // Success
        }

        if (result == -1) {
            switch (errno) {
                case EINTR:
                    // Interrupted, try again immediately
                    continue;

                case EIO:
                    // I/O error, device might be temporarily unavailable
                    printf("Device I/O error, retrying...\n");
                    usleep(100000); // 100ms delay
                    retry_count++;
                    break;

                case ENODEV:
                    // Device removed
                    printf("Device no longer available\n");
                    return -1;

                default:
                    printf("Unexpected error: %s\n", strerror(errno));
                    return -1;
            }
        } else {
            // Partial read
            printf("Partial read: got %zd bytes, expected %zu\n",
                   result, size);
            return -1;
        }
    }

    printf("Operation failed after %d retries\n", max_retries);
    return -1;
}
```

---

## Device Testing and Debugging

```c
// Device capability testing
void test_device_capabilities(const char *device) {
    int fd = open(device, O_RDWR);
    if (fd == -1) {
        printf("Cannot open %s: %s\n", device, strerror(errno));
        return;
    }

    struct stat st;
    fstat(fd, &st);

    printf("Device: %s\n", device);
    printf("Type: %s\n", S_ISBLK(st.st_mode) ? "Block" :
                         S_ISCHR(st.st_mode) ? "Character" : "Unknown");
    printf("Major: %u, Minor: %u\n", major(st.st_rdev), minor(st.st_rdev));

    // Test basic operations
    printf("Read support: %s\n",
           fcntl(fd, F_GETFL) & O_RDONLY ? "Yes" : "No");
    printf("Write support: %s\n",
           fcntl(fd, F_GETFL) & O_WRONLY ? "Yes" : "No");

    // Test ioctl support
    if (ioctl(fd, FIONREAD, 0) != -1) {
        printf("FIONREAD ioctl: Supported\n");
    }

    close(fd);
}

// Benchmark device performance
void benchmark_device(const char *device, size_t block_size, int iterations) {
    int fd = open(device, O_RDONLY);
    if (fd == -1) {
        return;
    }

    void *buffer = malloc(block_size);

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    for (int i = 0; i < iterations; i++) {
        read(fd, buffer, block_size);
    }

    clock_gettime(CLOCK_MONOTONIC, &end);

    double elapsed = (end.tv_sec - start.tv_sec) +
                    (end.tv_nsec - start.tv_nsec) / 1e9;
    double throughput = (iterations * block_size) / elapsed / (1024 * 1024);

    printf("Device: %s\n", device);
    printf("Block size: %zu bytes\n", block_size);
    printf("Iterations: %d\n", iterations);
    printf("Throughput: %.2f MB/s\n", throughput);

    free(buffer);
    close(fd);
}
```

---

## Sysfs Interface

```c
// Read device information from sysfs
char *read_sysfs_attribute(const char *device, const char *attribute) {
    char path[512];
    snprintf(path, sizeof(path), "/sys/class/%s/%s", device, attribute);

    int fd = open(path, O_RDONLY);
    if (fd == -1) {
        return NULL;
    }

    char *buffer = malloc(256);
    ssize_t bytes = read(fd, buffer, 255);
    close(fd);

    if (bytes > 0) {
        buffer[bytes] = '\0';
        // Remove trailing newline
        if (buffer[bytes - 1] == '\n') {
            buffer[bytes - 1] = '\0';
        }
        return buffer;
    }

    free(buffer);
    return NULL;
}

// Write to sysfs attribute
int write_sysfs_attribute(const char *device, const char *attribute,
                         const char *value) {
    char path[512];
    snprintf(path, sizeof(path), "/sys/class/%s/%s", device, attribute);

    int fd = open(path, O_WRONLY);
    if (fd == -1) {
        return -1;
    }

    ssize_t written = write(fd, value, strlen(value));
    close(fd);

    return written > 0 ? 0 : -1;
}
```

---

## Device Tree and Platform Devices

```c
// Parse device tree information
#include <fdt.h>

// Read device tree blob
void *load_device_tree(const char *dtb_file) {
    int fd = open(dtb_file, O_RDONLY);
    if (fd == -1) {
        return NULL;
    }

    struct stat st;
    fstat(fd, &st);

    void *fdt = malloc(st.st_size);
    if (read(fd, fdt, st.st_size) != st.st_size) {
        free(fdt);
        fdt = NULL;
    }

    close(fd);
    return fdt;
}

// Find device in device tree
int find_device_node(void *fdt, const char *compatible) {
    int node = 0;
    const char *comp;
    int len;

    while ((node = fdt_node_offset_by_compatible(fdt, node, compatible)) >= 0) {
        comp = fdt_getprop(fdt, node, "compatible", &len);
        if (comp && len > 0) {
            printf("Found device: %s at node %d\n", comp, node);
            return node;
        }
    }

    return -1;
}
```

---

## Real-Time Device Access

```c
// Real-time device access considerations
int setup_realtime_device_access() {
    // Set real-time scheduling
    struct sched_param param;
    param.sched_priority = 99;
    sched_setscheduler(0, SCHED_FIFO, &param);

    // Lock all memory to prevent swapping
    mlockall(MCL_CURRENT | MCL_FUTURE);

    // Set CPU affinity to isolated core
    cpu_set_t cpuset;
    CPU_ZERO(&cpuset);
    CPU_SET(1, &cpuset); // Use CPU 1
    sched_setaffinity(0, sizeof(cpuset), &cpuset);

    return 0;
}

// High-precision timing for device operations
void precise_delay_us(long microseconds) {
    struct timespec req, rem;
    req.tv_sec = microseconds / 1000000;
    req.tv_nsec = (microseconds % 1000000) * 1000;

    while (nanosleep(&req, &rem) == -1) {
        if (errno == EINTR) {
            req = rem;
        } else {
            break;
        }
    }
}
```

---

## Device Security Considerations

```c
// Secure device access
int secure_device_open(const char *device, int flags) {
    // Check device permissions
    struct stat st;
    if (stat(device, &st) != 0) {
        return -1;
    }

    // Verify it's actually a device file
    if (!S_ISCHR(st.st_mode) && !S_ISBLK(st.st_mode)) {
        errno = EINVAL;
        return -1;
    }

    // Check if we have appropriate permissions
    if (access(device, R_OK | W_OK) != 0) {
        return -1;
    }

    int fd = open(device, flags | O_CLOEXEC);
    if (fd != -1) {
        // Verify file descriptor refers to expected device
        struct stat fd_st;
        fstat(fd, &fd_st);

        if (st.st_rdev != fd_st.st_rdev) {
            close(fd);
            errno = EINVAL;
            return -1;
        }
    }

    return fd;
}
```

---

## Common Device Types Summary

1. **Character devices** - Serial ports, terminals, input devices
1. **Block devices** - Hard disks, SSDs, optical drives
1. **Network interfaces** - Ethernet, Wi-Fi adapters
1. **Graphics devices** - Framebuffers, GPU devices
1. **Audio devices** - Sound cards, MIDI interfaces
1. **Input devices** - Keyboards, mice, touchscreens

---

## Best Practices

1. **Always check return values** - Handle errors gracefully
1. **Use appropriate flags** - O_CLOEXEC, O_NONBLOCK when needed
1. **Clean up resources** - Close file descriptors, unmap memory
1. **Handle device removal** - Gracefully handle hot-plugged devices
1. **Respect device limitations** - Don't assume capabilities
1. **Use standard interfaces** - Prefer standard APIs over device-specific ones

---

## Performance Considerations

1. **Use memory mapping** - For high-throughput devices
1. **Align buffers** - For DMA and direct I/O
1. **Batch operations** - Reduce syscall overhead
1. **Use appropriate I/O schedulers** - Match workload characteristics
1. **Consider real-time constraints** - For time-critical applications
1. **Monitor device performance** - Use appropriate metrics

---

## Debugging Device Issues

1. **Check dmesg** - Kernel messages about devices
1. **Examine /proc/interrupts** - Interrupt statistics
1. **Use strace** - Trace system calls to devices
1. **Monitor /sys/class** - Device attributes and statistics
1. **Check permissions** - Device file permissions and ownership
1. **Use specialized tools** - hdparm, lshw, lsusb, lspci
