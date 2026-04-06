# CPU Architecture

---

## Table of Contents

1. CPU Overview and Components
1. The ALU and Registers
1. Control Unit and Instruction Cycle
1. Pipelining
1. Branch Prediction
1. Superscalar Execution
1. CISC vs RISC
1. x86 vs ARM
1. Cache Hierarchy
1. Cache Coherence

---

## What is a CPU?

The Central Processing Unit is the "brain" of the computer. It executes
instructions from programs by performing arithmetic, logic, control, and
I/O operations.

<svg xmlns="http://www.w3.org/2000/svg" width="640" height="400" font-family="sans-serif">
  <defs>
    <marker id="arr0" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 Z" fill="#555"/>
    </marker>
  </defs>
  <!-- Outer CPU box -->
  <rect x="10" y="10" width="620" height="330" rx="4" fill="#e3f2fd" stroke="#333333" stroke-width="1.5"/>
  <text x="320" y="34" text-anchor="middle" font-size="16" font-weight="bold" fill="#222222">CPU</text>
  <!-- Control Unit -->
  <rect x="35" y="50" width="115" height="70" rx="4" fill="#f0f4f8" stroke="#333333" stroke-width="1.5"/>
  <text x="93" y="78" text-anchor="middle" font-size="13" fill="#222222">Control Unit</text>
  <text x="93" y="97" text-anchor="middle" font-size="12" fill="#555">(CU)</text>
  <!-- ALU -->
  <rect x="213" y="50" width="145" height="70" rx="4" fill="#f0f4f8" stroke="#333333" stroke-width="1.5"/>
  <text x="286" y="78" text-anchor="middle" font-size="13" fill="#222222">ALU</text>
  <text x="286" y="95" text-anchor="middle" font-size="12" fill="#555">(Arithmetic Logic Unit)</text>
  <!-- Registers -->
  <rect x="425" y="50" width="150" height="70" rx="4" fill="#f0f4f8" stroke="#333333" stroke-width="1.5"/>
  <text x="500" y="78" text-anchor="middle" font-size="13" fill="#222222">Registers</text>
  <text x="500" y="95" text-anchor="middle" font-size="12" fill="#555">(Fast local storage)</text>
  <!-- Arrows between top boxes -->
  <line x1="150" y1="85" x2="213" y2="85" stroke="#555" stroke-width="1.5" marker-end="url(#arr0)"/>
  <line x1="358" y1="85" x2="425" y2="85" stroke="#555" stroke-width="1.5" marker-end="url(#arr0)"/>
  <!-- Lines down from each box to horizontal collector -->
  <line x1="93" y1="120" x2="93" y2="175" stroke="#555" stroke-width="1.5"/>
  <line x1="286" y1="120" x2="286" y2="175" stroke="#555" stroke-width="1.5"/>
  <line x1="500" y1="120" x2="500" y2="175" stroke="#555" stroke-width="1.5"/>
  <line x1="93" y1="175" x2="500" y2="175" stroke="#555" stroke-width="1.5"/>
  <line x1="286" y1="175" x2="286" y2="197" stroke="#555" stroke-width="1.5" marker-end="url(#arr0)"/>
  <!-- Internal Bus -->
  <rect x="206" y="197" width="160" height="30" rx="4" fill="#fff3e0" stroke="#333333" stroke-width="1.5"/>
  <text x="286" y="217" text-anchor="middle" font-size="13" fill="#222222">Internal Bus</text>
  <!-- Line down to lower boxes -->
  <line x1="286" y1="227" x2="286" y2="252" stroke="#555" stroke-width="1.5"/>
  <line x1="100" y1="252" x2="510" y2="252" stroke="#555" stroke-width="1.5"/>
  <line x1="100" y1="252" x2="100" y2="275" stroke="#555" stroke-width="1.5" marker-end="url(#arr0)"/>
  <line x1="286" y1="252" x2="286" y2="275" stroke="#555" stroke-width="1.5" marker-end="url(#arr0)"/>
  <line x1="480" y1="252" x2="480" y2="275" stroke="#555" stroke-width="1.5" marker-end="url(#arr0)"/>
  <!-- L1 I-Cache -->
  <rect x="35" y="275" width="130" height="40" rx="4" fill="#e8f5e9" stroke="#333333" stroke-width="1.5"/>
  <text x="100" y="300" text-anchor="middle" font-size="13" fill="#222222">L1 I-Cache</text>
  <!-- L1 D-Cache -->
  <rect x="211" y="275" width="150" height="40" rx="4" fill="#e8f5e9" stroke="#333333" stroke-width="1.5"/>
  <text x="286" y="300" text-anchor="middle" font-size="13" fill="#222222">L1 D-Cache</text>
  <!-- Branch Pred -->
  <rect x="405" y="275" width="150" height="40" rx="4" fill="#e8f5e9" stroke="#333333" stroke-width="1.5"/>
  <text x="480" y="300" text-anchor="middle" font-size="13" fill="#222222">Branch Pred.</text>
  <!-- Line down to External Bus -->
  <line x1="320" y1="340" x2="320" y2="363" stroke="#555" stroke-width="1.5" marker-end="url(#arr0)"/>
  <rect x="240" y="363" width="160" height="30" rx="4" fill="#fff3e0" stroke="#333333" stroke-width="1.5"/>
  <text x="320" y="383" text-anchor="middle" font-size="13" fill="#222222">External Bus</text>
</svg>

---

## The Arithmetic Logic Unit (ALU)

The ALU performs all arithmetic and logical operations inside the CPU.

**Arithmetic operations:**
- Addition, subtraction
- Multiplication, division
- Increment, decrement

**Logical operations:**
- AND, OR, NOT, XOR
- Shift left, shift right
- Comparison (sets flags)

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="150" font-family="sans-serif">
  <defs>
    <marker id="arr1" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 Z" fill="#555"/>
    </marker>
  </defs>
  <!-- ALU box -->
  <rect x="200" y="20" width="130" height="110" rx="4" fill="#e3f2fd" stroke="#333333" stroke-width="1.5"/>
  <text x="265" y="80" text-anchor="middle" font-size="15" font-weight="bold" fill="#222222">ALU</text>
  <!-- Input A -->
  <text x="10" y="50" font-size="13" fill="#222222">Input A</text>
  <line x1="80" y1="47" x2="200" y2="55" stroke="#555" stroke-width="1.5" marker-end="url(#arr1)"/>
  <!-- Input B -->
  <text x="10" y="80" font-size="13" fill="#222222">Input B</text>
  <line x1="80" y1="77" x2="200" y2="80" stroke="#555" stroke-width="1.5" marker-end="url(#arr1)"/>
  <!-- Opcode -->
  <text x="10" y="115" font-size="13" fill="#222222">Opcode</text>
  <line x1="80" y1="112" x2="200" y2="108" stroke="#555" stroke-width="1.5" marker-end="url(#arr1)"/>
  <!-- Result -->
  <line x1="330" y1="55" x2="400" y2="55" stroke="#555" stroke-width="1.5" marker-end="url(#arr1)"/>
  <text x="408" y="59" font-size="13" fill="#222222">Result</text>
  <!-- Flags -->
  <line x1="330" y1="100" x2="400" y2="100" stroke="#555" stroke-width="1.5" marker-end="url(#arr1)"/>
  <text x="408" y="104" font-size="13" fill="#222222">Flags (Zero, Carry, Overflow, Sign)</text>
</svg>

The ALU reads two operands (A and B), performs the operation specified by the
opcode, and produces a result plus status flags.

---

## Status Flags Register

The flags register records the outcome of the last ALU operation.
Conditional branches use these flags to make decisions.

| Flag | Name | Set When |
|------|------|----------|
| ZF | Zero Flag | Result is zero |
| CF | Carry Flag | Unsigned overflow occurred |
| OF | Overflow Flag | Signed overflow occurred |
| SF | Sign Flag | Result is negative (MSB = 1) |
| PF | Parity Flag | Result has even number of 1-bits |

Example: after computing `5 - 5`, ZF=1, SF=0, CF=0, OF=0.
A `JZ` (jump if zero) instruction would take the branch.

---

## CPU Registers

Registers are the fastest storage in a computer -- accessed in a single
clock cycle with zero latency.

**General-purpose registers (x86-64):**

<svg xmlns="http://www.w3.org/2000/svg" width="640" height="290" font-family="sans-serif">
  <!-- Outer box -->
  <rect x="10" y="10" width="620" height="270" rx="4" fill="#f0f4f8" stroke="#333333" stroke-width="1.5"/>
  <!-- Section: GP 64-bit -->
  <rect x="10" y="10" width="620" height="65" rx="4" fill="#e3f2fd" stroke="#333333" stroke-width="1.5"/>
  <text x="25" y="36" font-size="13" font-weight="bold" fill="#222222">64-bit GP:</text>
  <text x="115" y="36" font-size="13" fill="#222222">RAX  RBX  RCX  RDX  RSI  RDI  RSP  RBP</text>
  <text x="115" y="62" font-size="13" fill="#222222">R8   R9   R10  R11  R12  R13  R14  R15</text>
  <!-- Section: Special -->
  <rect x="10" y="75" width="620" height="65" rx="4" fill="#e8f5e9" stroke="#333333" stroke-width="1.5"/>
  <text x="25" y="98" font-size="13" font-weight="bold" fill="#222222">Special:</text>
  <text x="115" y="98" font-size="13" fill="#222222">RIP (instruction pointer)</text>
  <text x="115" y="118" font-size="13" fill="#222222">RFLAGS (status flags)   RSP (stack pointer)</text>
  <!-- Section: Segment -->
  <rect x="10" y="140" width="620" height="40" rx="4" fill="#fff3e0" stroke="#333333" stroke-width="1.5"/>
  <text x="25" y="165" font-size="13" font-weight="bold" fill="#222222">Segment:</text>
  <text x="115" y="165" font-size="13" fill="#222222">CS  DS  SS  ES  FS  GS</text>
  <!-- Section: Vector -->
  <rect x="10" y="180" width="620" height="100" rx="4" fill="#fce4ec" stroke="#333333" stroke-width="1.5"/>
  <text x="25" y="205" font-size="13" font-weight="bold" fill="#222222">Vector:</text>
  <text x="115" y="205" font-size="13" fill="#222222">XMM0–XMM15  (128-bit SSE)</text>
  <text x="115" y="228" font-size="13" fill="#222222">YMM0–YMM15  (256-bit AVX)</text>
  <text x="115" y="251" font-size="13" fill="#222222">ZMM0–ZMM31  (512-bit AVX-512)</text>
</svg>

---

## Register Naming in x86-64

The x86-64 registers have sub-register access for backward compatibility:

<svg xmlns="http://www.w3.org/2000/svg" width="640" height="160" font-family="sans-serif">
  <!-- Bit labels -->
  <text x="15" y="20" font-size="12" fill="#555">63</text>
  <text x="230" y="20" font-size="12" fill="#555">31</text>
  <text x="380" y="20" font-size="12" fill="#555">15</text>
  <text x="470" y="20" font-size="12" fill="#555">7</text>
  <text x="530" y="20" font-size="12" fill="#555">0</text>
  <!-- RAX outer (full 64-bit) -->
  <rect x="15" y="30" width="610" height="110" rx="4" fill="#e3f2fd" stroke="#333333" stroke-width="1.5"/>
  <text x="130" y="145" text-anchor="middle" font-size="12" font-weight="bold" fill="#222222">RAX (64-bit)</text>
  <!-- EAX (32-bit, right half) -->
  <rect x="245" y="40" width="380" height="85" rx="4" fill="#e8f5e9" stroke="#333333" stroke-width="1.5"/>
  <text x="385" y="130" text-anchor="middle" font-size="12" font-weight="bold" fill="#222222">EAX (32-bit)</text>
  <!-- AX (16-bit) -->
  <rect x="385" y="50" width="240" height="65" rx="4" fill="#fff3e0" stroke="#333333" stroke-width="1.5"/>
  <text x="455" y="128" text-anchor="middle" font-size="12" font-weight="bold" fill="#222222">AX (16-bit)</text>
  <!-- AL (8-bit) -->
  <rect x="505" y="60" width="120" height="45" rx="4" fill="#fce4ec" stroke="#333333" stroke-width="1.5"/>
  <text x="565" y="127" text-anchor="middle" font-size="12" font-weight="bold" fill="#222222">AL (8-bit)</text>
  <!-- Labels inside boxes -->
  <text x="130" y="80" text-anchor="middle" font-size="13" fill="#444">RAX</text>
  <text x="315" y="80" text-anchor="middle" font-size="13" fill="#444">EAX</text>
  <text x="455" y="78" text-anchor="middle" font-size="13" fill="#444">AX</text>
  <text x="565" y="87" text-anchor="middle" font-size="13" fill="#444">AL</text>
</svg>

- `AL` = low 8 bits of RAX
- `AX` = low 16 bits of RAX
- `EAX` = low 32 bits of RAX
- `RAX` = full 64 bits

Writing to `EAX` zero-extends into `RAX`. Writing to `AX` or `AL` does not.

---

## Register Conventions (System V AMD64 ABI)

On Linux/macOS x86-64, function arguments are passed in registers:

| Argument # | Register | Purpose |
|------------|----------|---------|
| 1st | RDI | First integer/pointer arg |
| 2nd | RSI | Second integer/pointer arg |
| 3rd | RDX | Third integer/pointer arg |
| 4th | RCX | Fourth integer/pointer arg |
| 5th | R8 | Fifth integer/pointer arg |
| 6th | R9 | Sixth integer/pointer arg |
| Return | RAX | Return value |
| Stack ptr | RSP | Stack pointer |
| Base ptr | RBP | Frame pointer (optional) |

Arguments beyond the 6th are passed on the stack. Floating-point arguments
use XMM0-XMM7.

---

## The Control Unit

The control unit orchestrates the CPU. It reads instructions from memory,
decodes them, and generates control signals that tell other components
what to do.

<svg xmlns="http://www.w3.org/2000/svg" width="600" height="380" font-family="sans-serif">
  <defs>
    <marker id="arr4" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 Z" fill="#555"/>
    </marker>
  </defs>
  <!-- Control Unit outer box -->
  <rect x="10" y="10" width="560" height="230" rx="4" fill="#e3f2fd" stroke="#333333" stroke-width="1.5"/>
  <text x="290" y="35" text-anchor="middle" font-size="15" font-weight="bold" fill="#222222">Control Unit</text>
  <!-- Instruction Register -->
  <rect x="40" y="55" width="155" height="70" rx="4" fill="#f0f4f8" stroke="#333333" stroke-width="1.5"/>
  <text x="118" y="83" text-anchor="middle" font-size="13" fill="#222222">Instruction</text>
  <text x="118" y="100" text-anchor="middle" font-size="13" fill="#222222">Register (IR)</text>
  <!-- Instruction Decoder -->
  <rect x="280" y="55" width="160" height="70" rx="4" fill="#f0f4f8" stroke="#333333" stroke-width="1.5"/>
  <text x="360" y="83" text-anchor="middle" font-size="13" fill="#222222">Instruction</text>
  <text x="360" y="100" text-anchor="middle" font-size="13" fill="#222222">Decoder</text>
  <!-- IR -> Decoder arrow -->
  <line x1="195" y1="90" x2="280" y2="90" stroke="#555" stroke-width="1.5" marker-end="url(#arr4)"/>
  <!-- Decoder -> Control Signal Generator arrow -->
  <line x1="360" y1="125" x2="360" y2="155" stroke="#555" stroke-width="1.5" marker-end="url(#arr4)"/>
  <!-- Control Signal Generator -->
  <rect x="280" y="155" width="160" height="60" rx="4" fill="#fff3e0" stroke="#333333" stroke-width="1.5"/>
  <text x="360" y="180" text-anchor="middle" font-size="13" fill="#222222">Control Signal</text>
  <text x="360" y="198" text-anchor="middle" font-size="13" fill="#222222">Generator</text>
  <!-- Line from CSG down out of box -->
  <line x1="360" y1="215" x2="360" y2="255" stroke="#555" stroke-width="1.5"/>
  <!-- Horizontal spread -->
  <line x1="100" y1="255" x2="530" y2="255" stroke="#555" stroke-width="1.5"/>
  <!-- Down to ALU -->
  <line x1="100" y1="255" x2="100" y2="285" stroke="#555" stroke-width="1.5" marker-end="url(#arr4)"/>
  <!-- Down to Registers -->
  <line x1="360" y1="255" x2="360" y2="285" stroke="#555" stroke-width="1.5" marker-end="url(#arr4)"/>
  <!-- Down to Memory -->
  <line x1="530" y1="255" x2="530" y2="285" stroke="#555" stroke-width="1.5" marker-end="url(#arr4)"/>
  <!-- ALU box -->
  <rect x="35" y="285" width="130" height="40" rx="4" fill="#e8f5e9" stroke="#333333" stroke-width="1.5"/>
  <text x="100" y="310" text-anchor="middle" font-size="13" fill="#222222">ALU</text>
  <!-- Registers box -->
  <rect x="285" y="285" width="150" height="40" rx="4" fill="#e8f5e9" stroke="#333333" stroke-width="1.5"/>
  <text x="360" y="310" text-anchor="middle" font-size="13" fill="#222222">Registers</text>
  <!-- Memory box -->
  <rect x="460" y="285" width="130" height="40" rx="4" fill="#e8f5e9" stroke="#333333" stroke-width="1.5"/>
  <text x="525" y="310" text-anchor="middle" font-size="13" fill="#222222">Memory</text>
</svg>

---

## The Instruction Cycle: Fetch-Decode-Execute

Every instruction goes through a fundamental cycle:

<svg xmlns="http://www.w3.org/2000/svg" width="680" height="210" font-family="sans-serif">
  <defs>
    <marker id="arr5" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 Z" fill="#555"/>
    </marker>
    <marker id="arr5r" markerWidth="8" markerHeight="8" refX="1" refY="3" orient="auto">
      <path d="M8,0 L8,6 L0,3 Z" fill="#555"/>
    </marker>
  </defs>
  <!-- FETCH -->
  <rect x="10" y="20" width="120" height="110" rx="4" fill="#e3f2fd" stroke="#333333" stroke-width="1.5"/>
  <text x="70" y="45" text-anchor="middle" font-size="14" font-weight="bold" fill="#222222">FETCH</text>
  <text x="70" y="68" text-anchor="middle" font-size="12" fill="#555">Read instr</text>
  <text x="70" y="85" text-anchor="middle" font-size="12" fill="#555">from</text>
  <text x="70" y="102" text-anchor="middle" font-size="12" fill="#555">memory</text>
  <!-- DECODE -->
  <rect x="175" y="20" width="120" height="110" rx="4" fill="#e8f5e9" stroke="#333333" stroke-width="1.5"/>
  <text x="235" y="45" text-anchor="middle" font-size="14" font-weight="bold" fill="#222222">DECODE</text>
  <text x="235" y="68" text-anchor="middle" font-size="12" fill="#555">Identify</text>
  <text x="235" y="85" text-anchor="middle" font-size="12" fill="#555">opcode &amp;</text>
  <text x="235" y="102" text-anchor="middle" font-size="12" fill="#555">operands</text>
  <!-- EXECUTE -->
  <rect x="340" y="20" width="120" height="110" rx="4" fill="#fff3e0" stroke="#333333" stroke-width="1.5"/>
  <text x="400" y="45" text-anchor="middle" font-size="14" font-weight="bold" fill="#222222">EXECUTE</text>
  <text x="400" y="68" text-anchor="middle" font-size="12" fill="#555">Perform</text>
  <text x="400" y="85" text-anchor="middle" font-size="12" fill="#555">operation</text>
  <text x="400" y="102" text-anchor="middle" font-size="12" fill="#555">in ALU</text>
  <!-- WRITE-BACK -->
  <rect x="505" y="20" width="135" height="110" rx="4" fill="#fce4ec" stroke="#333333" stroke-width="1.5"/>
  <text x="572" y="45" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">WRITE-BACK</text>
  <text x="572" y="68" text-anchor="middle" font-size="12" fill="#555">Store result</text>
  <text x="572" y="85" text-anchor="middle" font-size="12" fill="#555">in register</text>
  <text x="572" y="102" text-anchor="middle" font-size="12" fill="#555">or memory</text>
  <!-- Arrows between boxes -->
  <line x1="130" y1="75" x2="175" y2="75" stroke="#555" stroke-width="1.5" marker-end="url(#arr5)"/>
  <line x1="295" y1="75" x2="340" y2="75" stroke="#555" stroke-width="1.5" marker-end="url(#arr5)"/>
  <line x1="460" y1="75" x2="505" y2="75" stroke="#555" stroke-width="1.5" marker-end="url(#arr5)"/>
  <!-- Feedback loop arrow -->
  <line x1="572" y1="130" x2="572" y2="170" stroke="#555" stroke-width="1.5"/>
  <line x1="572" y1="170" x2="70" y2="170" stroke="#555" stroke-width="1.5"/>
  <line x1="70" y1="170" x2="70" y2="130" stroke="#555" stroke-width="1.5" marker-end="url(#arr5)"/>
  <text x="320" y="190" text-anchor="middle" font-size="12" fill="#555">(next instruction)</text>
</svg>

**Step by step:**

1. **Fetch**: Read instruction at address in PC (Program Counter / RIP)
2. **Decode**: Determine what operation and which operands
3. **Execute**: ALU performs the computation or address calculation
4. **Memory Access**: Load from or store to memory (if needed)
5. **Write-Back**: Write result to destination register

---

## Example: Instruction Execution Trace

Consider the x86 instruction: `ADD RAX, RBX`

```misc
Cycle 1 - FETCH:
    Memory[RIP] → Instruction Register
    RIP = RIP + instruction_length

Cycle 2 - DECODE:
    IR = "ADD RAX, RBX"
    Opcode = ADD
    Source1 = RAX, Source2 = RBX, Dest = RAX

Cycle 3 - EXECUTE:
    ALU_input_A = value of RAX
    ALU_input_B = value of RBX
    ALU_operation = ADD
    ALU_output = A + B

Cycle 4 - WRITE-BACK:
    RAX = ALU_output
    Update RFLAGS (ZF, CF, OF, SF)
```

Without pipelining, only one instruction completes every 4+ clock cycles.

---

## Pipelining

Pipelining overlaps instruction execution stages, like an assembly line.
While one instruction is being executed, the next is being decoded, and
the one after that is being fetched.

<svg xmlns="http://www.w3.org/2000/svg" width="680" height="310" font-family="sans-serif">
  <text x="10" y="25" font-size="13" font-weight="bold" fill="#222222">Clock:</text>
  <text x="163" y="25" text-anchor="middle" font-size="13" fill="#222222">1</text>
  <text x="223" y="25" text-anchor="middle" font-size="13" fill="#222222">2</text>
  <text x="283" y="25" text-anchor="middle" font-size="13" fill="#222222">3</text>
  <text x="343" y="25" text-anchor="middle" font-size="13" fill="#222222">4</text>
  <text x="403" y="25" text-anchor="middle" font-size="13" fill="#222222">5</text>
  <text x="463" y="25" text-anchor="middle" font-size="13" fill="#222222">6</text>
  <text x="523" y="25" text-anchor="middle" font-size="13" fill="#222222">7</text>
  <text x="583" y="25" text-anchor="middle" font-size="13" fill="#222222">8</text>
  <text x="10" y="63" font-size="13" fill="#222222">Instr 1:</text>
  <rect x="135" y="40" width="55" height="38" rx="3" fill="#bbdefb" stroke="#333333" stroke-width="1.5"/>
  <text x="162" y="64" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">IF</text>
  <rect x="195" y="40" width="55" height="38" rx="3" fill="#c8e6c9" stroke="#333333" stroke-width="1.5"/>
  <text x="222" y="64" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">ID</text>
  <rect x="255" y="40" width="55" height="38" rx="3" fill="#ffe0b2" stroke="#333333" stroke-width="1.5"/>
  <text x="282" y="64" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">EX</text>
  <rect x="315" y="40" width="55" height="38" rx="3" fill="#f8bbd0" stroke="#333333" stroke-width="1.5"/>
  <text x="342" y="64" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">WB</text>
  <text x="10" y="118" font-size="13" fill="#222222">Instr 2:</text>
  <rect x="195" y="95" width="55" height="38" rx="3" fill="#bbdefb" stroke="#333333" stroke-width="1.5"/>
  <text x="222" y="119" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">IF</text>
  <rect x="255" y="95" width="55" height="38" rx="3" fill="#c8e6c9" stroke="#333333" stroke-width="1.5"/>
  <text x="282" y="119" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">ID</text>
  <rect x="315" y="95" width="55" height="38" rx="3" fill="#ffe0b2" stroke="#333333" stroke-width="1.5"/>
  <text x="342" y="119" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">EX</text>
  <rect x="375" y="95" width="55" height="38" rx="3" fill="#f8bbd0" stroke="#333333" stroke-width="1.5"/>
  <text x="402" y="119" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">WB</text>
  <text x="10" y="173" font-size="13" fill="#222222">Instr 3:</text>
  <rect x="255" y="150" width="55" height="38" rx="3" fill="#bbdefb" stroke="#333333" stroke-width="1.5"/>
  <text x="282" y="174" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">IF</text>
  <rect x="315" y="150" width="55" height="38" rx="3" fill="#c8e6c9" stroke="#333333" stroke-width="1.5"/>
  <text x="342" y="174" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">ID</text>
  <rect x="375" y="150" width="55" height="38" rx="3" fill="#ffe0b2" stroke="#333333" stroke-width="1.5"/>
  <text x="402" y="174" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">EX</text>
  <rect x="435" y="150" width="55" height="38" rx="3" fill="#f8bbd0" stroke="#333333" stroke-width="1.5"/>
  <text x="462" y="174" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">WB</text>
  <text x="10" y="228" font-size="13" fill="#222222">Instr 4:</text>
  <rect x="315" y="205" width="55" height="38" rx="3" fill="#bbdefb" stroke="#333333" stroke-width="1.5"/>
  <text x="342" y="229" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">IF</text>
  <rect x="375" y="205" width="55" height="38" rx="3" fill="#c8e6c9" stroke="#333333" stroke-width="1.5"/>
  <text x="402" y="229" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">ID</text>
  <rect x="435" y="205" width="55" height="38" rx="3" fill="#ffe0b2" stroke="#333333" stroke-width="1.5"/>
  <text x="462" y="229" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">EX</text>
  <rect x="495" y="205" width="55" height="38" rx="3" fill="#f8bbd0" stroke="#333333" stroke-width="1.5"/>
  <text x="522" y="229" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">WB</text>
  <text x="10" y="280" font-size="12" fill="#555">IF = Instruction Fetch</text>
  <text x="220" y="280" font-size="12" fill="#555">ID = Instruction Decode</text>
  <text x="10" y="298" font-size="12" fill="#555">EX = Execute</text>
  <text x="220" y="298" font-size="12" fill="#555">WB = Write Back</text>
</svg>

**Throughput**: After the pipeline is full, one instruction completes per cycle.
**Latency**: Each instruction still takes 4 cycles from start to finish.

---

## Pipeline Hazards

Three types of hazards can stall or break the pipeline:

**1. Data Hazards** -- An instruction needs data not yet produced:
```asm
ADD RAX, RBX    ; produces RAX
SUB RCX, RAX    ; needs RAX -- but ADD hasn't written it yet!
```
Solution: **forwarding/bypassing** -- route ALU output directly to next stage.

**2. Control Hazards** -- Branch instructions change flow:
```asm
CMP RAX, 0
JZ  label       ; do we take the branch? Pipeline already fetched next instr
ADD RBX, 1      ; this might need to be flushed
```
Solution: **branch prediction** (next slide).

**3. Structural Hazards** -- Two instructions need the same hardware:
```misc
Both instruction fetch and data load need memory in same cycle
```
Solution: **separate I-cache and D-cache** (Harvard architecture internally).

---

## Branch Prediction

Modern CPUs predict branch outcomes to keep the pipeline full.
A misprediction costs 10-20+ cycles (pipeline flush).

**Static prediction:**
- Always predict "not taken"
- Backward branches predicted taken (loops)

**Dynamic prediction -- 2-bit saturating counter:**

<svg xmlns="http://www.w3.org/2000/svg" width="560" height="280" font-family="sans-serif">
  <defs>
    <marker id="arr7" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 Z" fill="#555"/>
    </marker>
  </defs>
  <!-- Strongly Not Taken -->
  <rect x="30" y="30" width="140" height="60" rx="4" fill="#fce4ec" stroke="#333333" stroke-width="1.5"/>
  <text x="100" y="55" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">Strongly</text>
  <text x="100" y="75" text-anchor="middle" font-size="13" fill="#222222">Not Taken</text>
  <!-- Strongly Taken -->
  <rect x="390" y="30" width="140" height="60" rx="4" fill="#c8e6c9" stroke="#333333" stroke-width="1.5"/>
  <text x="460" y="55" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">Strongly</text>
  <text x="460" y="75" text-anchor="middle" font-size="13" fill="#222222">Taken</text>
  <!-- Weakly Not Taken -->
  <rect x="30" y="190" width="140" height="60" rx="4" fill="#ffe0b2" stroke="#333333" stroke-width="1.5"/>
  <text x="100" y="215" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">Weakly</text>
  <text x="100" y="233" text-anchor="middle" font-size="13" fill="#222222">Not Taken</text>
  <!-- Weakly Taken -->
  <rect x="390" y="190" width="140" height="60" rx="4" fill="#bbdefb" stroke="#333333" stroke-width="1.5"/>
  <text x="460" y="215" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">Weakly</text>
  <text x="460" y="233" text-anchor="middle" font-size="13" fill="#222222">Taken</text>
  <!-- Top: SNT <-taken-> ST (bidirectional via two separate arrows) -->
  <line x1="170" y1="52" x2="390" y2="52" stroke="#555" stroke-width="1.5" marker-end="url(#arr7)"/>
  <line x1="390" y1="68" x2="170" y2="68" stroke="#555" stroke-width="1.5" marker-end="url(#arr7)"/>
  <text x="280" y="46" text-anchor="middle" font-size="11" fill="#555">taken</text>
  <text x="280" y="82" text-anchor="middle" font-size="11" fill="#555">not taken</text>
  <!-- Bottom: WNT <-taken-> WT -->
  <line x1="170" y1="212" x2="390" y2="212" stroke="#555" stroke-width="1.5" marker-end="url(#arr7)"/>
  <line x1="390" y1="228" x2="170" y2="228" stroke="#555" stroke-width="1.5" marker-end="url(#arr7)"/>
  <text x="280" y="208" text-anchor="middle" font-size="11" fill="#555">taken</text>
  <text x="280" y="244" text-anchor="middle" font-size="11" fill="#555">not taken</text>
  <!-- Left: SNT -taken-> WNT -->
  <line x1="100" y1="90" x2="100" y2="190" stroke="#555" stroke-width="1.5" marker-end="url(#arr7)"/>
  <text x="55" y="145" text-anchor="middle" font-size="11" fill="#555">taken</text>
  <!-- Right: ST -not taken-> WT -->
  <line x1="460" y1="90" x2="460" y2="190" stroke="#555" stroke-width="1.5" marker-end="url(#arr7)"/>
  <text x="515" y="145" text-anchor="middle" font-size="11" fill="#555">not taken</text>
</svg>

Modern CPUs (like Intel Alder Lake) use neural branch predictors with
97%+ accuracy on typical workloads.

---

## Branch Prediction Impact

Why does branch prediction matter? Consider a tight loop:

```c
// Summing an array -- branch at loop condition
int sum = 0;
for (int i = 0; i < N; i++) {   // branch: i < N
    if (data[i] > 128) {         // branch: data dependent
        sum += data[i];
    }
}
```

If `data` is sorted, the `data[i] > 128` branch is highly predictable:
first all "not taken", then all "taken". Prediction accuracy ~99%.

If `data` is unsorted, the branch is essentially random.
Prediction accuracy ~50%. Massive performance penalty.

**Benchmark result (typical):**
| Data | Time |
|------|------|
| Sorted array | ~5 ms |
| Unsorted array | ~15 ms |

Same algorithm, same data, 3x slowdown from branch misprediction.

---

## Superscalar Execution

A superscalar CPU can issue multiple instructions per clock cycle.
It has multiple execution units working in parallel.

<svg xmlns="http://www.w3.org/2000/svg" width="640" height="350" font-family="sans-serif">
  <defs>
    <marker id="arr8" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 Z" fill="#555"/>
    </marker>
  </defs>
  <!-- Outer box -->
  <rect x="10" y="10" width="620" height="330" rx="4" fill="#e3f2fd" stroke="#333333" stroke-width="1.5"/>
  <text x="320" y="35" text-anchor="middle" font-size="15" font-weight="bold" fill="#222222">Superscalar CPU</text>
  <!-- Fetch & Decode -->
  <rect x="40" y="50" width="550" height="55" rx="4" fill="#f0f4f8" stroke="#333333" stroke-width="1.5"/>
  <text x="315" y="74" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">Instruction Fetch &amp; Decode</text>
  <text x="315" y="93" text-anchor="middle" font-size="12" fill="#555">(fetches 4–6 instr/cycle)</text>
  <!-- Arrow -->
  <line x1="315" y1="105" x2="315" y2="125" stroke="#555" stroke-width="1.5" marker-end="url(#arr8)"/>
  <!-- Scheduler -->
  <rect x="40" y="125" width="550" height="55" rx="4" fill="#f0f4f8" stroke="#333333" stroke-width="1.5"/>
  <text x="315" y="149" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">Instruction Scheduler</text>
  <text x="315" y="168" text-anchor="middle" font-size="12" fill="#555">(out-of-order dispatch)</text>
  <!-- Lines down to execution units -->
  <line x1="315" y1="180" x2="315" y2="210" stroke="#555" stroke-width="1.5"/>
  <line x1="67" y1="210" x2="562" y2="210" stroke="#555" stroke-width="1.5"/>
  <!-- 6 execution units -->
  <!-- x positions: 40, 140, 240, 340, 440, 530 -->
  <line x1="67"  y1="210" x2="67"  y2="230" stroke="#555" stroke-width="1.5" marker-end="url(#arr8)"/>
  <line x1="162" y1="210" x2="162" y2="230" stroke="#555" stroke-width="1.5" marker-end="url(#arr8)"/>
  <line x1="257" y1="210" x2="257" y2="230" stroke="#555" stroke-width="1.5" marker-end="url(#arr8)"/>
  <line x1="352" y1="210" x2="352" y2="230" stroke="#555" stroke-width="1.5" marker-end="url(#arr8)"/>
  <line x1="447" y1="210" x2="447" y2="230" stroke="#555" stroke-width="1.5" marker-end="url(#arr8)"/>
  <line x1="533" y1="210" x2="533" y2="230" stroke="#555" stroke-width="1.5" marker-end="url(#arr8)"/>
  <!-- ALU 1 -->
  <rect x="30"  y="230" width="75" height="45" rx="4" fill="#e8f5e9" stroke="#333333" stroke-width="1.5"/>
  <text x="67"  y="257" text-anchor="middle" font-size="13" fill="#222222">ALU 1</text>
  <!-- ALU 2 -->
  <rect x="125" y="230" width="75" height="45" rx="4" fill="#e8f5e9" stroke="#333333" stroke-width="1.5"/>
  <text x="162" y="257" text-anchor="middle" font-size="13" fill="#222222">ALU 2</text>
  <!-- ALU 3 -->
  <rect x="220" y="230" width="75" height="45" rx="4" fill="#e8f5e9" stroke="#333333" stroke-width="1.5"/>
  <text x="257" y="257" text-anchor="middle" font-size="13" fill="#222222">ALU 3</text>
  <!-- FPU 1 -->
  <rect x="315" y="230" width="75" height="45" rx="4" fill="#fff3e0" stroke="#333333" stroke-width="1.5"/>
  <text x="352" y="257" text-anchor="middle" font-size="13" fill="#222222">FPU 1</text>
  <!-- FPU 2 -->
  <rect x="410" y="230" width="75" height="45" rx="4" fill="#fff3e0" stroke="#333333" stroke-width="1.5"/>
  <text x="447" y="257" text-anchor="middle" font-size="13" fill="#222222">FPU 2</text>
  <!-- AGU -->
  <rect x="496" y="230" width="75" height="45" rx="4" fill="#fce4ec" stroke="#333333" stroke-width="1.5"/>
  <text x="533" y="257" text-anchor="middle" font-size="13" fill="#222222">AGU</text>
  <!-- Legend -->
  <text x="40" y="302" font-size="12" fill="#555">ALU = Arithmetic Logic Unit</text>
  <text x="40" y="320" font-size="12" fill="#555">FPU = Floating Point Unit   AGU = Address Generation Unit</text>
</svg>

A modern Intel/AMD core can retire 4-6 instructions per cycle.

---

## Out-of-Order Execution

Modern CPUs do not execute instructions in program order. They find
independent instructions and execute them whenever their operands are ready.

```misc
Original order:           Reordered execution:
1: LOAD  R1, [addr1]      1: LOAD R1, [addr1]    (cycle 1, cache miss!)
2: ADD   R2, R1, 1        4: MUL  R5, R3, R4     (cycle 1, independent)
3: STORE [addr2], R2      5: ADD  R6, R5, 1      (cycle 2, depends on 4)
4: MUL   R5, R3, R4       2: ADD  R2, R1, 1      (cycle ~50, R1 ready)
5: ADD   R6, R5, 1        3: STORE [addr2], R2   (cycle 51)
```

Key hardware for OoO execution:
- **Reorder Buffer (ROB)**: tracks instruction order for correct retirement
- **Reservation Stations**: hold instructions waiting for operands
- **Register Renaming**: eliminates false dependencies (WAR, WAW hazards)

---

## CISC vs RISC

Two fundamental CPU design philosophies:

| Aspect | CISC | RISC |
|--------|------|------|
| Full name | Complex Instruction Set | Reduced Instruction Set |
| Instructions | Many, variable-length | Few, fixed-length |
| Complexity | In hardware | In compiler |
| Examples | x86, x86-64 | ARM, RISC-V, MIPS, PowerPC |
| Registers | Fewer (historically) | Many (32+) |
| Memory access | Many instructions can access memory | Load/Store only |
| Encoding | Variable (1-15 bytes on x86) | Fixed (4 bytes on ARM) |
| Decode | Complex, multi-cycle | Simple, single-cycle |
| Power efficiency | Higher power | Lower power |
| Philosophy | Do more per instruction | Do less but faster |

---

## CISC Example: x86

x86 has complex instructions that do multiple things at once:

```asm
; x86: single instruction does load + compare + conditional jump
REP MOVSB          ; copy RCX bytes from [RSI] to [RDI]
                   ; equivalent to a memcpy loop!

LOOP label         ; decrement RCX, jump if not zero

ENTER 16, 0        ; create stack frame: push RBP, mov RBP RSP, sub RSP 16
```

Variable-length instruction encoding:
```misc
90                      ; NOP                    (1 byte)
48 89 C3                ; MOV RBX, RAX           (3 bytes)
48 C7 C0 01 00 00 00    ; MOV RAX, 1             (7 bytes)
C4 E2 7D 36 04 0E       ; VPERMD YMM0, YMM0...  (6 bytes)
```

Modern x86 CPUs internally decompose CISC instructions into micro-ops (uops)
that are RISC-like internally.

---

## RISC Example: ARM

ARM has simple, fixed-size instructions:

```asm
; ARM AArch64: all instructions are 4 bytes
ADD  X0, X1, X2        ; X0 = X1 + X2
LDR  X3, [X4, #8]      ; X3 = memory[X4 + 8]
STR  X5, [X6]           ; memory[X6] = X5
CBZ  X0, label          ; compare and branch if zero
```

ARM design principles:
- All instructions same size (easy to decode, easy to pipeline)
- Load/Store architecture (only LDR/STR access memory)
- Conditional execution (reduces branches)
- Large register file (31 general-purpose 64-bit registers)

---

## x86 vs ARM: Modern Comparison

| Feature | x86-64 (Intel/AMD) | ARM (AArch64) |
|---------|-------------------|----------------|
| Market | Desktop, Server, Laptop | Mobile, Embedded, Server |
| Power | 15-250W typical | 1-30W typical |
| Performance/Watt | Good | Excellent |
| ISA license | Intel/AMD only | Licensed to many vendors |
| Software | Vast legacy ecosystem | Growing rapidly |
| Server examples | Intel Xeon, AMD EPYC | AWS Graviton, Ampere Altra |
| Desktop examples | Intel Core, AMD Ryzen | Apple M-series |
| Decode complexity | High (variable length) | Low (fixed length) |
| Transistor budget | More on decode | More on execution units |

Apple's M-series chips demonstrated that ARM can match or exceed x86
performance while using far less power.

---

## The Memory Wall Problem

CPU speed has grown much faster than memory speed. This gap is the
"memory wall" and is the reason caches exist.

<svg xmlns="http://www.w3.org/2000/svg" width="640" height="430" font-family="sans-serif">
  <text x="20" y="25" font-size="14" font-weight="bold" fill="#222222">Access Time (approximate):</text>
  <rect x="10" y="35" width="620" height="30" rx="4" fill="#37474f" stroke="#333333" stroke-width="1.5"/>
  <text x="100" y="55" text-anchor="middle" font-size="13" font-weight="bold" fill="white">Level</text>
  <text x="280" y="55" text-anchor="middle" font-size="13" font-weight="bold" fill="white">Access Time</text>
  <text x="450" y="55" text-anchor="middle" font-size="13" font-weight="bold" fill="white">CPU Cycles</text>
  <rect x="10" y="65" width="620" height="30" rx="0" fill="#bbdefb" stroke="#aaa" stroke-width="0.5"/>
  <text x="100" y="85" text-anchor="middle" font-size="13" fill="#222222">Register</text>
  <text x="280" y="85" text-anchor="middle" font-size="13" fill="#222222">~0.3 ns</text>
  <text x="450" y="85" text-anchor="middle" font-size="13" fill="#222222">1 cycle</text>
  <rect x="10" y="95" width="620" height="30" rx="0" fill="#c8e6c9" stroke="#aaa" stroke-width="0.5"/>
  <text x="100" y="115" text-anchor="middle" font-size="13" fill="#222222">L1 Cache</text>
  <text x="280" y="115" text-anchor="middle" font-size="13" fill="#222222">~1 ns</text>
  <text x="450" y="115" text-anchor="middle" font-size="13" fill="#222222">3–4 cycles</text>
  <rect x="10" y="125" width="620" height="30" rx="0" fill="#dcedc8" stroke="#aaa" stroke-width="0.5"/>
  <text x="100" y="145" text-anchor="middle" font-size="13" fill="#222222">L2 Cache</text>
  <text x="280" y="145" text-anchor="middle" font-size="13" fill="#222222">~3–5 ns</text>
  <text x="450" y="145" text-anchor="middle" font-size="13" fill="#222222">10–15 cycles</text>
  <rect x="10" y="155" width="620" height="30" rx="0" fill="#fff9c4" stroke="#aaa" stroke-width="0.5"/>
  <text x="100" y="175" text-anchor="middle" font-size="13" fill="#222222">L3 Cache</text>
  <text x="280" y="175" text-anchor="middle" font-size="13" fill="#222222">~10–20 ns</text>
  <text x="450" y="175" text-anchor="middle" font-size="13" fill="#222222">30–60 cycles</text>
  <rect x="10" y="185" width="620" height="30" rx="0" fill="#ffe0b2" stroke="#aaa" stroke-width="0.5"/>
  <text x="100" y="205" text-anchor="middle" font-size="13" fill="#222222">Main Memory</text>
  <text x="280" y="205" text-anchor="middle" font-size="13" fill="#222222">~50–100 ns</text>
  <text x="450" y="205" text-anchor="middle" font-size="13" fill="#222222">150–300 cyc</text>
  <rect x="10" y="215" width="620" height="30" rx="0" fill="#ffccbc" stroke="#aaa" stroke-width="0.5"/>
  <text x="100" y="235" text-anchor="middle" font-size="13" fill="#222222">SSD</text>
  <text x="280" y="235" text-anchor="middle" font-size="13" fill="#222222">~100 µs</text>
  <text x="450" y="235" text-anchor="middle" font-size="13" fill="#222222">300k cycles</text>
  <rect x="10" y="245" width="620" height="30" rx="0" fill="#ffcdd2" stroke="#aaa" stroke-width="0.5"/>
  <text x="100" y="265" text-anchor="middle" font-size="13" fill="#222222">HDD</text>
  <text x="280" y="265" text-anchor="middle" font-size="13" fill="#222222">~10 ms</text>
  <text x="450" y="265" text-anchor="middle" font-size="13" fill="#222222">30M cycles</text>
  <text x="20" y="300" font-size="14" font-weight="bold" fill="#222222">Analogy (if register = 1 second):</text>
  <text x="30" y="315" font-size="13" fill="#555">■ <tspan font-weight="bold" fill="#222222">Register:</tspan>  1 second</text>
  <text x="30" y="331" font-size="13" fill="#555">■ <tspan font-weight="bold" fill="#222222">L1 Cache:</tspan>  3 seconds</text>
  <text x="30" y="347" font-size="13" fill="#555">■ <tspan font-weight="bold" fill="#222222">L2 Cache:</tspan>  15 seconds</text>
  <text x="30" y="363" font-size="13" fill="#555">■ <tspan font-weight="bold" fill="#222222">L3 Cache:</tspan>  1 minute</text>
  <text x="30" y="379" font-size="13" fill="#555">■ <tspan font-weight="bold" fill="#222222">Main Memory:</tspan>  5 minutes</text>
  <text x="30" y="395" font-size="13" fill="#555">■ <tspan font-weight="bold" fill="#222222">SSD:</tspan>  3.8 days</text>
  <text x="30" y="411" font-size="13" fill="#555">■ <tspan font-weight="bold" fill="#222222">HDD:</tspan>  1 year</text>
</svg>

---

## Cache Hierarchy

Modern CPUs use a multi-level cache hierarchy to bridge the memory wall:

<svg xmlns="http://www.w3.org/2000/svg" width="620" height="380" font-family="sans-serif">
  <defs>
    <marker id="arr10" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 Z" fill="#555"/>
    </marker>
  </defs>
  <!-- CPU Core 0 outer box -->
  <rect x="10" y="10" width="600" height="150" rx="4" fill="#e3f2fd" stroke="#333333" stroke-width="1.5"/>
  <text x="310" y="32" text-anchor="middle" font-size="14" font-weight="bold" fill="#222222">CPU Core 0</text>
  <!-- L1 I + D caches (side by side) -->
  <rect x="30" y="45" width="260" height="55" rx="4" fill="#bbdefb" stroke="#333333" stroke-width="1.5"/>
  <text x="160" y="67" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">L1 I-Cache</text>
  <text x="160" y="87" text-anchor="middle" font-size="12" fill="#555">32 KB, ~1 ns</text>
  <rect x="310" y="45" width="280" height="55" rx="4" fill="#bbdefb" stroke="#333333" stroke-width="1.5"/>
  <text x="450" y="67" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">L1 D-Cache</text>
  <text x="450" y="87" text-anchor="middle" font-size="12" fill="#555">32–48 KB, ~1 ns</text>
  <!-- L2 cache -->
  <rect x="30" y="115" width="560" height="35" rx="4" fill="#c8e6c9" stroke="#333333" stroke-width="1.5"/>
  <text x="310" y="133" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">L2 Cache (Unified)  –  256 KB – 1.25 MB, ~3–5 ns</text>
  <!-- Arrow from L2 down -->
  <line x1="310" y1="160" x2="310" y2="185" stroke="#555" stroke-width="1.5" marker-end="url(#arr10)"/>
  <!-- L3 cache -->
  <rect x="10" y="185" width="600" height="50" rx="4" fill="#dce775" stroke="#333333" stroke-width="1.5"/>
  <text x="310" y="207" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">L3 Cache (Shared across cores)</text>
  <text x="310" y="226" text-anchor="middle" font-size="12" fill="#555">8–96 MB, ~10–20 ns</text>
  <!-- Arrow from L3 down -->
  <line x1="310" y1="235" x2="310" y2="260" stroke="#555" stroke-width="1.5" marker-end="url(#arr10)"/>
  <!-- Main Memory -->
  <rect x="10" y="260" width="600" height="50" rx="4" fill="#ffcc80" stroke="#333333" stroke-width="1.5"/>
  <text x="310" y="282" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">Main Memory (DRAM)</text>
  <text x="310" y="301" text-anchor="middle" font-size="12" fill="#555">8–512+ GB, ~50–100 ns</text>
  <!-- Note about arrow direction -->
  <text x="310" y="340" text-anchor="middle" font-size="12" fill="#888">← smaller &amp; faster        larger &amp; slower →</text>
</svg>

L1 is split into instruction cache (I-Cache) and data cache (D-Cache).
L2 and L3 are unified (hold both instructions and data).

---

## Cache Lines and Spatial Locality

Caches do not store individual bytes. They store **cache lines**, typically
64 bytes on x86.

<svg xmlns="http://www.w3.org/2000/svg" width="640" height="150" font-family="sans-serif">
  <!-- Title -->
  <text x="10" y="22" font-size="13" font-weight="bold" fill="#222222">Memory address: 0x1000</text>
  <!-- Cache line box with 5 visible cells -->
  <text x="10" y="55" font-size="13" fill="#555">Cache line:</text>
  <!-- cells -->
  <rect x="100" y="35" width="70" height="35" rx="2" fill="#bbdefb" stroke="#333333" stroke-width="1.5"/>
  <text x="135" y="57" text-anchor="middle" font-size="12" fill="#222222">byte 0</text>
  <rect x="170" y="35" width="70" height="35" rx="2" fill="#c8e6c9" stroke="#333333" stroke-width="1.5"/>
  <text x="205" y="57" text-anchor="middle" font-size="12" fill="#222222">byte 1</text>
  <rect x="240" y="35" width="70" height="35" rx="2" fill="#ffe0b2" stroke="#333333" stroke-width="1.5"/>
  <text x="275" y="57" text-anchor="middle" font-size="12" fill="#222222">byte 2</text>
  <rect x="310" y="35" width="70" height="35" rx="2" fill="#f0f4f8" stroke="#333333" stroke-width="1.5"/>
  <text x="345" y="57" text-anchor="middle" font-size="12" fill="#555">...</text>
  <rect x="380" y="35" width="80" height="35" rx="2" fill="#fce4ec" stroke="#333333" stroke-width="1.5"/>
  <text x="420" y="57" text-anchor="middle" font-size="12" fill="#222222">byte 63</text>
  <!-- Address labels below -->
  <text x="135" y="88" text-anchor="middle" font-size="11" fill="#555">0x1000</text>
  <text x="205" y="88" text-anchor="middle" font-size="11" fill="#555">0x1001</text>
  <text x="275" y="88" text-anchor="middle" font-size="11" fill="#555">0x1002</text>
  <text x="420" y="88" text-anchor="middle" font-size="11" fill="#555">0x103F</text>
  <!-- Note -->
  <text x="10" y="115" font-size="12" fill="#555">When you access address 0x1010, the entire 64-byte line (0x1000–0x103F) is loaded into cache.</text>
</svg>

This exploits **spatial locality**: if you access one byte, you are likely
to access nearby bytes soon.

**Implication for programming:**
```c
// GOOD: sequential access, uses spatial locality
for (int i = 0; i < N; i++)
    sum += array[i];          // next element is in same cache line

// BAD: strided access, wastes cache lines
for (int i = 0; i < N; i += 16)
    sum += array[i];          // skips most of each cache line
```

---

## Cache Associativity

Where can a cache line be placed? This defines associativity:

<svg xmlns="http://www.w3.org/2000/svg" width="640" height="340" font-family="sans-serif">
  <!-- Direct-mapped title -->
  <text x="10" y="22" font-size="14" font-weight="bold" fill="#222222">Direct-mapped (1-way)</text>
  <text x="10" y="40" font-size="12" fill="#555">Each address maps to exactly one cache slot</text>
  <!-- 8 slots -->
  <text x="10" y="70" font-size="12" fill="#555">Slots:</text>
  <rect x="50"  y="55" width="50" height="30" rx="2" fill="#bbdefb" stroke="#333333" stroke-width="1.5"/>
  <text x="75"  y="75" text-anchor="middle" font-size="13" fill="#222222">0</text>
  <rect x="100" y="55" width="50" height="30" rx="2" fill="#c8e6c9" stroke="#333333" stroke-width="1.5"/>
  <text x="125" y="75" text-anchor="middle" font-size="13" fill="#222222">1</text>
  <rect x="150" y="55" width="50" height="30" rx="2" fill="#ffe0b2" stroke="#333333" stroke-width="1.5"/>
  <text x="175" y="75" text-anchor="middle" font-size="13" fill="#222222">2</text>
  <rect x="200" y="55" width="50" height="30" rx="2" fill="#fce4ec" stroke="#333333" stroke-width="1.5"/>
  <text x="225" y="75" text-anchor="middle" font-size="13" fill="#222222">3</text>
  <rect x="250" y="55" width="50" height="30" rx="2" fill="#bbdefb" stroke="#333333" stroke-width="1.5"/>
  <text x="275" y="75" text-anchor="middle" font-size="13" fill="#222222">4</text>
  <rect x="300" y="55" width="50" height="30" rx="2" fill="#c8e6c9" stroke="#333333" stroke-width="1.5"/>
  <text x="325" y="75" text-anchor="middle" font-size="13" fill="#222222">5</text>
  <rect x="350" y="55" width="50" height="30" rx="2" fill="#ffe0b2" stroke="#333333" stroke-width="1.5"/>
  <text x="375" y="75" text-anchor="middle" font-size="13" fill="#222222">6</text>
  <rect x="400" y="55" width="50" height="30" rx="2" fill="#fce4ec" stroke="#333333" stroke-width="1.5"/>
  <text x="425" y="75" text-anchor="middle" font-size="13" fill="#222222">7</text>
  <text x="10" y="112" font-size="12" fill="#555">Address 0x100 → always slot 0  (conflict if 0x200 also maps here)</text>
  <!-- Divider -->
  <line x1="10" y1="130" x2="630" y2="130" stroke="#ccc" stroke-width="1"/>
  <!-- Fully associative -->
  <text x="10" y="152" font-size="14" font-weight="bold" fill="#222222">Fully Associative</text>
  <text x="10" y="170" font-size="12" fill="#555">Any address can go in any slot – most flexible but expensive to search.</text>
  <!-- Divider -->
  <line x1="10" y1="186" x2="630" y2="186" stroke="#ccc" stroke-width="1"/>
  <!-- N-way set associative -->
  <text x="10" y="208" font-size="14" font-weight="bold" fill="#222222">N-way Set Associative</text>
  <text x="10" y="226" font-size="12" fill="#555">Each address maps to a SET of N slots (ways).</text>
  <!-- 3 sets -->
  <rect x="30"  y="240" width="170" height="55" rx="4" fill="#e3f2fd" stroke="#333333" stroke-width="1.5"/>
  <text x="115" y="260" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">Set 0</text>
  <text x="115" y="283" text-anchor="middle" font-size="12" fill="#555">Way0  Way1 … WayN</text>
  <rect x="230" y="240" width="170" height="55" rx="4" fill="#e8f5e9" stroke="#333333" stroke-width="1.5"/>
  <text x="315" y="260" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">Set 1</text>
  <text x="315" y="283" text-anchor="middle" font-size="12" fill="#555">Way0  Way1 … WayN</text>
  <rect x="430" y="240" width="170" height="55" rx="4" fill="#fff3e0" stroke="#333333" stroke-width="1.5"/>
  <text x="515" y="260" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">Set 2</text>
  <text x="515" y="283" text-anchor="middle" font-size="12" fill="#555">Way0  Way1 … WayN</text>
  <text x="10" y="320" font-size="12" fill="#555">Modern L1: 8–12 way   L2: 8–16 way   L3: 12–20 way</text>
</svg>

**Typical modern CPUs:**
- L1: 8-12 way set associative
- L2: 8-16 way set associative
- L3: 12-20 way set associative

---

## Cache Replacement Policies

When a cache set is full and a new line must be loaded, which line is evicted?

| Policy | Description | Used In |
|--------|-------------|---------|
| LRU | Least Recently Used | Approximated in L1/L2 |
| Pseudo-LRU | Tree-based LRU approximation | Common in hardware |
| Random | Randomly select victim | Some ARM designs |
| RRIP | Re-Reference Interval Prediction | Intel L3 |

**LRU example (4-way set):**
```misc
Access sequence: A B C D E

After A: [A _ _ _]         A is most recent
After B: [A B _ _]         B is most recent
After C: [A B C _]         C is most recent
After D: [A B C D]         Full, A is LRU
After E: [E B C D]         A evicted (was LRU), E takes its place
```

---

## Write Policies

When the CPU writes data, when does it update main memory?

**Write-Through:**
<svg xmlns="http://www.w3.org/2000/svg" width="620" height="120" font-family="sans-serif">
  <defs>
    <marker id="arr13" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 Z" fill="#555"/>
    </marker>
  </defs>
  <!-- CPU Write -->
  <rect x="10" y="30" width="110" height="40" rx="4" fill="#e3f2fd" stroke="#333333" stroke-width="1.5"/>
  <text x="65" y="55" text-anchor="middle" font-size="13" fill="#222222">CPU Write</text>
  <line x1="120" y1="50" x2="165" y2="50" stroke="#555" stroke-width="1.5" marker-end="url(#arr13)"/>
  <!-- Update Cache -->
  <rect x="165" y="30" width="130" height="40" rx="4" fill="#c8e6c9" stroke="#333333" stroke-width="1.5"/>
  <text x="230" y="55" text-anchor="middle" font-size="13" fill="#222222">Update Cache</text>
  <line x1="295" y1="50" x2="340" y2="50" stroke="#555" stroke-width="1.5" marker-end="url(#arr13)"/>
  <!-- Update Memory -->
  <rect x="340" y="30" width="170" height="40" rx="4" fill="#ffcc80" stroke="#333333" stroke-width="1.5"/>
  <text x="425" y="48" text-anchor="middle" font-size="13" fill="#222222">Update Memory</text>
  <text x="425" y="65" text-anchor="middle" font-size="11" fill="#555">(immediately)</text>
  <!-- Note -->
  <text x="340" y="95" font-size="12" fill="#555">Slow but simple. Memory always consistent with cache.</text>
</svg>

**Write-Back:**
<svg xmlns="http://www.w3.org/2000/svg" width="620" height="130" font-family="sans-serif">
  <defs>
    <marker id="arr14" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 Z" fill="#555"/>
    </marker>
  </defs>
  <!-- CPU Write -->
  <rect x="10" y="30" width="110" height="40" rx="4" fill="#e3f2fd" stroke="#333333" stroke-width="1.5"/>
  <text x="65" y="55" text-anchor="middle" font-size="13" fill="#222222">CPU Write</text>
  <line x1="120" y1="50" x2="165" y2="50" stroke="#555" stroke-width="1.5" marker-end="url(#arr14)"/>
  <!-- Update Cache -->
  <rect x="165" y="30" width="130" height="40" rx="4" fill="#c8e6c9" stroke="#333333" stroke-width="1.5"/>
  <text x="230" y="55" text-anchor="middle" font-size="13" fill="#222222">Update Cache</text>
  <line x1="295" y1="50" x2="340" y2="50" stroke="#555" stroke-width="1.5" marker-end="url(#arr14)"/>
  <!-- Mark Dirty -->
  <rect x="340" y="30" width="150" height="40" rx="4" fill="#fce4ec" stroke="#333333" stroke-width="1.5"/>
  <text x="415" y="48" text-anchor="middle" font-size="13" fill="#222222">Mark line</text>
  <text x="415" y="65" text-anchor="middle" font-size="13" fill="#222222">"dirty"</text>
  <!-- Note -->
  <text x="10" y="100" font-size="12" fill="#555">Memory updated only on eviction. Fast but complex. Used in modern CPUs.</text>
</svg>

**Write-Allocate vs No-Write-Allocate:**
- Write-Allocate: on a write miss, load the line into cache first, then write
- No-Write-Allocate: on a write miss, write directly to memory, skip cache

Modern CPUs typically use **write-back + write-allocate**.

---

## Cache Coherence Problem

In multi-core systems, each core has its own L1/L2 cache. If two cores
cache the same memory address, writes by one core must be visible to others.

<svg xmlns="http://www.w3.org/2000/svg" width="580" height="280" font-family="sans-serif">
  <defs>
    <marker id="arr15" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 Z" fill="#555"/>
    </marker>
  </defs>
  <!-- Core 0 label -->
  <text x="110" y="22" text-anchor="middle" font-size="14" font-weight="bold" fill="#222222">Core 0</text>
  <!-- Core 1 label -->
  <text x="450" y="22" text-anchor="middle" font-size="14" font-weight="bold" fill="#222222">Core 1</text>
  <!-- Core 0 initial cache -->
  <rect x="30" y="35" width="160" height="60" rx="4" fill="#e3f2fd" stroke="#333333" stroke-width="1.5"/>
  <text x="110" y="57" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">L1 Cache</text>
  <text x="110" y="78" text-anchor="middle" font-size="13" fill="#222222">X = 42</text>
  <!-- Core 1 initial cache -->
  <rect x="390" y="35" width="160" height="60" rx="4" fill="#e3f2fd" stroke="#333333" stroke-width="1.5"/>
  <text x="470" y="57" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">L1 Cache</text>
  <text x="470" y="78" text-anchor="middle" font-size="13" fill="#222222">X = 42</text>
  <text x="290" y="65" text-anchor="middle" font-size="11" fill="#555">(both cached same address)</text>
  <!-- Core 0 writes -->
  <text x="110" y="125" text-anchor="middle" font-size="12" fill="#cc0000">Core 0 writes X = 99</text>
  <!-- Core 0 after write -->
  <rect x="30" y="140" width="160" height="60" rx="4" fill="#c8e6c9" stroke="#333333" stroke-width="1.5"/>
  <text x="110" y="162" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">L1 Cache</text>
  <text x="110" y="183" text-anchor="middle" font-size="13" fill="#cc0000">X = 99</text>
  <!-- Core 1 still stale -->
  <rect x="390" y="140" width="160" height="60" rx="4" fill="#ffcdd2" stroke="#cc0000" stroke-width="2"/>
  <text x="470" y="162" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">L1 Cache</text>
  <text x="470" y="183" text-anchor="middle" font-size="13" fill="#cc0000">X = 42  ← STALE!</text>
  <!-- INCOHERENT label -->
  <text x="290" y="220" text-anchor="middle" font-size="14" font-weight="bold" fill="#cc0000">INCOHERENT!</text>
  <text x="290" y="240" text-anchor="middle" font-size="12" fill="#555">Core 1 still sees the old value.</text>
  <text x="290" y="258" text-anchor="middle" font-size="12" fill="#555">Solution: cache coherence protocols (e.g. MESI)</text>
</svg>

Solution: **cache coherence protocols**.

---

## MESI Protocol

The most common cache coherence protocol. Each cache line has one of
four states:

| State | Meaning |
|-------|---------|
| **M**odified | Line is dirty, only in this cache, must write back |
| **E**xclusive | Line is clean, only in this cache |
| **S**hared | Line is clean, may be in other caches too |
| **I**nvalid | Line is not valid, treat as cache miss |

<svg xmlns="http://www.w3.org/2000/svg" width="620" height="340" font-family="sans-serif">
  <defs>
    <marker id="arr16" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 Z" fill="#555"/>
    </marker>
  </defs>
  <text x="310" y="22" text-anchor="middle" font-size="14" font-weight="bold" fill="#222222">MESI Cache Coherence State Transitions</text>
  <!-- I (Invalid) – bottom left -->
  <rect x="30"  y="240" width="100" height="50" rx="4" fill="#ffcdd2" stroke="#333333" stroke-width="1.5"/>
  <text x="80"  y="270" text-anchor="middle" font-size="16" font-weight="bold" fill="#222222">I</text>
  <text x="80"  y="286" text-anchor="middle" font-size="11" fill="#555">Invalid</text>
  <!-- S (Shared) – bottom right -->
  <rect x="490" y="240" width="100" height="50" rx="4" fill="#fff9c4" stroke="#333333" stroke-width="1.5"/>
  <text x="540" y="270" text-anchor="middle" font-size="16" font-weight="bold" fill="#222222">S</text>
  <text x="540" y="286" text-anchor="middle" font-size="11" fill="#555">Shared</text>
  <!-- E (Exclusive) – top left -->
  <rect x="30"  y="60" width="100" height="50" rx="4" fill="#c8e6c9" stroke="#333333" stroke-width="1.5"/>
  <text x="80"  y="90" text-anchor="middle" font-size="16" font-weight="bold" fill="#222222">E</text>
  <text x="80"  y="106" text-anchor="middle" font-size="11" fill="#555">Exclusive</text>
  <!-- M (Modified) – top right -->
  <rect x="490" y="60" width="100" height="50" rx="4" fill="#bbdefb" stroke="#333333" stroke-width="1.5"/>
  <text x="540" y="90" text-anchor="middle" font-size="16" font-weight="bold" fill="#222222">M</text>
  <text x="540" y="106" text-anchor="middle" font-size="11" fill="#555">Modified</text>
  <!-- I -> S: Read (other cores may have it) -->
  <line x1="130" y1="262" x2="490" y2="262" stroke="#555" stroke-width="1.5" marker-end="url(#arr16)"/>
  <text x="310" y="256" text-anchor="middle" font-size="11" fill="#555">Read (shared)</text>
  <!-- I -> E: Read (exclusive, no other copy) -->
  <line x1="80" y1="240" x2="80" y2="110" stroke="#555" stroke-width="1.5" marker-end="url(#arr16)"/>
  <text x="50" y="180" text-anchor="middle" font-size="11" fill="#555" transform="rotate(-90,50,180)">Read hit / excl</text>
  <!-- E -> M: Write hit -->
  <line x1="130" y1="85" x2="490" y2="85" stroke="#555" stroke-width="1.5" marker-end="url(#arr16)"/>
  <text x="310" y="79" text-anchor="middle" font-size="11" fill="#555">Write hit</text>
  <!-- M -> S: Other core reads (flush) -->
  <line x1="540" y1="110" x2="540" y2="240" stroke="#555" stroke-width="1.5" marker-end="url(#arr16)"/>
  <text x="590" y="180" text-anchor="middle" font-size="10" fill="#555" transform="rotate(90,590,180)">Other core reads (flush)</text>
  <!-- S -> M: Write (invalidate others) -->
  <line x1="540" y1="240" x2="540" y2="115" stroke="transparent" stroke-width="0"/>
  <!-- curved arrow hint via path: S -> M write -->
  <path d="M490,252 Q310,200 490,110" stroke="#777" stroke-width="1.5" fill="none" stroke-dasharray="5,3" marker-end="url(#arr16)"/>
  <text x="370" y="195" text-anchor="middle" font-size="11" fill="#777">Write → invalidate others</text>
  <!-- E -> S: Other core reads -->
  <path d="M130,70 Q310,40 490,70" stroke="#999" stroke-width="1.5" fill="none" stroke-dasharray="5,3" marker-end="url(#arr16)"/>
  <text x="310" y="42" text-anchor="middle" font-size="11" fill="#888">Other core reads</text>
  <!-- S -> I: Invalidate received -->
  <path d="M490,285 Q310,315 130,285" stroke="#cc0000" stroke-width="1.5" fill="none" stroke-dasharray="5,3" marker-end="url(#arr16)"/>
  <text x="310" y="325" text-anchor="middle" font-size="11" fill="#cc0000">Invalidate received</text>
</svg>

When Core 0 writes to a Shared line, it sends an "invalidate" message
to all other cores, forcing them to mark their copies Invalid.

---

## Cache Performance: Key Metrics

Understanding cache behavior is essential for performance tuning:

**Hit rate**: percentage of accesses found in cache (target: >95% for L1)

**Miss types:**
- **Compulsory (cold)**: first access to a line, unavoidable
- **Capacity**: cache is too small to hold all needed data
- **Conflict**: multiple addresses map to same set

**Measuring cache performance on Linux:**

```bash
# Using perf to measure cache misses
perf stat -e cache-references,cache-misses,L1-dcache-loads,\
L1-dcache-load-misses,LLC-loads,LLC-load-misses ./my_program

# Example output:
#  1,234,567,890  cache-references
#      5,678,901  cache-misses     # 0.46% of all refs
#  2,345,678,901  L1-dcache-loads
#     12,345,678  L1-dcache-load-misses  # 0.53% of L1 loads
```

---

## Summary: CPU Architecture

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="400" font-family="sans-serif">
  <!-- Outer box -->
  <rect x="10" y="10" width="640" height="380" rx="4" fill="#f0f4f8" stroke="#333333" stroke-width="1.5"/>
  <!-- Title bar -->
  <rect x="10" y="10" width="640" height="38" rx="4" fill="#37474f" stroke="#333333" stroke-width="1.5"/>
  <text x="330" y="35" text-anchor="middle" font-size="15" font-weight="bold" fill="white">Modern CPU Overview</text>
  <!-- Section: Core Components -->
  <rect x="25" y="60" width="290" height="120" rx="4" fill="#e3f2fd" stroke="#333333" stroke-width="1.5"/>
  <text x="170" y="80" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">Core Components</text>
  <text x="35" y="100" font-size="12" fill="#333">• ALU performs arithmetic/logic</text>
  <text x="35" y="118" font-size="12" fill="#333">• Registers: fastest storage</text>
  <text x="35" y="136" font-size="12" fill="#333">  (sub-nanosecond access)</text>
  <text x="35" y="154" font-size="12" fill="#333">• Control Unit: fetch-decode-execute</text>
  <!-- Section: Performance Features -->
  <rect x="345" y="60" width="290" height="120" rx="4" fill="#e8f5e9" stroke="#333333" stroke-width="1.5"/>
  <text x="490" y="80" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">Performance Features</text>
  <text x="355" y="100" font-size="12" fill="#333">• Pipelining: overlap stages</text>
  <text x="355" y="118" font-size="12" fill="#333">• Superscalar: multi instr/cycle</text>
  <text x="355" y="136" font-size="12" fill="#333">• Out-of-Order: exec when ready</text>
  <text x="355" y="154" font-size="12" fill="#333">• Branch Prediction: speculate</text>
  <!-- Section: Memory Hierarchy -->
  <rect x="25" y="200" width="290" height="110" rx="4" fill="#fff3e0" stroke="#333333" stroke-width="1.5"/>
  <text x="170" y="220" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">Memory Hierarchy</text>
  <text x="35" y="240" font-size="12" fill="#333">• L1/L2/L3 caches bridge memory wall</text>
  <text x="35" y="258" font-size="12" fill="#333">• Cache coherence (MESI) keeps</text>
  <text x="35" y="276" font-size="12" fill="#333">  multi-core caches consistent</text>
  <text x="35" y="294" font-size="12" fill="#333">• 64-byte cache lines, spatial locality</text>
  <!-- Section: ISA Families -->
  <rect x="345" y="200" width="290" height="110" rx="4" fill="#fce4ec" stroke="#333333" stroke-width="1.5"/>
  <text x="490" y="220" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">ISA Families</text>
  <text x="355" y="240" font-size="12" fill="#333">• CISC (x86): complex instructions,</text>
  <text x="355" y="258" font-size="12" fill="#333">  huge legacy ecosystem</text>
  <text x="355" y="278" font-size="12" fill="#333">• RISC (ARM): simple instructions,</text>
  <text x="355" y="296" font-size="12" fill="#333">  power efficient, growing fast</text>
  <!-- Bottom note -->
  <text x="330" y="370" text-anchor="middle" font-size="12" fill="#555">Modern CPUs combine all these features for peak performance.</text>
</svg>
