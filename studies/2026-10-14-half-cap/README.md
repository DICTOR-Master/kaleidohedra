# Half Admiral Cap (Fable study for DICTO, 2026-10-14)

Question (DICTO): can space be filled with half Admiral Caps, via the octahedron? **No, not with Cleo-Icos and half caps alone.**

- **Octahedron = 20 Cleo-Icos + 12 half caps, exactly** (volumes φ²/24, φ/24, φ⁶/6; 66,577 sample points each in exactly one piece).
- **The octet's tetrahedron cannot be made from them** (its volume would need exactly 5 Cleo-Icos + 3 half caps, but the angles forbid it), and **no tiling of space by Cleo-Icos + half caps (± Antonius) exists**, periodic or not, any sizes. Proof: the angles π, θ_I = arccos(−√5/3) and α = arccos(1/√3) are rationally independent, so a counting rule h with h(π) = h(θ_I) = 0, h(α) = 1 exists; Cleo-Icos and Antonius angles all have h = 0, the half cap's edges have h ≥ 0 with some positive, so they can never close to 2π (h = 0) round a half cap's AT or TC edge.
- So space needs a partner with negative α-content: the regular tetrahedron does it, which is the octet (20 Cleo-Icos + 12 half caps + 2 tetrahedra).
- **Fell out:** a Cleo-Icos and a half cap sharing a face make one kite pyramid (110.905° + 69.095° = 180°), so the octahedron = 8 Cleo-Icos + 12 kite pyramids. The half cap is not a known space-filling tetrahedron (its Dehn invariant is not zero). 5 Cleo-Icos + 3 half caps can be cut and rearranged into a quarter octahedron (same volume and Dehn invariant, Sydler), not constructed.

Scripts: halfcap_check.py → halfcap_check.json. DICTO · dictospheres.com
