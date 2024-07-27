method flip(a: array<int>, num: int)
  modifies a
  requires a.Length > 0
  requires 0 <= num < a.Length
  ensures  multiset(a[..]) == multiset(old(a[..]))

  ensures forall i :: 0 <= i <= num ==> a[i] == old(a[num - i])
  ensures forall i :: num < i <a.Length ==> a[i] == old(a[i])

{
  var tmp: int;
  var i := 0;
  var j := num;

  while (i < j)
    invariant 0 <= i <= num
    invariant 0 <= j <= num
    invariant i + j == num
    invariant multiset(a[..]) == multiset(old(a[..]))
    invariant forall k :: 0 <= k < i ==> a[k] == old(a[num - k])
    invariant forall k :: j < k <= num ==> a[k] == old(a[num - k])
    invariant forall k :: i<=k<=j ==> a[k] == old(a[k])
    invariant forall p :: num<p<a.Length==> a[p] == old(a[p])

    decreases j - i
  {
    tmp := a[i];
    a[i] := a[j];
    a[j] := tmp;
    i := i + 1;
    j := j - 1;
  }
}
