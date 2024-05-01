---
marp: true
theme: default
paginate: true
_paginate: false
---

# Port Scanning

*Understanding Network Security Vulnerabilities*

<!-- Speaker notes:
In this presentation, we will explore the concept of port scanning, a technique used to identify open ports on a computer or network device. By understanding port scanning, we can learn about potential security vulnerabilities and take steps to mitigate them.
-->

---

# What is Port Scanning?

* Port scanning is the process of identifying open ports on a computer or network device.
* Ports are virtual numbered connections that allow communication between devices on a network.
* Different ports are used for different services, such as web browsing (port 80), email (port 25), and remote access (port 22).

<!-- Speaker notes:
Think of ports like doorways on a castle wall. Each port has a specific number and allows a specific type of traffic to enter or exit the device. By scanning these ports, we can see which "doors" are open and potentially vulnerable.
-->

---

# Why Port Scanning is Done

* Port scanning can be used for both malicious and non-malicious purposes.
* **Malicious actors** can use port scanning to identify vulnerabilities in a network that they can exploit.
* **Network administrators** can use port scanning to identify open ports and assess the security posture of their networks.

<!-- Speaker notes:
Port scanning is a double-edged sword. Malicious actors can use it to find weaknesses in a network, while network administrators can use it to identify and address potential security risks.
-->

---

# Types of Port Scanning

* There are different types of port scanning techniques, each with its own advantages and disadvantages.
* **TCP SYN Scan:** A common technique that sends a SYN packet to a port and waits for a response.
* **UDP Scan:** Sends a UDP packet to a port and checks for a response.
* **Ping Scan:** Sends a ping request to a device to see if it is alive.

<!-- Speaker notes:
There are various port scanning methods, each suited for different purposes. TCP SYN scans are efficient, UDP scans can be used for firewalled networks, and ping scans simply check for active devices.
-->

---

# Protecting Against Port Scanning

* There are several ways to protect against port scanning and potential attacks.
* **Use a firewall:** A firewall can filter incoming and outgoing traffic, blocking access to unauthorized ports.
* **Keep software up to date:** Outdated software can contain vulnerabilities that attackers can exploit.
* **Use strong passwords:** Strong passwords make it more difficult for attackers to gain unauthorized access.

<!-- Speaker notes:
By implementing a layered security approach, including firewalls, software updates, and strong passwords, we can significantly reduce the risk of successful attacks that leverage port scanning techniques.
-->
