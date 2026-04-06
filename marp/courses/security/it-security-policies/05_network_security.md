# Network Security Awareness

## Your Connection Is Your Lifeline
- Everything you do at work depends on the network
- Attackers target network connections to intercept data
- Understanding basic network safety keeps you and the company safe
- No technical knowledge required - just good habits

---

## Secure Internet Usage

## Basic Rules for Safe Browsing
- Only visit `HTTPS` websites (look for the padlock icon)
- Do not download software from unknown sources
- Do not click on pop-up ads or "You've won!" banners
- Be cautious with shortened URLs (e.g., `bit.ly/xyz`)
- Do not enter credentials on sites you reached via email links
- Use bookmarks for frequently visited important sites

---

## `HTTPS` - What the Padlock Means

```diagram
Secure (HTTPS):                    Insecure (HTTP):

  You ---[encrypted]--- Website      You ---[plain text]--- Website
          |                                   |
     Attacker sees:                      Attacker sees:
     "x7$kL9#mQ2@..."                   "username: jsmith
                                          password: MyP@ss1"
```

- `HTTPS` encrypts data between your browser and the website
- Without it, anyone on the same network can read your traffic
- Never enter passwords or personal data on non-`HTTPS` sites

---

## What Is a `VPN`?

## Virtual Private Network

```misc
Without VPN:                      With VPN:

You ---> [open internet] ---> Server    You ---> [encrypted tunnel] ---> Server
              |                                        |
         Visible to:                              Hidden from:
         - ISP                                    - ISP
         - Network admin                          - Network admin
         - Attackers on                           - Attackers
           same network
```

- Creates an encrypted tunnel for all your internet traffic
- Essential when working outside the office
- Use the company `VPN` whenever connecting to company resources remotely

---

## `VPN` Guidelines

- **Always connect** to the company `VPN` before accessing work systems remotely
- **Use only** the company-provided `VPN` client
- **Do not use** free or personal `VPN` services for work
- **Keep the `VPN` client** updated to the latest version
- **Disconnect** when you are done working
- **Report** any `VPN` connection issues to IT immediately

---

## Public Wi-Fi: The Hidden Danger

## Why Free Wi-Fi Is Risky

- You do not know who controls the network
- Attackers can create fake hotspots with legitimate-sounding names
- Unencrypted traffic can be intercepted
- Common attack: "Evil Twin" access point

```misc
Real airport Wi-Fi:    "Airport_Free_WiFi"
Attacker's hotspot:    "Airport_Free_WiFi_Fast"
                        ^^^^^^^^^^^^^^^^^^^^^^^
                        Looks better, but it is a trap!
```

---

## Staying Safe on Public Wi-Fi

- **Best option**: use your phone's mobile hotspot instead
- **If you must use public Wi-Fi**:
    - Connect to the company `VPN` immediately
    - Avoid logging into sensitive accounts
    - Do not access banking or financial sites
    - Disable auto-connect to open networks
    - Forget the network when you are done
    - Verify the network name with staff at the location

---

## Firewall Basics

## What Is a Firewall?

```diagram
                     FIREWALL
                    +--------+
  Internet -------->| ALLOW  |--------> Approved traffic
  (all traffic)     |  or    |          reaches your network
                    | BLOCK  |
                    +---+----+
                        |
                        v
                  Blocked traffic
                  (threats stopped)
```

- A firewall is a security guard for network traffic
- It allows approved connections and blocks suspicious ones
- Your company has firewalls; your computer may have one too
- Never disable your computer's firewall

---

## Remote Work Security

## Your Home Is Now an Extension of the Office

- Home networks are less secure than office networks
- Other family members share your network
- Personal devices may not have security software
- Physical security may be weaker

---

## Remote Work Security Checklist

- **Router**: change the default admin password, use `WPA3` or `WPA2` encryption
- **Network**: create a separate Wi-Fi network for work if possible
- **`VPN`**: always use it when accessing company resources
- **Updates**: keep your home router firmware up to date
- **Physical**: lock your screen, use a privacy screen, work in a private area
- **Devices**: do not let family members use your work computer

---

## Recognizing Network Threats

## Warning Signs Something Is Wrong
- Unusually slow internet connection
- Browser redirecting to unexpected websites
- Pop-ups appearing even when the browser is closed
- Unknown devices appearing on your network
- `VPN` connection failing repeatedly
- Security certificate warnings in your browser

If you notice any of these, **contact IT security immediately**

---

## Browser Security Tips

- Keep your browser updated to the latest version
- Do not install unnecessary browser extensions
- Clear browsing data regularly on shared computers
- Use the company-approved browser
- Do not save passwords in the browser (use a password manager)
- Be cautious of sites requesting unusual permissions
- Watch for certificate warnings - they exist for a reason

---

## Bluetooth and Wireless Threats

- Turn off Bluetooth when not in use
- Do not accept pairing requests from unknown devices
- Disable `AirDrop` / file sharing from unknown contacts
- Be aware that wireless keyboards and mice can be intercepted
- In sensitive meetings, consider airplane mode

---

## Secure Video Conferencing

- Use company-approved platforms only
- Enable waiting rooms and meeting passwords
- Do not share meeting links publicly
- Be aware of what is visible in your background
- Mute when not speaking to prevent accidental information sharing
- Do not record meetings without consent
- Lock the meeting once all participants have joined

---

## Key Takeaways

- Always use `HTTPS` websites and look for the padlock
- Connect to the company `VPN` when working remotely
- Never use public Wi-Fi without `VPN` protection
- Keep your home network secure for remote work
- Never disable your firewall
- Report unusual network behavior to IT security
- Treat your home office with the same security as the office
