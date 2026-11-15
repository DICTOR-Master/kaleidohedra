module

public import LoopEquality.Main
public import LoopEquality.Explicit
public import LoopEquality.Fibonacci

/-! Axiom check: only `propext`, `Quot.sound` and `Classical.choice` may appear. -/

#print axioms LoopEqualityProof.nbLoops_finite
#print axioms LoopEqualityProof.loop_equality
#print axioms LoopEqualityProof.W_closed
#print axioms LoopEqualityProof.Graph.sum_F_eq
#print axioms LoopEqualityProof.loop_count_eq
#print axioms LoopEqualityProof.loopCount_values
#print axioms LoopEqualityProof.loopCount_values_34
#print axioms LoopEqualityProof.loopCount_eq_iharaBass_small
#print axioms LoopEqualityProof.closedWalks_domb_small
#print axioms LoopEqualityProof.fibonacci_isStacking
#print axioms LoopEqualityProof.fibonacci_layer_type
#print axioms LoopEqualityProof.isH_eq_word
#print axioms LoopEqualityProof.isH_not_periodic
#print axioms LoopEqualityProof.fibonacci_not_periodic
#print axioms LoopEqualityProof.fibonacci_loop_equality
