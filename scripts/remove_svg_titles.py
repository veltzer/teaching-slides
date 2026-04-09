#!/usr/bin/env python
"""
Remove the internal title block from SVG diagrams and shift content up.
The title block consists of:
  - A <!-- Title --> comment
  - A <text> with font-size="40" font-weight="bold" (the title text)
  - A <line> immediately after (horizontal rule)
After removal, all y-coordinates in the remaining content are shifted up
by SHIFT pixels to reclaim the freed space.
"""

import re
import sys

SHIFT = 70  # pixels to shift content up after removing the title block

FILES = [
    "svg/courses/embedded/effective-real-time-embedded-c-and-c++/01_intro/embedded_system_constraints.svg",
    "svg/courses/embedded/effective-real-time-embedded-c-and-c++/01_intro/the_embedded_software_stack.svg",
    "svg/courses/embedded/effective-real-time-embedded-c-and-c++/02_embedded_c/bit_manipulation.svg",
    "svg/courses/embedded/effective-real-time-embedded-c-and-c++/03_elements_of_c_cpp/structure_layout.svg",
    "svg/courses/embedded/effective-real-time-embedded-c-and-c++/04_pointers/pointer_arithmetic.svg",
    "svg/courses/embedded/effective-real-time-embedded-c-and-c++/05_memory_management/cache_line_effects.svg",
    "svg/courses/embedded/effective-real-time-embedded-c-and-c++/05_memory_management/memory_hierarchy.svg",
    "svg/courses/embedded/effective-real-time-embedded-c-and-c++/05_memory_management/memory_mapping_in_detail.svg",
    "svg/courses/embedded/effective-real-time-embedded-c-and-c++/05_memory_management/memory_regions.svg",
    "svg/courses/embedded/effective-real-time-embedded-c-and-c++/06_intertask_communication/concurrency_challenges.svg",
    "svg/courses/embedded/effective-real-time-embedded-c-and-c++/06_intertask_communication/priority_inversion.svg",
    "svg/courses/embedded/effective-real-time-embedded-c-and-c++/07_toolchain/toolchain_components.svg",
    "svg/courses/embedded/effective-real-time-embedded-c-and-c++/07_toolchain/runtime_memory_layout.svg",
    "svg/courses/embedded/effective-real-time-embedded-c-and-c++/08_optimization/optimization_goals.svg",
    "svg/courses/embedded/effective-real-time-embedded-c-and-c++/09_writing_safer_c/why_safety_matters.svg",
    "svg/courses/embedded/effective-real-time-embedded-c-and-c++/10_hardware_programming/interrupt_priorities_and_preemption.svg",
    "svg/courses/embedded/effective-real-time-embedded-c-and-c++/10_hardware_programming/interrupt_system_architecture.svg",
    "svg/courses/embedded/effective-real-time-embedded-c-and-c++/10_hardware_programming/nested_interrupts.svg",
    "svg/courses/embedded/effective-real-time-embedded-c-and-c++/11_timing/time_measurement_challenges.svg",
    "svg/courses/embedded/effective-real-time-embedded-c-and-c++/11_timing/watchdog_timer_types.svg",
    "svg/courses/embedded/effective-real-time-embedded-c-and-c++/12_object_oriented_c/why_oop_in_c.svg",
    "svg/courses/embedded/effective-real-time-embedded-c-and-c++/13_object_oriented_design/uml_diagram_example.svg",
    "svg/courses/embedded/effective-real-time-embedded-c-and-c++/14_embedded_c++/why_c_in_embedded.svg",
    "svg/courses/embedded/effective-real-time-embedded-c-and-c++/15_resource_management/raii_principle.svg",
    "svg/courses/embedded/effective-real-time-embedded-c-and-c++/16_templates_and_generic_programming/why_templates.svg",
    "svg/courses/embedded/effective-real-time-embedded-c-and-c++/17_stl/stl_architecture.svg",
    "svg/courses/embedded/effective-real-time-embedded-c-and-c++/18_streams/common_background_of_i_o_streams.svg",
    "svg/courses/embedded/effective-real-time-embedded-c-and-c++/18_streams/stream_buffer_classes_overview.svg",
    "svg/courses/embedded/effective-real-time-embedded-c-and-c++/18_streams/stream_hierarchy_overview.svg",
    "svg/courses/embedded/effective-real-time-embedded-c-and-c++/19_peripherals/analog_to_digital_converter_adc.svg",
    "svg/courses/embedded/effective-real-time-embedded-c-and-c++/19_peripherals/direct_memory_access_dma.svg",
    "svg/courses/embedded/effective-real-time-embedded-c-and-c++/19_peripherals/inter_integrated_circuit_i2c.svg",
    "svg/courses/embedded/effective-real-time-embedded-c-and-c++/19_peripherals/overview_of_embedded_peripherals.svg",
    "svg/courses/embedded/effective-real-time-embedded-c-and-c++/19_peripherals/serial_peripheral_interface_spi.svg",
    "svg/courses/embedded/effective-real-time-embedded-c-and-c++/19_peripherals/universal_asynchronous_receiver_transmitter_uart.svg",
]


def shift_y_value(match):
    """Subtract SHIFT from a captured y-coordinate value."""
    attr_name = match.group(1)  # e.g. 'y', 'y1', 'y2', 'cy'
    val = int(match.group(2))
    new_val = val - SHIFT
    return f'{attr_name}="{new_val}"'


def shift_translate_y(match):
    """Subtract SHIFT from the y component of translate(x, y)."""
    x_val = match.group(1)
    y_val = int(match.group(2))
    new_y = y_val - SHIFT
    return f'translate({x_val},{new_y})'


def process_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Pattern to match the title block:
    # <!-- Title --> (optional whitespace/newline)
    # <text ... font-size="40" ... font-weight="bold" ...>...</text>  (or with attributes in different order)
    # <line ... y1="66" ... /> (the horizontal rule)
    # Followed by a blank line or whitespace
    #
    # We use a multiline regex that captures the entire block including surrounding whitespace lines.

    # Match: optional blank line + "  <!-- Title -->\n" + "  <text ...font-size="40"...bold...>...</text>\n" + "  <line ...y1="6[0-9]"...>\n" + optional blank line
    title_block_pattern = re.compile(
        r'\n\s*<!--\s*Title\s*-->\n'
        r'\s*<text\b[^>]*font-size="40"[^>]*font-weight="bold"[^>]*>.*?</text>\n'
        r'\s*<line\b[^/]*/>\n'
        r'(?:\n)?',  # optional blank line after
        re.DOTALL
    )

    # Also try the reverse attribute order (font-weight before font-size)
    title_block_pattern2 = re.compile(
        r'\n\s*<!--\s*Title\s*-->\n'
        r'\s*<text\b[^>]*font-weight="bold"[^>]*font-size="40"[^>]*>.*?</text>\n'
        r'\s*<line\b[^/]*/>\n'
        r'(?:\n)?',
        re.DOTALL
    )

    matched = False
    for pattern in [title_block_pattern, title_block_pattern2]:
        m = pattern.search(content)
        if m:
            # Determine the end of the title block in the content
            title_end = m.end()
            before = content[:m.start()]  # everything up to (not including) the title block
            # We want to keep a single newline at the end of 'before'
            # The match starts with '\n', so before ends right before that newline
            after = content[title_end:]   # everything after the title block

            # Now shift all y-coordinates in 'after'
            # Attributes: y="N", y1="N", y2="N", cy="N"
            after_shifted = re.sub(
                r'\b(y[12]?|cy)="(-?\d+)"',
                shift_y_value,
                after
            )
            # Also handle translate(x, y) patterns
            after_shifted = re.sub(
                r'translate\((-?[\d.]+),\s*(-?\d+)\)',
                shift_translate_y,
                after_shifted
            )

            content = before + '\n' + after_shifted
            matched = True
            break

    if not matched:
        print(f"  WARNING: No title block found in {path}")
        return False

    if content == original:
        print(f"  WARNING: No changes made to {path}")
        return False

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  OK: {path}")
    return True


def main():
    base = "."
    ok = 0
    fail = 0
    for rel_path in FILES:
        path = f"{base}/{rel_path}"
        try:
            if process_file(path):
                ok += 1
            else:
                fail += 1
        except Exception as e:
            print(f"  ERROR: {path}: {e}")
            fail += 1
    print(f"\nDone: {ok} processed, {fail} failed/skipped")


if __name__ == "__main__":
    main()
