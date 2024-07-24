include "part.dfy"


method qsort(a:array<int>, l:nat, u:nat)
  requires a.Length > 0
  requires a!= null
  requires l <= u < a.Length;
  requires l>0 ==> partitioned(a, 0, l-1, l, u);
  requires u+1 <= a.Length -1 ==> partitioned(a, l, u, u+1, a.Length-1);
  modifies a
  ensures sorted_between(a, l, u+1);
  ensures l > 0 ==> beq(old(a[..]), a[..], 0, l-1);
  ensures l > 0 ==> partitioned(a, 0, l-1, l, u);
  ensures u < a.Length-1 ==> beq(old(a[..]), a[..], u+1, a.Length - 1);
  ensures u < a.Length - 1 ==> partitioned(a, l, u, u+1, a.Length-1);
  decreases u - l
{
  if (l >= u) {
    return;
  }
  else{
    var pivot := partition(a, l, u);
    assert forall i :: l <= i < pivot ==> a[i] <= a[pivot];
    if (l < pivot){
      qsort(a, l, pivot-1);
    }
    if (pivot<u){
      qsort(a, pivot + 1, u);
    }

  }
}