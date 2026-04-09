# GCC CPU-Specific Optimization
## A Comprehensive Guide
## Mark Veltzer
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)

---

![title](svg/lectures/build_systems/gcc-optimizations/title.svg)

## Understanding CPU Optimization
- Compiler optimization is crucial for performance
- CPU-specific tuning can provide significant speedups
- Different optimization levels available in GCC

---

## Basic Optimization Flags and Inspection
- `-O0`: No optimization (default)
- `-O1`: Basic optimization
- `-O2`: Recommended optimization level
- `-O3`: Aggressive optimization
- `-Os`: Optimize for size

```bash
# List all optimizations enabled at -O2
gcc -O2 -Q --help=optimizers

# See specific optimization state
gcc -O2 -fopt-info
```

---

## CPU-Specific Flags Overview
- `-march`: Architecture-specific instructions
- `-mtune`: Performance tuning
- `-mcpu`: Combined architecture and tuning (some platforms)

---

## Understanding -march
- Sets minimum CPU architecture
- Generates CPU-specific instructions
- Code won't run on older processors
- Example: `-march=skylake`

---

## Understanding -mtune
- Optimizes for target CPU
- Maintains backward compatibility
- Safe for distribution
- Example: `-mtune=skylake`

---

## Auto-detection with 'native'
- `-march=native`
- `-mtune=native`
- Automatically detects host CPU
- Optimal for local builds

---

## Common CPU Types

### Intel
- skylake
- haswell
- broadwell
- icelake

### AMD
- znver1 (Zen 1)
- znver2 (Zen 2)
- znver3 (Zen 3)

---

## Vector Extensions
- `-mavx`
- `-mavx2`
- `-msse4.2`
- Enable specific instruction sets
- Can be automatic with -march

---

## Finding Supported CPUs

```bash
gcc -march=help
gcc -mtune=help
gcc -Q --help=target
```

---

## Real-world Example

```bash
# Full optimization for current CPU
gcc -O3 -march=native program.c

# Specific CPU targeting
gcc -O2 -march=skylake -mtune=skylake program.c
```

---

## Profiling Tools
- `-fprofile-generate`
- `-fprofile-use`
- Allows optimization based on runtime behavior
- Can significantly improve performance

---

## Common Pitfalls
- Over-optimization
- Platform compatibility issues
- Testing implications
- Debug complexity

---

## Best Practices
1. Test performance impact
1. Maintain compatibility requirements
1. Document CPU requirements
1. Consider distribution needs

---

## Performance Monitoring
- Use perf tools
- Benchmark before/after
- Monitor CPU utilization
- Check generated assembly

---

## Distribution Considerations
- Binary compatibility
- Target audience
- Platform support
- Distribution method

---

## Optimization Strategy
1. Start with -O2
1. Profile code
1. Add CPU-specific flags
1. Benchmark results
1. Test compatibility

---

## When to Use CPU-Specific Tuning
- Performance-critical applications
- Known deployment environment
- Local builds
- Scientific computing

---

## Additional Resources
- GCC documentation
- CPU vendor optimization guides
- Performance tuning guides
- Architecture manuals

---

## Questions to Consider
1. What is your target platform?
1. Performance requirements?
1. Distribution needs?
1. Maintenance considerations?

---

## Summary
- CPU tuning can improve performance
- Consider compatibility needs
- Test thoroughly
- Document requirements
