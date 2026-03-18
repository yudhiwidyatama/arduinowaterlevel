import xml.etree.ElementTree as ET

def create_non_overlapping_svg(filename):
    svg = ET.Element('svg', {
        'width': '1200', 'height': '1100', 'viewBox': '0 0 1200 1100',
        'xmlns': 'http://www.w3.org/2000/svg'
    })

    style = ET.SubElement(svg, 'style')
    style.text = """
        .comp { stroke: #2c3e50; stroke-width: 2.5; rx: 8; fill-opacity: 0.95; }
        .label { font-family: Arial; font-size: 16px; font-weight: bold; fill: #ffffff; text-anchor: middle; }
        .pin-txt { font-family: 'Courier New', monospace; font-size: 12px; fill: #ecf0f1; }
        .wire { fill: none; stroke-width: 2.5; stroke-linecap: round; stroke-linejoin: round; }
        .rail { fill: none; stroke-width: 4; stroke-opacity: 0.3; }
        .junction { fill: #2c3e50; }
        .note { font-family: Arial; font-size: 13px; fill: #34495e; }
    """

    pin_map = {}

    def draw_box(x, y, w, h, name, color, left_pins, right_pins):
        g = ET.SubElement(svg, 'g')
        ET.SubElement(g, 'rect', {'x': str(x), 'y': str(y), 'width': str(w), 'height': str(h), 'class': 'comp', 'style': f'fill:{color}'})
        ET.SubElement(g, 'text', {'x': str(x + w//2), 'y': str(y - 15), 'class': 'note', 'style': 'font-weight:bold'}).text = name
        
        for i, p in enumerate(left_pins):
            py = y + 60 + (i * 40)
            ET.SubElement(g, 'text', {'x': str(x + 10), 'y': str(py), 'class': 'pin-txt'}).text = p
            pin_map[f"{name}:{p}"] = (x, py - 5)
            
        for i, p in enumerate(right_pins):
            py = y + 60 + (i * 40)
            ET.SubElement(g, 'text', {'x': str(x + w - 10), 'y': str(py), 'class': 'pin-txt', 'style': 'text-anchor: end'}).text = p
            pin_map[f"{name}:{p}"] = (x + w, py - 5)

    # 1. Place Components (Center, Left, and Right)
    # Based on image_a2752a.jpg, we use specific Arduino headers
    draw_box(450, 400, 300, 450, "Arduino Uno R3", "#005C94", 
             ["5V", "GND", "A4", "A5"], 
             ["D12", "D11", "D10"])
    
    draw_box(80, 500, 180, 200, "OLED Display", "#004D40", [], ["VCC", "GND", "SDA", "SCL"])
    
    draw_box(900, 200, 220, 220, "JSN-SR04T Sensor", "#7B4216", ["VCC", "Trig", "Echo", "GND"], [])
    
    draw_box(900, 500, 220, 180, "SSR Relay Module", "#4D2424", ["VCC", "GND", "IN"], [])

    # 2. Draw Main Power Rails (Global horizontal lines)
    ET.SubElement(svg, 'path', {'d': "M 50 50 H 1150", 'stroke': 'red', 'class': 'rail'}) # 5V Rail
    ET.SubElement(svg, 'path', {'d': "M 50 80 H 1150", 'stroke': '#7f8c8d', 'class': 'rail'}) # GND Rail
    ET.SubElement(svg, 'text', {'x': '60', 'y': '45', 'class': 'note', 'style': 'fill:red'}).text = "5V POWER RAIL"
    ET.SubElement(svg, 'text', {'x': '60', 'y': '100', 'class': 'note', 'style': 'fill:#7f8c8d'}).text = "GND RAIL"

    # 3. Routing Functions
    def tap_to_rail(pin_key, rail_y, color, channel_x):
        p = pin_map[pin_key]
        # From Pin -> Horizontal to Channel -> Vertical to Rail
        path = f"M {p[0]} {p[1]} H {channel_x} V {rail_y}"
        ET.SubElement(svg, 'path', {'d': path, 'stroke': color, 'class': 'wire'})
        ET.SubElement(svg, 'circle', {'cx': str(channel_x), 'cy': str(rail_y), 'r': '4', 'class': 'junction'})

    def draw_signal(start_key, end_key, color, channel_x):
        s = pin_map[start_key]
        e = pin_map[end_key]
        # From Start -> Channel -> Height of End -> End
        path = f"M {s[0]} {s[1]} H {channel_x} V {e[1]} H {e[0]}"
        ET.SubElement(svg, 'path', {'d': path, 'stroke': color, 'class': 'wire'})

    # --- Power Routing (Vertical Taps) ---
    # Each component gets a unique X-channel to reach the top rail without overlapping
    tap_to_rail("Arduino Uno R3:5V", 50, "red", 430)
    tap_to_rail("Arduino Uno R3:GND", 80, "#7f8c8d", 410)
    
    tap_to_rail("OLED Display:VCC", 50, "red", 300)
    tap_to_rail("OLED Display:GND", 80, "#7f8c8d", 320)
    
    tap_to_rail("JSN-SR04T Sensor:VCC", 50, "red", 850)
    tap_to_rail("JSN-SR04T Sensor:GND", 80, "#7f8c8d", 870)
    
    tap_to_rail("SSR Relay Module:VCC", 50, "red", 830)
    tap_to_rail("SSR Relay Module:GND", 80, "#7f8c8d", 810)

    # --- Signal Routing (Gutter Logic) ---
    # Left Gutter (OLED Signals)
    draw_signal("Arduino Uno R3:A4", "OLED Display:SDA", "green", 350)
    draw_signal("Arduino Uno R3:A5", "OLED Display:SCL", "teal", 370)

    # Right Gutter (Digital Signals)
    draw_signal("Arduino Uno R3:D12", "JSN-SR04T Sensor:Trig", "orange", 780)
    draw_signal("Arduino Uno R3:D11", "JSN-SR04T Sensor:Echo", "gold", 800)
    draw_signal("Arduino Uno R3:D10", "SSR Relay Module:IN", "brown", 820)

    # 4. Legend
    legend = ET.SubElement(svg, 'g', {'transform': 'translate(100, 950)'})
    ET.SubElement(legend, 'rect', {'width': '1000', 'height': '100', 'rx': '10', 'style': 'fill:#f8f9fa; stroke:#dee2e6'})
    ET.SubElement(legend, 'text', {'x': '20', 'y': '30', 'class': 'note', 'style': 'font-weight:bold'}).text = "ROUTING KEY"
    ET.SubElement(legend, 'text', {'x': '20', 'y': '60', 'class': 'note'}).text = "• Parallel lines are offset by 20px to prevent superimposition."
    ET.SubElement(legend, 'text', {'x': '20', 'y': '85', 'class': 'note'}).text = "• All Power/GND route to the shared Top Rails via dedicated vertical channels."

    tree = ET.ElementTree(svg)
    tree.write(filename)

create_non_overlapping_svg('arduino_clean_rails.svg')
