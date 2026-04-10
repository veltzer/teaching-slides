from pathlib import Path

# Common SVG wrapper and colors from palette
SVG_TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720">
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto">
      <path d="M1,2 L9,5 L1,8 Z" fill="#333" />
    </marker>
    <filter id="shadow" x="-4%" y="-8%" width="108%" height="124%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#00000022"/>
    </filter>
  </defs>
  <rect width="1280" height="640" fill="#ffffff" />
{content}
</svg>"""

COLORS = {
    'primary': '#e3f2fd',    # light blue
    'secondary': '#f3e5f5',  # light purple
    'accent': '#e8f5e9',     # light green
    'warning': '#fff3e0',    # light orange
    'danger': '#ffebee',     # light red
    'text': '#333333',
    'border': '#1e88e5'
}

def box(x, y, w, h, text, fill=COLORS['primary'], stroke=COLORS['border']):
    return f"""  <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="4" rx="8" filter="url(#shadow)" />
  <text x="{x + w/2}" y="{y + h/2 + 6}" text-anchor="middle" font-size="24" font-weight="bold" fill="{COLORS['text']}">{text}</text>"""

def text(x, y, text_content, size=24, anchor="middle", fill=COLORS['text']):
    return f'  <text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" fill="{fill}">{text_content}</text>'

def line(x1, y1, x2, y2, arrow=True, dashed=False):
    marker = ' marker-end="url(#arrow)"' if arrow else ''
    dash = ' stroke-dasharray="10 10"' if dashed else ''
    return f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#333" stroke-width="4"{marker}{dash} />'

def generate_diagram(name):
    # Depending on the name, we generate different shapes
    c = []
    
    if "lambda" in name:
        c.append(box(100, 200, 200, 100, "New Data"))
        c.append(box(400, 100, 250, 100, "Batch Layer (Hadoop)"))
        c.append(box(400, 300, 250, 100, "Speed Layer (Storm)"))
        c.append(box(800, 100, 250, 100, "Serving Layer"))
        c.append(box(800, 300, 250, 100, "Real-time Views"))
        c.append(line(300, 250, 400, 150))
        c.append(line(300, 250, 400, 350))
        c.append(line(650, 150, 800, 150))
        c.append(line(650, 350, 800, 350))
    elif "anti_corruption" in name:
        c.append(box(100, 200, 300, 200, "New System"))
        c.append(box(500, 150, 200, 300, "Anti-Corruption Layer", COLORS['warning'], '#f57c00'))
        c.append(box(800, 200, 300, 200, "Legacy System", COLORS['secondary'], '#8e24aa'))
        c.append(line(400, 300, 500, 300))
        c.append(line(700, 300, 800, 300))
    elif "peer_to_peer" in name:
        c.append(box(300, 100, 150, 100, "Peer A"))
        c.append(box(700, 100, 150, 100, "Peer B"))
        c.append(box(300, 400, 150, 100, "Peer C"))
        c.append(box(700, 400, 150, 100, "Peer D"))
        c.append(line(450, 150, 700, 150, arrow=False))
        c.append(line(450, 450, 700, 450, arrow=False))
        c.append(line(375, 200, 375, 400, arrow=False))
        c.append(line(775, 200, 775, 400, arrow=False))
        c.append(line(450, 200, 700, 400, arrow=False))
    elif "event_driven" in name:
        c.append(box(100, 250, 200, 100, "Event Producer"))
        c.append(box(450, 250, 300, 100, "Event Bus / Broker", COLORS['accent'], '#388e3c'))
        c.append(box(900, 100, 200, 100, "Consumer A"))
        c.append(box(900, 250, 200, 100, "Consumer B"))
        c.append(box(900, 400, 200, 100, "Consumer C"))
        c.append(line(300, 300, 450, 300))
        c.append(line(750, 300, 900, 150))
        c.append(line(750, 300, 900, 300))
        c.append(line(750, 300, 900, 450))
    elif "modular_monolith" in name:
        c.append('<rect x="200" y="100" width="800" height="400" fill="#fafafa" stroke="#ccc" stroke-width="4" rx="16" />')
        c.append(text(600, 140, "Modular Monolith", 28))
        c.append(box(300, 180, 250, 120, "Module A"))
        c.append(box(650, 180, 250, 120, "Module B"))
        c.append(box(300, 340, 250, 120, "Module C"))
        c.append(box(650, 340, 250, 120, "Module D"))
        c.append(line(550, 240, 650, 240, arrow=False, dashed=True))
        c.append(line(425, 300, 425, 340, arrow=False, dashed=True))
    elif "mesh" in name:
        c.append(box(200, 150, 200, 100, "Service A"))
        c.append(box(200, 270, 200, 60, "Sidecar Proxy", COLORS['accent'], '#388e3c'))
        c.append(box(700, 150, 200, 100, "Service B"))
        c.append(box(700, 270, 200, 60, "Sidecar Proxy", COLORS['accent'], '#388e3c'))
        c.append(box(450, 450, 200, 100, "Control Plane", COLORS['warning'], '#f57c00'))
        c.append(line(400, 300, 700, 300))
        c.append(line(300, 330, 450, 480, dashed=True))
        c.append(line(800, 330, 650, 480, dashed=True))
    elif "event_bus" in name:
        c.append(box(100, 150, 200, 100, "Publisher 1"))
        c.append(box(100, 350, 200, 100, "Publisher 2"))
        c.append(box(450, 100, 300, 400, "Event Bus", COLORS['accent'], '#388e3c'))
        c.append(box(900, 150, 200, 100, "Subscriber 1"))
        c.append(box(900, 350, 200, 100, "Subscriber 2"))
        c.append(line(300, 200, 450, 200))
        c.append(line(300, 400, 450, 400))
        c.append(line(750, 200, 900, 200))
        c.append(line(750, 400, 900, 400))
    elif "backend_for_frontend" in name:
        c.append(box(100, 100, 200, 100, "Mobile App"))
        c.append(box(100, 300, 200, 100, "Web App"))
        c.append(box(450, 100, 200, 100, "Mobile BFF", COLORS['warning'], '#f57c00'))
        c.append(box(450, 300, 200, 100, "Web BFF", COLORS['warning'], '#f57c00'))
        c.append(box(850, 150, 200, 80, "Microservice A", COLORS['accent'], '#388e3c'))
        c.append(box(850, 270, 200, 80, "Microservice B", COLORS['accent'], '#388e3c'))
        c.append(line(300, 150, 450, 150))
        c.append(line(300, 350, 450, 350))
        c.append(line(650, 150, 850, 190))
        c.append(line(650, 150, 850, 310))
        c.append(line(650, 350, 850, 190))
        c.append(line(650, 350, 850, 310))
    elif "kappa" in name:
        c.append(box(100, 250, 200, 100, "Event Stream"))
        c.append(box(450, 250, 300, 100, "Stream Processing Engine", COLORS['accent'], '#388e3c'))
        c.append(box(900, 250, 200, 100, "Serving Layer"))
        c.append(line(300, 300, 450, 300))
        c.append(line(750, 300, 900, 300))
    elif "api_gateway" in name:
        c.append(box(100, 250, 200, 100, "Clients"))
        c.append(box(450, 200, 150, 200, "API Gateway", COLORS['warning'], '#f57c00'))
        c.append(box(800, 100, 200, 80, "Service A"))
        c.append(box(800, 260, 200, 80, "Service B"))
        c.append(box(800, 420, 200, 80, "Service C"))
        c.append(line(300, 300, 450, 300))
        c.append(line(600, 300, 800, 140))
        c.append(line(600, 300, 800, 300))
        c.append(line(600, 300, 800, 460))
    elif "geode" in name:
        c.append(box(200, 100, 250, 150, "Geode A (US-East)"))
        c.append(box(700, 100, 250, 150, "Geode B (EU-West)"))
        c.append(box(450, 350, 250, 150, "Geode C (AP-South)"))
        c.append(line(450, 175, 700, 175, dashed=True))
        c.append(line(325, 250, 450, 425, dashed=True))
        c.append(line(825, 250, 700, 425, dashed=True))
    elif "service_oriented" in name:
        c.append(box(100, 250, 200, 100, "Client Apps"))
        c.append(box(450, 200, 200, 200, "Enterprise Service Bus", COLORS['warning'], '#f57c00'))
        c.append(box(800, 100, 200, 80, "Service 1 (CRM)"))
        c.append(box(800, 260, 200, 80, "Service 2 (ERP)"))
        c.append(box(800, 420, 200, 80, "Service 3 (Billing)"))
        c.append(line(300, 300, 450, 300))
        c.append(line(650, 300, 800, 140))
        c.append(line(650, 300, 800, 300))
        c.append(line(650, 300, 800, 460))
    elif "cqrs" in name:
        c.append(box(100, 250, 200, 100, "Client UI"))
        c.append(box(450, 100, 250, 100, "Command Model (Write)", COLORS['danger'], '#c62828'))
        c.append(box(450, 400, 250, 100, "Query Model (Read)", COLORS['accent'], '#388e3c'))
        c.append(box(850, 100, 200, 100, "Write DB"))
        c.append(box(850, 400, 200, 100, "Read DB"))
        c.append(line(300, 300, 450, 150))
        c.append(line(450, 450, 300, 300))
        c.append(line(700, 150, 850, 150))
        c.append(line(850, 450, 700, 450))
        c.append(line(950, 200, 950, 400, dashed=True))
        c.append(text(960, 300, "Async Sync", 16, "start"))
    elif "sharded" in name:
        c.append(box(100, 250, 200, 100, "App Servers"))
        c.append(box(450, 250, 200, 100, "Router / Balancer", COLORS['warning'], '#f57c00'))
        c.append(box(800, 100, 200, 100, "Shard 1 (A-M)"))
        c.append(box(800, 250, 200, 100, "Shard 2 (N-Z)"))
        c.append(box(800, 400, 200, 100, "Shard 3 (0-9)"))
        c.append(line(300, 300, 450, 300))
        c.append(line(650, 300, 800, 150))
        c.append(line(650, 300, 800, 300))
        c.append(line(650, 300, 800, 450))
    elif "microservices" in name:
        c.append(box(100, 250, 150, 100, "Clients"))
        c.append(box(350, 150, 150, 300, "API Gateway", COLORS['warning'], '#f57c00'))
        c.append(box(600, 100, 200, 80, "Service A", COLORS['accent']))
        c.append(box(850, 100, 150, 80, "DB A", COLORS['secondary']))
        c.append(box(600, 250, 200, 80, "Service B", COLORS['accent']))
        c.append(box(850, 250, 150, 80, "DB B", COLORS['secondary']))
        c.append(box(600, 400, 200, 80, "Service C", COLORS['accent']))
        c.append(box(850, 400, 150, 80, "DB C", COLORS['secondary']))
        c.append(line(250, 300, 350, 300))
        c.append(line(500, 300, 600, 140))
        c.append(line(500, 300, 600, 290))
        c.append(line(500, 300, 600, 440))
        c.append(line(800, 140, 850, 140))
        c.append(line(800, 290, 850, 290))
        c.append(line(800, 440, 850, 440))
    elif "microkernel" in name:
        c.append(box(400, 200, 400, 200, "Microkernel (Core System)", COLORS['accent'], '#388e3c'))
        c.append(box(200, 100, 200, 80, "Plugin A"))
        c.append(box(800, 100, 200, 80, "Plugin B"))
        c.append(box(200, 400, 200, 80, "Plugin C"))
        c.append(box(800, 400, 200, 80, "Plugin D"))
        c.append(line(300, 180, 450, 250))
        c.append(line(900, 180, 750, 250))
        c.append(line(300, 400, 450, 350))
        c.append(line(900, 400, 750, 350))
    elif "serverless" in name:
        c.append(box(100, 250, 200, 100, "Event Source (e.g. HTTP)"))
        c.append(box(450, 100, 200, 80, "Function A", COLORS['accent'], '#388e3c'))
        c.append(box(450, 250, 200, 80, "Function B", COLORS['accent'], '#388e3c'))
        c.append(box(450, 400, 200, 80, "Function C", COLORS['accent'], '#388e3c'))
        c.append(box(800, 250, 200, 100, "Managed Database", COLORS['secondary'], '#8e24aa'))
        c.append(line(300, 300, 450, 140))
        c.append(line(300, 300, 450, 290))
        c.append(line(300, 300, 450, 440))
        c.append(line(650, 140, 800, 300))
        c.append(line(650, 290, 800, 300))
        c.append(line(650, 440, 800, 300))
    elif "bulkhead" in name:
        c.append('<rect x="150" y="100" width="900" height="400" fill="#fafafa" stroke="#333" stroke-width="4" rx="16" />')
        c.append(text(600, 140, "Application Container", 28))
        c.append(box(200, 180, 250, 280, "Thread Pool A\n(Healthy)"))
        c.append(box(500, 180, 250, 280, "Thread Pool B\n(Healthy)"))
        c.append(box(800, 180, 250, 280, "Thread Pool C\n(Exhausted)", COLORS['danger'], '#c62828'))
    elif "space_based" in name:
        c.append(box(100, 250, 200, 100, "Clients"))
        c.append('<rect x="400" y="100" width="700" height="400" fill="#f3e5f5" stroke="#8e24aa" stroke-width="4" rx="16" />')
        c.append(text(750, 140, "In-Memory Data Grid", 28))
        c.append(box(450, 180, 200, 120, "Processing Unit 1"))
        c.append(box(800, 180, 200, 120, "Processing Unit 2"))
        c.append(box(450, 340, 200, 120, "Processing Unit 3"))
        c.append(box(800, 340, 200, 120, "Processing Unit 4"))
        c.append(line(300, 300, 400, 300))
    elif "publish_subscribe" in name:
        return generate_diagram("event_bus") # practically the same
    elif "circuit_breaker" in name:
        c.append(box(100, 250, 200, 100, "Service A"))
        c.append(box(450, 250, 250, 100, "Circuit Breaker", COLORS['warning'], '#f57c00'))
        c.append(box(900, 250, 200, 100, "Service B", COLORS['danger'], '#c62828'))
        c.append(line(300, 300, 450, 300))
        c.append(line(700, 300, 900, 300))
        c.append(text(575, 230, "State: OPEN (Failing fast)"))
    elif "hexagonal" in name:
        c.append('<circle cx="600" cy="300" r="250" fill="#e8f5e9" stroke="#2e7d32" stroke-width="4" />')
        c.append('<circle cx="600" cy="300" r="150" fill="#c8e6c9" stroke="#1b5e20" stroke-width="4" />')
        c.append(text(600, 300, "Domain Core", 28, "middle"))
        c.append(text(600, 120, "Ports & Adapters", 24, "middle"))
        c.append(box(50, 150, 200, 100, "Web Adapter"))
        c.append(box(50, 350, 200, 100, "CLI Adapter"))
        c.append(box(950, 150, 200, 100, "DB Adapter"))
        c.append(box(950, 350, 200, 100, "Event Adapter"))
        c.append(line(250, 200, 400, 250))
        c.append(line(250, 400, 400, 350))
        c.append(line(800, 250, 950, 200))
        c.append(line(800, 350, 950, 400))
    elif "onion" in name:
        c.append('<circle cx="600" cy="300" r="250" fill="#fff3e0" stroke="#ef6c00" stroke-width="4" />')
        c.append('<circle cx="600" cy="300" r="180" fill="#ffe0b2" stroke="#e65100" stroke-width="4" />')
        c.append('<circle cx="600" cy="300" r="100" fill="#ffcc80" stroke="#bf360c" stroke-width="4" />')
        c.append(text(600, 300, "Domain", 24, "middle"))
        c.append(text(600, 160, "Application Svc", 20, "middle"))
        c.append(text(600, 90, "Infrastructure", 20, "middle"))
    elif "monolithic" in name:
        c.append('<rect x="400" y="100" width="400" height="400" fill="#fafafa" stroke="#333" stroke-width="4" rx="16" filter="url(#shadow)" />')
        c.append(text(600, 140, "Monolithic Application", 28))
        c.append(box(450, 180, 300, 80, "User Interface"))
        c.append(box(450, 280, 300, 80, "Business Logic"))
        c.append(box(450, 380, 300, 80, "Data Access"))
        c.append(line(600, 260, 600, 280, arrow=False))
        c.append(line(600, 360, 600, 380, arrow=False))
    elif "strangler_fig" in name:
        c.append(box(100, 250, 150, 100, "Clients"))
        c.append(box(350, 200, 150, 200, "Facade / Router", COLORS['warning'], '#f57c00'))
        c.append(box(700, 100, 300, 150, "Legacy System", COLORS['secondary'], '#8e24aa'))
        c.append(box(700, 350, 300, 150, "Modern Microservices", COLORS['accent'], '#388e3c'))
        c.append(line(250, 300, 350, 300))
        c.append(line(500, 300, 700, 175))
        c.append(line(500, 300, 700, 425))
    elif "ddd" in name:
        c.append(box(100, 200, 300, 200, "Sales Context"))
        c.append(box(600, 200, 300, 200, "Support Context"))
        c.append(box(150, 250, 200, 100, "Aggregate A", COLORS['accent']))
        c.append(box(650, 250, 200, 100, "Aggregate B", COLORS['accent']))
        c.append(line(400, 300, 600, 300, dashed=True))
        c.append(text(500, 280, "Context Map", 16))
    elif "share_nothing" in name:
        c.append(box(200, 100, 200, 200, "Node 1\n(CPU+RAM+Disk)"))
        c.append(box(500, 100, 200, 200, "Node 2\n(CPU+RAM+Disk)"))
        c.append(box(800, 100, 200, 200, "Node 3\n(CPU+RAM+Disk)"))
        c.append(line(400, 200, 500, 200, arrow=False, dashed=True))
        c.append(line(700, 200, 800, 200, arrow=False, dashed=True))
    elif "database_per_service" in name:
        c.append(box(200, 100, 200, 100, "Service A"))
        c.append(box(200, 300, 200, 100, "Database A", COLORS['secondary'], '#8e24aa'))
        c.append(box(700, 100, 200, 100, "Service B"))
        c.append(box(700, 300, 200, 100, "Database B", COLORS['secondary'], '#8e24aa'))
        c.append(line(300, 200, 300, 300))
        c.append(line(800, 200, 800, 300))
    elif "architecture" in name:
        # Default generic block
        c.append(box(300, 250, 200, 100, "Component A"))
        c.append(box(700, 250, 200, 100, "Component B"))
        c.append(line(500, 300, 700, 300))
    else:
        # Default
        c.append(box(300, 250, 200, 100, "Input"))
        c.append(box(700, 250, 200, 100, "Output"))
        c.append(line(500, 300, 700, 300))

    return SVG_TEMPLATE.format(content="\n".join(c))

def main():
    svg_dir = Path("svg/courses/architecting/architecting/01_architectural_design_patterns")
    count = 0
    for f in svg_dir.glob("*.svg"):
        content = f.read_text(encoding="utf-8")
        if "Start</text>" in content:
            new_content = generate_diagram(f.name)
            f.write_text(new_content, encoding="utf-8")
            print(f"Generated {f.name}")
            count += 1
    print(f"Replaced {count} files")

if __name__ == '__main__':
    main()
